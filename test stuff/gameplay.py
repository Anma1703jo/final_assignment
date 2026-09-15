import pygame
from sys import exit

from scenes import *

pygame.init()

#basic variables
screen = pygame.display.set_mode((960, 540))
pygame.display.set_caption('Every time you ask')
clock = pygame.time.Clock()

BACKGROUND = pygame.image.load('../assets/console.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (960, 540))

milkyway = pygame.image.load('../assets/milkyway/milkyway9.png')
milkyway = pygame.transform.scale(milkyway, (860, 440))

zabka = pygame.image.load("../assets/zabka.png")
zabka = pygame.transform.scale(zabka, (960, 540))


#cat
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

moving_cat_sprites = pygame.sprite.Group()
cat = Cat(0, 0)
moving_cat_sprites.add(cat)

#eye close
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

#dialogue box
text_rect = pygame.Rect(280, 430, 400, 40)
color = (0,0,0)
back_rect = pygame.Rect(275, 425, 410, 50)
color_back = (200,200,200)

#font and text stuff
font = pygame.font.Font('../assets/Pixeltype.ttf', 27)
start_messages = scene_1["joystick"]

snip = font.render('', True, 'white')
counter = 0
speed = 3
active_message = 0
message = start_messages[active_message]
done = False


run = True
while run:
    screen.blit(milkyway, (0, 0))
    screen.blit(BACKGROUND, (0, 0))
    clock.tick(60)
    pygame.draw.rect(screen, color_back, back_rect)
    pygame.draw.rect(screen, color, text_rect)



  #  moving_cat_sprites.draw(screen)
 #   moving_cat_sprites.update()

  #  eye_close_sprites.draw(screen)
 #   eye_close_sprites.update()

    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):
        done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and done and active_message < len(start_messages) - 1:
                active_message += 1
                done = False
                message = start_messages[active_message]
                counter = 0

  #  snip = font.render(message[0:counter//speed], True, 'white')
 #   screen.blit(snip, (290, 440))


    pygame.display.flip()

