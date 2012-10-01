# Tests basic layout operations of the splitter used in advanced_editor_area_pane.py

import unittest

from advanced_editor_area_pane import AdvancedEditorAreaPane, EditorAreaWidget
from pyface.qt import QtGui, QtCore

class TestEditorAreaWidget(unittest.TestCase):

	def _setUp_split(self, parent=None):
		""" Sets up the root splitter for splitting. Returns this root.

		parent : parent of the returned root
		"""
		root = EditorAreaWidget(editor_area=AdvancedEditorAreaPane(), parent=parent)
		btn0 = QtGui.QPushButton('0')
		btn1 = QtGui.QPushButton('1')
		tabwidget = root.tabwidget()
		tabwidget.addTab(btn0, '0')
		tabwidget.addTab(btn1, '1')
		tabwidget.setCurrentIndex(1)

		return root

	def test_split(self):
		""" Does split function work correct?
		"""
		# setup
		root = self._setUp_split()
		tabwidget = root.tabwidget()
		btn0 = tabwidget.widget(0)
		btn1 = tabwidget.widget(1)

		# perform
		root.split(orientation=QtCore.Qt.Horizontal)

		# test
		# do we get correct leftchild and rightchild?
		self.assertIsNotNone(root.leftchild)
		self.assertIsNotNone(root.rightchild)
		self.assertIsInstance(root.leftchild, EditorAreaWidget)
		self.assertIsInstance(root.rightchild, EditorAreaWidget)
		self.assertEquals(root.leftchild.count(), 1)
		self.assertEquals(root.rightchild.count(), 1)

		# are the tabwidgets laid out correctly?
		self.assertEquals(root.leftchild.tabwidget(), tabwidget)
		self.assertIsNotNone(root.rightchild.tabwidget().empty_widget)

		# are the contents of the left tabwidget correct?
		self.assertEquals(root.leftchild.tabwidget().count(), 2)
		self.assertEquals(root.leftchild.tabwidget().widget(0), btn0)
		self.assertEquals(root.leftchild.tabwidget().widget(1), btn1)
		self.assertEquals(root.leftchild.tabwidget().currentWidget(), btn1)

		# does the right tabwidget contain nothing but the empty widget?
		self.assertEquals(root.rightchild.tabwidget().count(), 1)
		self.assertEquals(root.rightchild.tabwidget().widget(0), 
						root.rightchild.tabwidget().empty_widget)

		# do we have an equally sized split?
		self.assertEquals(root.leftchild.width(), root.rightchild.width())

		# is the rightchild active?
		self.assertEquals(root.editor_area.active_tabwidget, 
						root.rightchild.tabwidget())

	def _setUp_collapse(self, parent=None):
		""" Sets up self, sibling and parent - the necessary components of a collapse.
		Returns the root, leftchild and rightchild of such layout.

		parent : parent of the returned root
		"""
		# setup left
		left = EditorAreaWidget(editor_area=AdvancedEditorAreaPane(), parent=None)
		btn0 = QtGui.QPushButton('btn0')
		btn1 = QtGui.QPushButton('btn1')
		tabwidget = left.tabwidget()
		tabwidget.addTab(btn0, '0')
		tabwidget.addTab(btn1, '1')
		tabwidget.setCurrentIndex(1)
		
		# setup right
		right = EditorAreaWidget(editor_area=left.editor_area, parent=None)
		btn2 = QtGui.QPushButton('btn2')
		btn3 = QtGui.QPushButton('btn3')
		tabwidget = right.tabwidget()
		tabwidget.addTab(btn2, '2')
		tabwidget.addTab(btn3, '3')
		tabwidget.setCurrentIndex(0)
		
		# setup root
		root = EditorAreaWidget(editor_area=left.editor_area, parent=parent)
		tabwidget = root.tabwidget()
		tabwidget.setParent(None)
		root.addWidget(left)
		root.addWidget(right)
		root.leftchild = left
		root.rightchild = right

		return root, left, right

	def test_collapse_nonempty(self):
		""" Test for collapse function when the source of collapse is not an empty 
		tabwidget. This would result in a new tabwidget which merges the tabs of the 
		collapsing tabwidgets.
		"""
		# setup root
		root, left, right = self._setUp_collapse()
		btn0 = left.tabwidget().widget(0)
		btn1 = left.tabwidget().widget(1)
		btn2 = right.tabwidget().widget(0)
		btn3 = right.tabwidget().widget(1)

		# perform
		root.rightchild.collapse()

		# test
		# has the root now become the leaf?
		self.assertEquals(root.count(), 1)
		self.assertIsInstance(root.widget(0), QtGui.QTabWidget)

		# how does the combined list look?
		self.assertEquals(root.tabwidget().count(), 4)
		self.assertEquals(root.tabwidget().currentWidget(), 
						btn2)

	def test_collapse_empty(self):
		""" Test for collapse function when the collapse origin is an empty 
		tabwidget. It's sibling can have an arbitrary layout and the result would
		be such that this layout is transferred to the parent.
		"""
		# setup
		root = EditorAreaWidget(editor_area=AdvancedEditorAreaPane(), parent=None)
		tabwidget = root.tabwidget()
		tabwidget.setParent(None)
		left, left_left, left_right = self._setUp_collapse(parent=root)
		right = EditorAreaWidget(editor_area=root.editor_area, parent=root)
		root.leftchild = left
		root.rightchild = right

		# perform collapse on leftchild
		right.collapse()

		# test
		# is the layout of root now same as left?
		self.assertEquals(root.count(), 2)
		self.assertEquals(root.leftchild, left_left)
		self.assertEquals(root.rightchild, left_right)

		# are the contents of left_left and left_right preserved
		self.assertEquals(root.leftchild.tabwidget().count(), 2)
		self.assertEquals(root.rightchild.tabwidget().count(), 2)
		self.assertEquals(root.leftchild.tabwidget().currentIndex(), 1)
		self.assertEquals(root.rightchild.tabwidget().currentIndex(), 0)

		# what is the current active_tabwidget?
		self.assertEquals(root.editor_area.active_tabwidget, root.leftchild.tabwidget())


if __name__=="__main__":
	unittest.main()