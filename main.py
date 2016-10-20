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
		self.combineSpecButton.clicked.connect(self.combineSpecScansButtonClicked)

		return

	def connectSignals(self):

		self.specWidget.itemSelectionChanged.connect(self.specWidgetItemClicked)
		self.backWidget.itemSelectionChanged.connect(self.backWidgetItemClicked)
		self.slitWidget.itemSelectionChanged.connect(self.slitWidgetItemClicked)

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

		if self.getXCoordinate() == "Q":
			getX = lambda scan: scan.getQ()
		else:
			getX = lambda scan: scan.getTwoTheta()

		for specScan in self.dataBundle.getSpecScans():
			self.plot.addItem(pg.PlotDataItem(x=getX(specScan), y=specScan.getIntensity(), symbol='t', pen=None, symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 100)))

		if self.dataBundle.isProcessed():
			self.plot.addItem(pg.PlotDataItem(x=getX(self.dataBundle.getProcessed()), y=self.dataBundle.getProcessed().getIntensity(), symbol='t', pen=None, symbolPen=None, symbolSize=10, symbolBrush=(255, 100, 100, 100)))

		if self.footprintSlope.value() != 0 and self.footprintIntercept.value() != 0:

			x = np.linspace(0, .03, 1000)
			y = self.footprintSlope.value()*x + self.footprintIntercept.value()

			self.plot.addItem(pg.PlotDataItem(x=x, y=y))

			# fitLine = pg.InfiniteLine(pos=pg.Point(0, self.footprintIntercept.value()), angle=np.arctan(self.footprintSlope.value()))
			# self.plot.addItem(fitLine)

		self.refreshPlot()
		return

	def specWidgetItemClicked(self):

		items = [item.text() for item in self.specWidget.selectedItems()]
		self.dataBundle.addSpecScans(items)
		self.plotDataBundle()
		return

	def backWidgetItemClicked(self):

		items = [item.text() for item in self.backWidget.selectedItems()]
		self.dataBundle.addBackScans(items)
		self.plotDataBundle()

		return

	def slitWidgetItemClicked(self):

		items = [item.text() for item in self.slitWidget.selectedItems()]
		self.dataBundle.addSlitScans(items)
		self.plotDataBundle()

		return

	def loadFile(self, listWidget):

		#Dialog box for filenames
		filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption="Select data files: ")[0]

		#Get files already in listWidget
		listedFiles = [listWidget.item(i).text() for i in range(listWidget.count())]

		#Strip out filenames that are in the list already
		for i in range(len(filenames)):
			if filenames[i] in listedFiles:
				del filenames[i]

		#Add filenames to the listwidget
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
		return

	def footprintCalcFromGraphClicked(self):
		return

	def footprintRangeFullClicked(self):
		return

	def footprintRangeFromGraphClicked(self):
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

	def combineSpecScansButtonClicked(self):
		self.dataBundle.combineSpecScans()
		self.plotDataBundle()
		return


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	win = XRRRedGUI()
	win.setWindowTitle("XRRRed")
	win.show()
	sys.exit(app.exec_())