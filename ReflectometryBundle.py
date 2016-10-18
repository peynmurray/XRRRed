
# Holds a bunch of data files together in a bundle


from ReflectometryData import ReflectometryData

class ReflectometryBundle:

	def __init__(self, specScans=None, backScans=None, slitScans=None):

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