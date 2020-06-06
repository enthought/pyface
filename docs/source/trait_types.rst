===========
Trait Types
===========

Pyface defines a number of custom Trait types that represent quantities and
objects that are useful in the context of graphical user interfaces.

Fonts
=====

When working with fonts, there is the frequent difficulty that the desired
font may or may not be present in the environment where the application is
being run.  Additionally, the way that fonts are specified in different
toolkits are, clearly, different, although there is a lot of commonality.
Finally, while it is clearly preferable to specify fonts via a concrete
and well-defined API, it is common for developers to specify fonts via
strings like '12pt "Comic Sans"' or "bold italic 24 Arial, Helvetica, Sans".

Pyface defines a |Font| class that defines a toolkit-independent abstraction
of a font specification.  This is not a particular, concrete font that can
be used to render text, but instead a specification for what font the
developer or user would like to use, but allowing for the backend toolkit to
be able to fall-back to other options, or substitute similar font faces
where it cannot exactly match the requirements.  The attributes of the
font specification correspond closely to those that are described by CSS
fonts.  In particular, a |Font| instance has the following traits:

``family``
    A list of font family names in order of preference, such as "Helvetica"
    or "Comic Sans".  There are several generic font family names that can
    be used as fall-backs in case all preferred fonts are unavailable.  In
    the case of a font that has been selected by the toolkit this list will
    have one value which is the actual font family name.

``weight``
    How thick or dark the font glyphs are.  This value is specified by a
    string, either of the form "100", "200", ..., "1000" or a number of
    synonyms such as 'light' and 'bold' available for those values.
    This is a mapped trait where ``weight_`` holds the corresponding
    numerical value.

``stretch``
    The amount of horizontal compression or expansion to apply to the glyphs.
    These given by names such as 'condensed' and 'expanded', each of which is
    mapped to a number between 100 and 900, available in the ``stretch_``
    mapped value.

``style``
    This selects either 'oblique' or 'italic' variants typefaces of the given
    font family.  If neither is wanted, the value is 'normal'.

``size``
    The overall size of the glyphs. This can be expressed either as the
    numeric size in points, or as a string such as "small" or "large".

``variants``
    A set of additional font style specifiers, such as "small-caps",
    "strikethrough", "underline" or "overline", where supported by the
    underlying toolkit.

A |Font| object can be created in the usual way, by passing trait values as
keyword arguments, but there are classmethods :py:meth:`~!Font.from_toolkit`
and :py:meth:`~!Font.from_description` that create a |Font| from a toolkit
font specification object or a string description, respectively.

The string specification follows CSS conventions: fonts are specfied by a
string which specifies the weight, stretch, style and variants by text
synonyms (in any order), followed by size in points and font family
preferences (quoted if not a single word) and separated by commas.
Where the value is "normal" it can be omitted from the description.

For example::

    'italic bold 14pt Helvetica, Arial, sans-serif'
    '36pt "Comic Sans"'

are valid font descriptions, but "Helvetica bold 12pt" is not because the
order of elements is wrong.

The |Font| object also has a method :py:meth:`~!Font.to_toolkit` that
produces a toolkit font specification, which is usually what controls and
other toolkit-specific code excpect to be given.

While classes could simply use ``Instance(Font)`` whenever they want a
font specification, Pyface also provides a |PyfaceFont| trait type that
accepts either a |Font|, or a font description string.  The value held
is always a |Font| object.  This allows users to write code like::

    class Style(HasStrictTraits):
        font = PyfaceFont()

    style = Style(font='bold 10pt "Comic Sans"')
    style.font = "italic 12pt Arial, Helvetic, sans-serif"


.. |Font| replace:: :py:class:`~pyface.font.Font`
