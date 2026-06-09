# Suppress the message: "Deprecated module 'parser.meta_model_parser'"" as pylint seems
# to confuse our parser module with the python built-in parser module
from .merger import merge_meta_models # pylint: disable=W4901

__all__ = [
    "merge_meta_models"
]
