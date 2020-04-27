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
    "default": Qt.AlignLeft | Qt.AlignVCenter,
    "left": Qt.AlignLeft | Qt.AlignVCenter,
    "center": Qt.AlignHCenter | Qt.AlignVCenter,
    "right": Qt.AlignRight | Qt.AlignVCenter,
}
QALIGNMENT_TO_ALIGNMENT = {
    0: "default",
    Qt.AlignLeft: "left",
    Qt.AlignHCenter: "center",
    Qt.AlignRight: "right",
}
ALIGNMENT_MASK = Qt.AlignLeft | Qt.AlignHCenter | Qt.AlignRight


def alignment_to_qalignment(alignment):
    return ALIGNMENT_TO_QALIGNMENT[alignment]


def qalignment_to_alignment(alignment):
    h_alignment = int(alignment & ALIGNMENT_MASK)
    return QALIGNMENT_TO_ALIGNMENT[h_alignment]
