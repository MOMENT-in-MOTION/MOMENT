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
            return structure_data(meta_model)
    except Exception as e:
        raise IOError(
            f"Encountered the Error '{e}' while loading the file: {path}"
        ) from e


def structure_data(unstructured: dict) -> dict[str, list]:
    """Collect the relevant data in a structured dictionary.

    Args:
        unstructured (dict): Unstructured dictionary.

    Raises:
        KeyError: The unstructured dictionary contains unexpected keys.

    Returns:
        dict[str, list]: The structured dictionary.
    """
    structured = {"name": [], "enums": [], "classes": []}

    for key, value in unstructured.items():
        key_lower = key.lower()
        match key_lower:
            case k if "name" in k:
                structured["name"].append(value)
            case k if "enums" in k:
                structured["enums"] += value
            case k if "classes" in k:
                structured["classes"] += value
            case _:
                raise ValueError(f"Unexpected key '{key}' with value '{value}'.")

    if len(structured["name"]) > 1:
        names = structured["name"]
        raise ValueError(f"Multiple names where given: {names}")

    return structured
