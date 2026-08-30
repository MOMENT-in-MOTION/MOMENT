from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
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
    "StrictPrivacy": "true",
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
    "AllowUnreachableClasses": "false",
    "RelativeImports": "true",
    "Inheritance": "native",
}

for json_name in [
    "snsh_merge_json.json",
    "snsh_variance_base.json",
    "snsh_variance_imported.json",
    "snsh_variance_inheritance.json",
]:
    path = JSON_DIR / json_name
    model = parse_meta_model(structure_data(load_json_as_dict(path)))
    if json_name == "snsh_merge_json.json":
        merge_meta_models(model, path, allow_unreachable_classes=True)

    generated = generate_meta_model_api(
        model,
        CFG,
        get_formatter(CFG["NamingConvention"]),
        TEMPLATES_DIR,
        OUT_DIR,
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
