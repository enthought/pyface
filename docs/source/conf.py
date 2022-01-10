# -*- coding: utf-8 -*-
#
# CodeTools documentation build configuration file, created by
# sphinx-quickstart on Tue Jul 22 09:56:01 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import os
import runpy
import sys

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    # Link to code in sphinx generated API docs
    "sphinx.ext.viewcode",
    'traits.util.trait_documenter'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General substitutions.
project = 'pyface'
copyright = '2008-2022, Enthought'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
version_py = os.path.join('..', '..', 'pyface', '_version.py')
version_content = runpy.run_path(version_py)
version = ".".join(version_content["version"].split(".", 2)[:2])
release = version

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directories, that shouldn't be searched
# for source files.
#exclude_dirs = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
#html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (within the static path) to place at the top of
# the sidebar.
#html_logo = "_static/e-logo-rev.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = "favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = False

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Pyfacedoc'

# html theme information
try:
    import enthought_sphinx_theme

    html_theme_path = [enthought_sphinx_theme.theme_path]
    html_theme = 'enthought'
except ImportError as exc:
    import warnings
    msg = "Can't find Enthought Sphinx Theme, using default.\nException was:\n{}"
    warnings.warn(RuntimeWarning(msg.format(exc)))

    # old defaults
    html_logo = "e-logo-rev.jpg"
    html_favicon = "et.png"
    html_style = 'default.css'

# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
    (
        'index', 'TraitsGUI.tex', 'TraitsGUI Documentation', 'Enthought',
        'manual'
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

# Options for autodoc
# -------------------

autodoc_member_order = 'bysource'

autodoc_mock_imports = [
    'wx',
    'wx.grid',
    'wx.html',
    'wx.lib',
    'wx.lib.scrolledpanel',
    'wx.lib.layoutf',
    'wx.lib.mixins',
    'wx.lib.mixins.grid',
    'wx.lib.wxpTag',
    'wx.lib.gridmovers',
    'wx.stc',
    'wx.py',
    'IPython',
    'IPython.frontend',
    'IPython.frontend.wx',
    'IPython.frontend.wx.wx_frontend',
]


def autodoc_skip_member(app, what, name, obj, skip, options):
    # Skip load_tests
    return skip or name == "load_tests"


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)

intersphinx_mapping = {
    "traits": ("http://docs.enthought.com/traits", None),
    "traitsui": ("http://docs.enthought.com/traitsui", None),
    "python": ("https://docs.python.org/3", None),
}
