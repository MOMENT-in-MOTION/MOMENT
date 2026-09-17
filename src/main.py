import sys
import logging
import argparse

from pathlib import Path

from .config import PROJECT_ROOT, TEMPLATES_DIR, CONFIG_PATH

from .metamodel.parser import parse_meta_model
from .metamodel.codegenerator import (
    generate_meta_model_api,
    write_generated_code,
    get_formatter
)
from .metamodel.merger import merge_meta_models, UnreachableClassError, ModelMergeError
from .shared.structure import structure_data
from .shared.load_json_as_dict import load_json_as_dict
from .shared.configure_logging import configure_logging


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
        "-o", "--output",
        metavar="output_path",
        type=Path,
        default=Path(PROJECT_ROOT / "output"),
        help="Output directory for generated files (default: project-root/output/)",
        required=False
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging",
        required=False
    )
    args = parser.parse_args()

    if not args.metamodel.endswith(".json"):
        parser.error("Path must point to a .json file")

    metamodel_dir = Path(args.metamodel)

    configure_logging(verbose = args.verbose)

    try:
        meta_model_dict = structure_data(load_json_as_dict(metamodel_dir))

        api_config = load_json_as_dict(CONFIG_PATH)
        allow_unreachable = api_config.get("AllowUnreachableClasses", "false").lower() == "true"

        metamodel = parse_meta_model(meta_model_dict=meta_model_dict)
        merge_meta_models(
            metamodel,
            metamodel_dir,
            allow_unreachable_classes=allow_unreachable
        )

        logger.debug(metamodel.pretty())

        if api_config is not None:
            formatter = get_formatter(api_config["NamingConvention"])

            # create output dir if it doesn't exist
            args.output.mkdir(parents=True, exist_ok=True)

            generated_code = generate_meta_model_api(
                meta_model=metamodel,
                api_config=api_config,
                formatter=formatter,
                templates_dir=TEMPLATES_DIR,
            )

            write_generated_code(generated_code=generated_code, output_dir=args.output)
            logger.info(
                "Metamodel API generation completed successfully. Files written to: %s",
                args.output
            )
        else:
            raise ValueError(f"API configuration could not be loaded. "
                                f"Please check the configuration file at this path: {CONFIG_PATH}")
    except (UnreachableClassError, ModelMergeError, IOError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
