import sys
import logging

from pathlib import Path

from metamodel.parser import parse_meta_model
from metamodel.codegenerator import (
    generate_meta_model_api,
    write_generated_code,
    get_formatter
)
from shared.load_json_as_dict import load_json_as_dict
from shared.configure_logging import configure_logging

from config import METAMODEL_API_DIR, TEMPLATES_DIR
logger = logging.getLogger(__name__)


def main():
    """Entry point for the application."""

    if len(sys.argv) != 2:
        print("Usage: python main.py <path-to-metamodel> ")
        sys.exit(1)

    if not sys.argv[1].endswith(".json"):
        print("Path must be to json file!")
        sys.exit(1)

    path = Path(sys.argv[1])
    configure_logging(verbose = True)

    try:
        meta_model_dict = load_json_as_dict(path=path)
    except IOError as e:
        print(getattr(e, "message", str(e)))
        sys.exit(1)

    print(f"Successfully loaded metamodel: {path}")

    meta_model = parse_meta_model(meta_model_dict=meta_model_dict)

    logger.debug(meta_model)
    print(meta_model.pretty())

    api_config = load_json_as_dict(path=Path("src/api_config.json"))
    formatter = get_formatter(api_config["NamingConvention"])

    generated_code = generate_meta_model_api(
        meta_model=meta_model,
        api_config=api_config,
        formatter=formatter,
        templates_dir=TEMPLATES_DIR
    )

    write_generated_code(generated_code=generated_code, output_dir=METAMODEL_API_DIR)


if __name__ == "__main__":
    main()
