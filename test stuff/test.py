import pygame
import sys

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager("start")
        self.start = Start(self.screen, self.game_state_manager)
        self.level = Level(self.screen, self.game_state_manager)

        self.states = {"start": self.start, "level": self.level}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.game_state_manager.set_state("level")

            self.states[self.game_state_manager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)


class Level:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager

    def run(self):
        self.display.fill("black")


class Start:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager

    def run(self):
        self.display.fill("red")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.game_state_manager.set_state("level")


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state

if __name__ == "__main__":
    game = Game()
    game.run()
