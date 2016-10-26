
# Holds a single data file

import pandas as pd
import numpy as np

class ReflectometryData:

	def __init__(self, filename=None, filetype=None, twoTheta=None, Q=None, intensity=None,  wavelength=None):

		# Default wavelength is 1.54056 angstroms (Cu K-alpha)
		if wavelength is None:
			self.wavelength = 1.54056
		else:
			assert type(wavelength) == float
			self.wavelength = wavelength

		if intensity is not None and filename is None:

			self.intensity = intensity
			self.filename = "Data was input as arrays, not from file."

			if twoTheta is None and Q is not None:
				self.Q = np.array(Q)
				self.twoTheta = 0 * self.Q
				self.updateTwoTheta()
			elif twoTheta is not None and Q is None:
				self.twoTheta = np.array(twoTheta)
				self.Q = 0 * self.twoTheta
				self.updateQ()
			else:
				raise ValueError("Either twoTheta or Q must be specified, and not both.")


		elif intensity is None and twoTheta is None and Q is None and filename is not None:

			#Determine filetype from the file extension
			if filetype is None:
				filetype = filename.split(sep=".")[-1]

			#Use different read_csv options depending on the filetype
			if filetype == "xy":
				raw_data = pd.read_csv(filename, header=None, sep="\t", names=["TwoTheta", "Intensity"])
			else:
				raise ValueError("Invalid filetype.")

			self.filename = filename
			self.twoTheta = np.array(raw_data["TwoTheta"])
			self.intensity = np.array(raw_data["Intensity"])
			self.Q = 0 * self.twoTheta
			self.updateQ()

		else:
			raise ValueError("Invalid parameters pass to ReflectometryData constructor.")

		return

	def setWavelegth(self, wavelength=1.54056):
		"""
		Updates the value of the wavelength of radiation used. Recomputes self.Q afterward.

		:param wavelength: wavelength of radiation used, in angstroms. By default, Cu K-alpha is assumed.
		:return:
		"""

		self.wavelength = wavelength
		return

	def getWavelength(self):
		return self.wavelength

	def updateQ(self):
		"""
		Updates the values in self.Q. In general, Q = (4*pi/lambda)*sin(twoTheta/2)
		:return:
		"""

		self.Q = 4*np.pi*np.sin((np.pi/180)*self.twoTheta/2.0)/self.wavelength
		return

	def updateTwoTheta(self):
		self.twoTheta = 2*np.arcsin((self.Q*self.wavelength)/(4*np.pi))*np.pi/180
		return


	def getTwoTheta(self):
		return self.twoTheta

	def getIntensity(self):
		return self.intensity

	def getQ(self):
		return self.Q

	def getFilename(self):
		return self.filename

	def getMaxIntensity(self):
		return np.max(self.intensity)

	def getIndexMaxIntensity(self):
		return np.argmax(self.intensity)

	def getMaxQ(self):
		return np.max(self.Q)

	def getMinQ(self):
		return np.min(self.Q)

	def __add__(self, value):
		if type(value) == ReflectometryData:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()+value.getIntensity())
		elif type(value) == float or type(value) == np.ndarray or type(value) == np.float64:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()+value)

	def __sub__(self, value):
		if type(value) == ReflectometryData:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()-value.getIntensity())
		elif type(value) == float or type(value) == np.ndarray or type(value) == np.float64:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()-value)

	def __mul__(self, value):
		if type(value) == float or type(value) == np.ndarray or type(value) == np.float64:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()*value)
		elif type(value) == ReflectometryData:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()*value.getIntensity())

	def __truediv__(self, value):
		if type(value) == float or type(value) == np.ndarray or type(value) == np.float64:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()/value)
		elif type(value) == ReflectometryData:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()/value.getIntensity())

	def __floordiv__(self, value):
		if type(value) == float or type(value) == np.ndarray or type(value) == np.float64:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()/value)
		elif type(value) == ReflectometryData:
			return ReflectometryData(Q=self.getQ(), intensity=self.getIntensity()/value.getIntensity())

	def getNPoints(self):
		return len(self.intensity)