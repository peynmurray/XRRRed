
# Holds a single data file

import pandas as pd
import numpy as np

class ReflectometryData:

	def __init__(self, filename, filetype=None, wavelength=None):

		#Determine filetype from the file extension
		if filetype is None:
			filetype = filename.split(sep=".")[-1]

		#Use different read_csv options depending on the filetype
		if filetype == "xy":
			raw_data = pd.read_csv(filename, header=None, sep="\t", names=["TwoTheta", "Intensity"])
		else:
			raise ValueError("Invalid filetype.")

		#Default wavelength is 1.54056 angstroms (Cu K-alpha)
		if wavelength is None:
			self.wavelength = 1.54056
		else:
			assert type(wavelength) == float
			self.wavelength = wavelength

		self.filename = filename
		self.twoTheta = np.array(raw_data["TwoTheta"])
		self.intensity = np.array(raw_data["Intensity"])
		self.Q = 0 * self.twoTheta
		self.updateQ()

		return

	def setWavelegth(self, wavelength=1.54056):
		"""
		Updates the value of the wavelength of radiation used. Recomputes self.Q afterward.

		:param wavelength: wavelength of radiation used, in angstroms. By default, Cu K-alpha is assumed.
		:return:
		"""

		self.wavelength = wavelength
		self.updateQ()
		return

	def getWavelength(self):
		return self.wavelength

	def updateQ(self):
		"""
		Updates the values in self.Q. In general, Q = (4*pi/lambda)*sin(twoTheta/2)
		:return:
		"""

		self.Q = 4*np.pi*np.sin(self.twoTheta/2.0)/self.wavelength
		return


	def getTwoTheta(self):
		return self.twoTheta

	def getIntensity(self):
		return self.intensity

	def getQ(self):
		return self.Q

	def getFilename(self):
		return self.filename