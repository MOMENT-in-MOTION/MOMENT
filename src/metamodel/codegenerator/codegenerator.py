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
        j2_engine: The Jinja2 environment used for rendering the templates.
        context: A dictionary containing the metamodel data and configuration.
        formatter: The formatter instance used to prepare the field descriptors.

    Returns:
        A dictionary containing the generated "dataclass_code" and "enum_code".
    """
    formatter.format_descriptors(context)

    dataclass_code = render(j2_engine, "dataclass_template.py.j2", context)
    enum_code = render(j2_engine, "enum_template.py.j2", context)

    return {
        "dataclass_code": dataclass_code,
        "enum_code": enum_code,
    }
