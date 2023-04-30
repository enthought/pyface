# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from collections.abc import Sequence
from typing import Any, Callable, Dict, Optional, Union

from traits.api import ABCHasStrictTraits, Enum, Range
from traits.trait_type import _TraitType

from pyface.util.font_parser import simple_parser
from .color import Color
from .font import Font
from .i_image import IImage


class Image(_TraitType[Union[IImage, str], Optional[IImage]]):

    def __init__(self, value: Union[IImage, str, None] = None, **metadata) -> None:
        ...


class PyfaceColor(_TraitType[Union[Color, str, Sequence], Color]):

    def __init__(
        self,
        value: Union[Color, str, Sequence, None] = None,
        **metadata,
    ) -> None:
        ...


class PyfaceFont(_TraitType[Union[Font, str], Font]):

    def __init__(
        self,
        value: Union[Font, str, None] = None,
        parser: Callable[[str], Dict[str, Any]] = simple_parser,
        **metadata,
    ) -> None:
        ...


class BaseMB(ABCHasStrictTraits):
    ...


class Margin(BaseMB):

    # The amount of padding/margin at the top:
    top = Range(-32, 32, 0)

    # The amount of padding/margin at the bottom:
    bottom = Range(-32, 32, 0)

    # The amount of padding/margin on the left:
    left = Range(-32, 32, 0)

    # The amount of padding/margin on the right:
    right = Range(-32, 32, 0)


class HasMargin(_TraitType[Union[int, tuple, Margin], Margin]):
    ...


class Border(BaseMB):

    # The amount of border at the top:
    top = Range(0, 32, 0)

    # The amount of border at the bottom:
    bottom = Range(0, 32, 0)

    # The amount of border on the left:
    left = Range(0, 32, 0)

    # The amount of border on the right:
    right = Range(0, 32, 0)


class HasBorder(_TraitType[Union[int, tuple, Border], Border]):
    ...

Position = Enum("left", "right", "above", "below")

Alignment = Enum("default", "left", "center", "right")

Orientation = Enum("vertical", "horizontal")

