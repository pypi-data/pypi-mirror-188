from datetime import datetime


def split_separated_text(text, separator) -> list[str]:
    raw_parts = text.split(separator)
    clean_split = []
    for raw_part in raw_parts:
        if raw_part.strip():
            clean_split.append(raw_part)
    return clean_split


def timestamp_to_silver_display(timestamp) -> str:
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S%z")


def parse_silver_datetime(datetime_display: str) -> datetime:
    return datetime.strptime(datetime_display, "%Y-%m-%dT%H:%M:%S%z")


def remove_white_spaces_elements(elements: list[str]) -> list[str]:
    output = []
    for element in elements:
        if element.strip():
            output.append(element.strip())
    return output
