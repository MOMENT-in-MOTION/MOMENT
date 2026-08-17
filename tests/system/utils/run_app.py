import subprocess
import sys
from pathlib import Path

import os
import pytest


@pytest.fixture()
def run_app(tmp_path):
    """
    Factory fixture. Returns a callable that:
      - writes input_data as JSON to a temp file
      - invokes `python -m src.main --input <path> --output <path>`
      - returns (output_path, CompletedProcess) for assertions
    """
    def _run(
        input_path: Path,
        config_path: Path | None = None
    ) -> tuple[Path, subprocess.CompletedProcess]:
        # overwrite the api_config in tests
        env = os.environ.copy()
        if config_path is not None:
            env["APP_CONFIG_PATH"] = str(config_path)
        
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        cmd = [
            sys.executable, "-m", "src.main",
            str(input_path),
            "--output", str(output_dir),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return output_dir, result

    return _run
