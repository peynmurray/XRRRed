import pyqtgraph as pg
from PyQt5 import QtCore

class CustomViewBox(pg.ViewBox):

	def __init__(self, *args, **kwargs):
		pg.ViewBox.__init__(self, *args, **kwargs)
		self.setMouseMode(self.RectMode)
		return

	def mouseClickEvent(self, ev):
		print(ev.button())
		return
		# if ev.button() == QtCore.Qt.RightButton:
		# 	self.autoRange()
		# return

	def mouseDragEvent(self, ev):
		print(ev.button())
		return


		# if ev.button() == QtCore.Qt.RightButton:
		# 	ev.ignore()
		# else:
		# 	pg.ViewBox.mouseDragEvent(self, ev)
		# return