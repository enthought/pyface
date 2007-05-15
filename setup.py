from setuptools import setup, find_packages

setup(
    name = 'enthought.pyface',
    version = '1.1.1',
    description  = 'Traits capable windowing framework',
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url          = 'http://code.enthought.com/ets',
    license      = 'BSD',
    zip_safe     = False,
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        "enthought.debug",
        "enthought.logger",
        "enthought.naming",
        "enthought.traits",
    ],
    extras_require = {
        'tvtk': [
            'enthought.tvtk',
            'enthought.persistence',
        ],
    },
    namespace_packages = [
        "enthought",
    ],
)
