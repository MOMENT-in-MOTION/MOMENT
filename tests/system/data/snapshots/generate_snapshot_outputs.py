from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.metamodel.codegenerator.codegenerator import generate_meta_model_api
from src.metamodel.codegenerator.formatter import get_formatter
from src.metamodel.merger import merge_meta_models
from src.metamodel.parser.meta_model_parser import parse_meta_model
from src.shared.load_json_as_dict import load_json_as_dict
from src.shared.structure import structure_data

OUT_DIR = Path(__file__).resolve().parent
JSON_DIR = OUT_DIR / "test_jsons"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CFG = {
    "GenerateGetters": "true",
    "GenerateSetters": "true",
    "GenerateConstructors": "true",
    "GenerateHasFunctions": "true",
    "StrictPrivacy": "true",
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
    "AllowUnreachableClasses": "false",
    "RelativeImports": "true",
    "Inheritance": "native",
    "ImportMode": "merge",
}

for json_name, overrides in {
    "snsh_merge_json.json": {"AllowUnreachableClasses": "true", "ImportMode": "merge"},
    "snsh_variance_base.json": {
        "AllowUnreachableClasses": "true",
        "ImportMode": "merge",
    },
    "snsh_variance_imported.json": {
        "AllowUnreachableClasses": "false",
        "ImportMode": "merge",
    },
    "snsh_variance_inheritance.json": {
        "AllowUnreachableClasses": "true",
        "ImportMode": "merge",
    },
    "snsh_import_mode.json": {
        "AllowUnreachableClasses": "false",
        "ImportMode": "import",
    },
}.items():
    path = JSON_DIR / json_name
    cfg = CFG.copy()
    cfg.update(overrides)

    model = parse_meta_model(
        structure_data(load_json_as_dict(path)),
        import_mode=cfg["ImportMode"],
    )
    if json_name != "snsh_import_mode.json":
        merge_meta_models(
            model,
            path,
            allow_unreachable_classes=cfg["AllowUnreachableClasses"].lower() == "true",
            import_mode=cfg["ImportMode"],
        )

    generated = generate_meta_model_api(
        model,
        cfg,
        get_formatter(cfg["NamingConvention"]),
        TEMPLATES_DIR,
    )

    (OUT_DIR / f"{path.stem}_class_code.py").write_text(
        generated["class_code"],
        encoding="utf-8",
    )
    (OUT_DIR / f"{path.stem}_enum_code.py").write_text(
        generated["enum_code"],
        encoding="utf-8",
    )
    print(f"wrote {path.stem}_class_code.py and {path.stem}_enum_code.py")
