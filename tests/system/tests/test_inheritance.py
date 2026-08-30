import ast
from pathlib import Path

import pytest

# ignore import error for run_app fixture, as it is needed to run the tests
# pylint: disable=W0611
from tests.system.utils.run_app import run_app


@pytest.fixture
def create_class_tree(run_app):
    def _factory(config_path: Path | None = None):
        output_dir, proc = run_app(
            Path("tests/system/data/inheritance_metamodel.json"),
            config_path=config_path
        )
        assert proc.returncode == 0
        assert (output_dir / "class_code.py").exists()
        return ast.parse((output_dir / "class_code.py").read_text())
    return _factory


class TestInheritance:
    """
    Test the inheritance functionality of the application.
    """

    def test_classes_are_created(self, create_class_tree):
        config_path = Path("tests/system/data/configs/native_inheritance_config.json")
        class_tree = create_class_tree(config_path)
        classes_names = {"MetaModelDummy", "MetaClassDummy1", "MetaClassDummy2", "Interface"}


        classes = [n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef)]
        assert len(classes) == 4
        assert {n.name for n in classes} == classes_names

    def test_python_native_inheritance(self, create_class_tree):
        config_path = Path("tests/system/data/configs/native_inheritance_config.json")
        class_tree = create_class_tree(config_path)

        classes = [n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef)]
        class_dict = {cls.name: cls for cls in classes}

        # Check that MetaClassDummy1 inherits from MetaModelDummy
        assert any(
            base.id == "MetaModelDummy"
            for base in class_dict["MetaClassDummy1"].bases
            if isinstance(base, ast.Name)
        )

        # Check that MetaClassDummy2 inherits from MetaClassDummy1
        assert any(
            base.id == "MetaClassDummy1"
            for base in class_dict["MetaClassDummy2"].bases
            if isinstance(base, ast.Name)
        )

        # Check that MetaClassDummy2 inherits from Interface
        assert any(
            base.id == "Interface"
            for base in class_dict["MetaClassDummy2"].bases
            if isinstance(base, ast.Name)
        )

    def test_manual_inheritance(self, create_class_tree):
        config_path = Path("tests/system/data/configs/manual_inheritance_config.json")
        class_tree = create_class_tree(config_path)

        classes = [n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef)]
        class_dict = {cls.name: cls for cls in classes}

        # Get all fields of MetaClassDummy2, MetaClassDummy1, MetaModelDummy and Interface in
        # seperate lists
        mmd2_fields = [
            n for n in ast.walk(class_dict["MetaClassDummy2"]) if isinstance(n, ast.AnnAssign)
        ]
        mmd1_fields = [
            n for n in ast.walk(class_dict["MetaClassDummy1"]) if isinstance(n, ast.AnnAssign)
        ]
        mmd_fields = [
            n for n in ast.walk(class_dict["MetaModelDummy"]) if isinstance(n, ast.AnnAssign)
        ]
        interface_fields = [
            n for n in ast.walk(class_dict["Interface"]) if isinstance(n, ast.AnnAssign)
        ]

        mmd2_field_names = {
            n.target.id for n in mmd2_fields if isinstance(n.target, ast.Name)
        }
        mmd1_field_names = {
            n.target.id for n in mmd1_fields if isinstance(n.target, ast.Name)
        }
        mmd_field_names = {
            n.target.id for n in mmd_fields if isinstance(n.target, ast.Name)
        }
        interface_field_names = {
            n.target.id for n in interface_fields if isinstance(n.target, ast.Name)
        }

        # Check that MetaModelDummy1 has all fields from MetaModelDummy
        assert mmd_field_names.issubset(mmd1_field_names)

        # Check that MetaModelDummy2 has all fields from MetaModelDummy1, MetaModelDummy
        # and Interface
        assert mmd1_field_names.issubset(mmd2_field_names)
        assert mmd_field_names.issubset(mmd2_field_names)
        assert interface_field_names.issubset(mmd2_field_names)
