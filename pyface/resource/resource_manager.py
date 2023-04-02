# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The default resource manager.

A resource manager locates and loads application resources such as images and
sounds etc.
"""

import collections.abc
import glob
import inspect
import os
from os.path import join
import types
from zipfile import is_zipfile, ZipFile

# importlib.resources is new in Python 3.7, and importlib.resources.files is
# new in Python 3.9, so for Python < 3.9 we must rely on the 3rd party
# importlib_resources package.
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from traits.api import HasTraits, Instance, List
from traits.util.resource import get_path

from pyface.resource.resource_factory import ResourceFactory
from pyface.resource.resource_reference import ImageReference


class ResourceManager(HasTraits):
    """ The default resource manager.

    A resource manager locates and loads application resources such as images
    and sounds etc.
    """

    # Allowed extensions for image resources.
    IMAGE_EXTENSIONS = [".png", ".jpg", ".bmp", ".gif", ".ico"]

    # A list of additional search paths. These paths are fallbacks, and hence
    # have lower priority than the paths provided by resource objects.
    extra_paths = List()

    # The resource factory is responsible for actually creating resources.
    # This is used so that (for example) different GUI toolkits can create
    # a images in the format that they require.
    resource_factory = Instance(ResourceFactory)

    # ------------------------------------------------------------------------
    # 'ResourceManager' interface.
    # ------------------------------------------------------------------------

    def locate_image(self, image_name, path, size=None):
        """ Locates an image.

        Parameters
        ----------
        image_name : str
            Name of the image file.
        path : list of (str or ModuleType)
            Paths from which image files will be searched. Note that for each
            path, a subdirectory named 'images' will be search first.
            The first match will be returned.
        size : tuple of (m: int, n: int), optional
            Specific size of the image requested. If provided, then
            the subdirectory ``images/{m}x{n}`` will be searched first,
            followed by the ``images`` subdirectory and its containing folder.
            Default is None.

        Returns
        -------
        image_ref : ImageReference or None
            ImageReference to the image found, or None if no matching images
            are found.
        """

        if not isinstance(path, collections.abc.Sequence):
            path = [path]

        resource_path = []
        for item in list(path) + self.extra_paths:
            if isinstance(item, str):
                resource_path.append(item)
            elif isinstance(item, types.ModuleType):
                resource_path.append(item)
            else:
                resource_path.extend(self._get_resource_path(item))

        return self._locate_image(image_name, resource_path, size)

    def load_image(self, image_name, path, size=None):
        """ Loads an image. """

        reference = self.locate_image(image_name, path, size)
        if reference is not None:
            image = reference.load()

        else:
            image = None

        return image

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _locate_image(self, image_name, resource_path, size):
        """ Attempts to locate an image resource.

        If the image is found, an image resource reference is returned.
        If the image is NOT found None is returned.

        """

        # If the image name contains a file extension (eg. '.jpg') then we will
        # only accept an an EXACT filename match.
        basename, extension = os.path.splitext(image_name)
        if len(extension) > 0:
            extensions = [extension]
            pattern = image_name

        # Otherwise, we will search for common image suffixes.
        else:
            extensions = self.IMAGE_EXTENSIONS
            pattern = image_name + ".*"

        # Try the 'images' sub-directory first (since that is commonly
        # where we put them!).  If the image is not found there then look
        # in the directory itself.
        if size is None:
            subdirs = ["images", ""]
        else:
            subdirs = ["images/%dx%d" % (size[0], size[1]), "images", ""]

        # Concrete image filenames to be searched
        image_filenames = [basename + extension for extension in extensions]

        for dirname in resource_path:

            # If we come across a reference to a module, try and find the
            # image inside of an .egg, .zip, etc.
            if isinstance(dirname, types.ModuleType):
                try:
                    data = _find_resource_data(
                        dirname, subdirs, image_filenames
                    )
                except OSError:
                    continue
                else:
                    return ImageReference(
                        self.resource_factory, data=data
                    )

            # Is there anything resembling the image name in the directory?
            for path in subdirs:
                filenames = glob.glob(join(dirname, path, pattern))
                for filename in filenames:
                    not_used, extension = os.path.splitext(filename)
                    if extension in extensions:
                        reference = ImageReference(
                            self.resource_factory, filename=filename
                        )

                        return reference

            # Is there an 'images' zip file in the directory?
            zip_filename = join(dirname, "images.zip")
            if os.path.isfile(zip_filename):
                zip_file = ZipFile(zip_filename, "r")
                # Try the image name itself, and then the image name with
                # common images suffixes.
                for extension in extensions:
                    try:
                        image_data = zip_file.read(basename + extension)
                        reference = ImageReference(
                            self.resource_factory, data=image_data
                        )

                        return reference

                    except:
                        pass

            # is this a path within a zip file?
            # first, find the zip file in the path
            filepath = dirname
            zippath = ""
            while (
                not is_zipfile(filepath)
                and os.path.splitdrive(filepath)[1].startswith("\\")
                and os.path.splitdrive(filepath)[1].startswith("/")
            ):
                filepath, tail = os.path.split(filepath)
                if zippath != "":
                    zippath = tail + "/" + zippath
                else:
                    zippath = tail

            # if we found a zipfile, then look inside it for the image!
            if is_zipfile(filepath):

                zip_file = ZipFile(filepath)
                for subpath in ["images", ""]:
                    for extension in extensions:
                        try:
                            # this is a little messy. since zip files don't
                            # recognize a leading slash, we have to be very
                            # particular about how we build this path when
                            # there are empty strings
                            if zippath != "":
                                path = zippath + "/"
                            else:
                                path = ""

                            if subpath != "":
                                path = path + subpath + "/"

                            path = path + basename + extension
                            # now that we have the path we can attempt to load
                            # the image
                            image_data = zip_file.read(path)
                            reference = ImageReference(
                                self.resource_factory, data=image_data
                            )

                            # if there was no exception then return the result
                            return reference

                        except:
                            pass

        return None

    def _get_resource_path(self, object):
        """ Returns the resource path for an object. """

        if hasattr(object, "resource_path"):
            resource_path = object.resource_path

        else:
            resource_path = self._get_default_resource_path(object)

        return resource_path

    def _get_default_resource_path(self, object):
        """ Returns the default resource path for an object. """

        resource_path = []
        for klass in inspect.getmro(object.__class__):
            try:
                resource_path.append(get_path(klass))

            # We get an attribute error when we get to a C extension type (in
            # our case it will most likley be 'CHasTraits'.  We simply ignore
            # everything after this point!
            except AttributeError:
                break

        return resource_path


def _get_package_data(module, rel_path):
    """ Return package data in bytes for the given module and resource path.

    Parameters
    ----------
    module : ModuleType
        A module from which package data will be discovered.
        If the module name does not conform to the package requirement, then
        its "__file__" attribute is used for locating the directory to search
        for resource files.
    rel_path : str
        "/"-separated path for loading data file.

    Returns
    -------
    data : bytes
        Loaded data in bytes.

    Raises
    ------
    OSError
        If the path referenced does not resolve to an existing file or the
        file cannot be read.
    """

    if (module.__spec__ is None
            or module.__spec__.submodule_search_locations is None):
        module_dir_path = os.path.dirname(module.__file__)
        path = os.path.join(module_dir_path, *rel_path.split("/"))
        with open(path, "rb") as fp:
            return fp.read()

    return (
        files(module).joinpath(rel_path).read_bytes()
    )


def _find_resource_data(module, subdirs, filenames):
    """ For the given module, search directories and names, find a matching
    resource file and return its content as bytes.

    Parameters
    ----------
    module : ModuleType
        A module from which package data will be discovered.
        If the module name does not conform to the package requirement, then
        its "__file__" attribute is used for locating the directory to search
        for resource files.
    subdirs : list of str
        Name of subdirectories to try. Each value can be a "/"-separated
        string to represent more nested subdirectories.
    filenames : list of str
        File names to try.

    Returns
    -------
    data : bytes
        Loaded data in bytes.

    Raises
    ------
    OSError
        If the path referenced does not resolve to an existing file or the
        file cannot be read.
    """
    for path in subdirs:
        for filename in filenames:
            searchpath = "%s/%s" % (path, filename)
            try:
                return _get_package_data(module, searchpath)
            except OSError:
                pass
    raise OSError(
        "Unable to load data for the given module and search paths."
    )
