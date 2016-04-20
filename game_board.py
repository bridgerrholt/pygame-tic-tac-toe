import pygame
from pygame.locals import *

class GameBoard(object):
	def __init__(self, x, y, eventHandler, mainSurface):
		self.x, self.y = x, y
		self.eventHandler = eventHandler
		self.mainSurface = mainSurface

		self.backColor  = Color(255, 255, 255)
		self.hoverColor = Color(200, 200, 200)
		self.lineColor  = Color(  0,   0,   0)
		self.lineThickness = 3

		# List of squares, left to right, up to down.
		# 0: empty
		# 1: player 1
		# 2: player 2
		self.squares = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]


		self.setPoints()

		# (True if hovering over a square,
		#  index of said square)
		self.squareHover = (False, (0, 0))

		self.playerFirst = 1
		self.playerTurn = self.playerFirst

		self.font = pygame.font.SysFont("arial", 30)



	def setPoints(self):
		self.fullLength = min(self.mainSurface.get_width(), self.mainSurface.get_height())
		self.squareSideLength = self.fullLength / 3.0

		self.linePositions = [
			# Horizontal lines.
			[self.x + self.squareSideLength,
			 self.x + self.squareSideLength*2,
			 self.x + self.squareSideLength*3],

			# Vertical lines.
			[self.y + self.squareSideLength,
			 self.y + self.squareSideLength*2,
			 self.y + self.squareSideLength*3]
		]



	def update(self):
		mouseX, mouseY = self.eventHandler.mouse.x, self.eventHandler.mouse.y

		if (mouseX >= self.x and mouseX <= self.linePositions[0][2]) or \
		   (mouseY >= self.y and mouseY <= self.linePositions[1][2]):
			tileX, tileY = 0, 0

			if mouseY < self.linePositions[1][0]:
				tileY = 0
			elif mouseY < self.linePositions[1][1]:
				tileY = 1
			else:
				tileY = 2

			if mouseX < self.linePositions[0][0]:
				tileX = 0
			elif mouseX < self.linePositions[0][1]:
				tileX = 1
			else:
				tileX = 2

			self.squareHover = (True, (tileY, tileX))

		else:
			self.squareHover = (False, (0, 0))

		if self.squareHover[0] and self.eventHandler.mouse.left.release:
			if self.squares[self.squareHover[1][0]][self.squareHover[1][1]] == 0:
				self.squares[self.squareHover[1][0]][self.squareHover[1][1]] = self.playerTurn

				if self.playerTurn == 1:
					self.playerTurn = 2
				else:
					self.playerTurn = 1



	def drawSquares(self):
		x, y = 0, 0
		while y < 3:
			while x < 3:
				square = self.squares[y][x]
				if self.squareHover[0] and self.squareHover[1] == (y, x) and square == 0:
					color = self.hoverColor
				else:
					color = self.backColor

				rect = Rect(
					self.x + self.squareSideLength*x,
					self.y + self.squareSideLength*y,
					self.squareSideLength,
					self.squareSideLength
				)

				pygame.draw.rect(self.mainSurface, color, rect)

				if square != 0:
					if square == self.playerFirst:
						toBlit = self.font.render("O", True, self.lineColor)
					else:
						toBlit = self.font.render("X", True, self.lineColor)
					self.mainSurface.blit(toBlit, rect)

				x += 1

			y += 1
			x  = 0



	def draw(self):
		pygame.draw.rect(self.mainSurface, self.backColor,
			(self.x, self.y, self.fullLength, self.fullLength))

		self.drawSquares()

		# Horizontal lines.
		pygame.draw.line(self.mainSurface, self.lineColor,
			(self.x,                   self.linePositions[1][0]),
			(self.linePositions[0][2], self.linePositions[1][0]), self.lineThickness)

		pygame.draw.line(self.mainSurface, self.lineColor,
			(self.x,                   self.linePositions[1][1]),
			(self.linePositions[0][2], self.linePositions[1][1]), self.lineThickness)

		# Vertical lines.
		pygame.draw.line(self.mainSurface, self.lineColor,
			(self.linePositions[0][0], self.y),
			(self.linePositions[0][0], self.linePositions[1][2]), self.lineThickness)

		pygame.draw.line(self.mainSurface, self.lineColor,
			(self.linePositions[0][1], self.y),
			(self.linePositions[0][1], self.linePositions[1][2]), self.lineThickness)




