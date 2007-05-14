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
""" A renderer which will display a cell-specific image in addition to some
    text displayed in the same way the standard string renderer normally
    would. """

# Major package imports
from wx import EmptyIcon as wxEmptyIcon
from wx import Size as wxSize
from wx import TRUE as wxTRUE
from wxPython.sheet import wxPySheetCellRenderer as wxSheetCellRenderer
from wxPython.sheet import wxSheetCellStringRenderer
from wxPython.wx import wxBLACK_PEN, wxSOLID, wxBrush, wxRect,\
                        wxTRANSPARENT_PEN, wxWHITE

class SheetCellImageRenderer(wxSheetCellRenderer):
    """ A renderer which will display a cell-specific image in addition to some
        text displayed in the same way the standard string renderer normally
        would. """

    def __init__(self, provider = None):
        """ Build a new SheetCellImageRenderer.

            'provider', if provided, should implement
            get_image_for_cell(row, col) to specify an image to appear
            in the cell at row, col. """

        wxSheetCellRenderer.__init__(self)

        # save the string renderer to use for text.
        self._string_renderer = wxSheetCellStringRenderer()
        
        self._provider = provider

        return

    #########################################################################
    # SheetCellRenderer interface.
    #########################################################################
    def Draw(self, sheet, attr, dc, rect, row, col, isSelected):
        """ Draw the appropriate icon into the specified sheet cell. """

        #print 'SheetCellBmpRenderer.Draw'

        # clear the cell first
        if isSelected:
            bgcolor = sheet.GetSelectionBackground()
        else:
            bgcolor = sheet.GetCellBackgroundColour(row, col)
        
        dc.SetBackgroundMode(wxSOLID)
        dc.SetBrush(wxBrush(bgcolor, wxSOLID))
        dc.SetPen(wxTRANSPARENT_PEN)
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

        # find the correct image for this cell
        bmp = self._get_image(sheet, row, col)

        width = 0
        if bmp is not None:
            # hang onto this for later
            width = bmp.GetWidth()
            # now draw our image into it
            dc.DrawBitmap(bmp, rect.x, rect.y, wxTRUE)

        # draw any text that should be included
        new_rect = wxRect(rect.x + width, rect.y,
                          rect.width - width, rect.height)
        #print 'sheet: ', sheet
        self._string_renderer.Draw(sheet, attr, dc, new_rect,
                                   row, col, isSelected)

        return

    def GetBestSize(self, sheet, attr, dc, row, col):
        """ Determine best size for the cell. """

        # find the correct image
        bmp = self._get_image(sheet, row, col)

        if bmp is not None:
            bmp_size = wxSize(bmp.GetWidth(), bmp.GetHeight())
        else:
            bmp_size = wxSize(0, 0)

        bmp_size.width = bmp_size.width

        text_size = self._string_renderer.GetBestSize(sheet, attr, dc,
                                                      row, col)
        result = wxSize(bmp_size.width + text_size.width,
                        max(bmp_size.height, text_size.height))

        return result

    def Clone(self):
        return SheetIconRenderer(self._provider)

    #########################################################################
    # protected 'SheetCellIconRenderer' interface.
    #########################################################################
    def _get_image(self, sheet, row, col):
        """ Returns the correct bmp for the data at row, col. """

        bmp = None
        if self._provider is not None and \
           hasattr(self._provider, 'get_image_for_cell'):
            # get the image from the specified provider
            img = self._provider.get_image_for_cell(row, col)
            bmp = img.ConvertToBitmap()

        return bmp

#### EOF ######################################################################
    
