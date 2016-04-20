import time

def getTimeMilli():
	return int(round(time.time() * 1000))

class FrameRateHandler:
	def __init__(self, frameRate):
		# The desired amount of frames per second.
		self.frameRate = float(frameRate)
		# How long each frame needs to be to reach the ideal rate,
		# in seconds.
		self.frameDuration = 1.0 / frameRate

		self.frameStart = time.time()
		self.frameEnd = time.time()

		# Multiplied by per second speeds
		self.deltaCoefficient = 0

		self.previousRate = frameRate

	def updateStart(self):
		self.frameStart = time.time()

	def updateEnd(self):
		self.frameEnd = time.time()
		"""waitFor = self.frameDuration - (self.frameEnd - self.frameStart)
		if waitFor > 0.0:
			time.sleep(waitFor)"""
		waitUntil = self.frameEnd + self.frameDuration - (self.frameEnd - self.frameStart)
		while time.time() < waitUntil:
			self.deltaCoefficient = (time.time() - self.frameStart)
		if self.deltaCoefficient == 0:
			self.previousRate = 60
		else:
			self.previousRate = 1.0 / self.deltaCoefficient










