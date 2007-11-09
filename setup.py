from setuptools import setup, find_packages


# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
DEVELOPER = etsdep('enthought.developer', '2.0b1')
ETSCONFIG = etsdep('enthought.etsconfig', '2.0b1')
IO = etsdep('enthought.io', '2.0b1')
NAMING = etsdep('enthought.naming', '2.0b1')
PERSISTENCE = etsdep('enthought.persistence', '2.0b1')
RESOURCE = etsdep('enthought.resource', '2.0b1')
TRAITS_UI = etsdep('enthought.traits[ui]', '2.0b1')
TRAITSUIWX = etsdep('enthought.traits.ui.wx', '2.0b1')
TVTK = etsdep('enthought.tvtk', '2.0b1')
UTIL = etsdep('enthought.util', '2.0b1')


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        'http://code.enthought.com/enstaller/eggs/source/unstable',
        ],
    description = 'Traits capable windowing framework',
    extras_require = {
        'dock': [
            DEVELOPER,
            IO,
            ],
        'tvtk': [
            PERSISTENCE,
            TVTK,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            #wx
            ],
        },
    include_package_data = True,
    install_requires = [
        ETSCONFIG,
        NAMING,
        RESOURCE,
        TRAITS_UI,
        TRAITSUIWX,
        UTIL,
        ],
    license = 'BSD',
    name = 'enthought.pyface',
    namespace_packages = [
        "enthought",
        "enthought.pyface",
        "enthought.pyface.ui",
        ],
    packages = find_packages(),
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = '3.0.0a1',
    zip_safe = False,
    )

