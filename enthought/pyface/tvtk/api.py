# This is a temporary hack until things are properly restructured.
from enthought.etsconfig.api import ETSConfig

if ETSConfig.toolkit == 'qt4':
    from decorated_scene_qt4 import DecoratedScene
    from scene_qt4 import Scene
else:
    from decorated_scene import DecoratedScene
    from scene import Scene

    # Note that SimpleScene is deprecated.
    from simple_scene import SimpleScene
