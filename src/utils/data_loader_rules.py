from pathlib import Path


def is_csv(file_path: Path) -> bool:
    file_extension = file_path.suffix
    return bool(file_extension == ".csv")


def is_lower(file_name: str) -> bool:
    return file_name.islower()
