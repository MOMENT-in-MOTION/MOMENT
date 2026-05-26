

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
