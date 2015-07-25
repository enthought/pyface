from __future__ import absolute_import

import os

from traits.testing.unittest_tools import unittest

from ..file_dialog import FileDialog
from ..gui import GUI
from ..toolkit import toolkit_object

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestFileDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = FileDialog()

    def test_create_wildcard(self):
        wildcard = FileDialog.create_wildcard('Python', '*.py')
        self.assertTrue(len(wildcard) != 0)

    def test_create_wildcard_multiple(self):
        wildcard = FileDialog.create_wildcard(
            'Python', ['*.py', '*.pyo', '*.pyc', '*.pyd'])
        self.assertTrue(len(wildcard) != 0)

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_close(self):
        # test that close works
        self.dialog._create()
        self.gui.process_events()
        self.dialog.close()

    def test_default_path(self):
        # test that default path works
        self.dialog.default_path = os.path.join('images', 'core.png')
        self.dialog._create()
        self.gui.process_events()
        self.dialog.close()

    def test_default_dir_and_file(self):
        # test that default dir and path works
        self.dialog.default_directory = 'images'
        self.dialog.default_filename = 'core.png'
        self.dialog._create()
        self.gui.process_events()
        self.dialog.close()

    def test_open_files(self):
        # test that open files action works
        self.dialog.action = 'open files'
        self.dialog._create()
        self.gui.process_events()
        self.dialog.close()

    def test_save_as(self):
        # test that open files action works
        self.dialog.action = 'save as'
        self.dialog._create()
        self.gui.process_events()
        self.dialog.close()

    #XXX would be nice to actually test with an open dialog, but not right now
