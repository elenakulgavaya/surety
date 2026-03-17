# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Surety'
copyright = '2026, Elena Kulgavaya'
author = 'Elena Kulgavaya'
html_title = 'Surety — Contract-Driven Testing Framework for Python'
html_baseurl = 'https://surety.readthedocs.io/en/latest/'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_css_files = ["custom.css"]
html_favicon = "_static/surety.ico"
html_logo = "_static/surety.png"
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar-links.html",   # <-- our custom block
    ]
}
html_meta = {
    "google-site-verification": "kkzPK605few1TEm02D81pw_QzbuKvXapr7pXLks8r7k",
    "description": (
        "Surety is a Python contract-driven testing framework. "
        "Define schemas as Python classes, generate realistic test data, "
        "and validate API, database, and UI interactions deterministically."
    ),
    "keywords": (
        "python testing, contract testing, contract-driven testing, "
        "test automation, schema validation, api testing, test data generation, surety"
    ),
}
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/elenakulgavaya/surety/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "sidebar_hide_name": True,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

