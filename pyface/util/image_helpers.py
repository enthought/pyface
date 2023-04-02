# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Helper functions for working with images

This module provides helper functions for converting between numpy arrays
and toolkit images, as well as between the various image types in a standardized
way.

Helper functions
----------------

- :data:`~.array_to_image`
- :data:`~.bitmap_to_icon`
- :data:`~.bitmap_to_image`
- :data:`~.image_to_array`
- :data:`~.image_to_bitmap`
- :data:`~.resize_image`
- :data:`~.resize_bitmap`

Options for resizing images
---------------------------
- :data:`~.ScaleMode`
- :data:`~.AspectRatio`

"""

from pyface.toolkit import toolkit_object

# Enum types for function arguments
ScaleMode = toolkit_object("util.image_helpers:ScaleMode")
AspectRatio = toolkit_object("util.image_helpers:AspectRatio")

# Helper functions
array_to_image = toolkit_object("util.image_helpers:array_to_image")
bitmap_to_icon = toolkit_object("util.image_helpers:bitmap_to_icon")
bitmap_to_image = toolkit_object("util.image_helpers:bitmap_to_image")
image_to_array = toolkit_object("util.image_helpers:image_to_array")
image_to_bitmap = toolkit_object("util.image_helpers:image_to_bitmap")
resize_image = toolkit_object("util.image_helpers:resize_image")
resize_bitmap = toolkit_object("util.image_helpers:resize_bitmap")
