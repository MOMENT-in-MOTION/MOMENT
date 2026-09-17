import logging
from pathlib import Path

from ...metameta.m_m_m_classes import MetaModel
from ...config import TEMPLATES_DIR

from .jinja_engine import render, build_engine
from .mapper import TemplateContext
from .formatter import Formatter
from .serializer import Serializer, serialize_context

logger = logging.getLogger(__name__)

def generate_meta_model_api(
    meta_model: MetaModel,
    api_config: dict[str],
    formatter: Formatter,
    templates_dir: Path,
    output_path: Path,
    serializer: Serializer | None = None,
) -> dict[str, str]:
    """
    Generate Python API code from a metamodel.

    Prepares a template context from the metamodel, applies the formatter,
    optionally serializes the context to JSON or XML, and renders the
    dataclass and enum templates.

    Args:
        meta_model: The parsed metamodel to generate code for.
        api_config: Configuration passed through to the templates (e.g. package name).
        formatter: Visitor that applies naming-convention formatting to the context.
        templates_dir: Directory containing the Jinja2 templates.
        serializer: Optional visitor that serializes the context to a file
            (JSON, XML, ...) before rendering. If None, no file is written.

    Returns:
        A dictionary with keys "dataclass_code" and "enum_code" containing
        the rendered source code strings.
    """
    j2_engine = build_engine(templates_dir)
    context = TemplateContext.from_meta_model(meta_model=meta_model)

    if api_config.get("Inheritance") == "manual":
        context.resolve_manual_inheritance()
    
    formatter.visit_context(context)

    if serializer is not None:
        serialize_context(context, api_config, serializer, output_path)

    context_dict = context.to_dict()
    context_dict.update({"api_config": api_config})

    return _render_templates(j2_engine, context_dict)


def _render_templates(j2_engine, context_dict: dict) -> dict[str, str]:
    result = {
        "class_code": render(j2_engine, "class_template.py.j2", context_dict),
        "enum_code": render(j2_engine, "enum_template.py.j2", context_dict),
    }
    if context_dict.get("api_config", {}).get("RelativeImports") == "true":
        result["__init__"] = ""
    return result


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
            logger.debug("Generated Metamodel API file %s written to: %s", name, output_path)
        except OSError as e:
            raise OSError(f"Failed to write generated file '{output_path}': {e}") from e
