# This is a temporary hack until things are properly restructured.
from enthought.etsconfig.api import ETSConfig

if ETSConfig.toolkit == 'qt4':
    from scene_qt4 import Scene
else:
    from scene import Scene
    from simple_scene import SimpleScene
