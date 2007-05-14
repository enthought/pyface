#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
"""A VTK interactor scene widget.  See the class docs for more
details.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2004-2006, Enthought, Inc.
# License: BSD Style.


import sys
import types
import os
import os.path
import tempfile

import wx
from enthought.pyface.tvtk.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

from enthought.pyface.api import Widget
from enthought.traits.api import Any, Int, Property, Instance, Event, \
                                 Range, Bool, Trait, Button
from enthought.traits.ui.api import View, Group, Item, InstanceEditor

from enthought.pyface.tvtk import picker
from enthought.pyface.tvtk import light_manager

VTK_VER = tvtk.Version().vtk_version


######################################################################
# `FullScreen` class.
######################################################################
class FullScreen(object):
    """Creates a full screen interactor widget.  This will use VTK's
    event loop until the user presses 'q'/'e' on the full screen
    window.  This does not yet support interacting with any widgets on
    the renderered scene.

    This class is really meant to be used for VTK versions earlier
    than 5.1 where there was a bug with reparenting a window.

    """
    def __init__(self, scene):
        self.scene = scene
        self.old_rw = scene.render_window
        self.ren = scene.renderer

    def run(self):
        # Remove the renderer from the current render window.
        self.old_rw.remove_renderer(self.ren)

        # Creates renderwindow tha should be used ONLY for
        # visualization in full screen
        full_rw = tvtk.RenderWindow(stereo_capable_window=True,
                                    full_screen=True
                                    )
        # add the current visualization
        full_rw.add_renderer(self.ren)

        # Under OS X there is no support for creating a full screen
        # window so we set the size of the window here.
        if sys.platform  == 'darwin':
            full_rw.size = tuple(wx.GetDisplaySize())

        # provides a simple interactor
        style = tvtk.InteractorStyleTrackballCamera()
        self.iren = tvtk.RenderWindowInteractor(render_window=full_rw,
                                                interactor_style=style)

        # Gets parameters for stereo visualization
        if self.old_rw.stereo_render:
            full_rw.set(stereo_type=self.old_rw.stereo_type, stereo_render=True)

        # Starts the interactor
        self.iren.initialize()
        self.iren.render()
        self.iren.start()

        # Once the full screen window is quit this releases the
        # renderer before it is destroyed, and return it to the main
        # renderwindow.
        full_rw.remove_renderer(self.ren)
        self.old_rw.add_renderer(self.ren)
        self.old_rw.render()
        self.iren.disable()


######################################################################
# `PopupScene` class.
######################################################################
class PopupScene(object):
    """Pops up a Scene instance with an independent `wx.Frame` in
    order to produce either a standalone window or usually a full
    screen view with *complete* interactivity (including widget
    interaction).
    """
    def __init__(self, scene):
        self.orig_parent = None
        self.orig_size = None
        self.orig_pos = None
        self.frame = None
        self.scene = scene
        self.vtk_control = self.scene._vtk_control

    def _setup_frame(self):
        vtk_control = self.vtk_control
        self.orig_parent = vtk_control.GetParent()
        self.orig_size = vtk_control.GetSize()
        self.orig_pos = vtk_control.GetPosition()
        f = self.frame = wx.Frame(None, -1)
        return f

    def popup(self, size=None):
        """Create a popup window of scene and set its default size.
        """
        vc = self.vtk_control
        f = self._setup_frame()
        if size is None:
            f.SetSize(vc.GetSize())
        else:
            f.SetSize(size)
        f.Show(True)
        vc.Reparent(f)

    def fullscreen(self):
        """Create a popup window of scene.
        """
        f = self._setup_frame()
        f.Show(True)
        self.vtk_control.Reparent(f)
        f.ShowFullScreen(True)

    def close(self):
        """Close the window and reparent the TVTK scene.
        """
        f = self.frame
        if f is None:
            return

        vc = self.vtk_control
        vc.Reparent(self.orig_parent)
        vc.SetSize(self.orig_size)
        vc.SetPosition(self.orig_pos)
        f.ShowFullScreen(False)
        f.Show(False)
        f.Close()
        self.frame = None


######################################################################
# `Scene` class.
######################################################################
class Scene(Widget):
    """A VTK interactor scene widget.

    This widget uses a RenderWindowInteractor and therefore supports
    interaction with VTK widgets.  The widget uses TVTK.  The widget
    also supports the following:

    - Save the scene to a bunch of common (and not so common) image
      formats.

    - save the rendered scene to the clipboard.

    - adding/removing lists/tuples of actors

    - setting the view to useful predefined views (just like in
      MayaVi).

    - If one passes `stereo=1` to the constructor, stereo rendering is
      enabled.  By default this is disabled.  Changing the stereo trait
      has no effect during runtime.

    - One can disable rendering by setting `disable_render` to True.

    - This widget supports picking data on screen.  Press 'p' or 'P'
      when the mouse is over a point that you need to pick.

    - The widget also uses a light manager to manage the lighting of
      the scene.  Press 'l' or 'L' to activate a GUI configuration
      dialog for the lights.

    - Pressing the left, right, up and down arrow let you rotate the
      camera in those directions.  When shift-arrow is pressed then
      the camera is panned.  Pressing the '+' (or '=')  and '-' keys
      let you zoom in and out.

    """

    # The version of this class.  Used for persistence.
    __version__ = 0

    ###########################################################################
    # Traits.
    ###########################################################################

    # Turn on/off stereo rendering.  This is set on initialization and
    # has no effect once the widget is realized.
    stereo = Bool(False)

    # Perform line smoothing for all renderered lines.  This produces
    # much nicer looking lines but renders slower.  This setting works
    # only when called before the first render.
    line_smoothing = Bool(False)

    # Perform point smoothing for all renderered points.  This
    # produces much nicer looking points but renders slower.  This
    # setting works only when called before the first render.
    point_smoothing = Bool(False)

    # Perform polygon smoothing (anti-aliasing) for all rendered
    # polygons.  This produces much nicer looking points but renders
    # slower.  This setting works only when called before the first
    # render.
    polygon_smoothing = Bool(False)

    # Enable parallel projection.  This trait is synchronized with
    # that of the camera.
    parallel_projection = Bool(False, desc='if the camera uses parallel projection')

    # Disable rendering.
    disable_render = Bool(False, desc='if rendering is to be disabled')

    # Enable off-screen rendering.  This allows a user to render the
    # scene to an image without the need to have the window active.
    # For example, the application can be minimized and the saved
    # scene should be generated correctly.  This is handy for batch
    # scripts and the like.  This works under Win32.  Under Mac OS X
    # and Linux it requires a recent VTK version (later than Oct 2005
    # and ideally later than March 2006) to work correctly.
    off_screen_rendering = Bool(False, desc='if off-screen rendering is enabled')

    # The background color of the window.  This is really a shadow
    # trait of the renderer's background.  Delegation does not seem to
    # work nicely for this.
    background = Trait(vtk_color_trait((0.5, 0.5, 0.5)),
                       desc='the background color of the window')

    # The default foreground color of any actors.  This basically
    # saves the preference and actors will listen to changes --
    # the scene itself does not use this.
    foreground = Trait(vtk_color_trait((1.0, 1.0, 1.0)),
                       desc='the default foreground color of actors')

    # The magnification to use when generating images from the render
    # window.
    magnification = Range(1, 2048, 1,
                          desc='the magnification used when the screen is saved to an image')

    # Specifies the number of frames to use for anti-aliasing when
    # saving a scene.  This basically increases
    # `self.render_window.aa_frames` in order to produce anti-aliased
    # figures when a scene is saved to an image.  It then restores the
    # `aa_frames` in order to get interactive rendering rates.
    anti_aliasing_frames = Range(0, 20, 8, desc='number of frames to use for anti-aliasing when saving a scene')

    # Default JPEG quality.
    jpeg_quality = Range(10, 100, 95, desc='the quality of the JPEG image to produce')

    # Default JPEG progressive setting.
    jpeg_progressive = Bool(True, desc='if the generated JPEG should be progressive')

    # Turn on full-screen rendering.
    full_screen = Button('Full Screen')

    # The picker handles pick events.
    picker = Instance(picker.Picker)

    # The light manager is called when 'l' is pressed on the scene.
    light_manager = Instance(light_manager.LightManager)

    # Event fired when an actor is added to the scene.
    actor_added = Event
    # Event fired when any actor is removed from the scene.
    actor_removed = Event

    ########################################
    # Properties.

    # The interactor used by the scene.
    interactor = Property(Instance(tvtk.GenericRenderWindowInteractor))

    # The render_window.
    render_window = Property(Instance(tvtk.RenderWindow))

    # The renderer.
    renderer = Property(Instance(tvtk.Renderer))

    # The camera.
    camera = Property(Instance(tvtk.Camera))

    ########################################

    # Render_window's view.
    _stereo_view = Group(Item(name='stereo_render'),
                         Item(name='stereo_type'),
                         show_border=True,
                         label='Stereo rendering',
                         )

    # The default view of this object.
    default_view = View(Group(
                            Group(Item(name='background'),
                                  Item(name='foreground'),
                                  Item(name='parallel_projection'),
                                  Item(name='disable_render'),
                                  Item(name='off_screen_rendering'),
                                  Item(name='jpeg_quality'),
                                  Item(name='jpeg_progressive'),
                                  Item(name='magnification'),
                                  Item(name='anti_aliasing_frames'),
                                  Item(name='full_screen',
                                       show_label=False),
                                  ),
                            Group(Item(name='render_window',
                                       style='custom',
                                       visible_when='object.stereo',
                                       editor=InstanceEditor(view=View(_stereo_view)),
                                       show_label=False),
                                  )
                            )
                        )

    ########################################
    # Private traits.

    # The renderer instance.
    _renderer = Instance(tvtk.Renderer)
    _renwin = Instance(tvtk.RenderWindow)
    _vtk_control = Instance(wxVTKRenderWindowInteractor)
    _fullscreen = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    def __init__(self, parent, **traits):
        """ Initializes the object. """

        # Base class constructor.
        super(Scene, self).__init__(**traits)

        # Used to set the view of the scene.
        self._def_pos = 1

        # Create the widget's toolkit-specific control.
        # NOTE: Because there may be derived classes that wrap the vtk widget
        # within a panel containing other decorations, no one should assume
        # the widget is available from the self.control trait!  Use the trait
        # self._vtk_control created within this classes _create_control method.
        self.control = self._create_control(parent)

        # Setup the default picker.
        self.picker = picker.Picker(self)

        # The light manager is created in the OnPaint method.  This is
        # because the lights can be configured only when the window is
        # realized.  Doing it before that leads to errors when
        # embedding the Scene into a wx.Notebook.

    def __get_pure_state__(self):
        """Allows us to pickle the scene."""
        # The control attribute is not picklable since it is a VTK
        # object so we remove it.
        d = self.__dict__.copy()
        for x in ['control', '_renwin', '_vtk_control',
                  '__sync_trait__', '_fullscreen']:
            d.pop(x, None)
        # Additionally pickle these.
        d['camera'] = self.camera
        return d

    def __getstate__(self):
        return state_pickler.dumps(self)

    def __setstate__(self, str_state):
        # This method is unnecessary since this object will almost
        # never be pickled by itself and only via an object that
        # contains it, therefore __init__ will be called when the
        # scene is constructed.  However, setstate is defined just for
        # completeness.
        state_pickler.set_state(self, state_pickler.loads_state(str_state))

    ###########################################################################
    # 'Scene' interface.
    ###########################################################################
    def render(self):
        """ Force the scene to be rendered. Nothing is done if the
        `disable_render` trait is set to True."""
        if not self.disable_render:
            self._vtk_control.Render()

    def add_actors(self, actors):
        """ Adds a single actor or a tuple or list of actors to the
        renderer."""
        # Reset the zoom if this is the first actor.
        reset_zoom = (len(self._renderer.actors) == 0)
        if hasattr(actors, '__iter__'):
            for actor in actors:
                self._renderer.add_actor(actor)
        else:
            self._renderer.add_actor(actors)
        self.actor_added = actors

        if reset_zoom:
            self.reset_zoom()
        else:
            self.render()

    def remove_actors(self, actors):
        """ Removes a single actor or a tuple or list of actors from
        the renderer."""
        if hasattr(actors, '__iter__'):
            for actor in actors:
                self._renderer.remove_actor(actor)
        else:
            self._renderer.remove_actor(actors)
        self.actor_removed = actors
        self.render()

    # Conevenience methods.
    add_actor = add_actors
    remove_actor = remove_actors

    def x_plus_view(self):
        """View scene down the +X axis. """
        self._update_view(self._def_pos, 0, 0, 0, 0, 1)

    def x_minus_view(self):
        """View scene down the -X axis. """
        self._update_view(-self._def_pos, 0, 0, 0, 0, 1)

    def z_plus_view(self):
        """View scene down the +Z axis. """
        self._update_view(0, 0, self._def_pos, 0, 1, 0)

    def z_minus_view(self):
        """View scene down the -Z axis. """
        self._update_view(0, 0, -self._def_pos, 0, 1, 0)

    def y_plus_view(self):
        """View scene down the +Y axis. """
        self._update_view(0, self._def_pos, 0, 1, 0, 0)

    def y_minus_view(self):
        """View scene down the -Y axis. """
        self._update_view(0, -self._def_pos, 0, 1, 0, 0)

    def isometric_view(self):
        """Set the view to an iso-metric view. """
        self._update_view(self._def_pos, self._def_pos, self._def_pos,
                          0, 0, 1)

    def reset_zoom(self):
        """Reset the camera so everything in the scene fits."""
        self._renderer.reset_camera()
        self.render()

    def save(self, file_name, size=None, **kw_args):
        """Saves rendered scene to one of several image formats
        depending on the specified extension of the filename.

        If an additional size (2-tuple) argument is passed the window
        is resized to the specified size in order to produce a
        suitably sized output image.  Please note that when the window
        is resized, the window may be obscured by other widgets and
        the camera zoom is not reset which is likely to produce an
        image that does not reflect what is seen on screen.

        Any extra keyword arguments are passed along to the respective
        image format's save method.
        """
        ext = os.path.splitext(file_name)[1]
        meth_map = {'.ps': 'ps', '.bmp': 'bmp', '.tiff': 'tiff',
                    '.png': 'png', '.jpg': 'jpg', '.jpeg': 'jpg',
                    '.iv': 'iv', '.wrl': 'vrml', '.vrml':'vrml',
                    '.oogl': 'oogl', '.rib': 'rib', '.obj': 'wavefront',
                    '.eps': 'gl2ps', '.pdf':'gl2ps', '.tex': 'gl2ps'}
        if ext.lower() not in meth_map.keys():
            raise ValueError, \
                  'Unable to find suitable image type for given file extension.'
        meth = getattr(self, 'save_' + meth_map[ext])
        if size is not None:
            p = self._vtk_control
            orig_size = p.GetSize()
            p.SetSize(size)
            meth(file_name, **kw_args)
            p.SetSize(orig_size)
        else:
            meth(file_name, **kw_args)

    def save_to_clipboard(self):
        """Saves a bitmap of the scene to the clipboard."""
        handler, name = tempfile.mkstemp()
        self.save_bmp(name)
        bmp = wx.Bitmap(name, wx.BITMAP_TYPE_BMP)
        bmpdo = wx.BitmapDataObject(bmp)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(bmpdo)
        wx.TheClipboard.Close()
        os.close(handler)
        os.unlink(name)

    def save_ps(self, file_name):
        """Saves the rendered scene to a rasterized PostScript image.
        For vector graphics use the save_gl2ps method."""
        if len(file_name) != 0:
            w2if = tvtk.WindowToImageFilter()
            w2if.magnification = self.magnification
            self._lift()
            w2if.input = self._renwin
            ex = tvtk.PostScriptWriter()
            ex.file_name = file_name
            ex.input = w2if.output
            self._exporter_write(ex)

    def save_bmp(self, file_name):
        """Save to a BMP image file."""
        if len(file_name) != 0:
            w2if = tvtk.WindowToImageFilter()
            w2if.magnification = self.magnification
            self._lift()
            w2if.input = self._renwin
            ex = tvtk.BMPWriter()
            ex.file_name = file_name
            ex.input = w2if.output
            self._exporter_write(ex)

    def save_tiff(self, file_name):
        """Save to a TIFF image file."""
        if len(file_name) != 0:
            w2if = tvtk.WindowToImageFilter()
            w2if.magnification = self.magnification
            self._lift()
            w2if.input = self._renwin
            ex = tvtk.TIFFWriter()
            ex.file_name = file_name
            ex.input = w2if.output
            self._exporter_write(ex)

    def save_png(self, file_name):
        """Save to a PNG image file."""
        if len(file_name) != 0:
            w2if = tvtk.WindowToImageFilter()
            w2if.magnification = self.magnification
            self._lift()
            w2if.input = self._renwin
            ex = tvtk.PNGWriter()
            ex.file_name = file_name
            ex.input = w2if.output
            self._exporter_write(ex)

    def save_jpg(self, file_name, quality=None, progressive=None):
        """Arguments: file_name if passed will be used, quality is the
        quality of the JPEG(10-100) are valid, the progressive
        arguments toggles progressive jpegs."""
        if len(file_name) != 0:
            if not quality and not progressive:
                quality, progressive = self.jpeg_quality, self.jpeg_progressive
            w2if = tvtk.WindowToImageFilter()
            w2if.magnification = self.magnification
            self._lift()
            w2if.input = self._renwin
            ex = tvtk.JPEGWriter()
            ex.quality = quality
            ex.progressive = progressive
            ex.file_name = file_name
            ex.input = w2if.output
            self._exporter_write(ex)

    def save_iv(self, file_name):
        """Save to an OpenInventor file."""
        if len(file_name) != 0:
            ex = tvtk.IVExporter()
            self._lift()
            ex.input = self._renwin
            ex.file_name = file_name
            self._exporter_write(ex)

    def save_vrml(self, file_name):
        """Save to a VRML file."""
        if len(file_name) != 0:
            ex = tvtk.VRMLExporter()
            self._lift()
            ex.input = self._renwin
            ex.file_name = file_name
            self._exporter_write(ex)

    def save_oogl(self, file_name):
        """Saves the scene to a Geomview OOGL file. Requires VTK 4 to
        work."""
        if len(file_name) != 0:
            ex = tvtk.OOGLExporter()
            self._lift()
            ex.input = self._renwin
            ex.file_name = file_name
            self._exporter_write(ex)

    def save_rib(self, file_name, bg=0, resolution=None, resfactor=1.0):
        """Save scene to a RenderMan RIB file.

        Keyword Arguments:

        file_name -- File name to save to.

        bg -- Optional background option.  If 0 then no background is
        saved.  If non-None then a background is saved.  If left alone
        (defaults to None) it will result in a pop-up window asking
        for yes/no.

        resolution -- Specify the resolution of the generated image in
        the form of a tuple (nx, ny).

        resfactor -- The resolution factor which scales the resolution.
        """
        if resolution == None:
            # get present window size
            Nx, Ny = self.render_window.size
        else:
            try:
                Nx, Ny = resolution
            except TypeError:
                raise TypeError, \
                      "Resolution (%s) should be a sequence with two elements"%resolution

        if len(file_name) == 0:
            return

        f_pref = os.path.splitext(file_name)[0]
        ex = tvtk.RIBExporter()
        ex.size = int(resfactor*Nx), int(resfactor*Ny)
        ex.file_prefix = f_pref
        ex.texture_prefix = f_pref + "_tex"
        self._lift()
        ex.render_window = self._renwin
        ex.background = bg

        if VTK_VER[:3] in ['4.2', '4.4']:
            # The vtkRIBExporter is broken in respect to VTK light
            # types.  Therefore we need to convert all lights into
            # scene lights before the save and later convert them
            # back.

            ########################################
            # Internal functions
            def x3to4(x):
                # convert 3-vector to 4-vector (w=1 -> point in space)
                return (x[0], x[1], x[2], 1.0 )
            def x4to3(x):
                # convert 4-vector to 3-vector
                return (x[0], x[1], x[2])

            def cameralight_transform(light, xform, light_type):
                # transform light by 4x4 matrix xform
                origin = x3to4(light.position)
                focus = x3to4(light.focal_point)
                neworigin = xform.multiply_point(origin)
                newfocus = xform.multiply_point(focus)
                light.position = x4to3(neworigin)
                light.focal_point = x4to3(newfocus)
                light.light_type = light_type
            ########################################

            save_lights_type=[]
            for light in self.light_manager.lights:
                save_lights_type.append(light.source.light_type)

            # Convert lights to scene lights.
            cam = self.camera
            xform = tvtk.Matrix4x4()
            xform.deep_copy(cam.camera_light_transform_matrix)
            for light in self.light_manager.lights:
                cameralight_transform(light.source, xform, "scene_light")

            # Write the RIB file.
            self._exporter_write(ex)

            # Now re-convert lights to camera lights.
            xform.invert()
            for i,light in enumerate(self.light_manager.lights):
                cameralight_transform(light.source, xform, save_lights_type[i])

            # Change the camera position. Otherwise VTK would render
            # one broken frame after the export.
            cam.roll(0.5)
            cam.roll(-0.5)
        else:
            self._exporter_write(ex)

    def save_wavefront(self, file_name):
        """Save scene to a Wavefront OBJ file.  Two files are
        generated.  One with a .obj extension and another with a .mtl
        extension which contains the material proerties.

        Keyword Arguments:

        file_name -- File name to save to
        """
        if len(file_name) != 0:
            ex = tvtk.OBJExporter()
            self._lift()
            ex.input = self._renwin
            f_pref = os.path.splitext(file_name)[0]
            ex.file_prefix = f_pref
            self._exporter_write(ex)

    def save_gl2ps(self, file_name, exp=None):
        """Save scene to a vector PostScript/EPS/PDF/TeX file using
        GL2PS.  If you choose to use a TeX file then note that only
        the text output is saved to the file.  You will need to save
        the graphics separately.

        Keyword Arguments:

        file_name -- File name to save to.

        exp -- Optionally configured vtkGL2PSExporter object.
        Defaults to None and this will use the default settings with
        the output file type chosen based on the extention of the file
        name.
        """

        # Make sure the exporter is available.
        if not hasattr(tvtk, 'GL2PSExporter'):
            msg = "Saving as a vector PS/EPS/PDF/TeX file using GL2PS is "\
                  "either not supported by your version of VTK or "\
                  "you have not configured VTK to work with GL2PS -- read "\
                  "the documentation for the vtkGL2PSExporter class."
            print msg
            return

        if len(file_name) != 0:
            f_prefix, f_ext = os.path.splitext(file_name)
            ex = None
            if exp:
                ex = exp
                if not isinstance(exp, tvtk.GL2PSExporter):
                    msg = "Need a vtkGL2PSExporter you passed a "\
                          "%s"%exp.__class__.__name__
                    raise TypeError, msg
                ex.file_prefix = f_prefix
            else:
                ex = tvtk.GL2PSExporter()
                # defaults
                ex.file_prefix = f_prefix
                if f_ext == ".ps":
                    ex.file_format = 'ps'
                elif f_ext == ".tex":
                    ex.file_format = 'tex'
                elif f_ext == ".pdf":
                    ex.file_format = 'pdf'
                else:
                    ex.file_format = 'eps'
                ex.sort = 'bsp'
                ex.compress = 1
                ex.edit_traits(kind='livemodal')

            self._lift()
            ex.render_window = self._renwin
            if ex.write3d_props_as_raster_image:
                self._exporter_write(ex)
            else:
                ex.write()

    ###########################################################################
    # Properties.
    ###########################################################################
    def _get_interactor(self):
        """Returns the vtkRenderWindowInteractor of the parent class"""
        return tvtk.to_tvtk(self._vtk_control._Iren)

    def _get_render_window(self):
        """Returns the scene's render window."""
        return self._renwin

    def _get_renderer(self):
        """Returns the scene's renderer."""
        return self._renderer

    def _get_camera(self):
        """ Returns the active camera. """
        return tvtk.to_tvtk(self._renderer.active_camera)

    ###########################################################################
    # `wxVTKRenderWindowInteractor` interface.
    ###########################################################################
    def OnKeyDown(self, event):
        """This method is overridden to prevent the 's'/'w'/'e'/'q'
        keys from doing the default thing which is generally useless.
        It also handles the 'p' and 'l' keys so the picker and light
        manager are called.
        """
        keycode = event.GetKeyCode()
        modifiers = event.HasModifiers()
        camera = self.camera
        if keycode < 256:
            key = chr(keycode)
            if key == '-':
                camera.zoom(0.8)
                self.render()
                return
            if key in ['=', '+']:
                camera.zoom(1.25)
                self.render()
                return
            if key.lower() in ['q', 'e']:
                self._disable_fullscreen()
            if key.lower() in ['s', 'w']:
                event.Skip()
                return
            # Handle picking.
            if key.lower() in ['p']:
                # In wxPython-2.6, there appears to be a bug in
                # EVT_CHAR so that event.GetX() and event.GetY() are
                # not correct.  Therefore the picker is called on
                # KeyUp.
                event.Skip()
                return
            # Light configuration.
            if key.lower() in ['l'] and not modifiers:
                self.light_manager.configure()
                return
            
        shift = event.ShiftDown()
        if keycode == wx.WXK_LEFT:
            if shift:
                camera.yaw(-5)
            else:
                camera.azimuth(5)
            self.render()
            return
        elif keycode == wx.WXK_RIGHT:
            if shift:
                camera.yaw(5)
            else:
                camera.azimuth(-5)
            self.render()
            return
        elif keycode == wx.WXK_UP:
            if shift:
                camera.pitch(-5)
            else:
                camera.elevation(-5)
            camera.orthogonalize_view_up()
            self.render()
            return
        elif keycode == wx.WXK_DOWN:
            if shift:
                camera.pitch(5)
            else:
                camera.elevation(5)
            camera.orthogonalize_view_up()
            self.render()
            return

        self._vtk_control.OnKeyDown(event)

        # Skipping the event is not ideal but necessary because we
        # have no way of knowing of the event was really handled or
        # not and not skipping will break any keyboard accelerators.
        # In practice this does not seem to pose serious problems.
        event.Skip()

    def OnKeyUp(self, event):
        """This method is overridden to prevent the 's'/'w'/'e'/'q'
        keys from doing the default thing which is generally useless.
        It also handles the 'p' and 'l' keys so the picker and light
        manager are called.
        """
        keycode = event.GetKeyCode()
        modifiers = event.HasModifiers()
        if keycode < 256:
            key = chr(keycode)
            if key.lower() in ['s', 'w', 'e', 'q']:
                event.Skip()
                return
            # Handle picking.
            if key.lower() in ['p']:
                if not modifiers:
                    x = event.GetX()
                    y = self._vtk_control.GetSize()[1] - event.GetY()
                    self.picker.pick(x, y)
                    return
                else:
                    # This is here to disable VTK's own pick handler
                    # which can get called when you press Alt/Ctrl +
                    # 'p'.
                    event.Skip()
                    return
            # Light configuration.
            if key.lower() in ['l']:
                event.Skip()
                return

        self._vtk_control.OnKeyUp(event)
        event.Skip()


    def OnPaint(self, event):
        """This method is overridden temporarily in order to create
        the light manager.  This is necessary because it makes sense
        to create the light manager only when the widget is realized.
        Only when the widget is realized is the VTK render window
        created and only then are the default lights all setup
        correctly.  This handler is removed on the first Paint event
        and the default paint handler of the
        wxVTKRenderWindowInteractor is used instead."""

        # Call the original handler (this will Show the widget)
        self._vtk_control.OnPaint(event)
        # Now create the light manager.
        self.light_manager = light_manager.LightManager(self)
        self._renwin.update_traits()

        # Reset the event handler to the default since our job is done.
        wx.EVT_PAINT(self._vtk_control, None) # Remove the default handler.
        wx.EVT_PAINT(self._vtk_control, self._vtk_control.OnPaint)

    def OnSize(self, event):
        """Overrides the default OnSize in order to refresh the traits
        of the render window."""
        self._vtk_control.OnSize(event)
        self._renwin.update_traits()

    ###########################################################################
    # Non-public interface.
    ###########################################################################
    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        # Create the VTK widget.
        self._vtk_control = window = wxVTKRenderWindowInteractor(parent, -1,
                                                                 stereo=self.stereo)

        # Override these handlers.
        wx.EVT_CHAR(window, None) # Remove the default handler.
        wx.EVT_CHAR(window, self.OnKeyDown)
        wx.EVT_KEY_UP(window, None) # Remove the default handler.
        wx.EVT_KEY_UP(window, self.OnKeyUp)
        wx.EVT_PAINT(window, None) # Remove the default handler.
        wx.EVT_PAINT(window, self.OnPaint)
        wx.EVT_SIZE(window, None) # Remove the default handler.
        wx.EVT_SIZE(window, self.OnSize)

        # Enable the widget.
        window.Enable(1)
        # Switch the default interaction style to the trackball one.
        window.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        # Grab the renderwindow.
        renwin = self._renwin = tvtk.to_tvtk(window.GetRenderWindow())
        renwin.set(point_smoothing=self.point_smoothing,
                   line_smoothing=self.line_smoothing,
                   polygon_smoothing=self.polygon_smoothing)
        # Create a renderer and add it to the renderwindow
        self._renderer = tvtk.Renderer()
        renwin.add_renderer(self._renderer)

        # Sync various traits.
        self.sync_trait('background', self._renderer)
        self.renderer.on_trait_change(self.render, 'background')
        self.sync_trait('parallel_projection', self.camera)
        self.sync_trait('off_screen_rendering', self._renwin)
        self.render_window.on_trait_change(self.render, 'off_screen_rendering')
        self.render_window.on_trait_change(self.render, 'stereo_render')
        self.render_window.on_trait_change(self.render, 'stereo_type')
        self.camera.on_trait_change(self.render, 'parallel_projection')

        def _show_parent_hack(window, parent):
            """A hack to get the VTK scene properly setup for use."""
            # Force the parent to show itself.
            parent.Show(1)
            # on some platforms, this SetSize() is necessary to cause
            # an OnPaint() when the event loop begins; else we get an
            # empty window until we force a redraw.
            window.SetSize(parent.GetSize())
            # This is necessary on slow machines in order to force the
            # wx events to be handled.
            wx.Yield()
            window.Render()

        if wx.Platform == '__WXMSW__':
            _show_parent_hack(window, parent)
        else:
            if (wx.VERSION[0] == 2) and (wx.VERSION[1] < 5):
                _show_parent_hack(window, parent)
            window.Update()

        # Because of the way the VTK widget is setup, and because we
        # set the size above, the window sizing is usually completely
        # messed up when the application window is shown.  To work
        # around this a dynamic IDLE event handler is added and
        # immediately removed once it executes.  This event handler
        # simply forces a resize to occur.  The _idle_count allows us
        # to execute the idle function a few times (this seems to work
        # better).
        def _do_idle(event, window=window):
            w = wx.GetTopLevelParent(window)
            # Force a resize
            sz = w.GetSize()
            w.SetSize((sz[0]-1, sz[1]-1))
            w.SetSize(sz)
            window._idle_count -= 1
            if window._idle_count < 1:
                wx.EVT_IDLE(window, None)
                del window._idle_count

        window._idle_count = 2
        wx.EVT_IDLE(window, _do_idle)

        return window

    def _lift(self):
        """Lift the window to the top. Useful when saving screen to an
        image."""
        if self.render_window.off_screen_rendering:
            # Do nothing if off screen rendering is being used.
            return

        w = self._vtk_control
        while w and not w.IsTopLevel():
            w = w.GetParent()
        if w:
            w.Raise()
            wx.Yield()
            self.render()

    def _exporter_write(self, ex):
        """Abstracts the exporter's write method."""
        # Bumps up the anti-aliasing frames when the image is saved so
        # that the saved picture looks nicer.
        rw = self.render_window
        aa_frames = rw.aa_frames
        rw.aa_frames = self.anti_aliasing_frames
        rw.render()
        ex.write()
        # Set the frames back to original setting.
        rw.aa_frames = aa_frames
        rw.render()

    def _update_view(self, x, y, z, vx, vy, vz):
        """Used internally to set the view."""
        camera = self.camera
        camera.focal_point = 0.0, 0.0, 0.0
        camera.position = x, y, z
        camera.view_up = vx, vy, vz
        self._renderer.reset_camera()
        self.render()

    def _disable_render_changed(self, val):
        if not val:
            self.render()

    def _full_screen_fired(self):
        fs = self._fullscreen
        if isinstance(fs, PopupScene):
            fs.close()
            self._fullscreen = None
        elif fs is None:
            ver = tvtk.Version()
            if (ver.vtk_major_version >= 5) and \
               (ver.vtk_minor_version >= 1):
                # There is a bug with earlier versions of VTK that
                # breaks reparenting a window which is why we test for
                # the version above.
                f = PopupScene(self)
                self._fullscreen = f
                f.fullscreen()
            else:
                f = FullScreen(self)
                f.run() # This will block.
                self._fullscreen = None

    def _disable_fullscreen(self):
        fs = self._fullscreen
        if isinstance(fs, PopupScene):
            fs.close()
            self._fullscreen = None
