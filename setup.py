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

from distutils.core import setup
from cctagutils.const import version

packageroot = "."

def cleanManifest():
    try:
        os.remove('MANIFEST')
    except:
        pass
    
datafiles = [('', ['lookup.xrc',
          			os.path.join('resources','cc.ico'),
          			os.path.join('resources', 'publishguy_small.gif'),
          			'version.txt',
          			]
          	),
    		]

# check for win32 support
if sys.platform == 'win32':
    # py2exe allows building of executables
    import py2exe

if sys.platform == 'darwin':
	# import Mac OS X-specific packages
	import py2app
	
	datafiles.append(('../Frameworks', []))
	
# call the standard distutils builder for the GUI app
cleanManifest()

setup(name='ccLookup',
      version=version(),
      url='http://creativecommons.org',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',
      py_modules=['lookup', 'about', 'html'],
      data_files= datafiles,
      windows=[{'script':'lookup.py',
                'icon_resources':[(1, os.path.join('resources','cc.ico'))]
               }],
      app=['lookup.py'],
      scripts=['lookup.py', ],
      packages=['cctagutils', 'tagger', 'ccrdf',
                'rdflib', 'rdflib.syntax',
                'rdflib.syntax.serializers', 'rdflib.syntax.parsers',
                'rdflib.backends', 'rdflib.model',],
      options={ "py2exe": {"packages": ["encodings", 'rdflib']},
    			"py2app": {"argv_emulation": True,
    						"iconfile": os.path.join('resources', 'cc.icns')
    						}
               },
      )

if ('py2app' in sys.argv):
	os.system('./make_dmg.sh %s' % version())
	