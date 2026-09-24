from __future__ import annotations

import json
from pathlib import Path

import pytest

# pytest fixture registration; used indirectly by tests.
# pylint: disable=W0611
from tests.system.utils.run_app import run_app
from tests.unit.utils.setup_desciptors import DEFAULT_CONFIG, make_grouped_import_model

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT_ROOT = PROJECT_ROOT / "tests" / "system" / "data" / "snapshots"


def _write_api_config(tmp_path: Path, **overrides) -> Path:
    """Create a temporary API config that the CLI will read through APP_CONFIG_PATH."""
    config = DEFAULT_CONFIG.copy()
    config.update(overrides)
    config_path = tmp_path / "api_config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path


class TestSnapshots:
    """Snapshot checks for the application CLI output from realistic metamodel inputs."""

    @pytest.mark.parametrize(
        "json_name, config_overrides",
        [
            (
                "snsh_merge_json.json",
                {"AllowUnreachableClasses": "true", "ImportMode": "merge"},
            ),
            (
                "snsh_variance_base.json",
                {"AllowUnreachableClasses": "true", "ImportMode": "merge"},
            ),
            (
                "snsh_variance_imported.json",
                {"AllowUnreachableClasses": "false", "ImportMode": "merge"},
            ),
            (
                "snsh_variance_inheritance.json",
                {"AllowUnreachableClasses": "true", "ImportMode": "merge"},
            ),
            (
                "snsh_import_mode.json",
                {"AllowUnreachableClasses": "false", "ImportMode": "import"},
            ),
        ],
    )
    def test_complete_model_snapshot(
        self, run_app, tmp_path, json_name, config_overrides
    ):
        """Verify end-to-end generated code matches the expected snapshots."""
        metamodel_path = SNAPSHOT_ROOT / "test_jsons" / json_name
        assert metamodel_path.exists(), f"Missing snapshot input: {metamodel_path}"

        config_path = _write_api_config(tmp_path, **config_overrides)
        output_dir, proc = run_app(metamodel_path, config_path=config_path)

        assert proc.returncode == 0, proc.stderr

        class_snapshot = (
            SNAPSHOT_ROOT / f"{metamodel_path.stem}_class_code.py"
        ).read_text(encoding="utf-8")
        enum_snapshot = (
            SNAPSHOT_ROOT / f"{metamodel_path.stem}_enum_code.py"
        ).read_text(encoding="utf-8")

        assert (output_dir / "class_code.py").read_text(
            encoding="utf-8"
        ) == class_snapshot
        assert (output_dir / "enum_code.py").read_text(
            encoding="utf-8"
        ) == enum_snapshot

    def test_import_mode_snapshot_groups_symbols_from_same_module(
        self, run_app, tmp_path
    ):
        """Verify the CLI groups imports from the same external module in import mode."""
        metamodel_path = tmp_path / "grouped_import_model.json"
        metamodel_path.write_text(
            json.dumps(make_grouped_import_model()), encoding="utf-8"
        )

        config_path = _write_api_config(tmp_path, ImportMode="import")
        output_dir, proc = run_app(metamodel_path, config_path=config_path)

        assert proc.returncode == 0, proc.stderr
        generated = (output_dir / "class_code.py").read_text(encoding="utf-8")

        assert "from models.person import Driver, Person" in generated
