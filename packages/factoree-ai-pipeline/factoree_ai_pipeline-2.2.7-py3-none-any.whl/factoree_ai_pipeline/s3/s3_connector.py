import boto3
import json
from botocore.paginate import PageIterator
from factoree_ai_pipeline.file.file_types import S3TextFile, S3FileCreatedEvent
from concurrent.futures import ThreadPoolExecutor, as_completed
from factoree_ai_pipeline.file.file_utils import grid_to_csv
from typing import TypeVar
from logging import Logger
from factoree_ai_pipeline.file.file_types import S3File


T = TypeVar('T', bound=S3File)


class S3TestEventError(Exception):
    def __init__(self, handler: str, bucket: str):
        super().__init__('s3:TestEvent received')
        self.handler = handler
        self.bucket = bucket

    def get_handler(self) -> str:
        return self.handler

    def get_bucket(self) -> str:
        return self.bucket


class S3Connector:
    event_list: list[S3FileCreatedEvent] = []
    current_file = None

    def __init__(
            self,
            region_name: str,
            sqs_url: str,
            aws_access_key: str,
            aws_secret_key: str,
            logger: Logger
    ):
        self.sqs_url = sqs_url
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.logger = logger

    def list_objects(self, bucket_name: str, prefix: str = '') -> PageIterator:
        paginator = self.s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        return pages

    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        # TODO: error handling
        self.logger.info(f'Getting events from {self.sqs_url}')
        response = self.sqs_client.receive_message(
            QueueUrl=self.sqs_url,
            MaxNumberOfMessages=1,
        )
        event: S3FileCreatedEvent = S3Connector.get_file_created_event_from_response(response, self.logger)
        if event is None:
            self.logger.info('No messages in queue')
        else:
            self.logger.info(f'Received message of new file {event.filename}')

        return event

    def write_csv_file(self, bucket_name: str, filename: str, data: list[list]) -> bool:
        return self.s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=grid_to_csv(data)
        )

    def write_json_file(self, bucket_name: str, filename: str, json_data: dict) -> bool:
        self.logger.info(f'write_json_file({filename})')
        return self.s3_client.put_object(Bucket=bucket_name, Key=filename, Body=json.dumps(json_data))

    def write_json_files(self, bucket_name: str, filenames: list[str],
                         json_data: list[dict]) -> int:
        max_workers = max(30, len(filenames))
        written_json_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(write_json_file, self, bucket_name, filenames[i], json_data[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                written_json_files += 1 if future.result() else 0

        return written_json_files

    def delete_s3_object(self, bucket_name: str, s3_object: str) -> bool:
        self.s3_client.delete_object(Bucket=bucket_name, Key=s3_object)
        return True

    def delete_files(self, bucket_name: str, filenames: list[str]) -> int:
        max_workers = max(30, len(filenames))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, bucket_name, filenames[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def delete_s3_files(self, files: list[T]) -> int:
        max_workers = max(30, len(files))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, files[i].bucket_name, files[i].filename) for i in
                       range(len(files))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def move_s3_files(self, files: list[T], destinations: list[str]) -> int:
        max_workers = max(30, len(files))
        moved_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(
                move, self, files[i].bucket_name, files[i].filename, destinations[i]
            ) for i in
                       range(len(files))]
            for future in as_completed(futures):
                moved_files += 1 if future.result() else 0

        return moved_files

    def copy(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        copy_source = {'Bucket': src_bucket, 'Key': src_filename}
        response = self.s3_client.copy_object(CopySource=copy_source, Bucket=dst_bucket, Key=dst_filename)
        return response.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200

    def move(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        return self.copy(src_bucket, src_filename, dst_bucket, dst_filename) and \
               self.delete_s3_object(src_bucket, src_filename)

    def s3_object_exists(self, bucket_name: str, s3_object: str) -> bool:
        return self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_object, MaxKeys=1).get('KeyCount') == 1

    @staticmethod
    def get_file_created_event_from_response(response, logger: Logger) -> S3FileCreatedEvent | None:
        event: S3FileCreatedEvent | None = None
        for message in response.get('Messages', []):
            handler = message.get('ReceiptHandle', '')
            try:
                body_str = message.get('Body')
                body_json = json.loads(body_str)
                if body_json.get('Event') == 's3:TestEvent':
                    raise S3TestEventError(handler, body_json.get('Bucket'))
                for record in body_json.get('Records', []):
                    filename = record.get('s3', {}).get('object', {}).get('key')
                    bucket_name = record.get('s3', {}).get('bucket', {}).get('name')
                    event = S3FileCreatedEvent(bucket_name, filename, handler)
            except IndexError or TypeError as e:
                logger.error(str(e))

        return event

    def fetch_s3_file(self, bucket_name: str, file_key: str) -> S3TextFile:
        data: str = self.__read_file_content_from_s3(bucket_name, file_key)
        return S3TextFile(bucket_name, file_key, data)

    def purge_events(self):
        self.sqs_client.purge_queue(QueueUrl=self.sqs_url)

    def __read_file_content_from_s3(self, bucket_name: str, s3_path: str) -> str:
        data = self.s3_client.get_object(Bucket=bucket_name, Key=s3_path)
        return data['Body'].read().decode('UTF-8')

    def delete_message(self, handler: str) -> bool:
        # TODO: error handling
        self.logger.info(f'Deleting message with ReceiptHandle "{handler}" from queue')
        self.sqs_client.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=handler
        )
        return True


def write_json_file(connector: S3Connector, bucket_name: str, filename: str, json_data: dict) -> bool:
    return connector.write_json_file(bucket_name, filename, json_data)


def delete(connector: S3Connector, bucket_name: str, filename: str) -> bool:
    connector.delete_s3_object(bucket_name, filename)
    return True


def move(connector: S3Connector, bucket_name: str, filename: str, destination: str) -> bool:
    return connector.copy(bucket_name, filename, bucket_name, destination) and \
           connector.delete_s3_object(bucket_name, filename)
