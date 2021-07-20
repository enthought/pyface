Image Types
===========

Pyface's image model presumes that there are three different types of
image objects provided by a toolkit:

Images
    The "image" image type is optimized for pixel
    access and manipulation.  For the Qt toolkit this is the
    :class:`~pyface.qt.QtGui.QImage` class, while for the Wx toolkit it is
    :class:`wx.Image`.

Bitmap
    The "bitmap" image type is optimized for rendering
    to the screen.  For the Qt toolkit this is the
    :class:`~pyface.qt.QtGui.QPixmap` class, while for the Wx toolkit it is
    :class:`wx.Bitmap`.

Icon
    The "icon" image type is really a collection of related images that
    represent different states of a GUI, such as disabled, selected,
    activated and so on.  For the Qt toolkit this is the
    :class:`~pyface.qt.QtGui.QIcon` class, while for the Wx toolkit it is
    :class:`wx.Icon`.

Additionally, there may be other sources of images, such as images stored in
numpy arrays of appropriate shape and dtype, PIL/Pillow images, and images
stored in files, both user-supplied and stored as resources with a Python
library.

:class:`~pyface.i_image.IImage` Interface
-----------------------------------------

To handle all of these different notions of an "image", Pyface has a base
interface :class:`~pyface.i_image.IImage` that exposes methods for creating
each toolkit image type from underlying image data.  There are corresponding
concrete implementations of the interface for Numpy arrays and image resources.

Additionally, there is an :class:`~pyface.ui_traits.Image` trait that is
designed to accept any :class:`~pyface.i_image.IImage` as a value, but to
also accept the name of a resource or file to load into an image.

:class:`~pyface.array_image.ArrayImage`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This implementation of :class:`~pyface.i_image.IImage` wraps an NxMx3 or
NxMx4 numpy array of unsigned bytes which it treats as RGB or RGBA image
data.  When converting to toolkit objects, the data is copied.

:class:`~pyface.image_resource.ImageResource`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An image resource is an image stored as part of a Python package, either as
a file or inside a zip file or similar, and so guaranteed to be available
for use in an application for GUI components.  Pyface provides the
:class:`~pyface.image_resource.ImageResource` class and associated resource
discovery machinery to support this use-case.

Resources are specified to the :class:`~pyface.image_resource.ImageResource`
by filename (adding standard image file extensions if not present in the name).
The Pyface resource system searches for files matching the given name in these
places:

- in "images" directories inside the current Python package
- in "images.zip" files inside the current Python package
- in directories given as explicit search paths

If an image of a particular size is requested, the system will also look for
directories with names of the form ``images/{width}x{height}`` and will use
any matching image from these preferentially.

The most common way to specify images for use in button icons or complex
TraitsUI table and tree data structures is by adding an "images" directory
next to the module using the image, for example::

    my_package/
        my_module.py
        images/
            my_image.png

The image code like the following in my_module.py will work:

.. code-block:: python

    from pyface.api import ImageResource
    from pyface.actions.api import Action

    img_res = ImageResource("my_image")
    action = Action(image="my_image")

When using this approach, remember that image files will need to be added
to the ``package_data`` in ``setup.py`` or they will not be shipped alongside
the code.

:mod:`~pyface.util.image_helpers` Module
----------------------------------------

Since there is a lot of shared functionality between the various
implementations of the :class:`~pyface.i_image.IImage` interface, the
:mod:`pyface.util.image_helpers` module provides a number of functions and
other objects to perform lower-level tasks, such as converting between toolkit
types.

Implementers of new toolkits will likely want to write their own versions of
these, and writers of new concrete :class:`~pyface.i_image.IImage`
implementations may want to make use of them to simplify the implementation of
the interface.

:class:`~pyface.image.image.ImageLibrary`
-----------------------------------------

The :class:`~pyface.image_resource.ImageResource` system is built around
supplying image files which are local to the place where they are being used.
Sometimes, however, you want your images to be available throughout the
application.  Pyface provides the :class:`~pyface.image.image.ImageLibrary`
to allow for this use case.

The :class:`~pyface.image.image.ImageLibrary` is a global object that
holds a catalog of :class:`~pyface.image.image.ImageVolume` objects that in
turn contain images and associated metadata.  Image volumes are either
directories or zipfiles containing images and metadata files.

Accessing Images and Image Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you give an :class:`~pyface.ui_traits.Image` an image name which
starts with ``@``, then it will interpret the name to be the id of an
image in the :class:`~pyface.image.image.ImageLibrary` of the form
``@<volume-name>:<image-name>``.  Alternatively, you can ask the image
library directly for an image resource that corresponds to the id via the
:meth:`~pyface.image.image.ImageLibrary.image_resource` method:

.. code-block:: python

    from pyface.image.image import ImageLibrary
    from pyface.actions.api import Action

    red_ball_image = ImageLibrary.image_resource("@icons:red_ball")
    action = Action(image=red_ball_image)

Each image has an :class:`~pyface.image.image.ImageInfo` metadata object
associated with it which can be obtained via the
:meth:`~pyface.image.image.ImageLibrary.image_info` method.  A list of all
known image metadata can be obtained from the
:attr:`~pyface.image.image.ImageLibrary.images` trait.

:class:`~pyface.image.image.ImageVolume` Instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image volumes are represented by the :class:`~pyface.image.image.ImageVolume`
class.  Image volumes may have multiple aliases in addition to their primary
name, and these aliases can be used as part of the id of an image.  The
volume which stores an image can be found using the
:meth:`~pyface.image.image.ImageLibrary.find_volume` method.  The
:attr:`~pyface.image.image.ImageLibrary.catalog` and
:attr:`~pyface.image.image.ImageLibrary.aliases` attributes are dictionaries
that map names to volume objects.

By default the :class:`~pyface.image.image.ImageLibrary` is initialized
with:

- an ``"application"`` volume which is assumed to be in a "library" directory
  next to the application executable (ie. whatever is in ``sys.argv[0]``
  which is usually the main module's path);
- the ``std`` and ``icons`` volumes in ``pyface/image/library``
- any path listed in the ``TRAITS_IMAGES`` environment variable which contains
  a volume.

Additional volumes can be added programatically by calling
:meth:`~pyface.image.image.ImageLibrary.add_volume` with the path of a zipfile
or directory.  Alternatively :meth:`~pyface.image.image.ImageLibrary.add_path`
can be used to add volume by giving a name for the volume and a directory path
to use.  If no path is provided in either case, the library will look for an
``images`` directory next to the current module.

Just as with image libraries, the
:meth:`~pyface.image.image.ImageVolume.image_resource` method returns an
:class:`~pyface.image_resource.ImageResource` instance for the specified image
name.  Additionally, the bytes of the actual image file are available through
:meth:`~pyface.image.image.ImageVolume.image_data`.

Image volumes have a :attr:`~pyface.image.image.ImageVolume.info` trait that
holds a list of :class:`~pyface.image.image.ImageVolumeInfo` instances.  These
hold metadata about groups of images, including copyright and licensing
information.  The :attr:`~pyface.image.image.ImageVolume.category` and
:attr:`~pyface.image.image.ImageVolume.keywords` traits hold additional
information about the volume itself.

Image volumes are designed to reflect the actual contents of the directories
or zipfile that they refer to.  The
:meth:`~pyface.image.image.ImageVolume.update` method clears and reloads the
data from disk.  The :meth:`~pyface.image.image.ImageVolume.save` method saves
any changes made by the user into the data file.

Images stored in image volumes which are zipfiles are extracted to temporary
files as needed for actual use.
