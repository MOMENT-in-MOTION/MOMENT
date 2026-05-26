import json

from pathlib import Path


def load_json_as_dict(path: Path) -> dict[str] | None:
    """
    Returns the content of a .json file as a python dict.

    Raises:
        ValueError: If the file is not a json file.
        IOError: If an exception is encountered when loading the file.
    """
    if not path.name.endswith(".json"):
        raise ValueError("File needs to be a json file!")

    try:
        with open(path, encoding="UTF8") as json_file:
            meta_model = json.load(json_file)
            return meta_model
    except Exception as e:
        raise IOError(
            f"Encountered the Error '{e}' while loading the file: {path}"
        ) from e
