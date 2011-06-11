# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.

from setuptools import setup, find_packages


# This works around a setuptools bug which gets setup_data.py metadata
# from incorrect packages.
setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']

setup(
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
                    INFO['version']),
    install_requires = INFO['install_requires'],
    license = 'BSD',
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = 'pyface',
    package_data = {
        '': ['images/*'],
        },
    packages = find_packages(),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    tests_require = [
        'nose >= 0.10.3',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/traits_gui',
    version = INFO['version'],
    zip_safe   = False,
)
