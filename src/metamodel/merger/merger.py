from __future__ import annotations
from pathlib import Path
import re
import logging
from shared.load_json_as_dict import load_json_as_dict
from metamodel.parser.helper import structure_data
from metamodel.typing_helpers.typed_dicts import (
    MetaModelDict,
    MetaModelInfoDict,
    MetaClassDict,
    MetaEnumDict
)

CAMEL_CASE_PATTERN = re.compile(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+")
logger = logging.getLogger(__name__)


def merge_meta_models(path: Path) -> MetaModelDict:
    """Entry point for the merger that loads the main Meta-Model and all available
    sub-Meta-Models, merges them and returns the merged Meta-Model as a dictionary.

    Args:
        path (Path): The path to the directory containing the Meta-Model files.

    Returns:
        MetaModelDict: The merged Meta-Model as a dictionary.
    """

    merged_meta_model: MetaModelDict = {"name": "", "enums": [], "classes": []}
    meta_models: dict[str, MetaModelInfoDict] = {}

    main_name = _load_main(path, meta_models)
    merged_meta_model["name"] = main_name
    _load_available_sub_meta_models(path, meta_models)

    _merge_model(main_name, merged_meta_model, meta_models)

    return merged_meta_model


def _merge_model(
    name: str,
    merged_meta_model: MetaModelDict,
    meta_models: dict[str, MetaModelInfoDict],
) -> None:
    """Recursively merges the Meta-Model with the given name into the merged_meta_model."""
    logger.debug(f"Merging model with name '{name}.'")

    enums = meta_models[name]["model_dict"]["enums"]
    classes = meta_models[name]["model_dict"]["classes"]
    prefix = meta_models[name]["prefix"]

    merged_meta_model["enums"] += _prefix_names(enums, prefix)
    merged_meta_model["classes"] += _prefix_names(classes, prefix)

    meta_models[name]["merged"] = True

    _find_imports(classes, merged_meta_model, meta_models)


def _find_imports(
    classes: list[MetaClassDict],
    merged_meta_model: MetaModelDict,
    meta_models: dict[str, MetaModelInfoDict],
) -> None:
    """Finds all imports in the given classes and merges the corresponding
    Meta-Models if they have not been merged yet."""
    for cls in classes:
        for element in cls["attributes"] + cls["associations"]:
            if "import_" in element.keys():
                name = element.pop("import_",None)
                if name is None:
                    continue
                if name in meta_models.keys():
                    model = meta_models[name]
                    prefix = model["prefix"]
                    if "target" in element.keys():
                        element["target"] = prefix + element["target"]
                    else:
                        element["attribute_type"] = prefix + element["attribute_type"]
                    if not model["merged"]:
                        _merge_model(name, merged_meta_model, meta_models)
                else:
                    logger.info(
                        f"The Meta-Model with the Title '{name}' "
                        f"that is imported in the element with the name "
                        f"'{cls['name']}' could not be found among the available Meta-Models."
                    )


def _prefix_names(
    list_of_element_dicts: list[MetaClassDict | MetaEnumDict], prefix: str
) -> list[MetaClassDict | MetaEnumDict]:
    """Prefixes the names of the given list of element dictionaries with the given prefix."""
    for element_dict in list_of_element_dicts:
        element_dict["name"] = prefix + element_dict["name"]
        print(f"Prefixed element with name '{element_dict['name']}' with prefix '{prefix}'.")
    return list_of_element_dicts


def _load_available_sub_meta_models(
    path: Path, meta_models: dict[str, MetaModelInfoDict]
) -> None:
    """Loads all available sub-Meta-Models from the given path and adds them
    to the meta-models dictionary."""
    for model_path in _get_sub_model_path(path=path).glob("*.json"):
        logger.debug(f"Found Sub-Meta-Model: {model_path.name}")
        model = structure_data(load_json_as_dict(model_path))
        model_name = model["name"]
        prefix = _generate_unique_acronym(
            model_name, [model["prefix"][:-1] for model in meta_models.values()]
        )

        meta_models[model_name] = {
            "prefix": prefix,
            "model_dict": model,
            "merged": False,
        }
        logger.debug(
            f"Added Meta-Model with Name: '{model_name}' with prefix: '{prefix[:-1]}' to "
            f"available Models."
        )


def _load_main(path: Path, meta_models: dict[str, MetaModelInfoDict]) -> str:
    """Loads the main Meta-Model from the given path and adds it to the meta-models dictionary."""
    model: MetaModelDict = structure_data(load_json_as_dict(path))
    model_name = model["name"]
    prefix = ""

    meta_models[model_name] = {
        "prefix": prefix,
        "model_dict": model,
        "merged": False,
    }
    logger.debug(
        f"Added the Main-Meta-Model with Name: {model_name} to avilable Models."
    )

    return model_name


def _get_sub_model_path(path: Path) -> Path:
    """Returns the Path to the dictionary, containing the Sub-Meta-Models."""
    return path.parent / "sub_meta_models"


def _normalize(name: str) -> str:
    """Replaces common seperators from the given Name with a space."""
    return re.sub(r"[-_\s]+", " ", name.strip())


def _resolve_camel_case(name: str) -> list[str]:
    """Uses a Regular Expression, to seperate words that are chained together with camel case."""
    return CAMEL_CASE_PATTERN.findall(name)


def _split_words(name: str) -> list[str]:
    """Seperates the given name into its individual words by first normalizing it
    and then ressolving camel case."""
    normalized = _normalize(name=name)
    words = []

    for word in normalized.split():
        words.extend(_resolve_camel_case(word))

    return words


def _create_acronym(words: list[str], level: int = 1) -> str:
    """Creates an acronym from the given list of words by taking the first 'level'
    characters of each word. If a word is in uppercase and shorter than 4 characters,
    it is directly added to the acronym.
    """
    precise_name = []

    for word in words:
        if word.isupper() and len(word) < 4:
            precise_name.append(word)
        else:
            precise_name.append(word[:level].capitalize())
    return "".join(precise_name)


def _generate_unique_acronym(name: str, existing_prefixes: list[str]) -> str:
    """Generates a unique acronym for the given name by splitting it into
    words and creating an acronym."""
    words = _split_words(name)
    level = 1

    while True:
        acronym = _create_acronym(words, level)
        if acronym not in existing_prefixes:
            break
        level += 1

    return acronym + "_"
