.. _ui-trait-types:

===========
Trait Types
===========

Pyface defines a number of custom Trait types that represent quantities and
objects that are useful in the context of graphical user interfaces.

Colors
======

When working with user interfaces, it is common to want to be able to specify
the color to use in part of the UI.  Each toolkit usually has its own way of
representing colors, and so the ability to specify a color in a
toolkit-independent way that can be converted to a toolkit-specific
representation is important.  This is particularly so when you want to allow
the user to specify a color.

Pyface provides a |Color| class and a corresponding |PyfaceColor| trait-type
that allows this sort of representation.  Internally, the |Color| class
stores colors as a tuple of red, green, blue and alpha values which range
from 0.0 through to 1.0, inclusive.  Helper properties allow the user to
specify individual channel values, as well as specify colors in alternate
color spaces, such as HSV or HLS::

    Color(rgba=(0.4, 0.2, 0.6, 0.8))
    Color(red=0.4, green=0.2, blue=0.6, alpha=0.8)
    Color(hls=(0.2, 0.5, 0.8))

|Color| instances can also be created via the |Color.from_str| method
which allow specification of colors via CSS-style color strings, such as::

    Color.from_str("aquamarine")
    Color.from_str("#662244")

All standard web colors are understood, as well as hexadecimal RGB(A) with
1, 2 or 4 hex digits per channel.

|Color| instances are mutable, as their intended use is as values stored
in |PyfaceColor| trait classes which can be modified and listened to.  The
|PyfaceColor| validator understands string descriptions of colors, and will
accept them as values when initializing or modifying the trait::

    class Style(HasStrictTraits):

        color = PyfaceColor("#442266FF")

        @observe('color.rgba')
        def color_changed(self, event):
            print('The color has changed to {}'.format(self.color))

    shape = Style(color='orange')
    shape.color.blue = 0.8
    shape.color = "rebeccapurple"

For interactions with the toolkit, the |Color.from_toolkit| and
|Color.to_toolkit| methods allow conversion to and from the appropriate
toolkit color objects, such as Qt's :py:class:`QColor` or
:py:class:`wx.Colour`.  These are most likely to be needed by internal
Pyface functionality, and should not be needed by developers who are
building applications on top of Pyface.

It is intended that this trait will eventually replace the ``Color``
trait from TraitsUI.

.. |Color| replace:: :py:class:`~pyface.color.Color`
.. |Color.from_str| replace:: :py:meth:`~pyface.color.Color.from_str`
.. |Color.from_toolkit| replace:: :py:meth:`~pyface.color.Color.from_toolkit`
.. |Color.to_toolkit| replace:: :py:meth:`~pyface.color.Color.to_toolkit`
.. |PyfaceColor| replace:: :py:class:`~pyface.ui_traits.PyfaceColor`
