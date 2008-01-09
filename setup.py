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
APPTOOLS = etsdep('AppTools', '3.0.0b1')  # used in pyface/resource_manager, pyface/i_image_resource -- others are optional
DEVTOOLS_DEVELOPER = etsdep('DevTools[developer]', '3.0.0b1')  # all in pyface/dock
ENTHOUGHTBASE_UI = etsdep('EnthoughtBase[ui]', '3.0.0b1')
MAYAVI = etsdep('Mayavi', '2.0.3a1')  # all in pyface/tvtk
TRAITS_UI = etsdep('Traits[ui]', '3.0.0b1')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.0.0b1')
TRAITSBACKENDQT = etsdep('TraitsBackendQt', '3.0.0b1')


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = 'Traits capable windowing framework',
    extras_require = {
        'dock': [
            APPTOOLS,
            DEVTOOLS_DEVELOPER,
            TRAITSBACKENDWX,
            ],
        'qt': [
            TRAITSBACKENDQT,
            ],
        'tvtk': [
            APPTOOLS,
            MAYAVI,
            ],
        'wx': [
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            #wx
            ],
        },
    include_package_data = True,
    install_requires = [
        APPTOOLS,    # This should be removed -- see the TODO.txt file.
        ENTHOUGHTBASE_UI,
        TRAITS_UI
        ],
    license = 'BSD',
    name = 'TraitsGUI',
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
    version = '3.0.0b1',
    zip_safe = False,
    )

