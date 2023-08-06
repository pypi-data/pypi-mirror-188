from pathlib import Path


def path_exists(__path: str):
    return Path(__path).exists()


def read_text(__path: str):
    return Path(__path).read_text()


def write_text(path: str, data: str):
    Path(path).write_text(data=data)
