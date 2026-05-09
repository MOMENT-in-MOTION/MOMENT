# Suppress the message: "Deprecated module 'parser.meta_model_parser'"" as pylint seems
# to confuse our parser module with the python built-in parser module
from .meta_model_parser import parse_meta_model # pylint: disable=W4901

__all__ = [
    "parse_meta_model"
]
