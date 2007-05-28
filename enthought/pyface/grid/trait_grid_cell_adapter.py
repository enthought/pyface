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
""" Adapter class to make trait editor controls work inside of a grid. """

# Major package imports
from wx.grid import PyGridCellEditor
from wx import SIZE_ALLOW_MINUS_ONE

# Enthought library imports
from enthought.traits.api import false
from enthought.traits.ui.api import default_handler
from enthought.traits.ui.ui import UI

class TraitGridCellAdapter(PyGridCellEditor):
    """ Wrap a trait editor as a GridCellEditor object. """
    
    def __init__(self, trait_editor_factory, obj, name, description,
                 handler = None, context = None):
        """ Build a new TraitGridCellAdapter object. """

        PyGridCellEditor.__init__(self)
        self._factory = trait_editor_factory
        self._editor = None
        self._obj = obj
        self._name = name
        self._description = description
        self._handler = handler
        self._context = context
        return
        
    def Create(self, parent, id, evtHandler):
        """ Called to create the control, which must derive from wxControl. """

        if self._handler is not None:
            handler = self._handler
        else:
            handler = default_handler()

        if self._context is None:
            ui = UI(handler = handler)
        else:
            context = self._context.copy()
            context['table_editor_object'] = context['object']
            context['object'] = self._obj
            ui = UI(handler = handler, context = context)
            
        # make sure the factory knows this is a grid_cell editor
        self._factory.is_grid_cell = True
        self._editor = self._factory.simple_editor(ui,
                                                   self._obj,
                                                   self._name,
                                                   self._description,
                                                   parent)
                                 
        # Tell the editor to actually build the editing widget:
        self._editor.prepare(parent)
        self.SetControl(self._editor.control)

        if evtHandler:
            self._editor.control.PushEventHandler(evtHandler)

        return
    
    def SetSize(self, rect):
        """ Called to position/size the edit control within the cell rectangle.
            If you don't fill the cell (the rect) then be sure to override
            PaintBackground and do something meaningful there.
        """
        #print 'TraitGridCellAdapter.SetSize'
        self._editor.control.SetDimensions(rect.x, rect.y,
                                           rect.width+2, rect.height+2,
                                           SIZE_ALLOW_MINUS_ONE)
        return

    def Show(self, show, attr):
        """ Show or hide the edit control.  You can use the attr (if not None)
            to set colours or fonts for the control.
        """
        #print 'TraitGridCellAdapter.Show'
        if self.IsCreated():
            self.base_Show(show, attr)

        return

    def PaintBackground(self, rect, attr):
        """ Draws the part of the cell not occupied by the edit control.  The
            base  class version just fills it with background colour from the
            attribute.  In this class the edit control fills the whole cell so
            don't do anything at all in order to reduce flicker.
        """
        #print 'TraitGridCellAdapter.PaintBackground'
        return self.base_PaintBackground(rect, attr)

    def BeginEdit(self, row, col, grid):
        """ Make sure the control is ready to edit. """

        # print 'TraitGridCellAdapter.BeginEdit'

        # we have to manually set the focus to the control
        #print 'TraitGridCellAdapter.BeginEdit'
        self._editor.update_editor()
        self._editor.control.SetFocus()
        return 

    def EndEdit(self, row, col, grid):
        """ Do anything necessary to complete the editing. """

        #print 'TraitGridCellAdapter.EndEdit'

        # Note that we shouldn't have to do anything here, since the underlying
        # trait editor should take care of setting the value correctly
        #print 'TraitGridCellAdapter.EndEdit'
        return True

    def Reset(self):
        """ Reset the value in the control back to its starting value. """

        # fixme: should we be using the undo history here?
        return

    def IsAcceptedKey(self, evt):
        """ Return True to allow the given key to start editing: the base class
            version only checks that the event has no modifiers.  F2 is special
            and will always start the editor.
        """
        return PyGridCellEditor.base_IsAcceptedKey(self, evt)

    def StartingKey(self, evt):
        """ If the editor is enabled by pressing keys on the grid, this will be
            called to let the editor do something about that first key
            if desired.
        """
        #print 'TraitGridCellAdapter.StartingKey'
        return

    def StartingClick(self):
        """ If the editor is enabled by clicking on the cell, this method
            will be called to allow the editor to simulate the click on the
            control if needed.
        """
        return

    def Destroy(self):
        """ Final cleanup. """
        print 'TraitGridCellAdapter.Destroy'
        self._editor.dispose()
        return

    def Clone(self):
        """ Create a new object which is the copy of this one. """
        #print 'TraitGridCellAdapter.Clone'

        return TraitGridCellAdapter(self._factory, self._obj, self._name,
                                    self._description)

    def dispose(self):
        if self._editor is not None:
            self._editor.dispose()
        return


#### EOF ######################################################################
    
