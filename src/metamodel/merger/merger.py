from __future__ import annotations
import logging
from pathlib import Path

from ...metameta.m_m_m_classes import MetaClass, MetaModel, OpenAssociation
from ...metamodel.parser import parse_meta_model
from ...shared.load_json_as_dict import load_json_as_dict
from ...shared.structure import structure_data

logger = logging.getLogger(__name__)


class ModelMergeError(Exception):
    """Base exception for model merging errors."""


class MetaModelMerger:
    def __init__(self, main_model: MetaModel, main_import_path: Path):
        self.main_model = main_model
        self.visited_paths: set[Path] = {main_import_path}

    def merge(self) -> MetaModel:
        """Entry point for the merger that loads the main Meta-Model and all available
        sub-Meta-Models, merges them and returns the merged Meta-Model.
        Returns:
            MetaModel: The merged Meta-Model.
        """
        self._find_and_merge_imports()
        self._resolve_all_open_references()
        self._verify_all_resolved()
        return self.main_model

    def _find_and_merge_imports(self) -> None:
        """Recursively finds and merges all imported sub-models into the main model."""
        processed_classes: set[int] = set()

        while True:
            unprocessed = [
                c for c in self.main_model.classes if id(c) not in processed_classes
            ]
            if not unprocessed:
                break

            for cls in unprocessed:
                processed_classes.add(id(cls))
                for assoc in cls.associations:
                    if (
                        assoc.import_link
                        and assoc.import_link not in self.visited_paths
                    ):
                        self._load_and_merge_path(assoc.import_link)

    def _load_and_merge_path(self, path: Path) -> None:
        self.visited_paths.add(path)
        logger.info("Importing Meta-Model from path: %s", path)

        raw_dict = load_json_as_dict(path)
        meta_model_dict = structure_data(raw_dict)
        if meta_model_dict is None:
            raise ModelMergeError(
                f"The Meta_Model_Dict with path '{path}' could not be loaded."
            )

        new_model = parse_meta_model(meta_model_dict)
        self._merge_models(new_model)

    def _merge_models(self, new_model: MetaModel) -> None:
        existing_names = {cls.name for cls in self.main_model.classes}
        for cls in new_model.classes:
            if cls.name in existing_names:
                raise ModelMergeError(
                    f"Class name '{cls.name}' from model '{new_model.name}' is not unique."
                )

        self.main_model.classes.extend(new_model.classes)
        self.main_model.enums.extend(new_model.enums)

    def _resolve_all_open_references(self) -> None:
        class_map = {cls.name: cls for cls in self.main_model.classes}
        enum_map = {enum.name: enum for enum in self.main_model.enums}

        for cls in self.main_model.classes:
            for open_assoc in list(cls.associations):
                if not isinstance(open_assoc, OpenAssociation):
                    continue

                target_name = open_assoc.association_target_name
                if target := class_map.get(target_name) or enum_map.get(target_name):
                    cls.associations.append(open_assoc.to_association(target))
                    cls.associations.remove(open_assoc)
                else:
                    logger.warning(
                        "Association '%s' in class '%s' could not be resolved. "
                        "No class/enum '%s' found.",
                        open_assoc.name,
                        cls.name,
                        target_name,
                    )

    def _verify_all_resolved(self) -> bool:
        unresolved = [
            assoc.name
            for obj in self.main_model.classes
            for assoc in obj.associations
            if isinstance(assoc, OpenAssociation)
        ]
        if unresolved:
            logger.warning("Unresolved Associations remaining: %s", unresolved)
            return False
        return True


def merge_meta_models(metamodel: MetaModel, main_import_path: Path) -> MetaModel:
    """Entry point for merging the main Meta-Model with all sub-models."""
    return MetaModelMerger(metamodel, main_import_path).merge()
