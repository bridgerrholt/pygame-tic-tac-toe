import pygame
from pygame.locals import *

import time
import random

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

		self.font = pygame.font.SysFont("arial", 200)
		self.winFont = pygame.font.SysFont("arial", 100)

		self.screen = 0
		self.over = False
		self.winner = 0

		self.computerPause = 0



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
		if self.screen == 0:
			mouseX, mouseY = self.eventHandler.mouse.x, self.eventHandler.mouse.y

			played = False

			if self.playerTurn == 1:
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
						played = True

			elif time.time() > self.computerPause:
				self.computerTurn()
				played = True


			if played:
				print self.squares
				print self.playerTurn
				self.checkWin()
				if self.over:
					self.screen = 1
					print "ay"

				if self.playerTurn == 1:
					self.playerTurn = 2
					self.computerPause = time.time() + 1
				else:
					self.playerTurn = 1
		else:
			if self.eventHandler.mouse.left.release:
				if self.screen == 1:
					self.over = False
					self.squareHover = (False, (0, 0))
					self.playerTurn = self.playerFirst
					for i in range(len(self.squares)):
						for j in range(len(self.squares[i])):
							self.squares[i][j] = 0
					self.screen = 2
				else:
					self.winner = 0
					self.screen = 0

	def computerTurn(self):
		emptySlots = []
		for i in range(len(self.squares)):
			for j in range(len(self.squares[i])):
				if self.squares[i][j] == 0:
					emptySlots.append((i, j))

		# Counts player markers.
		counts = [
			[0, 0, 0],  # rows
			[0, 0, 0]   # columns
		]
		for i in range(len(self.squares)):
			for j in range(len(self.squares[i])):
				if self.squares[i][j] == 1:
					counts[0][i] += 1
					counts[1][j] += 1

		played = False
		for i in range(len(counts)):
			for j in range(len(counts[i])):
				if counts[i][j] == 2:
					if i == 0:
						for k in range(len(self.squares[j])):
							if self.squares[j][k] == 0:
								self.squares[j][k] = self.playerTurn
								played = True
								break

				if played: break
			if played: break




		print counts


		index = random.randrange(len(emptySlots))
		self.squares[emptySlots[index][0]][emptySlots[index][1]] = self.playerTurn

	def checkWin(self):
		emptyCount = 0
		for i in range(len(self.squares)):
			for j in range(len(self.squares[i])):
				if self.squares[i][j] == 0:
					emptyCount += 1

		for i in range(1, 3):
			for j in range(0, 3):
				if self.squares[j][0] == i and self.squares[j][1] == i and self.squares[j][2] == i:
					self.over = True
					self.winner = i
					break
				elif self.squares[0][j] == i and self.squares[1][j] == i and self.squares[2][j] == i:
					self.over = True
					self.winner = i
					break

			if self.over:
				break

			if (self.squares[0][0] == i and self.squares[1][1] == i and self.squares[2][2] == i) or \
			   (self.squares[2][0] == i and self.squares[1][1] == i and self.squares[0][2] == i):
				self.over = True
				self.winner = i
				break

		if not self.over and emptyCount == 0:
			self.winner = 0
			self.over = True
			return


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
					self.drawMarker(square, (rect.x, rect.y))

				x += 1

			y += 1
			x  = 0

	def drawMarker(self, square, pos):
		if square == self.playerFirst:
			toBlit = self.font.render("O", True, self.lineColor)
		else:
			toBlit = self.font.render("X", True, self.lineColor)
		pos = (
			pos[0] + self.squareSideLength/2.0 - toBlit.get_width()/2.0,
			pos[1] + self.squareSideLength/2.0 - toBlit.get_height()/2.0)
		self.mainSurface.blit(toBlit, pos)



	def draw(self):
		pygame.draw.rect(self.mainSurface, self.backColor,
			(self.x, self.y, self.fullLength, self.fullLength))

		if self.screen != 2:
			self.drawSquares()

			if self.screen == 1:
				lineColor = Color(150, 0, 0)
			else:
				lineColor = self.lineColor

			# Horizontal lines.
			pygame.draw.line(self.mainSurface, lineColor,
				(self.x,                   self.linePositions[1][0]),
				(self.linePositions[0][2], self.linePositions[1][0]), self.lineThickness)

			pygame.draw.line(self.mainSurface, lineColor,
				(self.x,                   self.linePositions[1][1]),
				(self.linePositions[0][2], self.linePositions[1][1]), self.lineThickness)

			# Vertical lines.
			pygame.draw.line(self.mainSurface, lineColor,
				(self.linePositions[0][0], self.y),
				(self.linePositions[0][0], self.linePositions[1][2]), self.lineThickness)

			pygame.draw.line(self.mainSurface, lineColor,
				(self.linePositions[0][1], self.y),
				(self.linePositions[0][1], self.linePositions[1][2]), self.lineThickness)

		else:
			if self.winner == 0:
				text = "CAT!"
			elif self.winner == 1:
				text = "Player wins!"
			elif self.winner == 2:
				text = "Computer wins!"

			toBlit = self.winFont.render(text, True, self.lineColor)
			self.mainSurface.blit(toBlit, (
				self.mainSurface.get_width()/2.0 - toBlit.get_width()/2.0,
				100))




