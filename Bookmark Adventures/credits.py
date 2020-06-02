import pygame
import sys
from pygame.locals import *
import os

mainClock = pygame.time.Clock()
pygame.init()

# Title & Icon
pygame.display.set_caption('Bookmark Adventures - Credits')
icon = pygame.image.load('images/Page.png')
pygame.display.set_icon(icon)

# Screen Size
SCREEN_SIZE = (960, 720)
screen = pygame.display.set_mode(SCREEN_SIZE)


def Credits():
    mainClock = pygame.time.Clock()
    # Complete
    backgroundComplete = pygame.image.load("images/Complete.png")
    backgroundComplete_rect = backgroundComplete.get_rect()

    # Sonido de Win
    finalWin_sound = pygame.mixer.Sound("music/beginningconFinalWin.ogg")
    finalWin_sound.play()

    click = False
    while True:
        pygame.mouse.set_visible(1)
        screen.blit(backgroundComplete, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(755, 635, 130, 55)

        if button_1.collidepoint((mx, my)):
            if click:
                Thanks()

        pygame.draw.rect(screen, [255, 139, 26], button_1, 1)

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

def Thanks():
    mainClock = pygame.time.Clock()
    # Thanks
    backgroundThanks = pygame.image.load("images/Thanks.png")
    backgroundThanks_rect = backgroundThanks.get_rect()

    # Sonido de Thanks
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/creditosamplificado.ogg'), loops = -1)
    pygame.mixer.music.set_volume(5)

    click = False
    while True:
        pygame.mouse.set_visible(1)
        screen.blit(backgroundThanks, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Botones
        button_1 = pygame.Rect(140, 560, 220, 80)
        button_2 = pygame.Rect(570, 550, 250, 70)

        if button_1.collidepoint((mx, my)):
        	if click:
        		pygame.quit()
        		os.system("python main.py")
        if button_2.collidepoint((mx, my)):
        	if click:
        		pygame.quit()
        		sys.exit()

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


Credits()
