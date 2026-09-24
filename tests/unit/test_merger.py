import json

import pytest

from src.metamodel.merger import UnreachableClassError, merge_meta_models
from src.metamodel.parser.meta_model_parser import parse_meta_model
from src.metameta.m_m_m_classes import Association
from src.shared.structure import structure_data


def test_repeated_submodel_reference_is_merged_once(tmp_path):
    """Merge one referenced submodel once even when multiple associations use it."""
    submodel_path = tmp_path / "shared_submodel.json"
    mainmodel_path = tmp_path / "main_model.json"

    submodel = {
        "name": "SharedSubmodel",
        "enums": [
            {
                "name": "SharedStatus",
                "values": ["ACTIVE", "ARCHIVED"],
            }
        ],
        "classes": [
            {
                "name": "SharedClass",
                "attributes": [],
                "associations": [],
                "inherits": [],
            }
        ],
    }
    submodel_path.write_text(json.dumps(submodel), encoding="utf-8")

    mainmodel = {
        "name": "MainModel",
        "enums": [],
        "classes": [
            {
                "name": "Root",
                "attributes": [],
                "associations": [
                    {
                        "name": "FirstReference",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "SharedClass",
                        "import_link": str(submodel_path),
                    },
                    {
                        "name": "SecondReference",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "SharedStatus",
                        "import_link": str(submodel_path),
                    },
                ],
                "inherits": [],
            }
        ],
    }
    mainmodel_path.write_text(json.dumps(mainmodel), encoding="utf-8")

    parsed_model = parse_meta_model(
        structure_data(mainmodel),
        import_mode="merge",
    )
    merged_model = merge_meta_models(
        parsed_model,
        mainmodel_path,
        allow_unreachable_classes=True,
        import_mode="merge",
    )

    assert [cls.name for cls in merged_model.classes].count("SharedClass") == 1
    assert [enum.name for enum in merged_model.enums].count("SharedStatus") == 1

    root = next(cls for cls in merged_model.classes if cls.name == "Root")
    assert all(
        isinstance(association, Association) for association in root.associations
    )
    assert {
        association.association_target.name for association in root.associations
    } == {
        "SharedClass",
        "SharedStatus",
    }


def test_reachability_follows_compositions_and_inheritance_only(tmp_path):
    """Require ownership paths while including derived classes in the owned tree."""
    model_path = tmp_path / "reachability_model.json"
    model = {
        "name": "ReachabilityModel",
        "enums": [],
        "classes": [
            {
                "name": "Root",
                "attributes": [],
                "associations": [
                    {
                        "name": "Children",
                        "multiplicity": "[0..*]",
                        "association_type": "COMPOSITION",
                        "target": "Child",
                    },
                    {
                        "name": "ReferenceOnly",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "ReferenceOnly",
                    },
                ],
                "inherits": [],
            },
            {
                "name": "Child",
                "attributes": [],
                "associations": [],
                "inherits": [],
            },
            {
                "name": "DerivedChild",
                "attributes": [],
                "associations": [],
                "inherits": ["Child"],
            },
            {
                "name": "ReferenceOnly",
                "attributes": [],
                "associations": [],
                "inherits": [],
            },
        ],
    }
    model_path.write_text(json.dumps(model), encoding="utf-8")

    parsed_model = parse_meta_model(structure_data(model), import_mode="merge")

    with pytest.raises(UnreachableClassError, match="ReferenceOnly"):
        merge_meta_models(parsed_model, model_path, import_mode="merge")
