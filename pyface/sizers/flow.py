#-------------------------------------------------------------------------------
#
#  Defines a horizontal or vertical flow layout sizer for wxPython
#
#  Written by: David C. Morrill
#
#  Date: 01/12/2006
#
#  (c) Copyright 2006 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx

from pyface.timer.api \
    import do_later

#-------------------------------------------------------------------------------
#  'FlowSizer' class:
#-------------------------------------------------------------------------------

class FlowSizer ( wx.PySizer ):

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, orient = wx.HORIZONTAL ):
        super( FlowSizer, self ).__init__()
        self._orient       = orient
        self._frozen       = False
        self._needed_size  = None

    #---------------------------------------------------------------------------
    #  Calculates the minimum size needed by the sizer:
    #---------------------------------------------------------------------------

    def CalcMin ( self ):
        """ Calculates the minimum size needed by the sizer.
        """
        if self._needed_size is not None:
            return self._needed_size

        horizontal  = (self._orient == wx.HORIZONTAL)
        dx = dy = 0

        for item in self.GetChildren() :
            idx, idy = item.CalcMin()
            if horizontal:
                dy = max( dy, idy )
            else:
                dx = max( dx, idx )

        return wx.Size( dx, dy )

    #---------------------------------------------------------------------------
    #  Layout the contents of the sizer based on the sizer's current size and
    #  position:
    #---------------------------------------------------------------------------

    def RecalcSizes ( self ):
        """ Layout the contents of the sizer based on the sizer's current size
            and position.
        """
        horizontal = (self._orient == wx.HORIZONTAL)
        x,   y     = self.GetPosition()
        dx, dy     = self.GetSize()
        x0, y0     = x, y
        ex         = x + dx
        ey         = y + dy
        mdx = mdy  = sdx = sdy = 0

        visible = True
        cur_max = 0

        for item in self.GetChildren() :
            idx, idy  = item.CalcMin()
            expand    = item.GetFlag() & wx.EXPAND
            if horizontal:
                if (x > x0) and ((x + idx) > ex):
                    x   = x0
                    y  += (mdy + sdy)
                    mdy = sdy = 0
                    if y >= ey:
                        visible = False

                cur_max = max( idy, cur_max )
                if expand:
                    idy = cur_max

                if item.IsSpacer():
                    sdy = max( sdy, idy )
                    if x == x0:
                        idx = 0
                item.SetDimension( wx.Point( x, y ), wx.Size( idx, idy ) )
                item.Show( visible )
                x  += idx
                mdy = max( mdy, idy )
            else:
                if (y > y0) and ((y + idy) > ey):
                    y   = y0
                    x  += (mdx + sdx)
                    mdx = sdx = 0
                    if x >= ex:
                        visible = False

                cur_max = max( idx, cur_max )
                if expand:
                    idx = cur_max

                if item.IsSpacer():
                    sdx = max( sdx, idx )
                    if y == y0:
                        idy = 0

                item.SetDimension( wx.Point( x, y ), wx.Size( idx, idy ) )
                item.Show( visible )
                y  += idy
                mdx = max( mdx, idx )

        if (not visible) and (self._needed_size is None):
            max_dx = max_dy = 0
            if horizontal:
                max_dy = max( dy, y + mdy + sdy - y0 )
            else:
                max_dx = max( dx, x + mdx + sdx - x0 )
            self._needed_size = wx.Size( max_dx, max_dy )
            if not self._frozen:
                self._do_parent( '_freeze' )
            do_later( self._do_parent, '_thaw' )
        else:
            self._needed_size = None

    #---------------------------------------------------------------------------
    #  Prevents the specified window from doing any further screen updates:
    #---------------------------------------------------------------------------

    def _freeze ( self, window ):
        """ Prevents the specified window from doing any further screen updates.
        """
        window.Freeze()
        self._frozen = True

    #---------------------------------------------------------------------------
    #  Lays out a specified window and then allows it to be updated again:
    #---------------------------------------------------------------------------

    def _thaw ( self, window ):
        """ Lays out a specified window and then allows it to be updated again.
        """
        window.Layout()
        window.Refresh()
        if self._frozen:
            self._frozen = False
            window.Thaw()

    #---------------------------------------------------------------------------
    #  Does a specified operation on the sizer's parent window:
    #---------------------------------------------------------------------------

    def _do_parent ( self, method ):
        """ Does a specified operation on the sizer's parent window.
        """
        i = 0
        while True:
            try:
                item = self.GetItem( i )
                if item is None:
                    break
                i += 1
            except:
                return

            if item.IsWindow():
                getattr( self, method )( item.GetWindow().GetParent() )
                return

