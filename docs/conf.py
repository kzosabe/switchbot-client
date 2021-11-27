import os
import sys
sys.path.insert(0, os.path.abspath("../switchbot_client"))

project = "switchbot-client"
copyright = "2021, kzosabe"
author = "kzosabe"
release = "0.3.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
templates_path = ["_templates"]
exclude_patterns = ["_build", ".DS_Store"]
html_theme = "alabaster"
html_static_path = []
