
# Holds a bunch of data files together in a bundle
import numpy as np
from scipy.optimize import curve_fit

from ReflectometryData import ReflectometryData

class ReflectometryBundle:

	def __init__(self, specScans=None, backScans=None, slitScans=None):

		self.processedScan = None

		if specScans is not None:
			self.specScans = specScans
		else:
			self.specScans = []
		if backScans is not None:
			self.backScans = specScans
		else:
			self.backScans = []
		if slitScans is not None:
			self.slitScans = specScans
		else:
			self.slitScans = []
		return

	def addSpecScan(self, scan, filetype, wavelength):

		if type(scan) == str:
			if len(self.specScans) != 0 and scan in [item.getFilename() for item in self.specScans]:
				return
			else:
				scan = ReflectometryData(filename=scan, filetype=filetype, wavelength=wavelength)
		elif type(scan) == ReflectometryData:
			if len(self.specScans) != 0 and scan.getFilename() in [item.getFilename() for item in self.specScans]:
				return
		else:
			return

		self.specScans.append(scan)
		return

	def addBackScan(self, scan, filetype, wavelength):

		if type(scan) == str:
			if len(self.backScans) != 0 and scan in [item.getFilename() for item in self.backScans]:
				return
			else:
				scan = ReflectometryData(filename=scan, filetype=filetype, wavelength=wavelength)
		elif type(scan) == ReflectometryData:
			if len(self.backScans) != 0 and scan.getFilename() in [item.getFilename() for item in self.backScans]:
				return
		else:
			return

		self.backScans.append(scan)
		return

	def addSlitScan(self, scan, filetype, wavelength):

		if type(scan) == str:
			if len(self.slitScans) != 0 and scan in [item.getFilename() for item in self.slitScans]:
				return
			else:
				scan = ReflectometryData(filename=scan, filetype=filetype, wavelength=wavelength)
		elif type(scan) == ReflectometryData:
			if len(self.slitScans) != 0 and scan.getFilename() in [item.getFilename() for item in self.slitScans]:
				return
		else:
			return

		self.slitScans.append(scan)
		return

	def getSpecScans(self):
		return self.specScans

	def getBackScans(self):
		return self.backScans

	def getSlitScans(self):
		return self.slitScans

	def addSpecScans(self, scans, filetypes=list(), wavelengths=list()):

		if len(scans) != len(filetypes):
			filetypes = [None for i in range(len(scans))]

		if len(scans) != len(wavelengths):
			wavelengths = [None for i in range(len(scans))]

		for scan, filetype, wavelength in zip(scans, filetypes, wavelengths):
			self.addSpecScan(scan=scan, filetype=filetype, wavelength=wavelength)
		return

	def addBackScans(self, scans, filetypes=list(), wavelengths=list()):

		if len(scans) != len(filetypes):
			filetypes = [None for i in range(len(scans))]

		if len(scans) != len(wavelengths):
			wavelengths = [None for i in range(len(scans))]

		for scan, filetype, wavelength in zip(scans, filetypes, wavelengths):
			self.addBackScan(scan=scan, filetype=filetype, wavelength=wavelength)
		return

	def addSlitScans(self, scans, filetypes=list(), wavelengths=list()):

		if len(scans) != len(filetypes):
			filetypes = [None for i in range(len(scans))]

		if len(scans) != len(wavelengths):
			wavelengths = [None for i in range(len(scans))]

		for scan, filetype, wavelength in zip(scans, filetypes, wavelengths):
			self.addSlitScan(scan=scan, filetype=filetype, wavelength=wavelength)
		return

	def combineScans(self, transmissionCoefficient=1.0):

		#If some scans have some points in overlapping Q ranges, average those. Otherwise, stitch them togeether.

		combinedSpecScan = self.stitchScans(self.specScans)
		combinedBackScan = self.stitchScans(self.backScans)
		combinedSlitScan = self.stitchScans(self.slitScans)

		if combinedSpecScan is None:
			raise ValueError("No spec scans available!")
		elif combinedBackScan is None and combinedSlitScan is None:
			self.processedScan = combinedSpecScan
		elif combinedBackScan is None and combinedSlitScan is not None:
			self.processedScan = combinedSpecScan/(transmissionCoefficient*combinedSlitScan)
		elif combinedBackScan is not None and combinedSlitScan is None:
			self.processedScan = (combinedSpecScan-combinedBackScan)
		else:
			self.processedScan = (combinedSpecScan - combinedBackScan)/(transmissionCoefficient*combinedSlitScan)
		return

	def sortScans(self, scans):

		sortedScans = []

		while len(scans) != 0:
			i_minQ = 0
			minQ = scans[0].getQ()[0]

			for j in range(len(scans)):
				if scans[j].getQ()[0] < minQ:
					minQ = scans[j].getQ()[0]
					i_minQ = j

				sortedScans.append(scans.pop(i_minQ))

		return sortedScans

	def stitchScans(self, scans):

		if len(scans) == 0:
			return None

		sortedScans = self.sortScans(scans)

		#Q is the proper coordinate to stitch together here because if scans are done with different
		#wavelengths, then they can't be compared in twoTheta space, only in Q.
		stitchedQ = np.hstack(tuple([scan.getQ() for scan in sortedScans]))
		stitchedIntensity = np.hstack(tuple([scan.getIntensity() for scan in sortedScans]))
		ret = ReflectometryData(twoTheta=stitchedQ, intensity=stitchedIntensity)

		#Update the twoTheta values from the default wavelength (Cu K-alpha).
		ret.updateTwoTheta()

		return ret

	def isProcessed(self):
		return self.processedScan is not None

	def getProcessed(self):
		if self.isProcessed():
			return self.processedScan
		else:
			return None

	def getNSpec(self):
		return len(self.specScans)

	def getNBack(self):
		return len(self.backScans)

	def getNSlit(self):
		return len(self.slitScans)

	def guessFootprintCorrection(self):

		indexMaxIntensity = self.processedScan.getIndexMaxIntensity()
		xdata = self.processedScan.getQ()[0:indexMaxIntensity]
		ydata = self.processedScan.getIntensity()[0:indexMaxIntensity]

		fitFunction = lambda x, a, b: a*x + b
		fitParameters, fitConvariances = curve_fit(fitFunction, xdata, ydata)

		return fitParameters[0], fitParameters[1]

	def footprintCorrection(self, minQ, maxQ, slope, intercept):
		self.processedScan = self.processedScan/(intercept+slope*np.linspace(minQ, maxQ, self.processedScan.getNPoints()))
		return

	def deleteSpec(self, index):
		del self.specScans[index]
		return

	def deleteBack(self, index):
		del self.backScans[index]
		return

	def deleteSlit(self, index):
		del self.slitScans[index]
		return
