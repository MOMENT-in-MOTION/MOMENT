import os

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CONFIG_PATH = Path(os.environ.get("APP_CONFIG_PATH", "src/api_config.json"))
