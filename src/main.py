import sys
import logging

from pathlib import Path

from metamodel.parser import parse_meta_model
from metamodel.codegenerator import generate_meta_model_api
from shared.load_json_as_dict import load_json_as_dict
from shared.configure_logging import configure_logging

from config import METAMODEL_API_DIR
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

    generated_code = generate_meta_model_api(meta_model=meta_model)

    for name, code in generated_code.items():

        with open(f"{METAMODEL_API_DIR}/{name}.py", "w", encoding="UTF-8") as text_file:
            text_file.write(code)


if __name__ == "__main__":
    main()
