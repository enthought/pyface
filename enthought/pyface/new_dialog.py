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
""" The dialog that allows the user to create new objects. """


# Major package imports.
import wx

# Enthought library imports.
from enthought.naming.api import Binding, Context
from enthought.naming.ui.api import NamingTree, NamingTreeModel
from enthought.traits.api import Any, Instance, Str

# Local imports.
from dialog import Dialog
from heading_text import HeadingText


class NewDialog(Dialog):
    """ The dialog that allows the user to create new objects. """

    #### 'Dialog' interface ###################################################
    
    # The dialog title.
    title = Str('New')

    #### 'NewDialog' interface ################################################

    # The root of the template hierarchy to be displayed in the tree.
    root = Instance(Context)

    # The selected template (None if the user hits 'Cancel').
    template = Any

    # The heading text.
    text = Str('Choose a wizard')

    ###########################################################################
    # Protected 'Dialog' interface.
    ###########################################################################

    def _create_dialog_area(self, parent):
        """ Creates the main content of the dialog. """

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The 'pretty' title bar ;^)
        title = HeadingText(panel, text=self.text)
        sizer.Add(title.control, 0, wx.EXPAND | wx.BOTTOM, 5)

        # Create the tree.
        tree = self._create_tree(panel)
        sizer.Add(tree, 1, wx.EXPAND)

        # Resize the panel to fit the sizer's minimum size.
        sizer.Fit(panel)

        return panel

    def _create_buttons(self, parent):
        """ Creates the buttons. """

        sizer = super(NewDialog, self)._create_buttons(parent)

        # Disable the 'Ok' button until a template is selected etc.
        self._no_template_selected()

        return sizer
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_tree(self, parent):
        """ Creates the preference page tree. """

        model = NamingTreeModel(root=Binding(name='root', obj=self.root))

        tree = NamingTree(parent, model=model, show_root=False)
        tree.on_trait_change(self._on_selection_changed, 'selection')
        
        return tree.control

    #### Trait event handlers #################################################

    def _on_selection_changed(self, selection):
        """ Called when a node in the tree is selected. """

        # The tree is in single selection mode.
        if len(selection) > 0:
            binding = selection[0]
            if isinstance(binding.obj, Context):
                self._no_template_selected()
                
            else:
                self._template_selected(binding.obj)
                
        else:
            self._no_template_selected()
        
        return

    def _template_selected(self, template):
        """ Configure buttons etc when a template IS selected. """

        self._ok.Enable(True)
        self._ok.SetDefault()
        self.template = template

        return

    def _no_template_selected(self):
        """ Configure buttons etc when NO template folder is selected. """

        self._ok.Enable(False)
        self._cancel.SetDefault()
        self.template = None

        return
    
#### EOF ######################################################################
