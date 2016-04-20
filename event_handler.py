import pygame
from pygame.locals import *

# Handles lists describing every key, primarily including whether they were
# pressed/released this frame and whether they are currently down or not.
class KeyLists:
	def __init__(self, length):
		# All 3 lists of bools are the same length.
		self.length = length
		# If the key was up last frame and down this frame.
		self.press = []
		# If the key is currently down.
		self.down = []
		# If the key was down last frame and up this frame.
		self.release = []

		# Simply fill with empty values.
		for i in range(self.length):
			self.press.append(False)
			self.down.append(False)
			self.release.append(False)

	# Clear the lists dependant on single frames.
	def clear(self):
		for i in range(self.length):
			self.press[i] = False
			self.release[i] = False

	# Changes a key based on an index.
	def setKeyDown(self, index):
		self.press[index] = True
		self.down[index] = True

	def setKeyUp(self, index):
		self.release[index] = True
		self.down[index] = False



# Handles everything about the mouse,
# including position, buttons, and the wheel.
class Mouse:
	# A single mouse button, works like a single key.
	class Button:
		def __init__(self):
			self.press = False
			self.down = False
			self.release = False

		def clear(self):
			self.press = False
			self.release = False


	def __init__(self):
		# The current position.
		self.x = 0
		self.y = 0

		# Left and right buttons.
		self.left = Mouse.Button()
		self.right = Mouse.Button()

	# Clear the bools dependant on single frames.
	def clear(self):
		self.left.clear()
		self.right.clear()

	# Simply sets the x and y based on a tuple (x, y).
	def setPosition(self, pos):
		self.x, self.y = pos

	# Given an integer, returns a reference to a member button.
	def getButton(self, button):
		if button == 1:
			return self.left
		else:
			return self.right

	# Locates the button from the integer and changes it accordingly.
	def setButtonDown(self, button):
		buttonObject = self.getButton(button)
		buttonObject.press = True
		buttonObject.down = True

	def setButtonUp(self, button):
		buttonObject = self.getButton(button)
		buttonObject.release = True
		buttonObject.down = False



class EventHandler:
	def __init__(self):
		self.quit = False

		self.keys = KeyLists(len(pygame.key.get_pressed()))

		self.mouse = Mouse()

	def update(self):
		self.quit = False

		self.keys.clear()

		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit = True
				break;

			elif event.type == KEYDOWN:
				self.keys.setKeyDown(event.key)
			elif event.type == KEYUP:
				self.keys.setKeyUp(event.key)

			elif event.type == MOUSEMOTION:
				self.mouse.setPosition(event.pos)
			elif event.type == MOUSEBUTTONDOWN:
				self.mouse.setButtonDown(event.button)
			elif event.type == MOUSEBUTTONUP:
				self.mouse.setButtonUp(event.button)

