import pygame
from game import Game


class DialogueBox:
    def __init__(self, game, messages, speed=3):
        self.game = game
        self.messages = messages
        self.active_message = 0
        self.message = self.messages[self.active_message]
        self.speed = speed
        self.counter = 0
        self.done = False

        self.font = pygame.font.Font(self.game.font_name, 27)

        self.dialogue_box = pygame.Rect(280, 430, 400, 70)
        self.back_rect = pygame.Rect(275, 425, 410, 80)
        self.back_rect_color = (200, 200, 200)

    def advance(self):
        if self.done and self.active_message < len(self.messages) - 1:
            self.active_message += 1
            self.message = self.messages[self.active_message]
            self.counter = 0
            self.done = False

    def is_finished(self):
        return self.done and self.active_message == len(self.messages) - 1

    def update(self):
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True

    def draw(self):
        pygame.draw.rect(self.game.window, self.back_rect_color, self.back_rect)
        pygame.draw.rect(self.game.window, self.game.Black, self.dialogue_box)
        snip = self.font.render(self.message[0:self.counter // self.speed], True, 'white')
        self.game.window.blit(snip, (290, 440))


class EyeClose(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for num in range(1,28):
            img = pygame.image.load(f'assets/eyeclose/eyeclose{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1

        if self.current_sprite >= 27:
            self.kill()
            return

        self.image = self.sprites[int(self.current_sprite)]


eye_close_sprites = pygame.sprite.Group()
eye_close = EyeClose(0, 0)
eye_close_sprites.add(eye_close)

class Start:
    def __init__(self, game, display, game_state_manager):
        self.game = game
        self.display = display
        self.game_state_manager = game_state_manager

    def run(self):
        self.display = pygame.image.load("../assets/console.png")
        eye_close_sprites.draw(self.game.display)
        eye_close_sprites.update()





class EyeClose(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for num in range(1, 28):
            img = pygame.image.load(f'assets/eyeclose/eyeclose{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1

        if self.current_sprite >= 27:
            self.kill()
            return

        self.image = self.sprites[int(self.current_sprite)]


eye_close_sprites = pygame.sprite.Group()
eye_close = EyeClose(0, 0)
eye_close_sprites.add(eye_close)


class Start:
    def __init__(self, display, game_state_manager):
        self.game = Game()
        self.display = display
        self.game_state_manager = game_state_manager

    def run(self):
        self.display = pygame.image.load("../assets/console.png")
        eye_close_sprites.draw(self.game.display)
        eye_close_sprites.update()


class Choice:
    def __init__(self, display, game_state_manager):
        self.game = Game()
        self.display = display
        pass


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state



