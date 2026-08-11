import sys
import logging
import argparse

from pathlib import Path

from .config import METAMODEL_API_DIR, TEMPLATES_DIR

from .metamodel.parser import parse_meta_model
from .metamodel.codegenerator import (
    generate_meta_model_api,
    write_generated_code,
    get_formatter,
    get_serializer
)
from .shared.structure import structure_data
from .shared.load_json_as_dict import load_json_as_dict
from .shared.configure_logging import configure_logging
from .metamodel.merger import merge_meta_models


logger = logging.getLogger(__name__)


def main():
    """Entry point for the application."""

    parser = argparse.ArgumentParser(description="MOMENT metamodel code generator")
    parser.add_argument(
        "metamodel",
        metavar="path-to-metamodel",
        help="Path to the metamodel JSON file"
    )
    parser.add_argument(
        "-s", "--serialize",
        metavar="format",
        choices=["json", "xml"],
        help="Serialize the parsed metamodel to the given format instead of generating code"
    )
    args = parser.parse_args()

    if not args.metamodel.endswith(".json"):
        parser.error("Path must point to a .json file")

    metamodel_dir = Path(args.metamodel)

    configure_logging(verbose = True)

    try:
        meta_model_dict = structure_data(load_json_as_dict(metamodel_dir))
    except IOError as e:
        print(getattr(e, "message", str(e)))
        sys.exit(1)

    metamodel = parse_meta_model(meta_model_dict=meta_model_dict)
    merge_meta_models(metamodel, metamodel_dir)
    logger.debug(metamodel.pretty())

    path=Path("src/api_config.json")

    api_config = load_json_as_dict(path)
    if api_config is not None:
        formatter = get_formatter(api_config["NamingConvention"])

        serializer = get_serializer(args.serialize) if args.serialize is not None else None

        generated_code = generate_meta_model_api(
            meta_model=metamodel,
            api_config=api_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
            serializer=serializer
        )

        write_generated_code(generated_code=generated_code, output_dir=METAMODEL_API_DIR)
    else:
        raise ValueError(f"API configuration could not be loaded. "
                         f"Please check the configuration file at this path: {path}")

if __name__ == "__main__":
    main()
