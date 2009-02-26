#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  Author: Scott Swarts <swarts@enthought.com>
#
#-----------------------------------------------------------------------------

"""A progress dialog for processing in a background thread.
"""

# Standard library imports.
import logging
import threading
import time

# Major packages.
import wx

# Enthought library imports
from enthought.traits.api import Bool, Instance, String

# Local imports.
from dialog import Dialog
from constant import CANCEL


logger = logging.getLogger(__name__)

##############################################################################
# class 'BackgroundProgressDialog'
##############################################################################

class BackgroundProgressDialog(Dialog):
    """A progress dialog for processing in a background thread
    """

    ##########################################################################
    # Traits
    ##########################################################################

    ### 'BackgroundProgressDialog' interface #################################

    initial_message = String            # The initial message in the dialog

    show_elapsed_time = Bool(False)           # Whether to show the times
    show_estimated_time = Bool(False)
    show_remaining_time = Bool(False)

    exception = Instance(Exception)     # Exception raised in background thread

    ### Private traits #######################################################

    _cancel = Bool(False)                # Whether to cancel processing
    _thread = Instance(threading.Thread) # The background processing thread
    _finished = Bool(False)              # Flag set when the thread finishes

    ##########################################################################
    # 'object' interface
    ##########################################################################

    ##########################################################################
    # 'Window' interface
    ##########################################################################

    def open(self):
        """Opens the window then creates and starts the thread."""
        # Start the thread
        self._thread = threading.Thread(target=self._run)
        self._thread.setDaemon(1)
        self._thread.start()

        # Create the dialog
        self._create()
        self.control.Show(True)
        # Wait for it to finish
        while not self._finished:
            wx.Yield()

        # Close it
        self.close()

        return self.return_code
        
    def _create_control(self, parent):
        """Create the progress dialog"""
        style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_CAN_ABORT

        if self.show_elapsed_time:
            style |= wx.PD_ELAPSED_TIME

        if self.show_estimated_time:
            style |= wx.PD_ESTIMATED_TIME

        if self.show_remaining_time:
            style |= wx.PD_REMAINING_TIME

        return wx.ProgressDialog(self.title, self.initial_message,
                                 style=style,
                                 parent=parent)

    def _create_contents(self, control):
        """Do nothing, the progress dialog already has content."""
        pass

    ##########################################################################
    # 'BackgroundProgressDialog' interface
    ##########################################################################

    def _run(self):
        """
        Calls run and sets the _finished flag when done.
        """
        try:
            try:
                self.run()
            except Exception, ex:
                logger.error("Error in background task: %s" % ex)
                self.exception = ex
        finally:
            # Update to 100%.  This will set the finished flag
            self.update(100)

    def run(self):
        """
        Does the background processing.  This will run in another thread.
        Should call update to update the percentage complete and
        check for _cancel being set.

        This should be overridden by subclasses
        """
        for i in range(10):
            if self._cancel:
                return
            self.update(i*10)
            time.sleep(1)
        self.update(100)

    def update(self, value, newmsg=""):
        """
        Calls update on the control
        """
        wx.CallAfter(self._update, value, newmsg)

    def _update(self, value, newmsg):
        """
        Does the update.  This will run in the main thread.
        """
        if self.control is None:
            return

        cont = self.control.Update(value, newmsg)

        # wx 2.7 API changed to return (continue, skip)
        if isinstance(cont, tuple):
            cont, skip = cont
        
        if not cont:
            # Abort has been pressed, set the flag.
            self._cancel = True
            self.return_code = CANCEL

        if value == 100:
            self._finished = True

## Test codel ################################################################
            
def _main():
    dlg = BackgroundProgressDialog(title="Progress",
                                   show_elapsed_time=True,
                                   show_estimated_time=True,
                                   show_remaining_time=True)
    res = dlg.open()
    print "Result = ", res

if __name__ == '__main__':

    from enthought.pyface.api import GUI, ApplicationWindow
    from enthought.pyface.action.api import Action, MenuManager, MenuBarManager

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        ######################################################################
        # 'object' interface.
        ######################################################################

        def __init__(self, **traits):
            """ Creates a new application window. """

            # Base class constructor.
            super(MainWindow, self).__init__(**traits)

            # Add a menu bar.
            self.menu_bar_manager = MenuBarManager(
                MenuManager(
                    Action(name='E&xit', on_perform=self.close),
                    Action(name='DoIt', on_perform=_main),
                    name = '&File',
                )  
            )

            return


    gui = GUI(redirect=False)

    # Create and open the main window.
    window = MainWindow()
    window.open()

    wx.CallAfter(_main)
    
    # Start the GUI event loop!
    gui.event_loop()
    



#### EOF ######################################################################
