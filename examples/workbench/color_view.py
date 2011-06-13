""" A view containing a colored panel! """


# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from pyface.workbench.api import View


class ColorView(View):
    """ A view containing a colored panel! """

    #### 'IView' interface ####################################################

    # The category that the view belongs to.
    category = 'Color'

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _id_default(self):
        """ Trait initializer. """

        # By making the Id the same as the name, we make it easy to specify
        # the views in the example perspectives. Note for larger applications
        # the Id should be globally unique, and by default we use the module
        # name and class name.
        return self.name

    #### Methods ##############################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        method = getattr(self, '_%s_create_control' % ETSConfig.toolkit, None)
        if method is None:
            raise SystemError('Unknown toolkit %s', ETSConfig.toolkit)

        color = self.name.lower()

        return method(parent, color)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _wx_create_control(self, parent, color):
        """ Create a wx version of the control. """

        import wx

        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour(color)

        return panel

    def _qt4_create_control(self, parent, color):
        """ Create a Qt4 version of the control. """

        from pyface.qt import QtGui

        widget = QtGui.QWidget(parent)

        palette = widget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

        return widget

#### EOF ######################################################################
