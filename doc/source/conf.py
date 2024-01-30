import os
import sys
import django
from django.conf import settings

settings.configure()

sys.path.insert(0, os.path.abspath(os.path.join('..','..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'oc_lettings_site.settings'
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'orange_county'
copyright = '2024, Payssan Jonathan'
author = 'Payssan Jonathan'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.autodoc",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- GraphViz configuration ----------------------------------
graphviz_output_format = 'svg'

# sphinx-build -M html doc/source doc/build -D graphviz_dot="C:\Program Files\Graphviz\bin\dot.exe"