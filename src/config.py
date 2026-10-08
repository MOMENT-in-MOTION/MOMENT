from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CONFIG_PATH = Path(__file__).resolve().with_name("api_config.json")
