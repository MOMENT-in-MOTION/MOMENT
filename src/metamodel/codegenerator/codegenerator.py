from pathlib import Path

from ...metameta.m_m_m_classes import MetaModel
from ...config import TEMPLATES_DIR

from .jinja_engine import render, build_engine
from .mapper import create_descriptors
from .formatter import Formatter


def generate_meta_model_api(
    meta_model: MetaModel,
    api_config: dict[str],
    formatter: Formatter,
    templates_dir: Path
) -> dict[str, str]:
    """
    Generates the API for the metamodel.

    Builds the Jinja2 engine, assembles the rendering context from the
    metamodel and API config, applies the formatter, and renders the
    dataclass and enum templates.

    Args:
        meta_model: The parsed metamodel instance to generate code for.
        api_config: Configuration dictionary containing settings such as
            the naming convention.
        formatter: The formatter instance used to prepare the field
            descriptors in the rendering context.
        templates_dir: Path to the directory containing the Jinja2 templates.

    Returns:
        A dictionary containing the generated "dataclass_code" and "enum_code".
    """
    j2_engine = build_engine(templates_dir)
    context = create_descriptors(meta_model=meta_model)
    context.update({"api_config": api_config})

    formatter.format_descriptors(context)

    dataclass_code = render(j2_engine, "dataclass_template.py.j2", context)
    enum_code = render(j2_engine, "enum_template.py.j2", context)

    return {
        "dataclass_code": dataclass_code,
        "enum_code": enum_code,
    }


def write_generated_code(generated_code: dict[str, str], output_dir: Path) -> None:
    """
    Writes the generated source code files to the specified output directory.

    Args:
        generated_code: A dictionary mapping file base names to source code
            strings, as returned by generate_meta_model_api.
        output_dir: Path to the directory where the generated files will
            be written.

    Raises:
        FileNotFoundError: If output_dir does not exist.
        OSError: If a file cannot be written due to a permissions or I/O error.
    """
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

    for name, code in generated_code.items():
        output_path = output_dir / f"{name}.py"
        try:
            output_path.write_text(code, encoding="UTF-8")
        except OSError as e:
            raise OSError(f"Failed to write generated file '{output_path}': {e}") from e
