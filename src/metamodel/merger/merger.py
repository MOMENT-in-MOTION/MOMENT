from pathlib import Path
import re
import logging
import sys
from shared.load_json_as_dict import load_json_as_dict
from metamodel.parser.helper import structure_data

CAMEL_CASE_PATTERN = re.compile(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+")
logger = logging.getLogger(__name__)


def merge_meta_models(path: Path) -> dict[str] | None:
    merged_meta_model: dict = {"name": "", "enums": [], "classes": []}
    meta_models: dict = {}

    main_name = _load_main(path, meta_models)
    merged_meta_model["name"] = main_name
    _load_available_sub_meta_models(path, meta_models)

    _merge_model(main_name, merged_meta_model, meta_models)

    return merged_meta_model


def _merge_model(name: str, merged_meta_model: dict, meta_models: dict):
    logger.debug(f"Merging model with name '{name}.'")

    enums = meta_models[name]["model_dict"]["enums"]
    classes = meta_models[name]["model_dict"]["classes"]
    prefix = meta_models[name]["prefix"]

    merged_meta_model["enums"] += _prefix_names(enums, prefix)
    merged_meta_model["classes"] += _prefix_names(classes, prefix)

    meta_models[name]["merged"] = True

    _find_imports(classes, merged_meta_model, meta_models)


def _find_imports(classes: list, merged_meta_model: dict, meta_models: dict):
    for cls in classes:
        for element in cls["attributes"] + cls["associations"]:
            if "import" in element.keys():
                name = element.pop("import")
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


def _prefix_names(list_of_element_dicts: list[dict], prefix: str):
    for element_dict in list_of_element_dicts:
        element_dict["name"] = prefix + element_dict["name"]
    return list_of_element_dicts


def _load_available_sub_meta_models(path: Path, meta_models: dict):

    for path in _get_sub_model_path(path=path).glob("*.json"):
        logger.debug(f"Found Sub-Meta-Model: {path.name}")
        model = load_json_as_dict(path)
        model_name = model["name"]
        prefix = _generate_acronym(
            model_name, [model["prefix"][:-1] for model in meta_models.values()]
        )
        if _is_valid_meta_model(model):
            meta_models[model_name] = {
                "prefix": prefix,
                "model_dict": model,
                "merged": False,
            }
            logger.debug(
                f"Added Meta-Model with Name: '{model_name}' with prefix: '{prefix[:-1]}' to avilable Models."
            )
        else:
            logger.info(
                f"The Meta-Model with the Title '{model_name}' from the file named '{path.stem}'"
            )


def _load_main(path: Path, meta_models: dict) -> str:

    model = load_json_as_dict(path)
    model_name = model["name"]
    prefix = ""
    if _is_valid_meta_model(model):
        meta_models[model_name] = {
            "prefix": prefix,
            "model_dict": model,
            "merged": False,
        }
        logger.debug(
            f"Added the Main-Meta-Model with Name: {model_name} to avilable Models."
        )
    else:
        logger.info(
            f"The Main-Meta-Model with the Title {model_name} from the file named {path.stem} "
            "could not be loaded."
        )
    return model_name


def _is_valid_meta_model(model: dict):
    result = False
    required_keys = {"name", "classes", "enums"}

    if required_keys.issubset(model.keys()):
        return True
    logger.info(
        f"The provided Meta-Model is missing one of the required keys: {required_keys}"
    )

    return result


def _get_sub_model_path(path: Path) -> Path:
    return path.parent / "sub_meta_models"


def _normalize(name: str) -> str:
    return re.sub(r"[-_\s]+", " ", name.strip())


def _resolve_camel_case(name: str) -> list[str]:
    return CAMEL_CASE_PATTERN.findall(name)


def _split_words(name: str) -> list[str]:
    normalized = _normalize(name=name)

    words = []

    for word in normalized.split():
        words.extend(_resolve_camel_case(word))

    return words

def _create_acronym(words: list[str], level: int = 1) -> str:
    precise_name = []

    for word in words:
        if word.isupper() and len(word) < 4:
            precise_name.append(word)
        else:
            precise_name.append(word[:level].capitalize())
    return "".join(precise_name)

def _generate_acronym(name: str, existing_prefixes: list[str]):
    words = _split_words(name)
    level = 1

    while True:
        acronym = _create_acronym(words, level)
        if acronym not in existing_prefixes:
            break
        level += 1

    return acronym + "_"
