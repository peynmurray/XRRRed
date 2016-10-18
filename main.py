import sys
from PyQt5 import QtWidgets
import XRRRedGUI
import pyqtgraph as pg
from ReflectometryData import ReflectometryData
from ReflectometryBundle import ReflectometryBundle
import numpy as np

class XRRRedGUI(QtWidgets.QMainWindow, XRRRedGUI.Ui_MainWindow, object):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectButtons()
		self.connectSignals()

		self.dataBundle = ReflectometryBundle()

		return

	def connectButtons(self):

		self.loadSpecButton.clicked.connect(self.loadSpecButtonClicked)
		self.loadBackButton.clicked.connect(self.loadBackButtonClicked)
		self.loadSlitButton.clicked.connect(self.loadSlitButtonClicked)
		self.footprintCalcGuess.clicked.connect(self.footprintCalcGuessClicked)
		self.footprintCalcFromGraph.clicked.connect(self.footprintCalcFromGraphClicked)
		self.footprintRangeFull.clicked.connect(self.footprintRangeFullClicked)
		self.footprintRangeFromGraph.clicked.connect(self.footprintRangeFromGraphClicked)
		self.footprintApply.clicked.connect(self.footprintApplyClicked)

		return

	def connectSignals(self):

		self.specWidget.itemSelectionChanged.connect(self.specWidgetItemClicked)
		self.backWidget.itemSelectionChanged.connect(self.backWidgetItemClicked)
		self.slitWidget.itemSelectionChanged.connect(self.slitWidgetItemClicked)

		return

	# def toPlot(self, data):
	# 	self.plot.addItem(pg.ScatterPlotItem(x=data.getQ(), y=data.getIntensity(), symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50)))
	# 	return

	def plotDataBundle(self):
		self.plot.clear()

		for specScan in self.dataBundle.getSpecScans():
			self.plot.addItem(pg.ScatterPlotItem(x=specScan.getTwoTheta(), y=specScan.getIntensity(), symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50)))

		self.plot.setLogMode(y=True)

		self.plot.repaint()
		return

	def specWidgetItemClicked(self):

		items = [item.text() for item in self.specWidget.selectedItems()]
		self.dataBundle.addSpecScans(items)
		self.plotDataBundle()
		return

	def backWidgetItemClicked(self):

		items = [item.text() for item in self.backWidget.selectedItems()]
		self.dataBundle.addBackScans(items)

		return

	def slitWidgetItemClicked(self):

		items = [item.text() for item in self.slitWidget.selectedItems()]
		self.dataBundle.addSlitScans(items)

		return

	def loadFile(self, listWidget):
		filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption="Select data files: ")[0]
		listWidget.addItems(filenames)
		return

	def loadSpecButtonClicked(self):
		self.loadFile(self.specWidget)
		return

	def loadBackButtonClicked(self):
		self.loadFile(self.backWidget)
		return

	def loadSlitButtonClicked(self):
		self.loadFile(self.slitWidget)
		return

	def footprintCalcGuessClicked(self):
		return

	def footprintCalcFromGraphClicked(self):
		return

	def footprintRangeFullClicked(self):
		return

	def footprintRangeFromGraphClicked(self):
		return

	def footprintApplyClicked(self):
		return


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	win = XRRRedGUI()
	win.setWindowTitle("XRRRed")
	win.show()
	sys.exit(app.exec_())