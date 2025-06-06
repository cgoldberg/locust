#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

from locust.argument_parser import get_parser

import os
import shutil
import subprocess

import locust_cloud

# Add fixes for RTD deprecation
# https://about.readthedocs.com/blog/2024/07/addons-by-default/

# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True


# Run command `locust --help` and store output in cli-help-output.txt which is included in the docs
def save_locust_help_output():
    cli_help_output_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cli-help-output.txt")
    print(f"Running `locust --help` command and storing output in {cli_help_output_file}")
    help_output = subprocess.check_output(["locust", "--help"], text=True)
    with open(cli_help_output_file, "w") as f:
        f.write(help_output)


save_locust_help_output()


def get_locust_cloud_docs():
    locust_cloud_docs = os.path.join(locust_cloud.__path__[0], "docs/")
    print("Copying `locust-cloud` docs/")
    shutil.copytree(
        locust_cloud_docs, os.path.join(os.path.abspath(os.path.dirname(__file__)), "locust-cloud/"), dirs_exist_ok=True
    )


get_locust_cloud_docs()

# Generate RST table with help/descriptions for all available environment variables


def save_locust_env_variables():
    env_options_output_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config-options.rst")
    print(f"Generating RST table for Locust environment variables and storing in {env_options_output_file}")
    parser = get_parser()
    table_data = []
    for action in parser._actions:
        if action.env_var and action.help != "==SUPPRESS==":
            table_data.append(
                (
                    ", ".join([f"``{c}``" for c in action.option_strings]),
                    f"``{action.env_var}``",
                    ", ".join([f"``{c}``" for c in parser.get_possible_config_keys(action) if not c.startswith("--")]),
                    action.help,
                )
            )
    colsizes = [max(len(r[i]) for r in table_data) for i in range(len(table_data[0]))]
    formatter = " ".join("{:<%d}" % c for c in colsizes)
    rows = [formatter.format(*row) for row in table_data]
    edge = formatter.format(*["=" * c for c in colsizes])
    divider = formatter.format(*["-" * c for c in colsizes])
    headline = formatter.format(*["Command line", "Environment", "Config file", "Description"])
    output = "\n".join(
        [
            edge,
            headline,
            divider,
            "\n".join(rows),
            edge,
        ]
    )
    with open(env_options_output_file, "w") as f:
        f.write(output)


save_locust_env_variables()


# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
from locust import __version__

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx-prompt",
    "sphinx_substitution_extensions",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_search.extension",
    "sphinx_rtd_theme",
    "sphinxcontrib.googleanalytics",
]

# autoclass options
# autoclass_content = "both"

autodoc_typehints = "none"  # I would have liked to use 'description' but unfortunately it too is very verbose

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = {".rst": "restructuredtext"}

# The master toctree document.
master_doc = "index"

# General substitutions.
project = "Locust"
copyright = "2009-2025, Carl Byström, Jonatan Heyman, Lars Holmberg"

# Intersphinx config
intersphinx_mapping = {
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}


# The full version, including alpha/beta/rc tags.
release = __version__

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%B %d, %Y"

# List of documents that shouldn't be included in the build.
# unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# Sphinx will recurse into subversion configuration folders and try to read
# any document file within. These should be ignored.
# Note: exclude_dirnames is new in Sphinx 0.5
exclude_dirnames = []

# Options for HTML output
# -----------------------

html_show_sourcelink = False
html_file_suffix = ".html"
html_theme = "sphinx_rtd_theme"

# Custom CSS overrides
html_static_path = ["_static"]
html_css_files = ["_static/theme-overrides.css", "_static/css/rtd_sphinx_search.min.css"]

# Google Analytics ID
googleanalytics_id = "G-MCG99XYF9M"
googleanalytics_enabled = True

# HTML theme
# html_theme = "default"
# html_theme_options = {
#    "rightsidebar": "true",
#    "codebgcolor": "#fafcfa",
#    "bodyfont": "Arial",
# }

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'trac'

rst_prolog = f"""
.. |version| replace:: {__version__}
"""
