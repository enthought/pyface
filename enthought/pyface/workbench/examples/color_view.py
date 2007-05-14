""" A view containing a colored panel! """


# Enthought library imports.
from enthought.pyface.api import toolkit
from enthought.pyface.workbench.api import View


class ColorView(View):
    """ A view containing a colored panel! """

    ###########################################################################
    # 'IView' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        color = self.name.lower()
        tk = toolkit().name

        if tk == 'wx':
            import wx
        
            panel = wx.Panel(parent, -1)
            panel.SetBackgroundColour(color)

        elif tk == 'qt4':
            from PyQt4 import QtGui
        
            panel = QtGui.QWidget(parent)

            palette = panel.palette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
            panel.setPalette(palette)
            panel.setAutoFillBackground(True)

        else:
            panel = None

        return panel

#### EOF ######################################################################
