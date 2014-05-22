# Copyright (c) 2008-2013 by Enthought, Inc.
# All rights reserved.

from os.path import join
from setuptools import setup, find_packages


info = {}
pyface_init = join('pyface', '__init__.py')
exec(compile(open(pyface_init).read(), pyface_init, 'exec'), info)


setup(
    name = 'pyface',
    version = info['__version__'],
    url = 'http://code.enthought.com/projects/traits_gui',
    author = 'David C. Morrill, et al.',
    author_email = 'dmorrill@enthought.com',
    classifiers = [c.strip() for c in """\
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.split()) > 0],
    description = 'traits-capable windowing framework',
    long_description = open('README.rst').read(),
    download_url = ('http://www.enthought.com/repo/ets/pyface-%s.tar.gz' %
                    info['__version__']),
    install_requires = info['__requires__'],
    license = 'BSD',
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    package_data = {
        '': ['images/*'],
    },
    packages = find_packages(),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    zip_safe   = False,
    use_2to3 = True,
)
