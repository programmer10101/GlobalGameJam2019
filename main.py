import constants
import math
import pygame
from pygame.locals import *
from graphics import Graphics
from world import World

bg_image = 'images/path01.png'
ENEMY_IMG = 'images/enemy03.png'
SOUND01 = 'sounds/explosion01.wav'
SOUND02 = 'sounds/explosion02.wav'



class App:
    def __init__(self):
        self.running = True
        self.screen = None
        pygame.init()
        self.world = World()
        self.graphics = Graphics(self.world)

    def on_init(self):
        # pygame.init()
        self.running = True
        # self.bg = pygame.image.load(bg_image).convert()
        # self.bg = pygame.transform.scale(self.bg, self.size)
        pygame.mixer.init()
        self.explosion1 = pygame.mixer.Sound(SOUND01)
        self.explosion2 = pygame.mixer.Sound(SOUND02)
        # self.enemy = pygame.image.load(ENEMY_IMG).convert_alpha()
        # self.enemy = pygame.transform.scale(self.enemy, (64,64))
        self.clock = pygame.time.Clock()
        return self.running

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            if event.button == 1:
                self.explosion1.play()
            else:
                self.explosion2.play()
    def on_loop(self, timedelta_millis):
        self.world.move_enemies(timedelta_millis)
        # self.world.print_enemies()
    def on_render(self, timedelta_millis):
        BLUE = (0,0,255)
        YELLOW = (255,255,2)
        WHITE = (255,255,255)
        # self.screen.blit(self.bg, (0,0))
        # pygame.draw.rect(self.screen, (200,33,33), (5,20,500,500))
        # pygame.gfxdraw.pie(self.screen, 600,300,300,0,-40,BLUE)
        # pygame.draw.ellipse(self.screen, YELLOW, (800,300,300,300))
        # pygame.draw.arc(self.screen, (255,0,0),(800,300,200,200),0,2)
        # draw_sector(self.screen, 444, 444, 245, BLUE, -90, 144)
        # self.screen.blit(self.enemy, (500,400))
        self.graphics.draw_background()
        self.graphics.draw_enemy_timeline(570, 5, 700, 45)
        # self.graphics.draw_path(self.world.get_path(0))
        self.graphics.draw_enemies()
        self.graphics.draw_text(str(self.clock.tick()), 60,30)
        self.graphics.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while( self.running ):
            timedelta_millis = self.clock.tick(constants.FRAMES_PER_SEC)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(timedelta_millis)
            self.on_render(timedelta_millis)
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
