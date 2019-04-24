#------------------------------------------------------------------------------
# Copyright (c) 2017-19, Enthought, Inc.
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
""" The text field interface. """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.api import Bool, Enum, HasTraits, Unicode

from pyface.fields.i_field import IField


class ITextField(IField):
    """ The text field interface. """

    #: The value held by the field.
    value = Unicode

    #: Should the text trait be updated on user edits, or when done editing.
    update_text = Enum('auto', 'editing_finished')

    #: Placeholder text for an empty field.
    placeholder = Unicode

    #: Display typed text, or one of several hidden "password" modes.
    echo = Enum('normal', 'password')

    #: Whether or not the field is read-only.
    read_only = Bool


class MTextField(HasTraits):
    """ The text field mix-in. """

    #: The value held by the field.
    value = Unicode

    #: Should the value be updated on every keystroke, or when done editing.
    update_text = Enum('auto', 'editing_finished')

    #: Placeholder text for an empty field.
    placeholder = Unicode

    #: Display typed text, or one of several hidden "password" modes.
    echo = Enum('normal', 'password')

    #: Whether or not the field is read-only.
    read_only = Bool

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        self._set_control_echo(self.echo)
        self._set_control_value(self.value)
        self._set_control_placeholder(self.placeholder)
        self._set_control_read_only(self.read_only)

        super(MTextField, self)._initialize_control()

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(MTextField, self)._add_event_listeners()
        self.on_trait_change(self._update_text_updated, 'update_text',
                             dispatch='ui')
        self.on_trait_change(self._placeholder_updated, 'placeholder',
                             dispatch='ui')
        self.on_trait_change(self._echo_updated, 'echo', dispatch='ui')
        self.on_trait_change(self._read_only_updated, 'read_only',
                             dispatch='ui')
        if self.control is not None:
            if self.update_text == 'editing_finished':
                self._observe_control_editing_finished()
            else:
                self._observe_control_value()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            if self.update_text == 'editing_finished':
                self._observe_control_editing_finished(remove=True)
            else:
                self._observe_control_value(remove=True)
        self.on_trait_change(self._update_text_updated, 'update_text',
                             dispatch='ui', remove=True)
        self.on_trait_change(self._placeholder_updated, 'placeholder',
                             dispatch='ui', remove=True)
        self.on_trait_change(self._echo_updated, 'echo', dispatch='ui',
                             remove=True)
        self.on_trait_change(self._read_only_updated, 'read_only',
                             dispatch='ui', remove=True)
        super(MTextField, self)._remove_event_listeners()

    def _editing_finished(self):
        if self.control is not None:
            value = self._get_control_value()
            self._update_value(value)

    # Toolkit control interface ---------------------------------------------

    def _get_control_placeholder(self):
        """ Toolkit specific method to set the control's placeholder. """
        raise NotImplementedError

    def _set_control_placeholder(self, placeholder):
        """ Toolkit specific method to set the control's placeholder. """
        raise NotImplementedError

    def _get_control_echo(self):
        """ Toolkit specific method to get the control's echo. """
        raise NotImplementedError

    def _set_control_echo(self, echo):
        """ Toolkit specific method to set the control's echo. """
        raise NotImplementedError

    def _get_control_read_only(self):
        """ Toolkit specific method to get the control's read_only state. """
        raise NotImplementedError

    def _set_control_read_only(self, read_only):
        """ Toolkit specific method to set the control's read_only state. """
        raise NotImplementedError

    def _observe_control_editing_finished(self, remove=False):
        """ Change observation of whether editing is finished. """
        raise NotImplementedError

    # Trait change handlers --------------------------------------------------

    def _placeholder_updated(self):
        if self.control is not None:
            self._set_control_placeholder(self.placeholder)

    def _echo_updated(self):
        if self.control is not None:
            self._set_control_echo(self.echo)

    def _read_only_updated(self):
        if self.control is not None:
            self._set_control_read_only(self.read_only)

    def _update_text_updated(self, new):
        """ Change how we listen to for updates to text value. """
        if self.control is not None:
            if new == 'editing_finished':
                self._observe_control_value(remove=True)
                self._observe_control_editing_finished()
            else:
                self._observe_control_editing_finished(remove=True)
                self._observe_control_value()
