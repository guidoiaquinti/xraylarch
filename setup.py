#!/usr/bin/env python
"""
Setup.py for xraylarch
"""
from __future__ import print_function
from setuptools import setup, find_packages

import time
import os
import sys
import site
import platform
from glob import glob
import shutil
import subprocess

DEBUG = False
cmdline_args = sys.argv[1:]
INSTALL =  len(cmdline_args)> 0 and (cmdline_args[0] == 'install')

uname = sys.platform.lower()
if os.name == 'nt':
    uname = 'win'
if uname.startswith('linux'):
    uname = 'linux'

_version__ = None
with open(os.path.join('larch', 'version.py'), 'r') as version_file:
    lines = version_file.readlines()
    for line in lines:
        line = line[:-1]
        if line.startswith('__version__'):
            key, vers = [w.strip() for w in line.split('=')]
            __version__ = vers.replace("'",  "").replace('"',  "").strip()


##
## Dependencies: required and recommended modules
required_modules = {'numpy': 'numpy',
                    'scipy': 'scipy',
                    'matplotlib': 'matplotlib',
                    'h5py': 'h5py',
                    'sqlalchemy': 'sqlalchemy',
                    'requests': 'requests',
                    'six' : 'six',
                    'psutil': 'psutil',
                    'pyshortcuts': 'pyshortcuts',
                    'peakutils': 'peakutils',
                    'PIL' : 'pillow',
                    'asteval': 'asteval',
                    'uncertainties': 'uncertainties',
                    'lmfit': 'lmfit',
                    'yaml': 'pyyaml',
                    'termcolor': 'termcolor'}


graphics_modules = {'wx': 'wxPython', 'wxmplot': 'wxmplot', 'wxutils':'wxutils'}

xrd_modules  = {'pyFAI': 'pyFAI', 'CifFile' : 'PyCifRW', 'fabio': 'fabio',
                'dioptas': 'Dioptas'}

tomo_modules = {'tomopy': 'tomopy', 'skimage': 'scikit-image'}

epics_modules = {'epics': 'pyepics'}
scan_modules = {'epicsscan': 'epicsscan', 'psycopg2': 'psycopg2'}

spec_modules = {'silx': 'silx'}
pca_modules = {'sklearn': 'scikit-learn'}

testing_modules = {'nose': 'nose', 'pytest': 'pytest'}

all_modules = (('basic analysis', required_modules),
               ('graphics and plotting', graphics_modules),
               ('xrd modules', xrd_modules),
               ('tomography modules', tomo_modules),
               ('connecting to the EPICS control system', epics_modules),
               ('reading Spec files', spec_modules),
               ('PCA and machine learning', pca_modules),
               ('testing tools',  testing_modules))

modules_imported = {}
missing = []

try:
    import matplotlib
    matplotlib.use('WXAgg')
except:
    pass

print( 'Checking dependencies....')
for desc, mods in all_modules:
    for impname, modname in mods.items():
        if impname not in modules_imported:
            modules_imported[modname] = False
        try:
            x = __import__(impname)
            modules_imported[modname] = True
        except ImportError:
            s = (modname + ' '*25)[:25]
            missing.append('     %s %s' % (s, desc))

## For Travis-CI, need to write a local site config file
##
if os.environ.get('TRAVIS_CI_TEST', '0') == '1':
    time.sleep(0.2)


isdir = os.path.isdir
pjoin = os.path.join
psplit = os.path.split
pexists = os.path.exists

# system-wide larch directory
larchdir = pjoin(sys.exec_prefix, 'share', 'larch')

libfmt = 'lib%s.so'
exefmt = "%s"
bindir = 'bin'
pyexe = pjoin(bindir, 'python')
larchbin = 'larch'

if uname == 'darwin':
    libfmt = 'lib%s.dylib'
elif uname == 'win':
    libfmt = '%s.dll'
    exefmt = "%s.exe"
    bindir = 'Scripts'
    pyexe = 'python.exe'
    larchbin = 'larch-script.py'

if DEBUG:
    print("##  Settings  (Debug mode) ## ")
    print(" sys.prefix: ",  sys.prefix)
    print(" sys.exec_prefix: ",  sys.exec_prefix)
    print(" cmdline_args: ",  cmdline_args)
    print("##   ")


# construct list of files to install besides the normal python modules
# this includes the larch executable files, and all the larch plugins

data_files = []
scripts = ['larch', 'larch_server', 'feff8l', 'xas_viewer',
           'gse_mapviewer', 'gse_dtcorrect', 'xrd1d_viewer','xrd2d_viewer',
           'dioptas_larch', 'xrfdisplay', 'xrfdisplay_epics']

larch_apps = ['{0:s} = larch.apps:run_{0:s}'.format(n) for n in scripts]

plugin_dir = pjoin(larchdir, 'plugins')

pluginfiles = []
pluginpaths = []
for fname in glob('plugins/*'):
    if isdir(fname):
        pluginpaths.append(fname)
    else:
        pluginfiles.append(fname)

data_files.append((plugin_dir, pluginfiles))

for pdir in pluginpaths:
    pfiles = []
    filelist = []
    for ext in ('py', 'txt', 'db', 'dat', 'rst', 'lar',
                'dll', 'dylib', 'so'):
        filelist.extend(glob('%s/*.%s' % (pdir, ext)))
    for fname in filelist:
        if isdir(fname):
            print('Warning -- not walking subdirectories for Plugins!!')
        else:
            pfiles.append(fname)
    data_files.append((pjoin(larchdir, pdir), pfiles))

# Get all required packages from requirements.txt:
with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

packages = ['larch', 'larch.bin']
for pname in find_packages('larch'):
    packages.append('larch.%s' % pname)


if INSTALL:
    # before install:  remove historical cruft, including old plugins
    cruft = {'bin': ['larch_makeicons', 'larch_gui', 'larch_client',
                     'gse_scanviewer', 'feff8l_ff2x', 'feff8l_genfmt',
                     'feff8l_pathfinder', 'feff8l_pot', 'feff8l_rdinp',
                     'feff8l_xsph']}

    def remove_file(base, fname):
        fullname = pjoin(base, fname)
        if pexists(fullname):
            try:
                os.unlink(fullname)
            except:
                pass

    for category, flist in cruft.items():
        if category == 'bin':
            basedir = pjoin(sys.exec_prefix, bindir)
            for fname in flist:
                remove_file(basedir, fname)

    # remove all files in share/larch from earlier code layouts
    for dirname in ('plugins', 'dlls', 'icons'):
        fname = pjoin(larchdir, 'plugins')
        if os.path.exists(fname):
            shutil.rmtree(fname)


package_data = ['icons/*', 'xray/*.dat', 'xray/*.db', 'xrd/*.db',
                'bin/darwin64/*', 'bin/linux64/*', 'bin/win64/*']
# now we have all the data files, so we can run setup
setup(name = 'xraylarch',
      version = __version__,
      author = 'Matthew Newville and the X-rayLarch Development Team',
      author_email = 'newville@cars.uchicago.edu',
      url          = 'http://xraypy.github.io/xraylarch/',
      download_url = 'http://xraypy.github.io/xraylarch/',
      license = 'BSD',
      description = 'Synchrotron X-ray data analysis in python',
      packages = packages,
      package_data={'larch': package_data},
      entry_points = {'console_scripts' : larch_apps},
      data_files  = data_files,
      platforms = ['Windows', 'Linux', 'Mac OS X'],
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering'],
      )

def fix_darwin_exes():
    "fix anaconda python apps on MacOs to launch with pythonw"

    pyapp = pjoin(sys.prefix, 'python.app', 'Contents', 'MacOS', 'python')
    if not pexists(pyapp):
        return
    for script in scripts:
        appname = os.path.join(sys.exec_prefix, bindir, script)
        if os.path.exists(appname):
            with open(appname, 'r') as fh:
                try:
                    lines = fh.readlines()
                except IOError:
                    lines = ['-']
            time.sleep(.025)
            if len(lines) > 1:
                text = ["#!%s\n" % pyapp]
                text.extend(lines[1:])
                with open(appname, 'w') as fh:
                    fh.write("".join(text))

# on install, after setup
#   fix darwin exes to run with pythonw
#   create desktop icons
if INSTALL:
    if uname == 'darwin':
        fix_darwin_exes()
    subprocess.check_call((pjoin(sys.exec_prefix, pyexe),
                           pjoin(sys.exec_prefix, bindir, larchbin), '-m'))

if len(missing) > 0:
    dl = "#%s#" % ("="*75)
    msg = """%s
 Note: Some optional Python Packages were not found. Some functionality
 will not be available without these packages:

     Package Name              Needed for
     ----------------          ----------------------------------
%s
     ----------------          ----------------------------------

 If you need some of these capabilities, you can install them with
    `pip install <Package Name>` or `conda install <Package Name>`

 See the Optional Modules section of doc/installation.rst for more details.
%s"""
    print(msg % (dl, '\n'.join(missing), dl))
