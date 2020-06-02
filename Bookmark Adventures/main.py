import pygame
import time
from menu import mainMenu
from pygame.locals import *
import sys

SCREEN_SIZE = (960, 720)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Bookmark Adventures')
icon = pygame.image.load('images/Page.png')
pygame.display.set_icon(icon)

mainMenu()

pygame.display.flip()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False