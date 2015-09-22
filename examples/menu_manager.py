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
from __future__ import print_function

# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Local imports.
from pyface.action.api import Action
from pyface.action.api import Group, MenuManager, Separator


file_menu = MenuManager(
    Group(
        Action(name='New Project...'),
        Action(name='Open Project...'),

        id = 'OpenGroup',
    ),

    Group(
        Action(name='Close Project'),
        Action(name='Close Active Editor'),

        id = 'CloseGroup'
    ),

    Group(
        Action(name='Export to HTML...'),
        Action(name='Print...'),

        id = 'ExportGroup'
    ),

    Group(
        Action(name='Exit'),

        id = 'ExitGroup'
    ),
)
file_menu.dump()

###############################################################################

file_menu = MenuManager(
    Action(name='New Project...'),
    Action(name='Open Project...'),

    Separator(),

    Action(name='Close Project'),
    Action(name='Close Active Editor'),

    Separator(),

    Action(name='Export to HTML...'),
    Action(name='Print...'),

    Separator(),

    Action(name='Exit'),
)
file_menu.dump()

###############################################################################



def new_project():
    print('new project')

def open_project():
    print('open project')

def close_project():
    print('close project')

def close_active_editor():
    print('close active editor')

def export_to_html():
    print('export to html')

def printit():
    print('print')

def exit():
    print('exit')


file_menu = MenuManager(
    open_project,

    Separator(),

    close_project,
    close_active_editor,

    Separator(),

    export_to_html,
    printit,

    Separator(),

    exit,
)
file_menu.dump()
