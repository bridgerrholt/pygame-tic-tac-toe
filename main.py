import sys
import time

import pygame
from pygame.locals import *

from initialize import *
from event_handler import EventHandler
from frame_rate_handler import *

def main():
	initialize()
	eventHandler = EventHandler()
	frameRateHandler = FrameRateHandler(60)

	backColor = Color(0, 0, 0)
	mainSurface = pygame.display.set_mode((720, 720))



	while True:
		frameRateHandler.updateStart()
		eventHandler.update()

		if eventHandler.quit or eventHandler.keys.release[K_ESCAPE]:
			break


		mainSurface.fill(backColor)

		pygame.display.flip()

		frameRateHandler.updateEnd()


if __name__ == "__main__":
	main()