from pathlib import Path
import re
import logging
import sys
from shared.load_json_as_dict import load_json_as_dict
from metamodel.parser.helper import structure_data

CAMEL_CASE_PATTERN = re.compile(
    r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+"
)
SUB_META_MODELS: dict = []
logger = logging.getLogger(__name__)


def merge_meta_models(path: Path) -> dict[str] | None:
    meta_model_dicts: list[dict] = []
    merged_meta_model: dict[str] = {}

    SUB_META_MODEL_NAMES = [
        file.name for file in get_sub_model_path(path=path).glob("*.json")
    ]
    logger.debug(f"Found Sub-Meta-Models: {SUB_META_MODEL_NAMES}")

    meta_models = resolve_imports(path=path)

    merged_meta_model = merge_models(meta_models)

    return merged_meta_model


def load_MetaModel(path: Path) -> dict[str] | None:

    try:
        meta_model_dict = load_json_as_dict(path=path)
    except IOError as e:
        print(getattr(e, "message", str(e)))
        sys.exit(1)

    return structure_data(meta_model_dict)


def get_sub_model_path(path: Path) -> Path:

    return path.parent / "sub_meta_models"


def find_imports(meta_model: dict[str]) -> list[dict]:
    pass


def collect_and_remove_key(model: dict, target_key: str = "import") -> list[str]:
    foreign_models = []

    for classes in model["classes"]:
        for associations in classes["associations"]:
            if target_key in associations:
                foreign_models.append(associations.pop(target_key))

    return foreign_models


def get_sub_model_path(path: Path, name: str = "") -> Path:

    return path.parent / "sub_meta_models" / (name + ".json")


def merge_models(meta_models: list[dict]) -> dict[str]:
    merged_models = []
    prefixes = []

def normalize(name:str)->str:
    return re.sub(r"[-_\s]+", " ", name.strip)

def resolve_camel_case(name:str)->list[str]:
    return CAMEL_CASE_PATTERN.findall(name)

def acronym_from_words(words:list[str], precise=False):

    if precise:
        precise_name = ""
        for word in words:
            if word.upper() == word:
                precise_name += word
                words.remove(word)
            else:
                precise_name += word[0].upper
                precise_name += word[1].upper
    return "".join(word[0] for word in words).upper()

def generate_acronym(name):
    result = acronym_from_words(resolve_camel_case(normalize(name)))
    prefixes = [model["prefix"] for model in SUB_META_MODELS]
    if result in prefixes:
        result = acronym_from_words(resolve_camel_case(normalize(name)), precise=True)
        if result in prefixes:
            result = name
    return result + "_"

def prefix_class():
    pass

def merge_model():
    pass