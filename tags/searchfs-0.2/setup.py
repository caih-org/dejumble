"""SearchFS: mounts a directory with the results of a query.

SearchFS is a FUSE that lets the user mount a virtual directory with the result of a query. This query can be a shell script (find, locate, etc) or many other backends as beagle.
"""

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Programming Language :: Python
Topic :: Filesystems
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
Operating System :: Linux
Operating System :: MacOS
"""

from distutils.core import setup

doclines = __doc__.splitlines()

setup(name='searchfs',
      version='0.2',
      package_dir = {'' : 'src'},
      packages = ['SearchFS'],
      package_data = {'':['conf/*.conf']},
      py_modules = ['searchfs'],
      scripts = ['scripts/mount_search'],
      maintainer='Cesar Izurieta',
      maintainer_email='cesar@caih.org',
      url='http://caih.org/searchfs',
      license='http://www.gnu.org/copyleft/gpl.html',
      platforms=['unix'],
      description = doclines[0],
      classifiers = filter(None, classifiers.splitlines()),
      long_description = '\n'.join(doclines[2:]),
)
