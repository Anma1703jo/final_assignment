import pygame
import random
from scenes import scene_1, scene_2, scene_3, scene_3_door
from sprites import EyeClose, Milkyway, RoboWave, Cat, CatSmall, BathCat, WarpSpeed

#Base Class for all the game scenes
#includes dialogue rendering, fade transitions, speaker animations, inout cooldown and the text corruption
class Scene:
    def __init__(self, game, image):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.image = image
        self.image = pygame.transform.scale(self.image, (960, 540))

        self.cat_visible = False
        self.robo_visible = True

        #sprites
        self.robowave_sprites = pygame.sprite.Group()
        self.robowave = RoboWave(0, 0)
        self.robowave_sprites.add(self.robowave)

        self.cat_sprites = pygame.sprite.Group()
        self.cat = Cat(0, 0)
        self.cat_sprites.add(self.cat)

        #add a fade for a nice change between images
        self.fade_alpha = 0
        self.fading = False
        self.fade_in = False
        self.next_image = False
        self.fade_done = False
        self.fade_next_state = None

#corrupts robo-john's dialogue by randomly replacing letters with special chars
#each time the player chooses an option to interact with the cat, the level goes up
    def corrupt_text(self, text, level):
        if level == 0:
            return text

        special_chars = "@#$%&*!?^~"
        result = ""
        corruption_chance = level * 0.05

        for char in text:
            if char.isalpha() and random.random() < corruption_chance:
                result += random.choice(special_chars)
            else:
                result += char

        return result

#helper method to create a special DialogueBox form for Robo-John, once the corruption levels goes up
    def robo_dialogue(self, key, scene_dict):
        messages = [self.corrupt_text(m, self.game.cat_interactions) for m in scene_dict[key]]
        return DialogueBox(self.game, messages, speaker="robo_john")

#draws the speaker animation based on current DialogueBox speaker
    def draw_speaker(self):
        if not hasattr(self, "dialogue_box") or self.dialogue_box is None:
            return
        if self.dialogue_box.speaker == "robo_john" and self.robo_visible:
            self.robowave_sprites.draw(self.game.display)
            self.robowave_sprites.update()

        if self.cat_visible:
            self.cat_sprites.draw(self.game.display)
            self.cat_sprites.update()

#menu cursor
    def draw_cursor(self):
        self.game.draw_text("*", 30, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def is_finished(self):
        pass

#the fades
    def do_fade(self, next_image=None):
        self.fading = True
        self.fade_in = False
        self.fade_alpha = 0
        self.fade_done = False
        self.next_image = next_image

    def do_fade_white(self):
        self.fading = True
        self.fade_in = False
        self.fade_alpha = 0
        self.fade_color = (255, 255, 255)
        self.state = ("fading_out")

    def draw_fade(self):
        if self.fading:
            fade_color = getattr(self, "fade_color", (0, 0, 0))
            fade_surface = pygame.Surface((960, 540))
            fade_surface.fill(fade_color)

            if not self.fade_in:
                self.fade_alpha += 8
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.fade_in = True
                    if self.next_image:
                        self.image = self.next_image

            else:
                self.fade_alpha -= 8
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fading = False
                    self.fade_done = True

            fade_surface.set_alpha(self.fade_alpha)
            self.game.display.blit(fade_surface, (0, 0))

#for fade at end of scene or end in general
    def do_fade_and_exit(self, next_image=None, next_state=None):
        self.do_fade(next_image=next_image)
        self.fade_next_state = next_state
        self.state = "fading_out"

#main menu screen
class MainMenu(Scene):
    def __init__(self, game):
        Scene.__init__(self, game, pygame.image.load('assets/milkyway.png'))
        self.state = "Start"
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.load_game_x, self.load_game_y = self.mid_w, self.mid_h + 60
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
        self.image = pygame.transform.scale(self.image, (960, 540))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.image, (0, 0))
            self.game.draw_text("Every Time You Ask", 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)
            self.game.draw_text("Start Game", 40, self.start_x, self.start_y)
            self.game.draw_text("Load Game", 40, self.load_game_x, self.load_game_y)
            self.game.draw_text("Credits", 40, self.credits_x, self.credits_y)
            self.draw_cursor()

            if self.state == "load_message" or self.state == "credits_message":
                self.dialogue_box.update()
                self.dialogue_box.draw()
                if self.game.START_KEY:
                    self.dialogue_box.advance()
                if self.dialogue_box.is_finished():
                    self.state = "Start"
                    self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.load_game_x + self.offset, self.load_game_y)
                self.state = "Load Game"
            elif self.state == "Load Game":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Load Game":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.load_game_x + self.offset, self.load_game_y)
                self.state = "Load Game"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                self.run_display = False
            elif self.state == "Load Game":
                self.dialogue_box = DialogueBox(self.game, ["Nothing to load, game's too short."])
                self.state = "load_message"
            elif self.state == "Credits":
                self.dialogue_box = DialogueBox(self.game, ["Hi there! Seems like you got lost.", "You need to go back and start the game!"])
                self.state = "credits_message"

#Handles the typewriter-style dialogue display
#had to add two different "is_finished" because every time the states switched, the dialogue didn't wait for the enter
#and quickly started the next dialogue, which made it frustrating to play / read
#so is_finished() fixes that
#but once is_finished() was implemented, it kind of broke the choice states
#so is_finished_choice() makes this nice again
class DialogueBox:
    def __init__(self, game, messages, speed=1, speaker=None):
        self.game = game
        self.messages = messages if isinstance(messages, list) else [messages]
        self.active_message = 0
        self.message = self.messages[self.active_message]
        self.speed = speed
        self.counter = 0
        self.done = False
        self.speaker = speaker

        self.font = pygame.font.Font(self.game.font_name, 27)
        self.dialogue_box = pygame.Rect(220, 430, 510, 40)
        self.back_rect = pygame.Rect(215, 425, 520, 50)
        self.back_rect_color = (200, 200, 200)

#advance to next text message
    def advance(self):
        if not self.done:
            return
        if self.active_message < len(self.messages) - 1:
            self.active_message += 1
            self.message = self.messages[self.active_message]
            self.counter = 0
            self.done = False

#prevents instant skipping when transitioning between dialogue boxes
    def is_finished(self):
        return self.done and self.active_message == len(self.messages) -1 and self.game.START_KEY

#used for states that show a ChoiceBox
    def is_finished_choice(self):
        return self.done and self.active_message == len(self.messages) - 1

#typewriter counter
    def update(self):
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True

#draws the dialogue box and the current typed text
#added different text colors depending on speaker
#probably it would have been nice to separate player thoughts (in cursive) and what he says, but well.. maybe for the next project
    def draw(self):
        pygame.draw.rect(self.game.display, self.back_rect_color, self.back_rect)
        pygame.draw.rect(self.game.display, self.game.Black, self.dialogue_box)

        if self.speaker == "cat":
            color = (200, 100, 255)
        elif self.speaker == "robo_john":
            color = (0, 255, 255)
        else:
            color = self.game.White

        snip = self.font.render(self.message[0:self.counter // self.speed], True, color)
        self.game.display.blit(snip, (230, 440))

#the boxes for the choice options
class ChoiceBox:
    def __init__(self, game, options, y_start=490, box_width=190, box_height=30, gap=20):
        self.game = game
        self.options = options
        self.selected = 0

        self.font = pygame.font.Font(self.game.font_name, 22)
        self.y_start = y_start
        self.box_width = box_width
        self.box_height = box_height
        self.gap = gap

        total_width = len(options) * box_width + (len(options) - 1) * gap
        start_x = (self.game.DISPLAY_W - total_width) / 2

        self.boxes = []
        for i in range(len(options)):
            x = start_x + i * (box_width + gap)
            self.boxes.append(pygame.Rect(x, y_start, box_width, box_height))

#moving the cursor
    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.RIGHT_KEY:
            self.selected = (self.selected + 1) % len(self.options)
        elif self.game.UP_KEY or self.game.LEFT_KEY:
            self.selected = (self.selected - 1) % len(self.options)

#returns selected option on enter press
    def get_selected(self):
        if self.game.START_KEY:
            return self.options[self.selected]
        return None

#draws the option boxes and highlights the selected one
    def draw(self):
        for i in range(len(self.options)):
            option = self.options[i]
            rect = self.boxes[i]

            is_selected = (i == self.selected)
            border_color = "yellow" if is_selected else "white"

            pygame.draw.rect(self.game.display, "orange", rect)
            pygame.draw.rect(self.game.display, border_color, rect, 3)

            text_surface = self.font.render(option, True, "white")
            text_rect = text_surface.get_rect(center=rect.center)
            self.game.display.blit(text_surface, text_rect)

#text input box for the calibration scene
class InputBox:
    def __init__(self, game):
        self.game = game
        self.input_text = ""
        self.confirmed = False
        self.font = pygame.font.Font(self.game.font_name, 27)
        self.rect = pygame.Rect(280, 490, 400, 40)

#handles the keyboard input - only digits, enter to confirm
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.confirmed = True
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            if event.unicode.isdigit():
                self.input_text += event.unicode

#returns the number if confirmed
    def get_result(self):
        if self.confirmed and self.input_text != "":
            return int(self.input_text)
        return None

#the input box with white boarder
#yeah this version is kind of easier, than what I did before with die DialogueBox but well. it works
    def draw(self):
        pygame.draw.rect(self.game.display, self.game.White, self.rect, 2)
        inner_rect = pygame.Rect(
            self.rect.x + 2,
            self.rect.y + 2,
            self.rect.width - 4,
            self.rect.height -4
        )
        pygame.draw.rect(self.game.display, self.game.Black, inner_rect)
        snip = self.font.render(self.input_text, True, self.game.White)
        self.game.display.blit(snip, (self.rect.x + 10, self.rect.y + 8))

#storyyyy starts
#we start with the EyeClose animation, as if the player has just woken up
#we have a cool milky way turn animation that is triggered by joystick choice or appears late while talking to robo-john
#also fade transitions, because that seemed easier than animating that from scratch (when the player looks around to the bed
class Scene1(Scene):
    def __init__(self, game):
        Scene.__init__(self, game, pygame.image.load("assets/console.png"))
        self.dialogue_box = DialogueBox(game, scene_1["start"])
        self.choice_box = None
        self.state = "Intro"
        self.input_box = InputBox(game)

        #sprites
        self.eye_close_sprites = pygame.sprite.Group()
        self.eye_close = EyeClose(0, 0)
        self.eye_close_sprites.add(self.eye_close)

        self.milkyway_sprites = pygame.sprite.Group()
        self.milkyway_still = pygame.image.load("assets/milkyway/milkyway9.png")
        self.milkyway_still = pygame.transform.scale(self.milkyway_still, (860, 440))

        self.robowave_sprites = pygame.sprite.Group()
        self.robowave = RoboWave(0, 0)
        self.robowave_sprites.add(self.robowave)

        self.joystick_used = False
        self.show_milkyway = False

    def run(self):
        self.run_display = True
        while self.run_display:
            events = pygame.event.get()
            self.game.check_events(events)
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.image, (0, 0))

            self.eye_close_sprites.draw(self.game.display)
            self.eye_close_sprites.update()

            #control of the milky way animation here
            #wanted the last image to stay after the animation is done, so added the milkyway_still
            if self.state == "joystick" or self.show_milkyway:
                if self.milkyway_sprites:
                    self.milkyway_sprites.draw(self.game.display)
                    self.milkyway_sprites.update()
                else:
                    self.game.display.blit(self.milkyway_still, (0, 0))
                self.game.display.blit(self.image, (0, 0))

            self.draw_speaker()

            #start handling states after EyeClose animation is done
            if not self.eye_close_sprites:
                self.handle_state(events)

            self.draw_fade()
            self.blit_screen()

#yeah and this is where all the "flow" or story is happening
#separated all the states / dialogues and well, just controling what is happening here
    def handle_state(self, events):
        self.dialogue_box.update()
        self.dialogue_box.draw()

        if self.state == "Intro":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.state = "awaiting_choice"

        elif self.state == "awaiting_choice":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["Try the joystick", "Try the touchpad"])

                self.choice_box.move_cursor()
                self.choice_box.draw()

                choice = self.choice_box.get_selected()

                if choice == "Try the joystick":
                    self.milkyway_sprites = pygame.sprite.Group()
                    self.milkyway = Milkyway(0, 0)
                    self.milkyway_sprites.add(self.milkyway)
                    self.show_milkyway = True
                    self.dialogue_box = DialogueBox(self.game, scene_1["joystick"])
                    self.choice_box = None
                    self.joystick_used = True
                    self.state = "joystick"
                if choice == "Try the touchpad":
                    self.dialogue_box = DialogueBox(self.game, scene_1["touchpad"], speaker="robo_john")
                    self.choice_box = None
                    self.state = "touchpad"

        elif self.state == "joystick":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["touchpad"], speaker="robo_john")
                self.choice_box = None
                self.state = "touchpad"

        elif self.state == "touchpad":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.state = "robojohn_intro"

        elif self.state == "robojohn_intro":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["What happened?", "Who are you?"])
                self.choice_box.move_cursor()
                self.choice_box.draw()
                choice = self.choice_box.get_selected()
                if choice == "What happened?":
                    self.dialogue_box = DialogueBox(self.game, scene_1["what happened"], speaker="robo_john")
                    self.choice_box = None
                    self.state = "what_happened"
                if choice == "Who are you?":
                    self.dialogue_box = DialogueBox(self.game, scene_1["who are you"], speaker="robo_john")
                    self.choice_box = None
                    self.state = "who_are_you"

        elif self.state == "who_are_you":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.state_timer = pygame.time.get_ticks()
                self.state = "going_on"

        elif self.state == "going_on":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["what happened"], speaker="robo_john")
                self.state = "what_happened"

        elif self.state =="what_happened":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["Wormhole?", "How long was I out?"])
                self.choice_box.move_cursor()
                self.choice_box.draw()
                choice = self.choice_box.get_selected()
                if choice == "Wormhole?":
                    self.dialogue_box = DialogueBox(self.game, scene_1["wormhole?"], speaker="robo_john")
                    self.choice_box = None
                    self.state = "wormhole"
                elif choice == "How long was I out?":
                    self.dialogue_box = DialogueBox(self.game, scene_1["how long was I out"], speaker="robo_john")
                    self.choice_box = None
                    self.state = "how_long"

        elif self.state == "how_long":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.state = "wormhole"

#added the wormhole_auto_turn here, because otherwise the screen stays black if the player doesn't use the joystick
        elif self.state == "wormhole":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                if not self.joystick_used:
                    self.show_milkyway = True
                    self.milkyway_sprites = pygame.sprite.Group()
                    self.milkyway = Milkyway(0, 0)
                    self.milkyway_sprites.add(self.milkyway)
                    self.dialogue_box = DialogueBox(self.game, scene_1["auto_wormhole"], speaker="robo_john")
                    self.state = "wormhole_auto_turn"
                else:
                   self.dialogue_box = DialogueBox(self.game, scene_1["wormhole_n"])
                   self.state = "wormhole_n"

        elif self.state == "wormhole_auto_turn":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["wormhole_n"])
                self.state = "wormhole_n"

        elif self.state == "wormhole_n":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["wormhole_r"], speaker="robo_john")
                self.state = "wormhole_r"

        elif self.state == "wormhole_r":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                bed_image = pygame.image.load("assets/bedroom.png")
                bed_image = pygame.transform.scale(bed_image, (960, 540))
                self.do_fade(next_image=bed_image)
                self.dialogue_box = DialogueBox(self.game, scene_1["catch"])
                self.state = "catch"

        elif self.state == "catch":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                console_image = pygame.image.load("assets/console.png")
                console_image = pygame.transform.scale(console_image, (960, 540))
                self.do_fade(next_image=console_image)
                self.dialogue_box = DialogueBox(self.game, scene_1["scoff"], speaker="robo_john")
                self.state = "scoff"

        elif self.state == "scoff":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["since_scoff"])
                self.state = "since_scoff"

        elif self.state == "since_scoff":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_1["calibrate"], speaker="robo_john")
                self.state = "calibrate"

        elif self.state == "calibrate":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.state = "calibrate_input"

        elif self.state == "calibrate_input":
            if self.input_box is None:
                self.input_box = InputBox(self.game)
            for event in events:
                self.input_box.handle_event(event)
            self.input_box.draw()
            result = self.input_box.get_result()
            if result is not None:
                self.input_box = None
                if 135 <= result <= 185:
                    self.dialogue_box = DialogueBox(self.game, scene_1["right"], speaker="robo_john")
                    self.state = "calibrate_correct"
                elif 0 < result < 360:
                    self.dialogue_box = DialogueBox(self.game, scene_1["wrong"], speaker="robo_john")
                    self.state = "calibrate_wrong"
                else:
                    self.dialogue_box = DialogueBox(self.game, scene_1["way off"], speaker="robo_john")
                    self.state = "calibrate_way_off"

        elif self.state == "calibrate_correct":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.run_display = False

        elif self.state == "calibrate_wrong":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.input_box = InputBox(self.game)
                self.state = "calibrate_input"

        elif self.state == "calibrate_way_off":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.input_box = InputBox(self.game)
                self.state = "calibrate_input"

#scene to, new sprites
#in the end there is a narrative choice
#if the player decides to continue, they enter the store directly
#if they argue, they confront robo-john and trigger the first corruption level
class Scene2(Scene):
    def __init__(self, game):
        Scene.__init__(self, game, pygame.image.load("assets/console.png"))
        self.dialogue_box = DialogueBox(game, scene_2["move"])
        self.choice_box = None
        self.state = "move"
        self.chosen_path = "continue"

        self.warp_speed_sprites = pygame.sprite.Group()
        self.warp_speed = WarpSpeed(0, -25)
        self.warp_speed_sprites.add(self.warp_speed)
        self.warp_visible = True

    def run(self):
        self.run_display = True
        while self.run_display:
            events = pygame.event.get()
            self.game.check_events(events)
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.image, (0, 0))

            if self.warp_visible:
                self.warp_speed_sprites.draw(self.game.display)
                self.warp_speed_sprites.update()
            self.game.display.blit(self.image, (0, 0))

            if self.state == "fading_out":
                if not self.fading:
                    self.run_display = False
            else:
                self.handle_state(events)

            self.draw_speaker()
            self.draw_fade()
            self.blit_screen()

    def handle_state(self, events):
        self.dialogue_box.update()
        self.dialogue_box.draw()

        if self.state == "move":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["cat_appears"], speaker="cat")
                self.state = "cat_appears"

        elif self.state == "cat_appears":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["player_sees_cat"])
                self.state = "player_sees_cat"

        elif self.state == "player_sees_cat":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["eggplant_intro"], speaker="cat")
                self.state = "eggplant_intro"

        elif self.state == "eggplant_intro":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["cat_contrast"])
                self.state = "cat_contrast"

        elif self.state == "cat_contrast":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_funny"], speaker="robo_john")
                self.state = "robo_funny"

        elif self.state == "robo_funny":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["player_confused"])
                self.state = "player_confused"

        elif self.state == "player_confused":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_scan"], speaker="robo_john")
                self.state = "robo_scan"

        elif self.state == "robo_scan":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["cat_pieces"], speaker="cat")
                self.state = "cat_pieces"

        elif self.state == "cat_pieces":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["player_how_know"])
                self.state = "player_how_know"

        elif self.state == "player_how_know":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["cat_logs"], speaker="cat")
                self.state = "cat_logs"

        elif self.state == "cat_logs":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = True
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_arrive"], speaker="robo_john")
                self.state = "robo_arrive"

        elif self.state == "robo_arrive":
            self.warp_visible = False
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_2["cat_warning"],speaker="cat")
                self.state = "cat_warning"

        elif self.state == "cat_warning":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.cat_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_2["player_hallucinate"])
                self.state = "player_hallucinate"

        elif self.state == "player_hallucinate":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_landing"], speaker="robo_john")
                self.state = "robo_landing"

#well, animating and coming up with pixel art / images took up more time than I thought
#in this case I decided to just to this fade black image thing and more text
        elif self.state == "robo_landing":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                black = pygame.Surface((960, 540))
                black.fill((0, 0, 0))
                self.do_fade(next_image=black)
                self.dialogue_box = DialogueBox(self.game, scene_2["leave_ship"])
                self.cat_visible = False
                self.state = "leave_ship"

        elif self.state == "leave_ship":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                zabka_image = pygame.image.load("assets/zabka.png")
                zabka_image = pygame.transform.scale(zabka_image, (960, 540))
                self.do_fade(next_image=zabka_image)
                self.dialogue_box = DialogueBox(self.game, scene_2["store_appears"])
                self.state = "store_appears"

        elif self.state == "store_appears":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_materials"], speaker="robo_john")
                self.state = "robo_materials"

        elif self.state == "robo_materials":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_2["approach_store"])
                self.state = "approach_store"

        elif self.state == "approach_store":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_silence"], speaker="robo_john")
                self.state = "robo_silence"

        elif self.state == "robo_silence":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_2["player_robo_question"])
                self.state = "player_robo_question"

        elif self.state == "player_robo_question":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_2["robo_syntax"], speaker="robo_john")
                self.state = "robo_syntax"

        elif self.state == "robo_syntax":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["Continue", "Start to argue"])
                self.choice_box.move_cursor()
                self.choice_box.draw()
                choice = self.choice_box.get_selected()
                if choice == "Continue":
                    store_image = pygame.image.load("assets/sklepinside.png")
                    store_image = pygame.transform.scale(store_image, (960, 540))
                    self.do_fade_and_exit(next_image=store_image)
                    self.chosen_path = "continue"
                elif choice == "Start to argue":
                    self.game.cat_interactions += 1
                    self.chosen_path = "argue"
                    self.run_display = False

#next scene
#fun fact: the store is designed to kind of remind one of the polish chain store (kiosk) Zabka (if you've ever been to
#poland, they really are at every corner
class Scene3(Scene):
    def __init__(self, game, path="continue"):
        if path == "continue":
            img = pygame.image.load("assets/sklepinside.png")
        else:
            img = pygame.image.load("assets/zabka.png")
        img = pygame.transform.scale(img, (960, 540))
        Scene.__init__(self, game, img)
        self.path = path
        self.choice_box = None
        self.chosen_path = "continue"

        #added a little variant of the cat
        #it kind of was easier to adjust the size of the cat in Aseprite directly, so made a new sprite for that
        self.cat_small_sprites = pygame.sprite.Group()
        self.cat_small = CatSmall(0, 0)
        self.cat_small_sprites.add(self.cat_small)
        self.cat_small_visible = False

        self.bathcat_sprites = pygame.sprite.Group()
        self.bathcat = BathCat(0, 0)
        self.bathcat_sprites.add(self.bathcat)
        self.bathcat_visible = False

        #while in the store, the player can't see the console / robo-john, so turning his waves of
        self.robo_visible = False

        if self.path == "continue":
            self.dialogue_box = DialogueBox(game, scene_3["enter_store"])
            self.state = "enter_store"
        else:
            self.dialogue_box = DialogueBox(game, scene_3["argue"])
            self.state = "argue"

    def run(self):
        self.run_display = True
        while self.run_display:
            events = pygame.event.get()
            self.game.check_events(events)
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.image, (0, 0))

            if self.cat_small_visible:
                self.cat_small_sprites.draw(self.game.display)
                self.cat_small_sprites.update()

            if self.bathcat_visible:
                self.bathcat_sprites.draw(self.game.display)
                self.bathcat_sprites.update()

            self.draw_speaker()

            if self.state == "fading_out":
                if not self.fading:
                    if self.fade_next_state:
                        self.state = self.fade_next_state
                    else:
                        self.run_display = False
            else:
                self.handle_state(events)

            self.draw_fade()
            self.blit_screen()

    def handle_state(self, events):
        self.dialogue_box.update()
        self.dialogue_box.draw()

        if self.state == "enter_store":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["notice_door"])
                self.state = "notice_door"

        elif self.state == "argue":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["cat_shadow"], speaker="cat")
                self.cat_small_visible = True
                self.state = "cat_shadow"

        elif self.state == "cat_shadow":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["argue_player"])
                self.state = "argue_player"

        elif self.state == "argue_player":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_3["robo_glitch_welcome"], speaker="robo_john")
                self.state = "robo_glitch_welcome"

        elif self.state == "robo_glitch_welcome":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["argue_player_2"])
                self.state = "argue_player_2"

        elif self.state == "argue_player_2":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_3["robo_welcome_back"], speaker="robo_john")
                self.state = "robo_welcome_back"

        elif self.state == "robo_welcome_back":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["argue_player_3"])
                self.state = "argue_player_3"

        elif self.state == "argue_player_3":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.dialogue_box = self.robo_dialogue("robo_aliens", scene_3)
                self.state = "robo_aliens"

        elif self.state == "robo_aliens":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["cat_mission"], speaker="cat")
                self.state = "cat_mission"

        elif self.state == "cat_mission":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                store_image = pygame.image.load("assets/sklepinside.png")
                store_image = pygame.transform.scale(store_image, (960, 540))
                self.do_fade_and_exit(next_image=store_image)
                self.dialogue_box = DialogueBox(self.game, scene_3["enter_store"])
                self.cat_small_visible = False
                self.state = "enter_store"

        elif self.state == "notice_door":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3["door_choice_intro"])
                self.state = "door_choice"

        elif self.state == "door_choice":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["Investigate door", "Check the store"])
                self.choice_box.move_cursor()
                self.choice_box.draw()
                choice = self.choice_box.get_selected()
                if choice == "Investigate door":
                    self.game.cat_interactions += 1
                    self.chosen_path = "door"
                    bathroom_image = pygame.image.load("assets/bathroom.png")
                    bathroom_image = pygame.transform.scale(bathroom_image, (960, 540))
                    self.do_fade_and_exit(next_image=bathroom_image)
                elif choice == "Check the store":
                    self.chosen_path = "store"
                    self.run_display = False

#and last scene
class Scene4(Scene):
    def __init__(self, game, path="door"):
        if path == "door":
            img = pygame.image.load("assets/bathroom.png")
        else:
            img = pygame.image.load("assets/sklepinside.png")
        img = pygame.transform.scale(img, (960, 540))
        Scene.__init__(self, game, img)
        self.path = path
        self.choice_box = None
        self.chosen_ending = "ending_1"
        self.fade_next_state = None

        self.bathcat_sprites = pygame.sprite.Group()
        self.bathcat = BathCat(0, 0)
        self.bathcat_sprites.add(self.bathcat)
        self.bathcat_visible = False

        self.cat_small_sprites = pygame.sprite.Group()
        self.cat_small = CatSmall(0, 0)
        self.cat_small_sprites.add(self.cat_small)
        self.cat_small_visible = False

        if self.path == "door":
            self.dialogue_box = DialogueBox(game, scene_3_door["investigate"])
            self.state = "investigate"
        else:
            self.dialogue_box = self.robo_dialogue("stay_store", scene_3_door)
            self.state = "stay_store"

        #another case of too lazy to animate, but this was a nice outcome
        self.alarm_visible = False
        self.alarm_alpha = 0
        self.alarm_direction = 1

    def run(self):
        self.run_display = True
        while self.run_display:
            events = pygame.event.get()
            self.game.check_events(events)
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.image, (0, 0))

            if self.bathcat_visible:
                self.bathcat_sprites.draw(self.game.display)
                self.bathcat_sprites.update()

            if self.cat_small_visible:
                self.cat_small_sprites.draw(self.game.display)
                self.cat_small_sprites.update()

            if self.state == "fading_out":
                if not self.fading:
                    if self.fade_next_state:
                        self.state = self.fade_next_state
                    else:
                        self.run_display = False
            else:
                self.draw_speaker()
                self.handle_state(events)

            #more of the alarm stuff
            if self.alarm_visible:
                alarm_surface = pygame.Surface((780,540))
                alarm_surface.fill((255, 0, 0))
                alarm_surface.set_alpha(self.alarm_alpha)
                self.game.display.blit(alarm_surface, (90, 0))

                self.alarm_alpha += 5 * self.alarm_direction
                if self.alarm_alpha >= 100:
                    self.alarm_direction = -1
                elif self.alarm_alpha <= 0:
                    self.alarm_direction = 1

            self.draw_fade()
            self.blit_screen()

    def handle_state(self, events):
        self.dialogue_box.update()
        self.dialogue_box.draw()

        if self.state == "investigate":
            if self.game.START_KEY:
                self.bathcat_visible = True
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_start"], speaker="cat")
                self.state = "cat_start"

        elif self.state == "cat_start":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_sink"])
                self.state = "cat_sink"

        elif self.state == "cat_sink":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_notice"], speaker="cat")
                self.state = "cat_notice"

        elif self.state == "cat_notice":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_dejavu"])
                self.state = "player_dejavu"

        elif self.state == "player_dejavu":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_hm"], speaker="cat")
                self.state = "cat_hm"

        elif self.state == "cat_hm":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_oxygen"])
                self.state = "player_oxygen"

        elif self.state == "player_oxygen":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_what"], speaker="cat")
                self.state = "cat_what"

        elif self.state == "cat_what":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_vacuum"])
                self.state = "player_vacuum"

        elif self.state == "player_vacuum":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_focus"], speaker="cat")
                self.bathcat_visible = False
                outside_image = pygame.image.load("assets/zabka.png")
                outside_image = pygame.transform.scale(outside_image, (960, 540))
                self.do_fade(next_image=outside_image)
                self.state = "cat_focus"

        elif self.state == "cat_focus":
            if self.game.START_KEY:
                self.cat_small_visible = True
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["outside"])
                self.state = "outside"

        elif self.state == "outside":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_because"], speaker="cat")
                self.cat_small_visible = False
                console_image = pygame.image.load("assets/console.png")
                console_image = pygame.transform.scale(console_image, (960, 540))
                self.do_fade(next_image=console_image)
                self.state = "cat_because"

        elif self.state == "cat_because":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("back_in_ship", scene_3_door)
                self.state = "back_in_ship"

        elif self.state == "stay_store":
            self.robo_visible = False
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = True
                console_image = pygame.image.load("assets/console.png")
                console_image = pygame.transform.scale(console_image, (960, 540))
                self.do_fade(next_image=console_image)
                self.dialogue_box = self.robo_dialogue("back_in_ship", scene_3_door)
                self.state = "back_in_ship"

        elif self.state == "back_in_ship":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["alarm"])
                self.state = "alarm"

        elif self.state == "alarm":
            self.alarm_visible = True
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("robo_attack", scene_3_door)
                self.state = "robo_attack"

        elif self.state == "robo_attack":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_dont"], speaker="cat")
                self.cat_visible = True
                self.state = "cat_dont"

        elif self.state == "cat_dont":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished_choice():
                self.cat_visible = False
                if self.choice_box is None:
                    self.choice_box = ChoiceBox(self.game, ["Attack", "Run", "Stay"])
                self.choice_box.move_cursor()
                self.choice_box.draw()
                choice = self.choice_box.get_selected()
                if choice == "Attack":
                    self.dialogue_box = DialogueBox(self.game, scene_3_door["attack"])
                    self.choice_box = None
                    self.state = "attack"
                elif choice == "Run":
                    self.dialogue_box = DialogueBox(self.game, scene_3_door["run"])
                    self.choice_box = None
                    self.state = "run"
                elif choice == "Stay":
                    self.dialogue_box = DialogueBox(self.game, scene_3_door["stay"])
                    self.choice_box = None
                    self.state = "stay"

        elif self.state == "attack":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("robo_well_done", scene_3_door)
                self.state = "robo_well_done"

        elif self.state == "robo_well_done":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_confused_attack"])
                self.state = "player_confused_attack"

        elif self.state == "player_confused_attack":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["last_ship"])
                self.state = "last_ship"

        elif self.state == "last_ship":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.alarm_visible = False
                self.robo_visible = False
                black = pygame.Surface((960, 540))
                black.fill((0, 0, 0))
                self.do_fade_and_exit(next_image=black)
                self.dialogue_box = self.robo_dialogue("ending_1", scene_3_door)
                self.state = "ending_1"


        elif self.state == "run":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_why"], speaker="cat")
                self.cat_visible = True
                self.state = "cat_why"

        elif self.state == "cat_why":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_shooting"])
                self.state = "player_shooting"

        elif self.state == "player_shooting":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("robo_shoot_back", scene_3_door)
                self.state = "robo_shoot_back"

        elif self.state == "robo_shoot_back":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_someday"], speaker="cat")
                self.state = "cat_someday"

        elif self.state == "cat_someday":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.alarm_visible = False
                self.robo_visible = False
                black = pygame.Surface((960, 540))
                black.fill((0, 0, 0))
                self.do_fade_and_exit(next_image=black)
                self.cat_visible = False
                self.dialogue_box = self.robo_dialogue("ending_1", scene_3_door)
                self.state = "ending_1"

        elif self.state == "stay":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("robo_shield", scene_3_door)
                self.state = "robo_shield"

        elif self.state == "robo_shield":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_understood"], speaker="cat")
                self.cat_visible = True
                self.state = "cat_understood"

        elif self.state == "cat_understood":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_comes_back"])
                self.state = "player_comes_back"

        elif self.state == "player_comes_back":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = self.robo_dialogue("robo_move", scene_3_door)
                self.state = "robo_move"

        elif self.state == "robo_move":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.alarm_visible = False
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_no_end"])
                self.state = "player_no_end"

        elif self.state == "player_no_end":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_time"], speaker="cat")
                self.state = "cat_time"

        elif self.state == "cat_time":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["player_how_often"])
                self.state = "player_how_often"

        elif self.state == "player_how_often":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.dialogue_box = DialogueBox(self.game, scene_3_door["cat_every_time"], speaker="cat")
                self.state = "cat_every_time"

#triggering the end sequence already because of the timing
        elif self.state == "cat_every_time":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.robo_visible = False
                self.cat_visible = False
                self.do_fade_white()
                white = pygame.Surface((960, 540))
                white.fill((255, 255, 255))
                self.do_fade_and_exit(next_image=white)
                self.dialogue_box = DialogueBox(self.game, scene_3_door["ending_2"])
                self.state = "ending_2"

#ending 1 results in the game restarting in the first scene, skipping the main menu (it's like a time loop)
        elif self.state == "ending_1":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.chosen_ending = "ending_1"
                self.run_display = False

#ending 2 finished the game and brings the player to the main menu
        elif self.state == "ending_2":
            if self.game.START_KEY:
                self.dialogue_box.advance()
            if self.dialogue_box.is_finished():
                self.chosen_ending = "ending_2"
                self.run_display = False

