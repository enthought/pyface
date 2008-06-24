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
import wx
from wx.grid import PyGridCellEditor
from wx import SIZE_ALLOW_MINUS_ONE

# Enthought library imports
from enthought.traits.api import false
from enthought.traits.ui.api import default_handler
from enthought.traits.ui.ui import UI

class TraitGridCellAdapter(PyGridCellEditor):
    """ Wrap a trait editor as a GridCellEditor object. """
    
    def __init__(self, trait_editor_factory, obj, name, description,
                 handler = None, context = None, style = 'simple'):
        """ Build a new TraitGridCellAdapter object. """

        PyGridCellEditor.__init__(self)
        self._factory     = trait_editor_factory
        self._style       = style 
        self._editor      = None
        self._obj         = obj
        self._name        = name
        self._description = description
        self._handler     = handler
        self._context     = context
        
    def Create(self, parent, id, evtHandler):
        """ Called to create the control, which must derive from wxControl. """
        # If the editor has already been created, ignore the request:
        if hasattr( self, '_control' ):
            return

        handler = self._handler
        if handler is None:
            handler = default_handler()

        if self._context is None:
            ui = UI(handler = handler)
        else:
            context = self._context.copy()
            context['table_editor_object'] = context['object']
            context['object'] = self._obj
            ui = UI(handler = handler, context = context)
            
        # Link the editor's undo history in to the main ui undo history if the
        # UI object is available:
        factory = self._factory
        if factory._ui is not None:
            ui.history = factory._ui.history
            
        # make sure the factory knows this is a grid_cell editor
        factory.is_grid_cell = True
        factory_method = getattr(factory, self._style + '_editor')
        self._editor = factory_method(ui,
                                      self._obj,
                                      self._name,
                                      self._description,
                                      parent)
                                 
        # Tell the editor to actually build the editing widget:
        self._editor.prepare(parent)
        
        # Find the control to use as the editor:
        self._control = control = self._editor.control
            
        # Save the required editor size:
        self._edit_height = control.GetBestSize()[1]
        
        # Handle the case of a simple control:
        if isinstance(control, wx.Control):
            self.SetControl(control)
           
        if evtHandler: 
            control.PushEventHandler(evtHandler) 
    
    def SetSize(self, rect):
        """ Called to position/size the edit control within the cell rectangle.
            If you don't fill the cell (the rect) then be sure to override
            PaintBackground and do something meaningful there.
        """
        edit_height = rect.height
        grid, row = getattr(self, '_grid_info', (None, None))
        if grid is not None:
            edit_height, cur_height = self._edit_height, grid.GetRowSize(row)
            if edit_height > cur_height:
                self._restore_height = cur_height
                grid.SetRowSize(row, edit_height + 1 + (row == 0))
                grid.ForceRefresh()
                
        self._editor.control.SetDimensions(rect.x + 1, rect.y + 1,
                                           rect.width - 1, edit_height,
                                           SIZE_ALLOW_MINUS_ONE)

    def PaintBackground(self, rect, attr):
        """ Draws the part of the cell not occupied by the edit control.  The
            base  class version just fills it with background colour from the
            attribute.  In this class the edit control fills the whole cell so
            don't do anything at all in order to reduce flicker.
        """
        return

    def BeginEdit(self, row, col, grid):
        """ Make sure the control is ready to edit. """
        # We have to manually set the focus to the control
        self._editor.update_editor()
        self._control.Show(True)
        self._control.SetFocus()

    def EndEdit(self, row, col, grid):
        """ Do anything necessary to complete the editing. """
        self._control.Show(False)
        
        height = getattr(self, '_restore_height', None)
        if height is not None:
            grid, row = self._grid_info
            grid.SetRowSize(row, height)
            del self._restore_height
            grid.ForceRefresh()

    def Reset(self):
        """ Reset the value in the control back to its starting value. """

        # fixme: should we be using the undo history here?
        return

    def StartingKey(self, evt):
        """ If the editor is enabled by pressing keys on the grid, this will be
            called to let the editor do something about that first key
            if desired.
        """
        return

    def StartingClick(self):
        """ If the editor is enabled by clicking on the cell, this method
            will be called to allow the editor to simulate the click on the
            control if needed.
        """
        return

    def Destroy(self):
        """ Final cleanup. """
        self._editor.dispose()
        return

    def Clone(self):
        """ Create a new object which is the copy of this one. """
        return TraitGridCellAdapter(self._factory, self._obj, self._name,
                                    self._description, style=self._style)

    def dispose(self):
        if self._editor is not None:
            self._editor.dispose()
            
        self.DecRef()
        
#### EOF ######################################################################
    
