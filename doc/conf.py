# -*- coding: utf-8 -*-
#
# larch documentation build configuration file, created by
# sphinx-quickstart on Fri Feb 12 01:10:08 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
CURDIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.abspath(os.path.join('sphinx', 'ext')))

# from sphinxtr
import html_mods
import latex_mods

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.extlinks',
              'sphinx.ext.mathjax',  'sphinx.ext.ifconfig',
              'sphinx.ext.intersphinx']

# from sphinxtr
extensions.extend([
              'fix_equation_ref',
              'subfig',
              'numfig',
              'numsec',
              'natbib',
              'figtable',
              'singlehtml_toc',
              'singletext',
              ])


intersphinx_mapping = {'py': ('http://docs.python.org/', None)}


# Turns on numbered figures for HTML output
number_figures = True

# configures bibliography
# see http://wnielson.bitbucket.org/projects/sphinx-natbib/
natbib = {
    'file': 'larch.bib',
    'brackets': '[]',
    'separator': ',',
    'style': 'authors',
    'sort': False,
}

# List of patterns, relative to source directory, that match files and
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'larch'
author = u'Matthew Newville'
copyright = u'Matthew Newville, The University of Chicago, 2012'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
try:
    import larch
    release = larch.__version__
# The full version, including alpha/beta/rc tags.
except ImportError:
    release = 'unknown (larch import failed??)'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']
exclude_patterns = ['_build', 'sphinx', '_junk', 'epilog.rst']

#sphinxtr
# Ideally, we wouldn't have to do this, but sphinx seems to have trouble with
# directives inside only directives
if tags.has('latex'):
    master_doc = 'index_tex'
    exclude_patterns.append('index.rst')
else:
    master_doc = 'index'
    exclude_patterns.append('index_tex.rst')

#sphinxtr
# A string of reStructuredText that will be included at the end of
# every source file that is read.
rst_epilog = open(os.path.join(CURDIR, 'epilog.rst'),'r').read().decode('utf8')

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['sphinx/theme']

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_theme = 'default'
html_theme = 'larchdoc'
# html_theme = 'cloud'
# html_theme_path.append(csp.get_theme_dir())

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {'collapsiblesidebar': True}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title =

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typograpbhically correct entities.
html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'index': ['indexsidebar.html','searchbox.html']}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = False

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'larchdoc'
html_domain_indices = False

# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '11pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'larch.tex', u'Larch Documentation',
   u'Matthew Newville', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '_static/larchcones.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False


# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
latex_use_modindex = False

latex_additional_files = [
    #    'sphinx/tex/puthesis.cls',
    'sphinx/tex/preamble._tex',
    'sphinx/tex/refstyle.bst',
    'sphinx/tex/biblio.tex',
    'sphinx/tex/sphinx.sty',
    'larch.bib',
]

## \setcounter{secnumdepth}{2}
## \setcounter{tocdepth}{2}

latex_elements = {'pointsizee': '11pt',
                  'preamble': """
\input{preamble._tex}
\usepackage{sphinx}
""",
                 'footer':"""
input{biblio.tex}
"""
}

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
latex_domain_indices = False

latex_use_modindex = False
