import pygame
import sys
from pygame.locals import *
import os

mainClock = pygame.time.Clock()
pygame.init()

# Title & Icon
pygame.display.set_caption('Bookmark Adventures - Menu')
icon = pygame.image.load('images/Page.png')
pygame.display.set_icon(icon)

# Screen Size
SCREEN_SIZE = (960, 720)
screen = pygame.display.set_mode(SCREEN_SIZE)

# Background Images
# Main Menu
backgroundMainMenu = pygame.image.load("images/Main Menu.png")
backgroundMainMenu_rect = backgroundMainMenu.get_rect()
# Instructions
backgroundInstructions = pygame.image.load("images/Instructions.png")
backgroundInstructions_rect = backgroundInstructions.get_rect()
# Part 1
backgroundPart1 = pygame.image.load("images/Part 1.png")
backgroundPart1_rect = backgroundPart1.get_rect()
# Falling
backgroundFalling = pygame.image.load("images/Part 2.png")
backgroundFalling_rect = backgroundFalling.get_rect()
# Teletransportation
backgroundTeletransportation = pygame.image.load("images/Teletransportation.png")
backgroundTeletransportation_rect = backgroundTeletransportation.get_rect()

pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/menu.ogg'), loops = -1)

# font = pygame.font.SysFont(None, 20)

def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

# Main Menu
def mainMenu():
	click = False
	while True:
		pygame.mouse.set_visible(1)
		screen.blit(backgroundMainMenu, (0, 0))
		
		# Posición Mouse
		mx, my = pygame.mouse.get_pos()

		# Botones
		button_1 = pygame.Rect(140, 560, 180, 80)
		button_2 = pygame.Rect(570, 550, 250, 70)

		if button_1.collidepoint((mx, my)):
			if click:
				Part1()
		if button_2.collidepoint((mx, my)):
			if click:
				instructions()

		pygame.draw.rect(screen, [120, 95, 58], button_1, 1)
		pygame.draw.rect(screen, [120, 95, 58], button_2, 1)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)

# Instrucciones
def instructions():
	click = False
	while True:
		pygame.mouse.set_visible(1)
		screen.blit(backgroundInstructions, (0, 0))
		
		# Posición Mouse
		mx, my = pygame.mouse.get_pos()

		# Botones
		button_1 = pygame.Rect(140, 560, 180, 80)
		button_2 = pygame.Rect(600, 550, 250, 80)

		if button_1.collidepoint((mx, my)):
			if click:
				mainMenu()
		if button_2.collidepoint((mx, my)):
			if click:
				Part1()

		pygame.draw.rect(screen, [120, 95, 58], button_1, 1)
		pygame.draw.rect(screen, [120, 95, 58], button_2, 1)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)

# Parte 1
def Part1():
	pygame.mixer.Channel(0).stop()
	pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/beginning.ogg'), loops = -1)
	click = False
	while True:
		pygame.mouse.set_visible(1)
		screen.blit(backgroundPart1, (0, 0))
		
		# Posición Mouse
		mx, my = pygame.mouse.get_pos()

		# Boton
		button_1 = pygame.Rect(755, 635, 130, 55)
		
		if button_1.collidepoint((mx, my)):
			if click:
				Falling()		

		pygame.draw.rect(screen, [237, 127, 18], button_1, 1)
		
		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)

# Falling
def Falling():
	pygame.mixer.Channel(1).stop()
	pygame.mixer.Channel(2).play(pygame.mixer.Sound('music/beginningconFalling.ogg'), loops = -1)
	click = False
	while True:
		pygame.mouse.set_visible(1)
		screen.blit(backgroundFalling, (0, 0))
		
		# Posición Mouse
		mx, my = pygame.mouse.get_pos()

		# Boton
		button_1 = pygame.Rect(755, 635, 130, 55)
		
		if button_1.collidepoint((mx, my)):
			if click:
				Teletransportation()		

		pygame.draw.rect(screen, [234, 127, 24], button_1, 1)
		
		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)

# Teletransportation
def Teletransportation():
	pygame.mixer.Channel(2).stop()
	pygame.mixer.Channel(3).play(pygame.mixer.Sound('music/beginningconTeleport.ogg'), loops = -1)
	click = False
	while True:
		pygame.mouse.set_visible(1)
		screen.blit(backgroundTeletransportation, (0, 0))
		
		# Posición Mouse
		mx, my = pygame.mouse.get_pos()

		# Boton
		button_1 = pygame.Rect(755, 635, 130, 55)
		
		if button_1.collidepoint((mx, my)):
			if click:
				pygame.quit()
				os.system("python level1.py")

		pygame.draw.rect(screen, [206, 112, 22], button_1, 1)
		
		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)


mainMenu()
