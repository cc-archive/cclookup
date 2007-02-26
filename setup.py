"""
lookup build script
Builds platform appropriate packages for distribution.  Takes standard
distutils commands on non-Mac OS X platforms.  Builds a .app on Mac OS X.

Nathan R. Yergler

$Id$
"""

import os
import sys
import shutil
import fnmatch

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# set the basics for setup_requires (which is nothing on linux)
setup_requirements = []

# check for win32 support
if sys.platform == 'win32':
    # py2exe allows building of executables
    setup_requirements.append('py2exe')
    
    import py2exe

if sys.platform == 'darwin':
    # import Mac OS X-specific packages
    setup_requirements.append('py2app')
    
    import py2app

    #datafiles.append(('../Frameworks', []))


setup(name='cclookup',
      version='2.0',
      url='http://wiki.creativecommons.org/CcLookup',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',

      packages = ['cclookup', 'tagger', 'eyeD3'],

      setup_requires = setup_requirements,
      install_requires = ['setuptools',
                          'rdflib==2.3.3',
                          'ccrdf>=0.6a4',
                          'cctagutils>=0.5a1',
                          'rdfadict',
                         ],
      include_package_data = True,
      zip_safe = False,

      entry_points = {

    'console_scripts':['cclookup = cclookup:main'],
    },

      options={ "py2exe": {"packages": ["encodings", 'rdflib']},
                "py2app": {"argv_emulation": True,
                           "iconfile": os.path.join('resources', 'cc.icns')
                           }
                },
      )

## if ('py2app' in sys.argv):
## 	os.system('./make_dmg.sh %s' % version())
	
