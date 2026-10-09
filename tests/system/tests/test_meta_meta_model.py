import ast
import dataclasses
from enum import Enum
from pathlib import Path

import pytest

# ignore import error for run_app fixture, as it is needed to run the tests
# pylint: disable=W0611
from tests.system.utils.run_app import run_app
# ignore import error as the imported classes are used for comparison with the generated classes
# pylint: disable=W0614, W0401
from src.metameta.m_m_m_classes import *

META_META_MODEL = Path("src/metameta/meta_meta_model.json")
CONFIG = Path("tests/system/data/configs/meta_meta_model_config.json")


def all_subclasses(root: type) -> set[type]:
    """Return root and all of its transitive subclasses."""
    return {root}.union(*(all_subclasses(sub) for sub in root.__subclasses__()))


EXPECTED_CLASSES = {c.__name__: c for c in all_subclasses(MetaElement)}
EXPECTED_ENUMS = {e.__name__: e for e in (AssociationOptions, TypeOptions)}


@pytest.fixture
def generate(run_app):
    """Run MOMENT on the meta-meta-model and return the source of one generated file."""
    def _generate(filename: str) -> str:
        output_dir, proc = run_app(META_META_MODEL, config_path=CONFIG)
        assert proc.returncode == 0
        assert (output_dir / filename).exists()
        return (output_dir / filename).read_text()
    return _generate


@pytest.fixture
def generated_classes(generate):
    """All class definitions (AST nodes) of the generated class code."""
    tree = ast.parse(generate("class_code.py"))
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


@pytest.fixture
def generated_enums(generate):
    """All enums of the generated enum code, as {name: enum class}."""
    namespace: dict = {}
    # pylint: disable=W0122
    exec(compile(generate("enum_code.py"), "<generated>", "exec"), namespace)
    return {
        name: obj
        for name, obj in namespace.items()
        if isinstance(obj, type) and issubclass(obj, Enum) and obj is not Enum
    }


class TestMetaMetaModel:
    """
    Verify that MOMENT generates the same api from the json meta-meta-model as the one defined
    in the m_m_m_classes.py file.
    """

    def test_root_class_is_created(self, generated_classes):
        assert len(generated_classes) == 9
        assert generated_classes[0].name == "MetaElement"

    def test_classes_are_the_same_as_in_m_m_m_classes(self, generated_classes):
        assert {c.name for c in generated_classes} == set(EXPECTED_CLASSES)

    def test_classes_have_same_attributes_as_in_m_m_m_classes(self, generated_classes):
        for cls in generated_classes:
            # The root class has no attributes and is not a dataclass
            if cls.name == "MetaElement":
                continue

            generated = {n.target.id for n in cls.body if isinstance(n, ast.AnnAssign)}
            expected = {f.name for f in dataclasses.fields(EXPECTED_CLASSES[cls.name])}

            assert generated == expected, (
                f"Attributes mismatch for class {cls.name}: "
                f"generated={sorted(generated)}, expected={sorted(expected)}"
            )

    def test_enums_are_the_same_as_in_m_m_m_classes(self, generated_enums):
        assert set(generated_enums) == set(EXPECTED_ENUMS)

    def test_enums_have_same_members_as_in_m_m_m_classes(self, generated_enums):
        assert generated_enums, "No enums were generated"
        for name, gen_enum in generated_enums.items():
            generated = set(gen_enum.__members__)
            expected = set(EXPECTED_ENUMS[name].__members__)
            assert generated == expected, (
                f"Members mismatch for enum {name}: "
                f"generated={sorted(generated)}, expected={sorted(expected)}"
            )
