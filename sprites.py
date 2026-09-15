import pygame

#here we have all the sprites / animations

class Cat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for num in range(1,9):
            img = pygame.image.load(f'assets/cat/cat_pic{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

class CatSmall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for num in range(1,9):
            img = pygame.image.load(f'assets/smallcat/smallcat{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

class BathCat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for num in range(1,9):
            img = pygame.image.load(f'assets/bathcat/bathcat{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

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
        self.current_sprite += 0.05

        if self.current_sprite >= 27:
            self.kill()
            return
        self.image = self.sprites[int(self.current_sprite)]

class Milkyway(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for num in range(1,10):
            img = pygame.image.load(f'assets/milkyway/milkyway{num}.png')
            img = pygame.transform.scale(img, (860, 440))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.05

        if self.current_sprite >= 9:
            self.kill()
            return
        self.image = self.sprites[int(self.current_sprite)]

class RoboWave(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for num in range(1,10):
            img = pygame.image.load(f'assets/robo/robovoice{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

class WarpSpeed(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for num in range(1,7):
            img = pygame.image.load(f'assets/warp/warp{num}.png')
            img = pygame.transform.scale(img, (960, 540))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]