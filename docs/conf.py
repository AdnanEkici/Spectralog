from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SOURCE_DIRECTORY),
)


project = "SpectraLog"
author = "Adnan Ekici"
copyright = "2026"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
]

autosummary_generate = True

autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_preserve_defaults = True
autodoc_member_order = "bysource"

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True

autosectionlabel_prefix_document = True

intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3",
        None,
    ),
}

templates_path = [
    "_templates",
]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

html_theme = "furo"

html_static_path = [
    "_static",
]

html_title = "SpectraLog Documentation"

html_theme_options = {
    "navigation_with_keys": True,
}
