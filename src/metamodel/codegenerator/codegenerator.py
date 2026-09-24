import logging
from pathlib import Path

from ...metameta.m_m_m_classes import MetaModel, OpenAssociation
from ...config import TEMPLATES_DIR

from .jinja_engine import render, build_engine
from .mapper import TemplateContext
from .formatter import Formatter

logger = logging.getLogger(__name__)


def _collect_module_imports(meta_model: MetaModel) -> list[str]:
    """Collect grouped import statements for module-based imports from the model."""
    imports_by_module: dict[str, set[str]] = {}

    for cls in meta_model.classes:
        for assoc in cls.associations:
            import_link = getattr(assoc, "import_link", None)
            if not import_link:
                continue

            target_name = getattr(assoc, "association_target_name", None)
            if not target_name:
                continue

            module_name = import_link
            if module_name.endswith(".py"):
                module_name = module_name[:-3]

            imports_by_module.setdefault(module_name, set()).add(target_name)

    return [
        f"from {module_name} import {', '.join(sorted(symbols))}"
        for module_name, symbols in sorted(imports_by_module.items())
    ]


def generate_meta_model_api(
    meta_model: MetaModel,
    api_config: dict[str],
    formatter: Formatter,
    templates_dir: Path,
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
    import_mode = str(api_config.get("ImportMode", "merge")).lower()
    context = TemplateContext.from_meta_model(
        meta_model=meta_model, import_mode=import_mode
    )

    if api_config.get("Inheritance") == "manual":
        context.resolve_manual_inheritance()

    formatter.visit_context(context)

    context_dict = context.to_dict()
    context_dict.update({"api_config": api_config})
    context_dict.update(
        {
            "module_imports": (
                _collect_module_imports(meta_model) if import_mode == "import" else []
            )
        }
    )

    return _render_templates(j2_engine, context_dict)


def _render_templates(j2_engine, context_dict: dict) -> dict[str, str]:
    result = {
        "class_code": render(j2_engine, "class_template.py.j2", context_dict),
        "enum_code": render(j2_engine, "enum_template.py.j2", context_dict),
    }
    if context_dict.get("api_config", {}).get("RelativeImports") == "true":
        result["__init__"] = ""

    serialization_fmt = context_dict.get("api_config", {}).get("SerializationFormat")
    if (
        serialization_fmt
        and isinstance(serialization_fmt, list)
        and len(serialization_fmt) > 0
    ):
        result["serializer"] = render(
            j2_engine, "serializer_template.py.j2", context_dict
        )

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
            logger.debug(
                "Generated Metamodel API file %s written to: %s", name, output_path
            )
        except OSError as e:
            raise OSError(f"Failed to write generated file '{output_path}': {e}") from e
