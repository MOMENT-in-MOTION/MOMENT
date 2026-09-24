import pytest

from src.metamodel.parser.meta_model_parser import parse_meta_model
from src.metamodel.codegenerator.codegenerator import generate_meta_model_api
from src.metamodel.codegenerator.formatter.formatter_factory import get_formatter
from tests.unit.utils.setup_desciptors import DEFAULT_CONFIG, make_grouped_import_model


def test_parse_meta_model_accepts_valid_merge_import_link_in_merge_mode():
    """Test that parse_meta_model accepts a valid file path when in merge mode."""
    meta_model = {
        "name": "demo",
        "enums": [],
        "classes": [
            {
                "name": "Car",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "C:/project/models/person.json",
                    }
                ],
                "inherits": [],
            }
        ],
    }

    parsed = parse_meta_model(meta_model, import_mode="merge")
    assert parsed.name == "demo"
    assert (
        parsed.classes[0].associations[0].import_link == "C:/project/models/person.json"
    )


def test_parse_meta_model_rejects_import_link_in_merge_mode():
    """Test that parse_meta_model rejects a module import when in merge mode."""
    meta_model = {
        "name": "demo",
        "enums": [],
        "classes": [
            {
                "name": "Car",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "package.module",
                    }
                ],
                "inherits": [],
            }
        ],
    }

    with pytest.raises(
        ValueError, match="Merge mode expects a JSON file path|ImportMode='import'"
    ):
        parse_meta_model(meta_model, import_mode="merge")


def test_parse_meta_model_rejects_module_name_in_merge_mode():
    """Bare module names are a strong sign the model was authored for import mode."""
    meta_model = {
        "name": "demo",
        "enums": [],
        "classes": [
            {
                "name": "Car",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "customer_domain",
                    }
                ],
                "inherits": [],
            }
        ],
    }

    with pytest.raises(
        ValueError, match="Merge mode expects a JSON file path|ImportMode='import'"
    ):
        parse_meta_model(meta_model, import_mode="merge")


def test_import_mode_resolves_local_model_targets():
    """Local classes/enums should still resolve in import mode without needing a merge pass."""
    meta_model = {
        "name": "demo",
        "enums": [{"name": "OrderStatus", "values": ["DRAFT", "CONFIRMED"]}],
        "classes": [
            {
                "name": "RetailPlatform",
                "attributes": [],
                "associations": [
                    {
                        "name": "orders",
                        "multiplicity": "[0..*]",
                        "association_type": "COMPOSITION",
                        "target": "Order",
                    },
                    {
                        "name": "status",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "OrderStatus",
                    },
                ],
                "inherits": [],
            },
            {
                "name": "Order",
                "attributes": [],
                "associations": [
                    {
                        "name": "platform",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "RetailPlatform",
                    }
                ],
                "inherits": [],
            },
        ],
    }

    parsed = parse_meta_model(meta_model, import_mode="import")
    merged = __import__(
        "src.metamodel.merger", fromlist=["merge_meta_models"]
    ).merge_meta_models(
        parsed,
        __import__("pathlib").Path("modelle_JSON/import_example.json"),
        import_mode="import",
    )

    assert any(
        assoc.name == "status" and assoc.association_target.name == "OrderStatus"
        for assoc in merged.classes[0].associations
    )
    assert any(
        assoc.name == "orders" and assoc.association_target.name == "Order"
        for assoc in merged.classes[0].associations
    )


def test_parse_meta_model_accepts_valid_import_link_in_import_mode():
    """Test that parse_meta_model accepts a valid module import when in import mode."""
    meta_model = {
        "name": "demo",
        "enums": [],
        "classes": [
            {
                "name": "Car",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "package.module",
                    }
                ],
                "inherits": [],
            }
        ],
    }

    parsed = parse_meta_model(meta_model, import_mode="import")
    assert parsed.classes[0].associations[0].import_link == "package.module"


def test_parse_meta_model_rejects_file_path_in_import_mode():
    """Test that parse_meta_model rejects a file path when in import mode."""
    meta_model = {
        "name": "demo",
        "enums": [],
        "classes": [
            {
                "name": "Car",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "/tmp/person.json",
                    }
                ],
                "inherits": [],
            }
        ],
    }

    with pytest.raises(
        ValueError,
        match="ImportMode='merge'|set the config option 'ImportMode' to 'merge'|merge mode",
    ):
        parse_meta_model(meta_model, import_mode="import")


def test_generate_meta_model_api_groups_module_imports_for_import_mode():
    """Test that the generator groups symbols from the same module into one import statement."""
    meta_model = parse_meta_model(
        make_grouped_import_model(),
        import_mode="import",
    )

    generated = generate_meta_model_api(
        meta_model=meta_model,
        api_config={**DEFAULT_CONFIG, "ImportMode": "import"},
        formatter=get_formatter("snake_case"),
        templates_dir=__import__("pathlib").Path("templates"),
    )

    assert "from models.person import Driver, Person" in generated["class_code"]
    assert "_owner: Person" in generated["class_code"]
    assert "_driver: Driver" in generated["class_code"]
