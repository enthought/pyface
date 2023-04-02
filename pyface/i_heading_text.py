# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Heading text. """

import warnings

from traits.api import HasTraits, Int, Interface, Str


class IHeadingText(Interface):
    """ A widget which shows heading text in a panel. """

    # 'IHeadingText' interface ---------------------------------------------

    #: Heading level.  This is currently unused.
    level = Int(1)

    #: The heading text.
    text = Str("Default")


class MHeadingText(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IHeadingText interface.
    """

    # 'IHeadingText' interface ---------------------------------------------

    #: Heading level.  This is currently unused.
    level = Int(1)

    #: The heading text.
    text = Str("Default")

    def __init__(self, parent=None, **traits):
        """ Creates the heading text. """

        if "image" in traits:
            warnings.warn(
                "background images are no-longer supported for Wx and the "
                "'image' trait will be removed in a future Pyface update",
                DeprecationWarning,
                stacklevel=2,
            )

        create = traits.pop("create", None)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )
        elif create is not None:
            warnings.warn(
                "setting create=False is no longer required",
                DeprecationWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        """ Perform any toolkit-specific initialization for the control. """
        super()._initialize_control()
        self._set_control_text(self.text)

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.observe(self._text_updated, 'text', dispatch="ui")

    def _remove_event_listeners(self):
        self.observe(self._text_updated, 'text', dispatch="ui", remove=True)
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _set_control_text(self, text):
        """ Set the text on the control.

        Parameters
        ----------
        text : str
            The text to display.  This can contain basic HTML-like markeup.
        """
        raise NotImplementedError()

    def _get_control_text(self):
        """ Get the text on the control.

        Returns
        ----------
        text : str
            The text to displayed in the widget.
        """
        raise NotImplementedError()

    # Trait change handlers --------------------------------------------------

    def _text_updated(self, event):
        if self.control is not None:
            self._set_control_text(self.text)
