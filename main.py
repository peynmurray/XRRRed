import sys
from PyQt5 import QtWidgets
import XRRRedGUI
import pyqtgraph as pg
from ReflectometryData import ReflectometryData
from ReflectometryBundle import ReflectometryBundle
import numpy as np
from scipy.optimize import curve_fit
from CustomViewBox import CustomViewBox

class XRRRedGUI(QtWidgets.QMainWindow, XRRRedGUI.Ui_MainWindow, object):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectButtons()
		self.connectSignals()

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

		return

	def connectSignals(self):

		# self.actionQ.toggled.connect(self.actionQToggled)
		# self.action2Theta.toggled.connect(self.action2ThetaToggled)
		self.actionLog.toggled.connect(self.actionLogToggled)
		self.actionLinear.toggled.connect(self.actionLinearToggled)

		return

	def actionLogToggled(self, status):
		if status:
			self.actionLinear.setChecked(False)
			self.refreshPlot()
		else:
			self.actionLog.setChecked(True)
		return

	def actionLinearToggled(self, status):
		self.actionLog.setChecked(not status)
		self.refreshPlot()
		return

	def xAxisToggled(self):
		return

	def yAxisToggled(self):
		return

	def plotDataBundle(self):
		self.plot.clear()

		getX = lambda scan: scan.getQ() if self.getXCoordinate() == "Q" else lambda scan: scan.getTwoTheta()

		if self.dataBundle.isProcessed():
			self.plot.addItem(pg.PlotDataItem(x=getX(self.dataBundle.getProcessed()), y=self.dataBundle.getProcessed().getIntensity(), symbol='t', pen=None, symbolPen=None, symbolSize=10, symbolBrush=(255, 100, 100, 100), name="Data"))
		else:
			for specScan in self.dataBundle.getSpecScans():
				self.plot.addItem(pg.PlotDataItem(x=getX(specScan), y=specScan.getIntensity(), symbol='t', pen=None, symbolPen=None,symbolSize=10, symbolBrush=(100, 100, 255, 100)))

		self.plot.autoRange()
		self.refreshPlot()
		return

	def plotFootprintCorrectionCurve(self):
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

		scan = self.dataBundle.getProcessed()
		indexMaxIntensity = scan.getIndexMaxIntensity()
		xdata = scan.getQ()[0:indexMaxIntensity]
		ydata = scan.getIntensity()[0:indexMaxIntensity]

		fitFunction = lambda x, a, b: a*x + b
		fitParameters, fitConvariances = curve_fit(fitFunction, xdata, ydata)

		a, b = fitParameters[0], fitParameters[1]

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
		return

	def getXCoordinate(self):
		if self.actionQ.isChecked():
			return "Q"
		else:
			return "twoTheta"

	def refreshPlot(self):

		self.plot.getPlotItem().setLabel("left", text="Intensity")

		if self.actionLog.isChecked():
			self.plot.getPlotItem().setLogMode(y=True)

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