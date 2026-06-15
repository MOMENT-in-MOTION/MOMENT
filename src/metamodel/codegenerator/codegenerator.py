from pathlib import Path

from ...metameta.m_m_m_classes import MetaModel
from ...config import TEMPLATES_DIR

from .mapper import create_descriptors
from .jinja_engine import build_engine, render


def generate_meta_model_api(meta_model: MetaModel) -> dict[str, str]:
    """
    Generates the API for the metamodel.

    Args:
        meta_model: A instance of the metametamodel containing all the data of the metamodel.
    """
    j2_engine = build_engine(TEMPLATES_DIR)
    context = create_descriptors(meta_model=meta_model)

    dataclass_code = render(j2_engine, "dataclass_template.py.j2", context)
    enum_code = render(j2_engine, "enum_template.py.j2", context)

    generated_code = {
        "dataclass_code": dataclass_code,
        "enum_code": enum_code
    }

    return generated_code
