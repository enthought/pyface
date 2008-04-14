""" A view containing a colored panel! """


# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.pyface.workbench.api import View


class ColorView(View):
    """ A view containing a colored panel! """

    #### 'IView' interface ####################################################

    # The category that the view belongs to.
    category = 'Color'

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        # By making the Id the same as the name, we make it easy to specify
        # the views in the example perspectives. Note for larger applications
        # the Id should be globally unique, and by default we use the module
        # name and class name.
        return self.name
    
    ###########################################################################
    # 'IView' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        color = self.name.lower()
        tk = ETSConfig.toolkit

        if tk == 'wx':
            import wx
        
            panel = wx.Panel(parent, -1)
            panel.SetBackgroundColour(color)

        elif tk == 'qt4':
            from PyQt4 import QtGui
        
            panel = QtGui.QWidget(parent)

            palette = QtGui.QPalette(panel.palette())
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
            panel.setPalette(palette)
            panel.setAutoFillBackground(True)

        else:
            panel = None

        return panel

#### EOF ######################################################################
