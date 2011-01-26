#!/usr/bin/env python
#
# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.

"""
Traits-capable windowing framework.

The TraitsGUI project contains a toolkit-independent GUI abstraction layer
(known as Pyface), which is used to support the "visualization" features of
the Traits package. Thus, you can write code in terms of the Traits API
(views, items, editors, etc.), and let TraitsGUI and your selected toolkit
and back-end take care of the details of displaying them.

To display Traits-based user interfaces, in addition to the TraitsGUI project,
you must install one of the following combinations of packages:

- Traits, TraitsBackendWX, and wxPython
- Traits, TraitsBackendQt, and PyQt

Prerequisites
-------------
If you want to build TraitsGUI from source, you must first install
`setuptools <http://pypi.python.org/pypi/setuptools/0.6c8>`_.

"""
from setuptools import setup, find_packages


# FIXME: This works around a setuptools bug which gets setup_data.py metadata
# from incorrect packages. Ticket #1592
#from setup_data import INFO
setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")

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
    description = DOCLINES[1],
    download_url = ('http://www.enthought.com/repo/ETS/TraitsGUI-%s.tar.gz' %
                    INFO['version']),
    include_package_data = True,
    install_requires = INFO['install_requires'],
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = 'TraitsGUI',
    namespace_packages = [
        "enthought",
        "enthought.pyface",
        "enthought.pyface.ui",
        ],
    package_data = {
        '': ['library/*', 'images/*'],
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
