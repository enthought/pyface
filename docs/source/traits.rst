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
    Color.from_str("#662244cc")

All `standard web colors <https://en.wikipedia.org/wiki/Web_colors#Extended_colors>`_
are understood, as well as hexadecimal RGB(A) with 1, 2 or 4 hex digits per
channel.

|Color| instances are mutable, as their intended use is as values stored
in |PyfaceColor| trait classes which can be modified and listened to.  This
means that they are comparatively heavyweight objects and should be shared
where possible and aren't particularly suited for situations where large
numbers of distinct and independent colors are needed: NumPy arrays are likely
better suited for this sort of application.

The
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

Fonts
=====

Just as with colors, it is common to want to be able to specify the font to use
for text in the UI.  Each toolkit usually has its own way of representing
fonts, and so the ability to specify a font in a toolkit-independent way that
can be converted to a toolkit-specific representation is important.  This is
particularly so when you want to allow the user to specify a font.

Pyface provides a |Font| class and a corresponding |PyfaceFont| trait-type
that allows this sort of representation.  Internally, the |Font| class
stores font attributes such as |Font.weight| or |Font.size| as traits::

    font = Font(family=["Comic Sans"], size=24, weight="bold")
    font.weight

Some of these attributes are mapped traits, or otherwise convert string
values to numeric values.  For example |Font.size| will accept strings like
"12pt", while |Font.weight| holds a numeric weight value in a mapped
attribute::

..  code-block:: pycon

    >>> font.weight
    "bold"
    >>> font.weight_
    700

|Font| instances are mutable, as their intended use is as values stored
in |PyfaceFont| trait classes which can be modified and listened to.

As a convenience, the |PyfaceFont| validator understands string descriptions
of fonts, and will accept them as values when initializing or modifying the
trait::

    class Style(HasStrictTraits):

        font = PyfaceFont("24 pt Bold Comic Sans")

        @observe('font.*')
        def font_changed(self, event):
            print('The font has changed to {}'.format(self.font))

    style = Style(font='12 italc Helvetica')
    style.font.weight = 'light'
    style.font = Font(
        family=["Helvetica", "Arial", "sans-serif"],
        variants={"small-caps"},
    )

The parsing of strings to fonts is currently handled by a |simple_parser| that
is modelled on the ``Font`` trait from TraitsUI, but it can be substituted
for a more sophisticated one, if needed.

For interactions with the toolkit, the |Font.from_toolkit| and
|Font.to_toolkit| methods allow conversion to and from the appropriate
toolkit font objects, such as Qt's :py:class:`QFont` or
:py:class:`wx.Font`.  These are most likely to be needed by internal
Pyface functionality, and should not be needed by developers who are
building applications on top of Pyface.

It is intended that this trait will eventually replace the ``Font``
trait from TraitsUI.  It is also likely that the simple parser will be replaced
with a parser that understands CSS-like font strings.

Layout Traits
=============

Pyface also provides a number of classes and traits to assist with
layout-related functionality.  These include the convenience Enums |Alignment|,
|Orientation| and |Position| as well as the classes |Margin| and |Border| and
their corresponding traits |HasMargin| and |HasBorder|.


.. |Alignment| replace:: :py:attr:`~pyface.ui_traits.Alignment`
.. |Border| replace:: :py:class:`~pyface.ui_traits.Border`
.. |Color| replace:: :py:class:`~pyface.color.Color`
.. |Color.from_str| replace:: :py:meth:`~pyface.color.Color.from_str`
.. |Color.from_toolkit| replace:: :py:meth:`~pyface.color.Color.from_toolkit`
.. |Color.to_toolkit| replace:: :py:meth:`~pyface.color.Color.to_toolkit`
.. |Font| replace:: :py:class:`~pyface.font.Font`
.. |Font.size| replace:: :py:attr:`~pyface.font.Font.size`
.. |Font.from_toolkit| replace:: :py:meth:`~pyface.font.Font.from_toolkit`
.. |Font.to_toolkit| replace:: :py:meth:`~pyface.font.Font.to_toolkit`
.. |Font.weight| replace:: :py:attr:`~pyface.font.Font.weight`
.. |HasMargin| replace:: :py:class:`~pyface.ui_traits.HasMargin`
.. |HasBorder| replace:: :py:class:`~pyface.ui_traits.HasBorder`
.. |Margin| replace:: :py:class:`~pyface.ui_traits.Margin`
.. |Orientation| replace:: :py:attr:`~pyface.ui_traits.Orientation`
.. |Position| replace:: :py:attr:`~pyface.ui_traits.Position`
.. |PyfaceColor| replace:: :py:class:`~pyface.ui_traits.PyfaceColor`
.. |PyfaceFont| replace:: :py:class:`~pyface.ui_traits.PyfaceFont`
.. |simple_parser| replace:: :py:func:`~pyface.util.font_parser.simple_parser`
