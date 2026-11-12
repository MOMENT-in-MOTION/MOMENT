import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

project = "MOMENT"
copyright = "2026, MOMENT contributors"
author = "MOMENT contributors"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

templates_path = []
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = []
