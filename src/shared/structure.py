from ..metameta.m_m_m_dicts import MetaModelDict, MetaClassDict

def structure_data(unstructured: MetaModelDict) -> MetaModelDict:
    """Collect the relevant data in a structured dictionary.

    Args:
        unstructured (MetaModelDict): Unstructured dictionary.

    Raises:
        KeyError: The unstructured dictionary contains unexpected keys.

    Returns:
        MetaModelDict: The structured dictionary.
    """
    names = []
    enums = []
    classes = []

    for key, value in unstructured.items():
        key_lower = key.lower()
        match key_lower:
            case k if "name" in k:
                names.append(value)
            case k if "enums" in k:
                enums += value
            case k if "classes" in k:
                classes += value
            case _:
                raise ValueError(f"Unexpected key '{key}' with value '{value}'.")

    if len(names) > 1:
        raise ValueError(f"Multiple names where given: {names}")

    return {"name": names[0], "enums": enums, "classes": classes}
