# Standard library imports.
import logging

import os

# Major package imports.
import wx

# Logger.
logger = logging.getLogger(__name__)

# Multiple AUI versions are no longer supported; the C version in wx.aui is not
# capable of supporting the windowing flexibility needed by tasks. Therefore,
# only AGW's pure-python AUI implementation is used.

from wx.lib.agw import aui

# AGW's library does need some patching for some usability differences desired
# for pyface but not for the standard wxPython version

class PyfaceAuiNotebook(aui.AuiNotebook):
    if wx.version() >= '3.':
        SetPageToolTip = aui.AuiNotebook.SetPageTooltip
        GetPageToolTip = aui.AuiNotebook.GetPageTooltip


class PyfaceAuiManager(aui.AuiManager):
    # The standard AuiManager dock resizing attempts to adjust all the docks to
    # provide some sort of best fit, but when there are more than two panes in
    # a dock it isn't very intuitive. The modifications to these three methods
    # tries to keep as many sizers fixes as it can and only adjust the one that
    # is added.

    def CalculateDockSizerLimits(self, dock):
        # Replacement for default calculation for min/max dock sizes. Instead
        # of adjusting the sizes of all the docks, only adjusts one to make the
        # dock insertion process a little more like what the user expected.

        docks, panes = aui.CopyDocksAndPanes2(self._docks, self._panes)

        sash_size = self._art.GetMetric(aui.AUI_DOCKART_SASH_SIZE)
        caption_size = self._art.GetMetric(aui.AUI_DOCKART_CAPTION_SIZE)
        opposite_size = self.GetOppositeDockTotalSize(docks, dock.dock_direction)

        for tmpDock in docks:

            if tmpDock.dock_direction == dock.dock_direction and \
               tmpDock.dock_layer == dock.dock_layer and \
               tmpDock.dock_row == dock.dock_row:

                tmpDock.size = 1
                break
        neighbor_docks = []
        horizontal = dock.dock_direction == aui.AUI_DOCK_LEFT or dock.dock_direction == aui.AUI_DOCK_RIGHT
        right_or_down = dock.dock_direction == aui.AUI_DOCK_RIGHT or dock.dock_direction == aui.AUI_DOCK_BOTTOM
        for d in docks:
            if d.dock_direction == dock.dock_direction and d.dock_layer == dock.dock_layer:
                if horizontal:
                    neighbor_docks.append((d.rect.x, d.rect.width))
                else:
                    neighbor_docks.append((d.rect.y, d.rect.height))
        neighbor_docks.sort()

        sizer, panes, docks, uiparts = self.LayoutAll(panes, docks, [], True, False)
        client_size = self._frame.GetClientSize()
        sizer.SetDimension(0, 0, client_size.x, client_size.y)
        sizer.Layout()

        for part in uiparts:

            part.rect = wx.RectPS(part.sizer_item.GetPosition(), part.sizer_item.GetSize())
            if part.type == aui.AuiDockUIPart.typeDock:
                part.dock.rect = part.rect

        sizer.Destroy()
        new_dock = None

        for tmpDock in docks:
            if tmpDock.dock_direction == dock.dock_direction and \
               tmpDock.dock_layer == dock.dock_layer and \
               tmpDock.dock_row == dock.dock_row:

                new_dock = tmpDock
                break

        partnerDock = self.GetPartnerDock(dock)

        if partnerDock:
            if horizontal:
                pos = dock.rect.x
                size = dock.rect.width
            else:
                pos = dock.rect.y
                size = dock.rect.height

            min_pos = pos
            max_pos = pos + size
            if right_or_down:
                for p, s in neighbor_docks:
                    if p >= pos:
                        max_pos = p + s - sash_size
                        break
                    else:
                        min_pos = p + sash_size
            else:
                for p, s in neighbor_docks:
                    if p > pos:
                        max_pos = p + s - sash_size
                        break
                    else:
                        min_pos = p + sash_size

            return min_pos, max_pos

        direction = new_dock.dock_direction

        if direction == aui.AUI_DOCK_LEFT:
            minPix = new_dock.rect.x + new_dock.rect.width
            maxPix = client_size.x - opposite_size - sash_size

        elif direction == aui.AUI_DOCK_TOP:
            minPix = new_dock.rect.y + new_dock.rect.height
            maxPix = client_size.y - opposite_size - sash_size

        elif direction == aui.AUI_DOCK_RIGHT:
            minPix = opposite_size
            maxPix = new_dock.rect.x - sash_size

        elif direction == aui.AUI_DOCK_BOTTOM:
            minPix = opposite_size
            maxPix = new_dock.rect.y - sash_size

        return minPix, maxPix

    def GetPartnerDockFromPos(self, dock, point):
        """Get the neighboring dock located at the given position, used to
        find the other dock that is going to change size when resizing the
        specified dock.
        """
        horizontal = dock.dock_direction == aui.AUI_DOCK_LEFT or dock.dock_direction == aui.AUI_DOCK_RIGHT
        right_or_down = dock.dock_direction == aui.AUI_DOCK_RIGHT or dock.dock_direction == aui.AUI_DOCK_BOTTOM
        if horizontal:
            pos = point.x
        else:
            pos = point.y
        neighbor_docks = []
        for d in self._docks:
            if d.dock_direction == dock.dock_direction and d.dock_layer == dock.dock_layer:
                if horizontal:
                    neighbor_docks.append((d.rect.x, d.rect.width, d))
                else:
                    neighbor_docks.append((d.rect.y, d.rect.height, d))
        neighbor_docks.sort()
        last = None
        if right_or_down:
            for p, s, d in neighbor_docks:
                if pos < p + s:
                    if d.dock_row == dock.dock_row:
                        d = last
                    break
                last = d
        else:
            neighbor_docks.reverse()
            for p, s, d in neighbor_docks:
                if pos > p:
                    if d.dock_row == dock.dock_row:
                        d = last
                    break
                last = d
        return d

    def RestrictResize(self, clientPt, screenPt, createDC):
        """ Common method between :meth:`DoEndResizeAction` and :meth:`OnLeftUp_Resize`. """

        dock = self._action_part.dock
        pane = self._action_part.pane

        if createDC:
            if wx.Platform == "__WXMAC__":
                dc = wx.ClientDC(self._frame)
            else:
                dc = wx.ScreenDC()

            aui.DrawResizeHint(dc, self._action_rect)
            self._action_rect = wx.Rect()

        newPos = clientPt - self._action_offset

        if self._action_part.type == aui.AuiDockUIPart.typeDockSizer:
            minPix, maxPix = self.CalculateDockSizerLimits(dock)
        else:
            if not self._action_part.pane:
                return
            minPix, maxPix = self.CalculatePaneSizerLimits(dock, pane)

        if self._action_part.orientation == wx.HORIZONTAL:
            newPos.y = aui.Clip(newPos.y, minPix, maxPix)
        else:
            newPos.x = aui.Clip(newPos.x, minPix, maxPix)

        if self._action_part.type == aui.AuiDockUIPart.typeDockSizer:
            partner = self.GetPartnerDockFromPos(dock, newPos)
            sash_size = self._art.GetMetric(aui.AUI_DOCKART_SASH_SIZE)
            button_size = self._art.GetMetric(aui.AUI_DOCKART_PANE_BUTTON_SIZE)
            new_dock_size = 0
            direction = dock.dock_direction

            if direction == aui.AUI_DOCK_LEFT:
                new_dock_size = newPos.x - dock.rect.x

            elif direction == aui.AUI_DOCK_TOP:
                new_dock_size = newPos.y - dock.rect.y

            elif direction == aui.AUI_DOCK_RIGHT:
                new_dock_size = dock.rect.x + dock.rect.width - newPos.x - sash_size

            elif direction == aui.AUI_DOCK_BOTTOM:
                new_dock_size = dock.rect.y + dock.rect.height - newPos.y - sash_size

            delta = new_dock_size - dock.size
            if delta < -dock.size + sash_size:
                delta = -dock.size + sash_size
            elif -button_size < delta < button_size:
                delta = button_size * (1 if delta > 0 else -1)

            if partner:
                if delta > partner.size - sash_size:
                    delta = partner.size - sash_size
                partner.size -= delta
            dock.size += delta
            self.Update()

        else:

            # determine the new pixel size that the user wants
            # this will help us recalculate the pane's proportion
            if dock.IsHorizontal():
                oldPixsize = pane.rect.width
                newPixsize = oldPixsize + newPos.x - self._action_part.rect.x

            else:
                oldPixsize = pane.rect.height
                newPixsize = oldPixsize + newPos.y - self._action_part.rect.y

            totalPixsize, totalProportion = self.GetTotalPixSizeAndProportion(dock)
            partnerPane = self.GetPartnerPane(dock, pane)

            # prevent division by zero
            if totalPixsize <= 0 or totalProportion <= 0 or not partnerPane:
                return

            # adjust for the surplus
            while (oldPixsize > 0 and totalPixsize > 10 and \
                  oldPixsize*totalProportion/totalPixsize < pane.dock_proportion):

                totalPixsize -= 1

            # calculate the new proportion of the pane

            newProportion = newPixsize*totalProportion/totalPixsize
            newProportion = aui.Clip(newProportion, 1, totalProportion)
            deltaProp = newProportion - pane.dock_proportion

            if partnerPane.dock_proportion - deltaProp < 1:
                deltaProp = partnerPane.dock_proportion - 1
                newProportion = pane.dock_proportion + deltaProp

            # borrow the space from our neighbor pane to the
            # right or bottom (depending on orientation)
            partnerPane.dock_proportion -= deltaProp
            pane.dock_proportion = newProportion

            self.Update()

        return True

    def UpdateWithoutLayout(self):
        """If the layout in the AUI manager is not changing, this can be called
        to refresh all the panes but preventing a big time usage doing a re-
        layout that isn't necessary.
        """
        pane_count = len(self._panes)

        for ii in range(pane_count):
            p = self._panes[ii]
            if p.window and p.IsShown() and p.IsDocked():
                p.window.Refresh()
                p.window.Update()

        if wx.Platform == "__WXMAC__":
            self._frame.Refresh()
        else:
            self.Repaint()
