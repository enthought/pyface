# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Qt alignment helper functions """

from pyface.qt.QtCore import Qt


ALIGNMENT_TO_QALIGNMENT = {
    "default": Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
    "left": Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
    "center": Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
    "right": Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
}
QALIGNMENT_TO_ALIGNMENT = {
    0: "default",
    Qt.Alignment.AlignLeft: "left",
    Qt.Alignment.AlignHCenter: "center",
    Qt.Alignment.AlignRight: "right",
}
ALIGNMENT_MASK = (
    Qt.AlignmentFlag.AlignLeft
    | Qt.AlignmentFlag.AlignHCenter
    | Qt.AlignmentFlag.AlignRight
)


def alignment_to_qalignment(alignment):
    return ALIGNMENT_TO_QALIGNMENT[alignment]


def qalignment_to_alignment(alignment):
    h_alignment = int(alignment & ALIGNMENT_MASK)
    return QALIGNMENT_TO_ALIGNMENT[h_alignment]
