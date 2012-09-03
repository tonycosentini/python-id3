class ID3Tag:
	def __init__(self, major_version, minor_version, flag):
		self.major_version = major_version
		self.minor_version = minor_version
		self.flag = flag
		self.frames = {}

	def __str__(self):
		description = 'Major version: {self.major_version}\nMinor version: {self.minor_version}\n'.format(self=self)
		for frame_id, data in self.frames.iteritems():
			description += "Frame ID: %s\n" % frame_id
			if len(data) <= 100:
				description += "Data: %s" % data
			else:
				description += "Data is too large."
			description += "\n\n"
		return description