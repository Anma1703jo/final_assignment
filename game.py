import pygame
import sys
from flow import MainMenu

#game speed
FPS = 60

#core game class - manages the game loop, input handling etc.
#all scenes and menus receive a reference of this object
class Game:
    def __init__(self):
        pygame.init()

        #game state flags
        self.running, self.playing = True, False

        #input flags
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

        #display setup and window
        self.DISPLAY_W, self.DISPLAY_H = 960, 540 
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption('Every time you ask')

        #font and colors used
        self.font_name = 'assets/Pixeltype.ttf'
        self.Black, self.White = (0, 0, 0), (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.curr_menu = MainMenu(self)

        #the Robo-John Corruption Counter
        #tracks how many times the player sided with the cat
        self.cat_interactions = 0

#basic game loop
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(FPS)
            self.reset_keys()

#processes pygame events and sets input flags
    def check_events(self, events=None):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.LEFT_KEY = False
        self.RIGHT_KEY = False

#text for game
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.White)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

