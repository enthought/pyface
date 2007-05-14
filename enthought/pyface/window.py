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
""" The abstract base class for all Pyface windows. """


# Enthought library imports.
from enthought.logger import logger
from enthought.traits.api import Any, Event, Int, Property, Str, Tuple

# Local imports.
from constant import OK, NO
from key_pressed_event import KeyPressedEvent
from widget import Widget


class Window(Widget):
    """ The abstract base class for all Pyface windows.

    A Pyface window has no visual representation until it is opened (ie. its
    'control' trait will be None until it is opened).

    Usage: Create a sub-class of this class and override the protected
    '_create_control' (if necessary), '_create_contents', and '_size_control'
    (if necessary) methods.
    """

    __tko__ = 'Window'

    #### 'Window' interface ###################################################
    
    # The position of the window.
    position = Property(Tuple) 
    
    # The size of the window.
    size = Property(Tuple)

    # The window title.
    title = Str

    # The return code after the window is closed (this is useful in dialogs
    # etc, to indicate whether the dialog was closed via 'Ok' or 'Cancel').
    return_code = Int(OK)

    # The optional layout manager for the window control.
    # FIXME v3: Decide if we should introduce a toolkit independent layout
    # managers.
    main_sizer = Any

    # The optional layout manager for the window content.
    # FIXME v3: Decide if we should introduce a toolkit independent layout
    # managers.
    sizer = Any
    
    #### Events #####

    # The window has been activated.
    activated = Event

    # The window has been deactivated.
    deactivated = Event
    
    # The window is about to be closed.
    closing =  Event
    
    # The window has been closed.
    closed =  Event

    # The window is about to open.
    opening = Event
    
    # The window has been opened.
    opened = Event

    # A key was pressed while the window had focus.
    key_pressed = Event(KeyPressedEvent)

    #### Private interface ####################################################

    # Shadow trait for size.
    _size = Tuple((-1, -1))

    # Shadow trait for position.
    _position = Tuple((-1, -1))

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_position(self):
        """ Property getter for position. """

        return self._position

    def _set_position(self, position):
        """ Property setter for position. """

        # Save for event notification.
        old = self._position

        # Set the shadow trait.
        self._position = position

        # Notify interested parties.
        self.trait_property_changed('position', old, position)

        return

    def _get_size(self):
        """ Property getter for size. """

        return self._size

    def _set_size(self, size):
        """ Property setter for size. """

        # Save for event notification.
        old = self._size

        # Set the shadow trait.
        self._size = size

        # Notify interested parties.
        self.trait_property_changed('size', old, size)
            
        return
    
    #### Methods ##############################################################

    def open(self):
        """ Opens the window. """

        # Trait notification.
        self.opening = self

        if self.control is None:
            self._create()

        self.show(True)

        # Trait notification.
        self.opened = self
        
        return

    def close(self):
        """ Closes the window. """

        if self.control is not None:
            # Trait notification.
            self.closing = self

            # Cleanup the toolkit-specific control.
            self.destroy()

            # Trait notification.
            self.closed = self

        else:
            logger.debug('window is not open %s' % str(self))
            
        return

    def show(self, visible):
        """ Show or hide the window. """

        self._tk_window_set_visible(visible)

        return

    # ZZZ: Review if this is specific to wx.  (Assume it is for the moment.)
    def refresh(self):
        """ Workaround for VTK render window sizing bug. """

        self._tk_window_refresh()

        return

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog. """

        # fixme: Circular import issue!
        from confirmation_dialog import confirm

        return confirm(self.control, message, title, cancel, default)
    
    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _add_event_listeners(self, control):
        """ Adds any event listeners required by the window. """

        self._tk_window_add_event_listeners(control)

        return
    
    def _create_contents(self, parent):
        """ Creates the (optional) window contents. """

        return self._tk_window_create_contents(parent)

    def _size_control(self, control, content):
        """ Set the size of the toolkit specific control.

        This method is intended to be overridden if necessary.  By default we
        set the size to the value of the 'size' trait.  Subclasses may choose
        another strategy for their initial size, if for instance, they wish
        to set the size based on the size of the contents.
        """

        if self.size != (-1, -1):
            self._tk_window_set_size(self.size)

        return

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the window's widget hierarchy. """

        # Create the toolkit-specific control that represents the window.
        Widget._create(self)

        # Create the contents of the window.
        content = self._create_contents(self.control)
        
        if content is not None and self.sizer is not None:
            self._tk_window_layout_contents(content)

        if self.main_sizer is not None:
            self._tk_window_layout_control()

        self._size_control(self.control, content)

        # Wire up event any event listeners required by the window.
        self._add_event_listeners(self.control)
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    #### Static ####

    def _position_changed(self, position):
        """ Static trait change handler. """

        if self.control is not None:
            self._tk_window_set_position(position)

        return

    def _size_changed(self, size):
        """ Static trait change handler. """

        if self.control is not None:
            self._tk_window_set_size(size)

        return

    def _title_changed(self, title):
        """ Static trait change handler. """

        if self.control is not None:
            self._tk_window_set_title(title)

        return

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        window.

        This must be reimplemented.
        """

        raise NotImplementedError

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_add_event_listeners(self, control):
        """ Adds any event listeners required by the window.

        This must be reimplemented.
        """

        raise NotImplementedError
    
    def _tk_window_create_contents(self, parent):
        """ Create and return the (optional) window contents.

        This default implementation returns None.
        """

        return None

    def _tk_window_layout_contents(self, content):
        """ Layout the window contents.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_window_layout_control(self):
        """ Layout the window control.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_window_refresh(self):
        """ Workaround for VTK render window sizing bug.

        This default implementation does nothing.
        """

        pass

    def _tk_window_set_position(self, position):
        """ Set the window's position.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_window_set_size(self, size):
        """ Set the window's size.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_window_set_title(self, title):
        """ Set the window's title.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_window_set_visible(self, visible):
        """ Show or hide the window.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
