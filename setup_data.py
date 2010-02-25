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


# Declare our ETS project dependencies:
APPTOOLS = etsdep('AppTools', '3.3.2')
ENTHOUGHTBASE_UI = etsdep('EnthoughtBase[ui]', '3.0.5')
TRAITS = etsdep('Traits', '3.3.1')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.3.1')
TRAITSBACKENDQT = etsdep('TraitsBackendQt', '3.3.1')


# A dictionary of the setup data information.
INFO = {
    'extras_require' : {

        # Extra denoting that the Traits UI DockWindow support should be
        # installed. DockWindow support allows Traits user interfaces with tabs
        # and splitters to be created when using the wxPython back-end:
        'dock': [
            TRAITSBACKENDWX,
            ],

        # Extra denoting that Traits user interface Qt toolkit support should
        # be installed:
        'qt': [
            TRAITSBACKENDQT,
            ],

        # Extra denoting that Traits user interface wxPython toolkit support
        # should be installed:
        'wx': [
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            #'wx',  # fixme: not available as an egg on all platforms.
            ],
        },
    'install_requires' : [
        ENTHOUGHTBASE_UI,
        TRAITS
        ],
    'name': 'TraitsGUI',
    'version': '3.3.1',
    }
