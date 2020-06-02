import pygame
from pygame.locals import *
import pygame.mixer
import sys
import os

SCREEN_SIZE = (960, 720) # Tamaño de la pantalla
screen = pygame.display.set_mode(SCREEN_SIZE)
global HORIZ_MOV_INCR
HORIZ_MOV_INCR = 10 # Velocidad de movimiento
global FPS
global clock
global time_spent

# Title & Icon
pygame.display.set_caption('Bookmark Adventures - Medieval')
icon = pygame.image.load('images/Page.png')
pygame.display.set_icon(icon)

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

# Clase para tener la pantalla en el centro del jugador
class Camera(object):
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    def update(self):
      if self.player.centerx > self.rect.centerx + 100:
          self.rect.centerx = self.player.centerx - 100
      if self.player.centerx < self.rect.centerx - 100:
          self.rect.centerx = self.player.centerx + 100
      if self.player.centery > self.rect.centery + 100:
          self.rect.centery = self.player.centery - 100
      if self.player.centery < self.rect.centery - 100:
          self.rect.centery = self.player.centery + 100
      self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))

# Clase para crear los obstáculos
class BlockMedieval(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/BlockMedieval.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class FireBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Fire.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class PageBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Page.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class PotionBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Potion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class FruitBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/MagicFruit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class WinBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Portal.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

# Clase para el jugador y sus colisiones
class Tom(pygame.sprite.Sprite):    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contact = False
        self.jump = False
        self.image = pygame.image.load('images/Right00.png').convert()
        self.rect = self.image.get_rect()
        self.run_left = ["images/Left00.png","images/Left01.png",
                         "images/Left02.png", "images/Left03.png",
                         "images/Left00.png", "images/Left01.png",
                         "images/Left02.png", "images/Left03.png"]
        self.run_right = ["images/Right00.png","images/Right01.png",
                         "images/Right02.png", "images/Right03.png",
                         "images/Right00.png","images/Right01.png",
                         "images/Right02.png", "images/Right03.png"]
        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0
        self.score = 0
        self.health = 100
        self.countPages = 0
        self.salida = False

    def update(self, up, down, left, right):
        if up:
            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load("images/Right03.png")
                self.jump = True
                self.movy -= 20
        if down:
            if self.contact and self.direction == "right":
                self.image = pygame.image.load('images/Right00.png').convert_alpha()
            if self.contact and self.direction == "left":
                self.image = pygame.image.load('images/Left00.png').convert_alpha()

        if not down and self.direction == "right":
                self.image = pygame.image.load('images/Right00.png').convert_alpha()

        if not down and self.direction == "left":
            self.image = pygame.image.load('images/Left00.png').convert_alpha()

        if left:
            self.direction = "left"
            self.movx = -HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_left[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("images/Left03.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_right[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("images/Right03.png").convert_alpha()

        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)


        if not self.contact:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.jump:
            self.movy += 2
            self.rect.top += self.movy
            if self.contact == True:
                self.jump = False

        self.contact = False
        self.collide(0, self.movy, world)

    # Colisiones
    def collide(self, movx, movy, world):
        self.contact = False        
        pygame.mixer.init()
        # Sonido de auch
        auch_sound = pygame.mixer.Sound('music/auch.ogg')  
        # Sonido de Lose
        lose_sound = pygame.mixer.Sound("music/lose.ogg")
        # Sonido de Win
        win_sound = pygame.mixer.Sound("music/win.ogg")
        # Sonido de beber poción
        drink_sound = pygame.mixer.Sound("music/drink.ogg")
        # Sonido de eat
        eat_sound = pygame.mixer.Sound("music/eat.ogg")
        # Sonido de agarrar page 
        page_sound = pygame.mixer.Sound("music/page.ogg")
        
        for o in world:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
        for i in badBlocksList:
            if self.rect.colliderect(i):
                self.score += 1        
                self.health -= 1    
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/auch.ogg'))
            if self.health == 0:
                pygame.mixer.music.set_volume(0)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/lose.ogg'))
                Tom.Lose()

        for j in pageBlocksList:
            if self.rect.colliderect(j):
                self.score += 40        
                self.countPages += 1  
                pageBlocksList.remove(j)
                pygame.mixer.Sound.play(page_sound)

            if self.countPages == 4:
                self.salida = True

        for l in potionBlocksList:
            if self.rect.colliderect(l):
                self.score += 10  
                self.health += 50
                if self.health > 100:
                    self.health = 100        
                pygame.mixer.Sound.play(drink_sound)
                potionBlocksList.remove(l)

        for m in fruitBlocksList:
            if self.rect.colliderect(m):
                self.score += 20 
                self.health += 25
                if self.health > 100:
                    self.health = 100     
                pygame.mixer.Sound.play(eat_sound)   
                fruitBlocksList.remove(m)

        for k in winBlocksList:
            if self.rect.colliderect(k) and self.salida == True:
                pygame.mixer.Sound.play(win_sound)
                mainClock = pygame.time.Clock()
                backgroundWin = pygame.image.load("images/You win.png")
                backgroundWin_rect = backgroundWin.get_rect()

                pygame.mixer.music.set_volume(0)
                win_sound.play()

                click = False
                while True:
                    pygame.mouse.set_visible(1)
                    screen.blit(backgroundWin, (0, 0))
            
                    mx, my = pygame.mouse.get_pos()

                    font = pygame.font.Font(None, 60)
                    scoreText = font.render("Final Score: " + str(self.score), 1, (0, 0, 0))
                    screen.blit(scoreText, (345, 640))

                    button_1 = pygame.Rect(755, 630, 130, 65)
                    
                    if button_1.collidepoint((mx, my)):
                        if click:
                            pygame.quit()
                            os.system("python level2.py")
                    
                    pygame.draw.rect(screen, [179, 179, 179], button_1, 1)
                    
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

                               

        font = pygame.font.Font(None, 36)
        scoreText = font.render("Score: " + str(self.score), 1, (255, 255, 255))
        healthText = font.render("Health: " + str(self.health) + "/100", 1, (255, 255, 255))

        if self.health < 20:
            healthText = font.render("Health: " + str(self.health) + "/100", 1, (255, 0, 0))

        pagesText = font.render("Pages: " + str(self.countPages) + "/4", 1, (255, 255, 255))
        screen.blit(scoreText, (5, 10))
        screen.blit(healthText, (5, 50))
        screen.blit(pagesText, (5, 90))

    # Función al perder el juego
    def Lose():    	

    	mainClock = pygame.time.Clock()
    	backgroundLose = pygame.image.load("images/You lose.png")
    	backgroundLose_rect = backgroundLose.get_rect()

    	click = False
    	while True:
    		pygame.mouse.set_visible(1)
    		screen.blit(backgroundLose, (0, 0))
    		
    		mx, my = pygame.mouse.get_pos()

    		button_1 = pygame.Rect(395, 620, 200, 80)
    		
    		if button_1.collidepoint((mx, my)):
    			if click:
    				pygame.quit()
    				os.system("python level1.py")
    		
    		pygame.draw.rect(screen, [129, 24, 8], button_1, 1)
    		
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

# Lee el mapa del nivel y crea el nivel
class Level(object):
    def __init__(self, open_level):
        self.level1 = []
        self.world = []
        self.badBlocks = []
        self.pageBlocks = []
        self.potionBlocks = []
        self.fruitBlocks = []
        self.winBlocks = []
        self.badBlocksList = pygame.sprite.Group()        
        self.pageBlocksList = pygame.sprite.Group()
        self.potionBlocksList = pygame.sprite.Group()
        self.fruitBlocksList = pygame.sprite.Group()
        self.winBlocksList = pygame.sprite.Group()

        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                # Donde Tom aparece por primera vez
                if col == "P":
                    tom = self.tom = Tom(x,y)
                    self.all_sprite.add(tom)   
                # Medieval Block Obstacle
                if col == "X":
                    blockMedieval = BlockMedieval(x, y)
                    self.world.append(blockMedieval)
                    self.all_sprite.add(self.world)                                                  
                # Fire Block Obstacle
                if col == "F":
                    fireBlock = FireBlock(x, y)
                    self.badBlocks.append(fireBlock)
                    self.badBlocksList.add(self.badBlocks)
                # Pages
                if col == "H":
                    pageBlock = PageBlock(x, y)
                    self.pageBlocks.append(pageBlock)
                    self.pageBlocksList.add(self.pageBlocks)
                # Win Block
                if col == "W":
                    winBlock = WinBlock(x, y)
                    self.winBlocks.append(winBlock)
                    self.winBlocksList.add(self.winBlocks)
                # Potion Block
                if col == "L":
                    potionBlock = PotionBlock(x, y)
                    self.potionBlocks.append(potionBlock)
                    self.potionBlocksList.add(self.potionBlocks)
                # Fruit Block
                if col == "G":
                    fruitBlock = FruitBlock(x, y)
                    self.fruitBlocks.append(fruitBlock)
                    self.fruitBlocksList.add(self.fruitBlocks)
                    
                x += 25   
            y += 25
            x = 0        

    def get_size(self):
        lines = self.level1
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)

def tps(reloj, fps):
    temp = reloj.tick(fps)
    tps = temp / 1000.
    return tps


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 32)
screen_rect = screen.get_rect()
background = pygame.image.load("images/Medieval Background.png").convert_alpha()
background_rect = background.get_rect()
level = Level("level/level1")
level.create_level(0, 0)
world = level.world
badBlocks = level.badBlocks
potionBlocks = level.potionBlocks
fruitBlocks = level.fruitBlocks
winBlocks = level.winBlocks

tom = level.tom
pygame.mouse.set_visible(0)

camera = Camera(screen, tom.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite
badBlocksList = level.badBlocksList
pageBlocksList = level.pageBlocksList
potionBlocksList = level.potionBlocksList
fruitBlocksList = level.fruitBlocksList
winBlocksList = level.winBlocksList

FPS = 90
clock = pygame.time.Clock()


# Comienzo del nivel
def startLevel1():
    up = down = left = right = False
    x, y = 0, 0
    frame_count = 0
    frame_rate = 90
    start_time = 180

    # Música del nivel 
    pygame.mixer.music.load("music/medieval.ogg")  
    pygame.mixer.music.play(-1)
    # Sonido de salto
    jump_sound = pygame.mixer.Sound("music/jump.ogg")
    # Sonido de Perder
    lose_sound = pygame.mixer.Sound("music/lose.ogg")

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                up = True
            if event.type == KEYDOWN and event.key == K_DOWN:
                down = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_SPACE:
                up = False
            if event.type == KEYUP and event.key == K_DOWN:
                down = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False

            if up == True:
                pygame.mixer.Sound.play(jump_sound)

        asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
        bg = pygame.Surface(asize)

        for x in range(0, asize[0], background_rect.w):
            for y in range(0, asize[1], background_rect.h):
                screen.blit(background, (x, y))        

        font = pygame.font.Font(None, 36)
        
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
            pygame.mixer.music.set_volume(0)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/lose.ogg'))
            Tom.Lose()

        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time left: {0:01}:{1:01}".format(minutes, seconds)
        text = font.render(output_string, 1, (255, 255, 255))
        screen.blit(text, [780, 10])
        frame_count += 5
        clock.tick(frame_rate)

        time_spent = tps(clock, FPS)
        camera.draw_sprites(screen, all_sprite)
        camera.draw_sprites(screen, badBlocksList)
        camera.draw_sprites(screen, pageBlocksList)
        camera.draw_sprites(screen, potionBlocksList)
        camera.draw_sprites(screen, fruitBlocksList)
        camera.draw_sprites(screen, winBlocksList)

        tom.update(up, down, left, right)
        camera.update()
        pygame.display.flip()


startLevel1()
