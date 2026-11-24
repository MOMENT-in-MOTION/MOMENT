import ast
import subprocess
import sys
from pathlib import Path

import pytest

# ignore import error for run_app fixture, as it is needed to run the tests
# pylint: disable=W0611
from tests.system.utils.run_app import run_app


@pytest.fixture()
def class_tree(run_app):
    output_dir, proc = run_app(Path("tests/system/data/basic_metamodel.json"))
    assert proc.returncode == 0
    assert (output_dir / "class_code.py").exists()
    return ast.parse((output_dir / "class_code.py").read_text())


class TestBasicClass:
    """
    Test the basic class generation that the application creates a class from a json with the 
    default api_config.
    """

    def test_class_is_created(self, class_tree):
        classes = [n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef)]
        assert len(classes) == 1
        assert classes[0].name == "MyGeneratedClass"

    def test_class_has_init(self, class_tree):
        cls = next(n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef))
        method_names = [n.name for n in ast.walk(cls) if isinstance(n, ast.FunctionDef)]
        assert "__init__" in method_names

    def test_name_field_accessors_and_conventions(self, class_tree):
        cls = next(n for n in ast.walk(class_tree) if isinstance(n, ast.ClassDef))
        method_names = [n.name for n in ast.walk(cls) if isinstance(n, ast.FunctionDef)]

        assert "get_name" in method_names
        assert "set_name" in method_names

        # _name is assigned in __init__
        init = next(
            n for n in ast.walk(cls) if isinstance(n, ast.FunctionDef) and n.name == "__init__"
        )
        assignments = [n for n in ast.walk(init) if isinstance(n, ast.Assign)]
        target_names = [
            t.attr
            for a in assignments
            for t in a.targets
            if isinstance(t, ast.Attribute)
        ]
        assert "_name" in target_names

        # _name: str = "default" is a class-level annotated assignment
        ann_assigns = [n for n in cls.body if isinstance(n, ast.AnnAssign)]
        name_field = next(
            (n for n in ann_assigns if isinstance(n.target, ast.Name) and n.target.id == "_name"),
            None
        )
        assert name_field is not None, "_name class field not found"

        # type annotation is str
        assert isinstance(name_field.annotation, ast.Name) and name_field.annotation.id == "str"

        # default value is "default"
        assert isinstance(
            name_field.value, ast.Constant
        ) and isinstance(
            name_field.value.value, str
        )
        assert name_field.value.value == "default"

    def test_generated_serializer_and_deserializer_round_trip(self, run_app):
        output_dir, proc = run_app(Path("tests/system/data/basic_metamodel.json"))
        assert proc.returncode == 0, proc.stderr

        script = """
from pathlib import Path
from output.class_code import MyGeneratedClass
from output.deserializer import Deserializer
from output.serializer import Serializer

original = MyGeneratedClass(name="example")
for fmt in ("json", "xml"):
    Serializer(original).serialize(fmt, output_path=Path.cwd())
    text = Path(f"serialized_model.{fmt}").read_text(encoding="utf-8")
    assert Deserializer.from_text(fmt, text).to_dict() == original.to_dict()
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=output_dir.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
