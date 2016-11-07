import sys
from PyQt5 import QtWidgets
import XRRRedGUI
import pyqtgraph as pg
from ReflectometryData import ReflectometryData
from ReflectometryBundle import ReflectometryBundle
import numpy as np
from CustomViewBox import CustomViewBox

class XRRRedGUI(QtWidgets.QMainWindow, XRRRedGUI.Ui_MainWindow, object):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectButtons()

		self.dataBundle = ReflectometryBundle()
		self.initializePlot()
		self.refreshPlot()

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
		self.combineScansButton.clicked.connect(self.combineScansButtonClicked)

		self.yAxisLog.toggled.connect(self.yAxisLogToggled)
		self.xAxisQ.toggled.connect(self.xAxisQToggled)

		self.deleteBackButton.clicked.connect(self.deleteBackButtonClicked)
		self.deleteSpecButton.clicked.connect(self.deleteSpecButtonClicked)
		self.deleteSlitButton.clicked.connect(self.deleteSlitButtonClicked)

		return

	def deleteSpecButtonClicked(self):
		for item in self.specWidget.selectedItems():
			index = self.specWidget.row(item)
			self.specWidget.takeItem(index)
			self.dataBundle.deleteSpec(index)
		self.plotDataBundle()
		return

	def deleteBackButtonClicked(self):
		for item in self.backWidget.selectedItems():
			index = self.backWidget.row(item)
			self.backWidget.takeItem(index)
			self.dataBundle.deleteBack(index)
		self.plotDataBundle()
		return

	def deleteSlitButtonClicked(self):
		for item in self.slitWidget.selectedItems():
			index = self.slitWidget.row(item)
			self.slitWidget.takeItem(index)
			self.dataBundle.deleteSlit(index)
		self.plotDataBundle()
		return

	def yAxisLogToggled(self, b):
		self.plot.getPlotItem().setLogMode(y=b)
		return

	def xAxisQToggled(self, b):
		self.plotDataBundle()
		return

	def plotDataBundle(self):
		self.plot.clear()

		getX = lambda scan: scan.getQ() if self.xAxisQ.isChecked() else lambda scan: scan.getTwoTheta()

		if self.dataBundle.isProcessed():
			self.plot.addItem(pg.PlotDataItem(x=getX(self.dataBundle.getProcessed()), y=self.dataBundle.getProcessed().getIntensity(), symbol='t', pen=None, symbolPen=None, symbolSize=10, symbolBrush=(255, 100, 100, 100), name="Data"))
		else:
			for specScan in self.dataBundle.getSpecScans():
				self.plot.addItem(pg.PlotDataItem(x=getX(specScan), y=specScan.getIntensity(), symbol='t', pen=None, symbolPen=None,symbolSize=10, symbolBrush=(100, 100, 255, 100)))

		self.plot.autoRange()
		self.refreshPlot()
		return

	def plotFootprintCorrectionCurve(self):
		if self.footprintRangeMax.value() - self.footprintRangeMin.value() == 0:
			return
		x = np.linspace(self.footprintRangeMin.value(), self.footprintRangeMax.value(), 1000)
		y = self.footprintSlope.value()*x + self.footprintIntercept.value()
		self.plot.addItem(pg.PlotDataItem(x=x, y=y, name="Footprint Correction"))
		self.plot.autoRange()
		return

	def loadSpecButtonClicked(self):
		filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption="Select data files: ")[0]
		self.dataBundle.addSpecScans(filenames)
		self.specWidget.clear()
		self.specWidget.addItems(filenames)
		self.plotDataBundle()
		return

	def loadBackButtonClicked(self):
		filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption="Select data files: ")[0]
		self.dataBundle.addBackScans(filenames)
		self.backWidget.clear()
		self.backWidget.addItems(filenames)
		self.plotDataBundle()
		return

	def loadSlitButtonClicked(self):
		filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption="Select data files: ")[0]
		self.dataBundle.addSlitScans(filenames)
		self.slitWidget.clear()
		self.slitWidget.addItems(filenames)
		self.plotDataBundle()
		return

	def footprintCalcGuessClicked(self):

		a, b = self.dataBundle.guessFootprintCorrection()
		self.footprintSlope.setValue(a)
		self.footprintIntercept.setValue(b)
		self.plotDataBundle()
		self.plotFootprintCorrectionCurve()
		return

	def footprintCalcFromGraphClicked(self):
		self.plotDataBundle()
		self.plotFootprintCorrectionCurve()
		self.plot.autoRange()
		return

	def footprintRangeFullClicked(self):
		self.plotDataBundle()
		self.plotFootprintCorrectionCurve()
		self.plot.autoRange()
		return

	def footprintRangeFromGraphClicked(self):
		self.plotDataBundle()
		self.plotFootprintCorrectionCurve()
		self.plot.autoRange()
		return

	def footprintApplyClicked(self):
		self.dataBundle.footprintCorrection(minQ=self.footprintRangeMin.value(), maxQ=self.footprintRangeMax.value(), slope=self.footprintSlope.value(), intercept=self.footprintIntercept.value())
		self.plotDataBundle()

		self.footprintRangeMax.setEnabled(False)
		self.footprintRangeMin.setEnabled(False)
		self.footprintIntercept.setEnabled(False)
		self.footprintSlope.setEnabled(False)
		self.footprintApply.setEnabled(False)
		self.footprintRangeFromGraph.setEnabled(False)
		self.footprintRangeFull.setEnabled(False)
		self.footprintCalcMax.setEnabled(False)
		self.footprintCalcMin.setEnabled(False)
		self.footprintCalcGuess.setEnabled(False)
		self.footprintCalcFromGraph.setEnabled(False)
		return

	def refreshPlot(self):

		self.plot.getPlotItem().setLabel("left", text="Intensity")

		if self.actionLog.isChecked():
			self.plot.getPlotItem().setLogMode(y=True)
		else:
			self.plot.getPlotItem().setLogMode(y=False)

		if self.actionQ.isChecked():
			self.plot.getPlotItem().setLabel("bottom", text="Q (1/A)")
		else:
			self.plot.getPlotItem().setLabel("bottom", text="2Theta (°)")

		self.plot.repaint()

		return

	def initializePlot(self):
		vb = CustomViewBox()
		self.plot = pg.PlotWidget(parent=self, viewbox=vb, title="Reflectivity")
		self.plotLayout.addWidget(self.plot)
		return

	def combineScansButtonClicked(self):
		try:
			self.dataBundle.combineScans()
			self.plotDataBundle()
			self.footprintRangeMin.setValue(self.dataBundle.getProcessed().getMinQ())
			self.footprintRangeMax.setValue(self.dataBundle.getProcessed().getMaxQ())

			self.loadSlitButton.setEnabled(False)
			self.loadBackButton.setEnabled(False)
			self.loadSpecButton.setEnabled(False)
			self.deleteSlitButton.setEnabled(False)
			self.deleteBackButton.setEnabled(False)
			self.deleteBackButton.setEnabled(False)
			self.combineScansButton.setEnabled(False)
			self.specWidget.setEnabled(False)
			self.backWidget.setEnabled(False)
			self.slitWidget.setEnabled(False)
		except ValueError as e:
			self.msg(str(e))
		return

	def msg(self, string):
		self.statusBar().showMessage(string, msecs=2000)
		return

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	win = XRRRedGUI()
	win.setWindowTitle("XRRRed")
	win.show()
	sys.exit(app.exec_())