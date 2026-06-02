from .jinja_engine import render, Environment
from .formatter import Formatter


def generate_meta_model_api(
    j2_engine: Environment,
    context: dict,
    formatter: Formatter
) -> dict[str, str]:
    """
    Generates the API for the metamodel.

    Args:
        meta_model: A instance of the metametamodel containing all the data of the metamodel.
    """
    formatter.format_descriptors(context)

    dataclass_code = render(j2_engine, "dataclass_template.py.j2", context)
    enum_code  = render(j2_engine, "enum_template.py.j2",       context)

    return {
        "dataclass_code": dataclass_code,
        "enum_code":      enum_code,
    }
