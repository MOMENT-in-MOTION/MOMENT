from dataclasses import dataclass
from pathlib import Path


@dataclass
class RuntimeConfig:
    metamodel_dir: Path

    @property
    def submodel_dir(self):
        return self.metamodel_dir.parent / "submodels"
