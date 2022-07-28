# libraries
import pygame
import os
import sys
import pickle

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

# screen,display
window_x = 900
window_y = 600
window = pygame.display.set_mode((window_x, window_y))
window_rect = window.get_rect()

pygame.display.set_caption("Ace Drag Race")
pygame.display.set_icon(pygame.image.load(os.path.join("icon.png")))

fps = pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)


# classes
class Text:
    def __init__(self, font: str, size: int, color: tuple, text: str, background: tuple = None):
        self.size = size
        self.font = pygame.font.Font(os.path.join("assets", "fonts", f"{font}.ttf"), self.size)
        self.color = color
        self.text = text
        self.background = background
        self.image = self.font.render(self.text, False, self.color, self.background)
        self.rect = self.image.get_rect()

    def place(self, center: bool = False, xy: tuple = (0, 0)):
        if center:
            self.rect.center = window_rect.center
            self.rect.x += xy[0]
            self.rect.y += xy[1]
        else:
            self.rect.x = xy[0]
            self.rect.y = xy[1]

        window.blit(self.image, self.rect)

    def render(self):
        self.image = self.font.render(self.text, True, self.color, self.background)
        self.rect = self.image.get_rect()


class Image:
    def __init__(self, file: str, name: str, wh: tuple):
        self.image = pygame.image.load(os.path.join("assets", "images", file, name))
        self.image = pygame.transform.scale(self.image, wh)
        self.rect = self.image.get_rect()
        self.brightness = 0

    def place(self, center: bool = False, xy: tuple = (0, 0)):
        if center:
            self.rect.center = window_rect.center
            self.rect.x += xy[0]
            self.rect.y += xy[1]
        else:
            self.rect.x = xy[0]
            self.rect.y = xy[1]

        window.blit(self.image, self.rect)


menu = "main"
# backgrounds
main_background = Image("background", "main.jpg", (window_x, window_y))
play_background = Image("background", "play.jpg", (window_x, window_y))
about_background = Image("background", "about.jpg", (window_x, window_y))
settings_background = Image("background", "settings.jpg", (window_x, window_y))
garage_background = Image("background", "garage.jpg", (window_x, window_y))
store_background = Image("background", "store.jpg", (window_x, window_y))
storymode_background = Image("background", "story_mode.jpg", (window_x, window_y))

# sounds
click1_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click1.wav"))
click2_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click2.wav"))
click3_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click3.wav"))
buy_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "buy.wav"))
warning_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "warning.wav"))
win_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "win.wav"))
lose_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "lose.wav"))
menu_music = pygame.mixer.Sound(os.path.join("assets", "sounds", "menu.wav"))
race_music = pygame.mixer.Sound(os.path.join("assets", "sounds", "race.wav"))
ready_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "ready.wav"))
go_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "go.wav"))
final_match_music = pygame.mixer.Sound(os.path.join("assets", "sounds", "final.ogg"))
game_over_music = pygame.mixer.Sound(os.path.join("assets", "sounds", "game_over.ogg"))

# main menu assets
title_text = Text("game_font", 60, white, "Ace Drag Race", (255, 122, 82))
play_button = Image("button", "play.png", (200, 85))
about_button = Image("button", "about.png", (200, 85))
back_button = Image("button", "back.png", (120, 50))

# about texts
about_text1 = Text("game_font", 30, (200, 100, 60), "Ace Drag Race v1.0 - made by 'Eorhan23'")
about_text2 = Text("game_font", 30, black, "This game is a short distance and flat road car racing game.")
about_text3 = Text("game_font", 30, black, "Game progress will save to the current file location.")
about_text4 = Text("game_font", 30, black, "It is written with the 'Python: PyGame'")
about_text5 = Text("game_font", 30, black, "It is a beginner game that you can play on your computer.")
about_text6 = Text("game_font", 30, (150, 100, 100), "Contact: eorhan2396@gmail.com")

# save game loading
loading_text = Text("game_font", 35, white, "Save game loading...")
loading_text2 = Text("game_font", 35, white, "Save file can't found, new save creating...")
loading_time = 0

# play top bar
money_img = Image("miscellaneous", "money.png", (40, 40))
money_text = Text("game_font", 30, white, "0")

settings_button = Image("button", "settings.png", (125, 50))
settings_title = Text("game_font", 35, white, "SETTINGS")

help_button = Image("button", "help.png", (115, 42))

# game menus
storymode_button = Image("button", "story_mode.png", (320, 200))
storymode_text = Text("game_font", 22, white, "Story mode")

challange_button = Image("button", "challange.png", (320, 200))
challange_text = Text("game_font", 22, (180, 180, 180), "Challange")
challange_button.image.fill((60, 60, 60), special_flags=pygame.BLEND_RGBA_MULT)

customrace_button = Image("button", "custom_race.png", (320, 200))
customrace_text = Text("game_font", 22, (180, 180, 180), "Custom race")
customrace_button.image.fill((60, 60, 60), special_flags=pygame.BLEND_RGBA_MULT)

garage_button = Image("button", "garage.png", (320, 200))
garage_text = Text("game_font", 22, black, "Garage")
garage_title = Text("game_font", 45, white, "GARAGE", (80, 120, 90))

# music setting
music_img = Image("miscellaneous", "music.png", (90, 90))
music_stick = pygame.Rect(380, 190, 200, 16)
music_ball_pos = (580, 198)
music_volume = 1

# sound setting
sound_img = Image("miscellaneous", "sound.png", (90, 90))
sound_stick = pygame.Rect(380, 320, 200, 16)
sound_ball_pos = (580, 328)
sound_volume = 1

# click arrows
right_arrow = Image("button", "right.png", (50, 30))
left_arrow = Image("button", "left.png", (50, 30))

# buttons
save_game_button = Image("button", "save_game.png", (160, 65))
go_button = Image("button", "go.png", (140, 65))

# cars
car_images = []
for i in range(1, 16):
    car_images.append(Image("car", f"car{i}.png", (120, 60)))

car_images2 = []
for i in range(1, 16):
    car_images2.append(Image("car", f"car{i}.png", (120, 60)))

car_costs = {2: 20000, 3: 30000, 4: 50000, 5: 90000, 6: 150000, 7: 180000, 8: 250000,
             9: 340000, 10: 390000, 11: 470000, 12: 520000, 13: 580000, 14: 620000}

car_colors = {0: (53, 125, 202), 1: (240, 156, 18), 2: (19, 141, 117), 3: (169, 50, 38), 4: (135, 215, 55),
              5: (120, 27, 129), 6: (133, 146, 158), 7: (148, 146, 121), 8: (30, 47, 151), 9: (203, 67, 53),
              10: (229, 231, 233), 11: (244, 208, 63), 12: (93, 109, 126), 13: (97, 106, 107), 14: (220, 118, 51)}

current_car = 0

opponent_attributes = {0: [1, 1, 1], 1: [1, 1, 2], 2: [3, 2, 2], 3: [2, 3, 4], 4: [3, 2, 5], 5: [4, 2, 6],
                       6: [6, 5, 5], 7: [7, 5, 6], 8: [6, 4, 7], 9: [7, 7, 7], 10: [9, 8, 7], 11: [8, 8, 10],
                       12: [7, 8, 11], 13: [11, 10, 10], 14: [11, 10, 12], 15: [13, 12, 11]}

road_distances = {0: 750, 1: 750, 2: 1000, 3: 1000, 4: 1250, 5: 1000, 6: 1500, 7: 1250, 8: 500, 9: 1000, 10: 1250,
                  11: 750, 12: 500, 13: 1250, 14: 1000, 15: 1500}

### SAVE DATAS ###

# read or write save file
try:
    with open(os.path.join("save", "save.bin"), "rb") as saveFile:
        saved_data = pickle.load(saveFile)

        money = saved_data[0]
        car_attributes = saved_data[1]
        car_upgrades = saved_data[2]
        buyable_cars = saved_data[3]
        owned_cars = saved_data[4]
        using_car = saved_data[5]
        story_stage = saved_data[6]

        saveFile.close()

except FileNotFoundError:
    money = 10000
    car_attributes = {0: [1, 1, 2], 1: [2, 1, 1], 2: [2, 2, 2], 3: [1, 3, 3], 4: [2, 3, 4], 5: [3, 4, 5],
                      6: [5, 5, 4], 7: [5, 4, 6], 8: [6, 6, 6], 9: [7, 8, 7], 10: [8, 8, 8], 11: [8, 9, 10],
                      12: [9, 10, 10], 13: [10, 10, 11], 14: [11, 11, 10]}
    car_upgrades = {0: [False, False, False], 1: [False, False, False], 2: [False, False, False],
                    3: [False, False, False], 4: [False, False, False], 5: [False, False, False],
                    6: [False, False, False], 7: [False, False, False], 8: [False, False, False],
                    9: [False, False, False], 10: [False, False, False], 11: [False, False, False],
                    12: [False, False, False], 13: [False, False, False], 14: [False, False, False]}
    buyable_cars = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    owned_cars = [0, 1]
    using_car = 0
    story_stage = 0

    loading_time = 61
    with open(os.path.join("save", "save.bin"), "wb") as saveFile:
        pickle.dump([money, car_attributes, car_upgrades,
                     buyable_cars, owned_cars, story_stage], saveFile)

        saveFile.close()


def save_game():
    with open(os.path.join("save", "save.bin"), "wb") as saveFile:
        pickle.dump([money, car_attributes, car_upgrades,
                     buyable_cars, owned_cars, using_car, story_stage], saveFile)

        saveFile.close()


##################

# horsepower
horsepower_text = Text("game_font", 30, white, "HORSEPOWER", (235, 83, 65))
horsepower_upgrade = Image("button", "upgrade_hp.png", (50, 50))
horsepower_images = []
for i in range(1, 13):
    horsepower_images.append(Image("bar", f"horsepower{i}.png", (230, 50)))

# max speed
maxspeed_text = Text("game_font", 30, white, "MAX SPEED", (28, 66, 234))
maxspeed_upgrade = Image("button", "upgrade_ms.png", (50, 50))
maxspeed_images = []
for i in range(1, 13):
    maxspeed_images.append(Image("bar", f"maxspeed{i}.png", (230, 50)))

# acceleration
acceleration_text = Text("game_font", 30, white, "ACCELERATION", (74, 229, 102))
acceleration_upgrade = Image("button", "upgrade_acc.png", (50, 50))
acceleration_images = []
for i in range(1, 13):
    acceleration_images.append(Image("bar", f"acceleration{i}.png", (230, 50)))

# miscellaneous
yellow_ok = Image("miscellaneous", "yellow_ok.png", (50, 50))
upgrade_cost_text = Text("game_font", 30, white, "0")
buycar_button = Image("button", "store.png", (160, 140))
buy_button = Image("button", "buy.png", (130, 65))
buycost_text = Text("game_font", 30, white, "0")
use_button = Image("button", "use.png", (120, 55))
inuse_button = Image("button", "in_use.png", (120, 55))
store_title = Text("game_font", 45, white, "STORE", (150, 40, 180))
next_button = Image("button", "next.png", (120, 50))
warning_img = Image("button", "warning.png", (32, 32))
saved_text = Image("miscellaneous", "saved.png", (100, 60))
saved_text_delay = 0

# descriptions
stage_descriptions = []
for i in range(16):
    stage_descriptions.append(Image("description", f"stage{i}.png", (300, 200)))
difficulty_warning = Image("description", "difficulty_warning.png", (180, 150))
save_description = Image("description", "save_description.png", (220, 190))
help_menu_text = Image("description", "help.png", (750, 450))

# story mode menu
level_text = Text("game_font", 45, white, f"Story mode - Level {story_stage}", (26, 188, 156))
opponent_text = Text("game_font", 35, white, "  Opponent  ", (56, 20, 10))
difficulty_text = Text("game_font", 35, white, "  Difficulty  ", (56, 20, 10))
difficultyRate_text = Text("game_font", 35, white, "Easy", (0, 180, 0))
road_distance_text = Text("game_font", 35, white, "  Road distance  ", (56, 20, 10))
road_distance_number_text = Text("game_font", 35, white, "1000 Meter", black)

# before race
before_text = Text("game_font", 30, white, "-Hello racer.")
text_td = 0

# race
road = Image("background", "road.png", (window_x, 250))
road2 = Image("background", "road.png", (window_x, 250))
road_x = 0
road2_x = window_x

race_background = Image("background", "grass.png", (window_x, window_y))
race_background2 = Image("background", "grass.png", (window_x, window_y))
race_background_x = 0
race_background2_x = window_x

you_img = Image("miscellaneous", "you.png", (150, 60))
tachometer = Image("miscellaneous", "tachometer.png", (260, 260))
meter_stick = Image("miscellaneous", "meter_stick.png", (24, 210))
gear_img = Image("miscellaneous", "gear.png", (30, 30))
go_text = Text("game_font", 40, (40, 220, 30), "GO!")

finish_flag = Image("miscellaneous", "finish.png", (150, 250))

race_end_screen = pygame.Surface((window_x, window_y))
race_end_screen.set_alpha(210)
race_end_screen.fill((0, 0, 0))

kmh_number = Text("game_font", 25, white, "0")
kmh_text = Text("game_font", 20, white, "km/h")
gear_text = Text("game_font", 25, (231, 185, 29), "1")

shift_text = Text("game_font", 30, white, "Perfect shift")

earned_money_text = Text("game_font", 30, white, "Earned money:")
perfect_shifts_text = Text("game_font", 30, white, "Perfect shifts:")
top_speed_text = Text("game_font", 30, white, "Top speed:")
you_won_lost_text = Text("game_font", 45, white, "YOU WON!")

menu_music_ot = 0
race_music_ot = 0
winlose_sound_ot = 0

race_end_ot = 0

# game loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    # menus
    if menu == "main":
        main_background.place()
        title_text.place(True, (0, -200))
        play_button.place(True, (0, -45))
        about_button.place(True, (0, 70))

    elif menu == "about":
        about_background.place()
        about_text1.place(True, (0, -100))
        about_text2.place(True, (0, -50))
        about_text3.place(True, (0, 0))
        about_text4.place(True, (0, 50))
        about_text5.place(True, (0, 100))
        about_text6.place(True, (0, 175))
        back_button.place(xy=(window_x - back_button.rect.width, 0))

    elif menu == "save game loading":
        window.fill(black)
        if loading_time < 60:
            loading_text.place(True)
            loading_time += 1

        if loading_time == 60:
            menu = "play"

        if 60 < loading_time < 120:
            loading_text.place(True)
            loading_time += 1

        if 119 < loading_time < 240:
            loading_text2.place(True)
            loading_time += 1

        if loading_time == 240:
            menu = "play"

    elif menu == "play":
        if menu_music_ot == 0:
            menu_music.play(-1)
        menu_music_ot = 1

        play_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))
        pygame.draw.rect(window, (0, 0, 0), (0, 0, window_x - back_button.rect.width, back_button.rect.height))

        money_img.place(xy=(5, 5))
        money_text.place(xy=(55, 15))

        settings_button.place(xy=(630, 0))
        help_button.place(xy=(495, 5))

        storymode_button.place(xy=(40, 90))
        if story_stage == 0:
            storymode_text.place(xy=(150, 265))
        elif story_stage == 16:
            storymode_text.text = f"Story mode - Finished"
            storymode_text.render()
            storymode_text.place(xy=(105, 265))
        else:
            storymode_text.text = f"Story mode - Stage {story_stage}"
            storymode_text.render()
            storymode_text.place(xy=(105, 265))

        challange_button.place(xy=(450, 90)),
        challange_text.place(xy=(575, 265))

        customrace_button.place(xy=(40, 340))
        customrace_text.place(xy=(145, 514))

        garage_button.place(xy=(450, 340))
        garage_text.place(xy=(585, 514))

    elif menu == "settings":
        settings_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))
        settings_title.place(True, (0, -180))

        music_img.place(xy=(250, 150))
        pygame.draw.rect(window, black, music_stick)
        pygame.draw.circle(window, white, music_ball_pos, 15)
        if pygame.mouse.get_pressed()[0] == 1 and music_stick.collidepoint(mouse_pos[0], mouse_pos[1]):
            music_ball_pos = (mouse_pos[0], 198)
            music_volume = abs((380 - music_ball_pos[0]) / 200)

        sound_img.place(xy=(255, 280))
        pygame.draw.rect(window, black, sound_stick)
        pygame.draw.circle(window, white, sound_ball_pos, 15)
        if pygame.mouse.get_pressed()[0] == 1 and sound_stick.collidepoint(mouse_pos[0], mouse_pos[1]):
            sound_ball_pos = (mouse_pos[0], 328)
            sound_volume = abs((380 - sound_ball_pos[0]) / 200)

        save_game_button.place(True, (0, 150))
        if saved_text_delay >= 1:
            saved_text_delay += 1
            saved_text.place(True, (0, 210))

        if save_game_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            save_description.place(True, (120, 40))

        if saved_text_delay == 100:
            saved_text_delay = 0

    elif menu == "help":
        about_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))
        help_menu_text.place(xy=(50, 100))

    elif menu == "garage":
        garage_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))
        garage_title.place(True, (0, -180))

        def car_select():
            # top money
            money_img.place(xy=(5, 5))
            money_text.place(xy=(55, 15))

            # car
            right_arrow.place(xy=(330, 220))
            left_arrow.place(xy=(95, 220))
            car_images[current_car].place(xy=(180, 205))

            # dynamic car attributes
            current_car_attributes = {"horsepower": car_attributes.get(current_car)[0],
                                      "maxspeed": car_attributes.get(current_car)[1],
                                      "acceleration": car_attributes.get(current_car)[2]}

            # horsepwer
            current_horsepower = horsepower_images[current_car_attributes.get("horsepower") - 1]
            horsepower_text.place(xy=(35, 340))
            current_horsepower.place(xy=(205, 328))

            # max speed
            current_maxspeed = maxspeed_images[current_car_attributes.get("maxspeed") - 1]
            maxspeed_text.place(xy=(35, 426))
            current_maxspeed.place(xy=(205, 413))

            # acceleration
            current_acceleration = acceleration_images[current_car_attributes.get("acceleration") - 1]
            acceleration_text.place(xy=(35, 515))
            current_acceleration.place(xy=(205, 503))

        car_select()

        # upgrade cost
        if 0 <= current_car <= 4:
            upgrade_cost = 10000
        elif 5 <= current_car <= 11:
            upgrade_cost = 20000
        elif 12 <= current_car <= 14:
            upgrade_cost = 40000
        upgrade_cost_text.text = str(upgrade_cost)
        upgrade_cost_text.render()

        # horsepower upgrade
        if not car_upgrades.get(current_car)[0]:
            horsepower_upgrade.place(xy=(450, 328))
            money_img.place(xy=(520, 333))
            upgrade_cost_text.place(xy=(575, 342))
        else:
            yellow_ok.place(xy=(450, 328))

        # max speed upgrade
        if not car_upgrades.get(current_car)[1]:
            maxspeed_upgrade.place(xy=(450, 413))
            money_img.place(xy=(520, 418))
            upgrade_cost_text.place(xy=(575, 427))
        else:
            yellow_ok.place(xy=(450, 413))

        # acceleration upgrade
        if not car_upgrades.get(current_car)[2]:
            acceleration_upgrade.place(xy=(450, 503))
            money_img.place(xy=(520, 508))
            upgrade_cost_text.place(xy=(575, 517))
        else:
            yellow_ok.place(xy=(450, 503))

        # use
        if using_car == current_car:
            inuse_button.place(xy=(425, 209))
        else:
            use_button.place(xy=(425, 209))

        ###
        buycar_button.place(xy=(670, 120))

    elif menu == "store":
        store_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))
        store_title.place(True, (0, -180))

        car_select()

        buycost_text.text = str(car_costs.get(current_car))
        buycost_text.render()

        buy_button.place(xy=(530, 200))
        money_img.place(xy=(530, 290))
        buycost_text.place(xy=(590, 300))

    elif menu == "story_mode":
        storymode_background.place()
        back_button.place(xy=(window_x - back_button.rect.width, 0))

        level_text.text = f"Story mode - Stage {story_stage}"
        level_text.render()
        level_text.place(xy=(40, 40))

        opponent_text.place(xy=(145, 110))
        if story_stage == 0:
            car_images2[0].place(xy=(165, 160))
        else:
            car_images2[story_stage - 1].place(xy=(165, 160))

        difficulty_text.place(xy=(145, 280))
        # difficulties
        # 500 meter
        if road_distances.get(story_stage) == 500:
            if car_attributes.get(using_car)[2] * 2.5 + car_attributes.get(using_car)[0] \
                    > opponent_attributes.get(story_stage)[2] * 2.5 + opponent_attributes.get(story_stage)[0]:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Easy"
                difficultyRate_text.background = (0, 180, 0)

            elif (opponent_attributes.get(story_stage)[2] * 2.5 + opponent_attributes.get(story_stage)[0]) - 2 \
                <= car_attributes.get(using_car)[2] * 2.5 + car_attributes.get(using_car)[0] \
                    <= (opponent_attributes.get(story_stage)[2] * 2.5 + opponent_attributes.get(story_stage)[0]):
                difficultyRate_text.place(xy=(187, 335))
                difficultyRate_text.text = "Medium"
                difficultyRate_text.background = (230, 180, 30)

            else:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Hard"
                difficultyRate_text.background = (180, 0, 0)

        # 750 meter
        if road_distances.get(story_stage) == 750:
            if car_attributes.get(using_car)[2] * 1.75 + car_attributes.get(using_car)[0] * 1.25 \
                    > opponent_attributes.get(story_stage)[2] * 1.75 + opponent_attributes.get(story_stage)[0] * 1.25:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Easy"
                difficultyRate_text.background = (0, 180, 0)

            elif (opponent_attributes.get(story_stage)[2] * 1.75 + opponent_attributes.get(story_stage)[0] * 1.25) - 2 \
                <= car_attributes.get(using_car)[2] * 1.75 + car_attributes.get(using_car)[0] * 1.25 \
                    <= (opponent_attributes.get(story_stage)[2] * 1.75 + opponent_attributes.get(story_stage)[0]*1.25):
                difficultyRate_text.place(xy=(187, 335))
                difficultyRate_text.text = "Medium"
                difficultyRate_text.background = (230, 180, 30)

            else:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Hard"
                difficultyRate_text.background = (180, 0, 0)

        # 1000 meter
        if road_distances.get(story_stage) == 1000:
            if car_attributes.get(using_car)[2] * 1.5 + car_attributes.get(using_car)[0] * 1.5 \
                    > opponent_attributes.get(story_stage)[2] * 1.5 + opponent_attributes.get(story_stage)[0] * 1.5:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Easy"
                difficultyRate_text.background = (0, 180, 0)

            elif (opponent_attributes.get(story_stage)[2] * 1.5 + opponent_attributes.get(story_stage)[0] * 1.5) - 2 \
                <= car_attributes.get(using_car)[2] * 1.5 + car_attributes.get(using_car)[0] * 1.5 \
                    <= (opponent_attributes.get(story_stage)[2] * 1.5 + opponent_attributes.get(story_stage)[0]*1.5):
                difficultyRate_text.place(xy=(187, 335))
                difficultyRate_text.text = "Medium"
                difficultyRate_text.background = (230, 180, 30)

            else:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Hard"
                difficultyRate_text.background = (180, 0, 0)

        # 1250 meter
        if road_distances.get(story_stage) == 1250:
            if car_attributes.get(using_car)[2] * 1.25 + car_attributes.get(using_car)[0] * 1.75 \
                    > opponent_attributes.get(story_stage)[2] * 1.25 + opponent_attributes.get(story_stage)[0] * 1.75:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Easy"
                difficultyRate_text.background = (0, 180, 0)

            elif (opponent_attributes.get(story_stage)[2] * 1.25 + opponent_attributes.get(story_stage)[0] * 1.75) - 2 \
                <= car_attributes.get(using_car)[2] * 1.25 + car_attributes.get(using_car)[0] * 1.75 \
                    <= (opponent_attributes.get(story_stage)[2] * 1.25 + opponent_attributes.get(story_stage)[0]*1.75):
                difficultyRate_text.place(xy=(187, 335))
                difficultyRate_text.text = "Medium"
                difficultyRate_text.background = (230, 180, 30)

            else:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Hard"
                difficultyRate_text.background = (180, 0, 0)

        # 1500 meter
        if road_distances.get(story_stage) == 1500:
            if car_attributes.get(using_car)[2] + car_attributes.get(using_car)[0] * 2.5 \
                    > opponent_attributes.get(story_stage)[2] + opponent_attributes.get(story_stage)[0] * 2.5:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Easy"
                difficultyRate_text.background = (0, 180, 0)

            elif (opponent_attributes.get(story_stage)[2] + opponent_attributes.get(story_stage)[0] * 2.5) - 2 \
                <= car_attributes.get(using_car)[2] + car_attributes.get(using_car)[0] * 2.5 \
                    <= (opponent_attributes.get(story_stage)[2] + opponent_attributes.get(story_stage)[0] * 2.5):
                difficultyRate_text.place(xy=(187, 335))
                difficultyRate_text.text = "Medium"
                difficultyRate_text.background = (230, 180, 30)

            else:
                difficultyRate_text.place(xy=(200, 335))
                difficultyRate_text.text = "Hard"
                difficultyRate_text.background = (180, 0, 0)

        difficultyRate_text.render()

        if difficultyRate_text.text == "Hard":
            warning_img.place(xy=(155, 335))

        if warning_img.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            difficulty_warning.place(xy=(150, 200))

        road_distance_text.place(xy=(120, 425))
        road_distance_number_text.text = f"{road_distances.get(story_stage)} Meter"
        road_distance_number_text.render()

        if road_distances.get(story_stage) < 1000:
            road_distance_number_text.place(xy=(168, 475))
        else:
            road_distance_number_text.place(xy=(162, 475))

        stage_descriptions[story_stage].place(xy=(470, 120))

        go_button.place(xy=(window_x - 200, window_y - 120))

    elif menu == "before_race":
        def go_race():
            global menu, text_td, race_music_ot
            menu = "race"
            text_td = 0
            race_music_ot = 0
            menu_music.stop()

        window.fill(black)

        # race prepare
        prepare_td = 0

        # race settings
        race_start = False
        race_end = False
        winned = False
        finish_flag_x = window_x

        player_throttle = 0
        player_gear = 1
        player_kmh = 0
        player_maxspeed = 160 + car_attributes.get(using_car)[1] * 20
        player_progress = 0
        meter_stick_rotate = 0
        shifted = 0
        shift_quality = 0
        player_drown = 0
        player_acceleration = 1 + car_attributes.get(using_car)[2] * 2
        player_horsepower = car_attributes.get(using_car)[0] * 2 / 200

        opponent_car = story_stage
        opponent_kmh = 0
        opponent_x = 100
        opponent_progress = 0
        opponent_maxspeed = 160 + opponent_attributes.get(story_stage)[1] * 20

        shift_text_td = 0

        earned_money = 0
        perfect_shifts = 0
        good_shifts = 0
        top_speed = 0

        race_M = road_distances.get(story_stage)

        # story texts
        text_td += 1
        if story_stage == 0:
            if 40 <= text_td <= 120:
                before_text.place(True)
            elif 180 <= text_td <= 300:
                before_text.text = "-So you want to be a racer?"
                before_text.render()
                before_text.place(True)
            elif 380 <= text_td <= 480:
                before_text.text = "-Let's see your abilities!"
                before_text.render()
                before_text.place(True)
            elif 540 <= text_td <= 640:
                before_text.text = f"Stage: 1 (Preparing)"
                before_text.render()
                before_text.place(True)
            elif text_td == 680:
                go_race()

        if story_stage == 1:
            if 40 <= text_td <= 120:
                before_text.text = "-Hey, I'm Kevin."
                before_text.render()
                before_text.place(True)
            elif 180 <= text_td <= 340:
                before_text.text = "-It looks like it's our first race in the league."
                before_text.render()
                before_text.place(True)
            elif 460 <= text_td <= 560:
                before_text.text = "-And i will beat you. :)"
                before_text.render()
                before_text.place(True)
            elif 620 <= text_td <= 720:
                before_text.text = f"Stage: 1 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 760:
                go_race()

        if story_stage == 2:
            if 40 <= text_td <= 160:
                before_text.text = "-Hi, i am George. Nice to meet you."
                before_text.render()
                before_text.place(True)
            elif 170 <= text_td <= 340:
                before_text.text = "-Let's see which car of us is faster?"
                before_text.render()
                before_text.place(True)
            elif 420 <= text_td <= 520:
                before_text.text = "-Good luck. :)"
                before_text.render()
                before_text.place(True)
            elif 580 <= text_td <= 680:
                before_text.text = f"Stage: 2 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 720:
                go_race()

        if story_stage == 3:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 3 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 4:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 4 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 5:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 5 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 6:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 6 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 7:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 7 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 8:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 8 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 9:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 9 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 10:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 10 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 11:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 11 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 12:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 12 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 13:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 13 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 14:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 14 (League)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

        if story_stage == 15:
            if 40 <= text_td <= 160:
                before_text.text = f"Stage: 15 (League - FINAL)"
                before_text.render()
                before_text.place(True)
            elif text_td == 200:
                go_race()

    elif menu == "after_race":
        def return_play_menu():
            global menu, text_td, menu_music_ot
            menu = "play"
            text_td = 0
            menu_music_ot = 0
            race_music.stop()
            game_over_music.stop()

        window.fill(black)

        text_td += 1
        if story_stage == 1:
            if 40 <= text_td <= 140:
                before_text.text = "-Good job, racer."
                before_text.render()
                before_text.place(True)
            elif 220 <= text_td <= 380:
                before_text.text = "-Now you have a long way to go."
                before_text.render()
                before_text.place(True)
            elif 480 <= text_td <= 560:
                before_text.text = "-See you..."
                before_text.render()
                before_text.place(True)
            elif text_td == 640:
                return_play_menu()

        if story_stage == 2:
            if 40 <= text_td <= 140:
                before_text.text = "-Damn it!"
                before_text.render()
                before_text.place(True)
            elif 220 <= text_td <= 380:
                before_text.text = "-You were on your lucky day."
                before_text.render()
                before_text.place(True)
            elif 500 <= text_td <= 600:
                before_text.text = "-I'll see you later, lucky."
                before_text.render()
                before_text.place(True)
            elif text_td == 680:
                return_play_menu()

        if story_stage == 3:
            if 40 <= text_td <= 140:
                before_text.text = "-It was a good race, congratulations!"
                before_text.render()
                before_text.place(True)
            elif 220 <= text_td <= 360:
                before_text.text = "-You have potential, man. See you later..."
                before_text.render()
                before_text.place(True)
            elif text_td == 440:
                return_play_menu()

        if story_stage == 4:
            if text_td == 40:
                return_play_menu()

        if story_stage == 5:
            if text_td == 40:
                return_play_menu()

        if story_stage == 6:
            if text_td == 40:
                return_play_menu()

        if story_stage == 7:
            if text_td == 40:
                return_play_menu()

        if story_stage == 8:
            if text_td == 40:
                return_play_menu()

        if story_stage == 9:
            if text_td == 40:
                return_play_menu()

        if story_stage == 10:
            if text_td == 40:
                return_play_menu()

        if story_stage == 11:
            if text_td == 40:
                return_play_menu()

        if story_stage == 12:
            if text_td == 40:
                return_play_menu()

        if story_stage == 13:
            if text_td == 40:
                return_play_menu()

        if story_stage == 14:
            if text_td == 40:
                return_play_menu()

        if story_stage == 15:
            if 40 <= text_td <= 160:
                before_text.text = "-Wow, So you came up here!"
                before_text.render()
                before_text.place(True)
            elif 220 <= text_td <= 320:
                before_text.text = "-Good luck, racer..."
                before_text.render()
                before_text.place(True)
            elif text_td == 400:
                return_play_menu()

        if story_stage == 16:
            if text_td == 10:
                win_sound.stop()
                game_over_music.play()

            elif 40 <= text_td <= 220:
                before_text.text = "YOUU WINNNNNNNNNNN!!!!!!!!"
                before_text.render()
                before_text.place(True)

            elif 300 <= text_td <= 400:
                before_text.text = "-Nice job, racer."
                before_text.render()
                before_text.place(True)

            elif 440 <= text_td <= 540:
                before_text.text = "-You impressed me!"
                before_text.render()
                before_text.place(True)

            elif 600 <= text_td <= 700:
                before_text.text = "-See you in the future..."
                before_text.render()
                before_text.place(True)

            elif 840 <= text_td <= 1000:
                before_text.text = "Ace Drag Race"
                before_text.size = 40
                before_text.color = (200, 100, 60)
                before_text.render()
                before_text.place(True)

            elif 1080 <= text_td <= 1200:
                before_text.text = "Made by 'Eorhan23'"
                before_text.render()
                before_text.place(True)

            elif text_td == 1400:
                return_play_menu()

    elif menu == "race":

        if race_music_ot == 0:
            if story_stage == 15:
                final_match_music.play(-1)
            else:
                race_music.play(-1)
        race_music_ot = 1

        if prepare_td <= 500:
            prepare_td += 1

        if prepare_td == 440:
            race_start = True

        # place objects
        race_background.place(xy=(race_background_x, 0))
        race_background2.place(xy=(race_background2_x, 0))
        road.place(True, (road_x, -25))
        road2.place(True, (road2_x, -25))

        if 40 < prepare_td < 200:
            you_img.place(xy=(250, 300))

        tachometer.place(xy=(640, 340))
        gear_img.place(xy=(825, 460))

        pygame.draw.rect(window, (17, 23, 65), (800, 500, 65, 30))
        pygame.draw.rect(window, (27, 33, 95), (797, 497, 69, 34), 4)

        gear_text.place(xy=(810, 467))
        gear_text.text = str(player_gear)
        gear_text.render()

        kmh_number.place(xy=(817, 506))
        kmh_number.text = str(int(player_kmh))
        kmh_number.render()

        kmh_text.place(xy=(815, 545))

        window.blit(pygame.transform.rotozoom(meter_stick.image, meter_stick_rotate, 1),
                    pygame.transform.rotozoom(meter_stick.image, meter_stick_rotate, 1).get_rect(center=(770, 465)))

        if player_progress > race_M - 60:
            finish_flag.place(True, (finish_flag_x, -25))
            finish_flag_x -= player_kmh / 15
            if car_images[using_car].rect.colliderect(finish_flag.rect):
                if race_end_ot == 0:
                    if player_progress > opponent_progress:
                        winned = True
                        you_won_lost_text.text = "YOU WON!"

                    elif opponent_progress > player_progress:
                        winned = False
                        you_won_lost_text.text = "YOU LOST!"
                    else:
                        winned = False
                        you_won_lost_text.text = "YOU LOST!"

                    top_speed = int(player_kmh)
                    if winned:
                        earned_money = 15000 * story_stage + 200 * perfect_shifts + 50 * good_shifts + top_speed
                    else:
                        earned_money = 2000 * story_stage + 200 * perfect_shifts + 50 * good_shifts + top_speed

                    earned_money_text.text = f"Earned money: {earned_money}"
                    perfect_shifts_text.text = f"Perfect shifts: {perfect_shifts}"
                    top_speed_text.text = f"Top speed: {top_speed}"
                    earned_money_text.render()
                    perfect_shifts_text.render()
                    top_speed_text.render()
                    you_won_lost_text.render()

                    race_end = True

                race_end_ot = 1

        car_images[using_car].place(xy=(100, 300))  # player car

        if story_stage == 0:
            car_images2[opponent_car].place(xy=(opponent_x, 190))  # opponent car
        else:
            car_images2[opponent_car - 1].place(xy=(opponent_x, 190))  # opponent car

        pygame.draw.rect(window, black, (0, 25, window_x, 10))
        pygame.draw.rect(window, black, (0, 70, window_x, 10))

        # start lights
        if 200 < prepare_td < 500:
            pygame.draw.rect(window, black, (330, 255, 240, 90))
            pygame.draw.circle(window, (90, 15, 15), (370, 300), 35)
            pygame.draw.circle(window, (90, 15, 15), (450, 300), 35)
            pygame.draw.circle(window, (90, 15, 15), (530, 300), 35)

            if 260 < prepare_td < 500:
                pygame.draw.circle(window, (200, 20, 20), (370, 300), 35)

            if 320 < prepare_td < 500:
                pygame.draw.circle(window, (200, 20, 20), (450, 300), 35)

            if 380 < prepare_td < 500:
                pygame.draw.circle(window, (200, 20, 20), (530, 300), 35)

            if 440 < prepare_td < 500:
                pygame.draw.circle(window, (40, 220, 30), (370, 300), 35)
                pygame.draw.circle(window, (40, 220, 30), (450, 300), 35)
                pygame.draw.circle(window, (40, 220, 30), (530, 300), 35)
                go_text.place(True, (0, -50))

        if prepare_td == 256:
            ready_sound.play()

        if prepare_td == 316:
            ready_sound.play()

        if prepare_td == 376:
            ready_sound.play()

        if prepare_td == 436:
            go_sound.play()

        # player progress
        if player_progress < race_M:
            pygame.draw.circle(window, car_colors.get(using_car), (player_progress * (90 / (race_M / 10)), 74.5), 9)
        else:
            pygame.draw.circle(window, car_colors.get(using_car), (900, 74.5), 9)

        # opponent progress
        if story_stage == 0:
            if opponent_progress < race_M:
                pygame.draw.circle(window, car_colors.get(opponent_car), (
                    opponent_progress * (90 / (race_M / 10)), 29.5), 9)
            else:
                pygame.draw.circle(window, car_colors.get(opponent_car), (900, 29.5), 9)
        else:
            if opponent_progress < race_M:
                pygame.draw.circle(window, car_colors.get(opponent_car - 1), (
                    opponent_progress * (90 / (race_M / 10)), 29.5), 9)
            else:
                pygame.draw.circle(window, car_colors.get(opponent_car - 1), (900, 29.5), 9)

        # objects movement
        race_background_x -= player_kmh / 15
        race_background2_x -= player_kmh / 15
        opponent_x += (opponent_kmh - player_kmh) / 15
        road_x -= player_kmh / 15
        road2_x -= player_kmh / 15

        if race_background_x <= window_x - window_x * 2:
            race_background_x = window_x

        if race_background2_x <= window_x - window_x * 2:
            race_background2_x = window_x

        if race_background_x <= 00:
            race_background2_x = race_background.rect.right - (player_kmh / 10)

        if race_background2_x <= 0:
            race_background_x = race_background2.rect.right - (player_kmh / 10)

        if road_x <= window_x - window_x * 2:
            road_x = window_x

        if road2_x <= window_x - window_x * 2:
            road2_x = window_x

        if road_x <= 00:
            road2_x = road.rect.right - (player_kmh / 10)

        if road2_x <= 0:
            road_x = road2.rect.right - (player_kmh / 10)

        # RACING
        if race_start:
            keys = pygame.key.get_pressed()
            if not race_end:
                if keys[pygame.K_UP] and player_kmh < player_maxspeed and player_throttle < 80 and shifted == 0:
                    player_throttle += (((3 + car_attributes.get(using_car)[2] * 1.5) / (
                            player_kmh / 2 + 10)) + car_attributes.get(using_car)[0] / 150) / (
                            (player_drown + 10 + player_gear) / 10)
                    player_kmh += ((car_attributes.get(using_car)[2] * 2 / (player_kmh + 10)) + car_attributes.get(
                        using_car)[0] * 2 / 200) / ((player_drown + 10) / 10)

                    player_drown -= car_attributes.get(using_car)[0] * 2 / 100

            # dynamics
            player_progress += (player_kmh / race_M) * 4
            meter_stick_rotate = -player_throttle * 3.3

            # opponent
            opponent_progress += (opponent_kmh / race_M) * 4
            opponent_kmh += ((opponent_attributes.get(opponent_car)[2] * 2 / (
                    opponent_kmh + 10)) + opponent_attributes.get(opponent_car)[0] * 2 / 200)

            # gear shift
            if shifted > 0:
                shifted += 1
                player_throttle -= 1

                if shift_quality == 1:
                    player_kmh += (1 + car_attributes.get(using_car)[0] / 2) / (20 + (player_kmh / 20))
                    player_drown -= 0.2

                if shift_quality == 2:
                    player_kmh += (1 + car_attributes.get(using_car)[0] / 2) / (12 + (player_kmh / 20))
                    player_drown -= 0.35

                if shifted > 30 + car_attributes.get(using_car)[0] / 2:
                    shifted = 0

            if shift_text_td > 0:
                shift_text_td += 1
                shift_text.place(xy=(500, 560))

                if shift_text_td == 120:
                    shift_text_td = 0

            # fix
            if player_throttle > 80:
                player_throttle = 80

            if player_throttle < 0:
                player_throttle = 0

            if player_kmh > player_maxspeed:
                player_kmh = player_maxspeed

            if player_drown < 0:
                player_drown = 0

            if opponent_kmh > opponent_maxspeed:
                opponent_kmh = opponent_maxspeed

        if race_end:
            window.blit(race_end_screen, (0, 0))

            prepare_td = 0
            text_td = 0

            race_music.stop()
            final_match_music.stop()
            if winlose_sound_ot == 0:
                if winned:
                    win_sound.play()
                else:
                    lose_sound.play()
            winlose_sound_ot = 1

            you_won_lost_text.place(True, (0, -200))
            earned_money_text.place(True, (0, -75))
            perfect_shifts_text.place(True, (0, 0))
            top_speed_text.place(True, (0, 75))
            next_button.place(True, (0, 200))

    # similar menu codes
    money_text.text = str(money)
    money_text.render()

    click1_sound.set_volume(sound_volume)
    click2_sound.set_volume(sound_volume)
    click3_sound.set_volume(sound_volume)
    buy_sound.set_volume(sound_volume)
    warning_sound.set_volume(sound_volume)
    menu_music.set_volume(music_volume)
    race_music.set_volume(music_volume)
    win_sound.set_volume(sound_volume)
    lose_sound.set_volume(sound_volume)
    ready_sound.set_volume(sound_volume)
    go_sound.set_volume(sound_volume)

    # events
    for event in pygame.event.get():  # quit event
        if event.type == pygame.QUIT:
            save_game()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            try:
                if not race_end:
                    if event.key == pygame.K_SPACE:
                        if player_gear < 7 and player_kmh < player_maxspeed:
                            shifted = 1
                            player_gear += 1

                            if 59 < player_throttle < 63:
                                shift_quality = 2
                                shift_text.text = "Perfect shift"
                                shift_text.render()
                                shift_text_td = 1
                                perfect_shifts += 1

                            elif 54 < player_throttle < 60:
                                shift_quality = 1
                                shift_text.text = "Good shift"
                                shift_text.render()
                                shift_text_td = 1
                                good_shifts += 1

                            else:
                                shift_quality = 0

                            player_drown += 60 - (player_throttle + 1)
            except NameError:
                pass

        if event.type == pygame.MOUSEBUTTONDOWN:  # single button clicks
            if play_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "main":
                click3_sound.play()
                menu = "save game loading"

            if about_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "main":
                click3_sound.play()
                menu = "about"

            if back_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if menu == "about" or menu == "play":
                    click3_sound.play()
                    menu = "main"
                elif menu == "settings" or menu == "garage" or menu == "story_mode" or menu == "help":
                    click3_sound.play()
                    menu = "play"
                elif menu == "store":
                    click3_sound.play()
                    current_car = using_car
                    menu = "garage"

            if settings_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "play":
                click3_sound.play()
                menu = "settings"

            if help_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "play":
                click3_sound.play()
                menu = "help"

            if garage_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "play":
                click2_sound.play()
                current_car = using_car
                menu = "garage"

            if right_arrow.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if menu == "garage":
                    click1_sound.play()
                    if not owned_cars.index(current_car) >= len(owned_cars) - 1:
                        current_car = owned_cars[owned_cars.index(current_car) + 1]

                elif menu == "store":
                    click1_sound.play()
                    if not buyable_cars.index(current_car) >= len(buyable_cars) - 1:
                        current_car = buyable_cars[buyable_cars.index(current_car) + 1]

            if left_arrow.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if menu == "garage":
                    click1_sound.play()
                    if owned_cars.index(current_car) > 0:
                        current_car = owned_cars[owned_cars.index(current_car) - 1]

                elif menu == "store":
                    click1_sound.play()
                    if buyable_cars.index(current_car) > 0:
                        current_car = buyable_cars[buyable_cars.index(current_car) - 1]

            if horsepower_upgrade.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "garage":
                if money >= upgrade_cost and car_upgrades.get(current_car)[0] == False:
                    buy_sound.play()
                    money -= upgrade_cost
                    car_upgrades[current_car][0] = True
                    car_attributes[current_car][0] += 1
                else:
                    warning_sound.play()

            if maxspeed_upgrade.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "garage":
                if money >= upgrade_cost and car_upgrades.get(current_car)[1] == False:
                    buy_sound.play()
                    money -= upgrade_cost
                    car_upgrades[current_car][1] = True
                    car_attributes[current_car][1] += 1
                else:
                    warning_sound.play()

            if acceleration_upgrade.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "garage":
                if money >= upgrade_cost and car_upgrades.get(current_car)[2] == False:
                    buy_sound.play()
                    money -= upgrade_cost
                    car_upgrades[current_car][2] = True
                    car_attributes[current_car][2] += 1
                else:
                    warning_sound.play()

            if use_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "garage":
                if not current_car == using_car:
                    click2_sound.play()
                    using_car = current_car

            if buycar_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "garage":
                if len(buyable_cars) != 0:
                    click2_sound.play()
                    menu = "store"
                    current_car = buyable_cars[0]
                else:
                    warning_sound.play()

            if buy_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "store":
                if money >= car_costs.get(current_car):
                    buy_sound.play()
                    money -= car_costs.get(current_car)
                    owned_cars.append(current_car)
                    owned_cars.sort()
                    buyable_cars.remove(current_car)
                    menu = "garage"
                else:
                    warning_sound.play()

            if storymode_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "play":
                if story_stage == 16:
                    warning_sound.play()
                else:
                    click2_sound.play()
                    menu = "story_mode"

            if go_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "story_mode":
                click2_sound.play()
                menu = "before_race"

            if next_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "race" and race_end:
                click3_sound.play()
                text_td = 0
                money += earned_money
                winlose_sound_ot = 0
                race_end_ot = 0

                if you_won_lost_text.text == "YOU WON!":
                    menu = "after_race"
                    story_stage += 1
                else:
                    menu = "play"
                    menu_music_ot = 0

                save_game()

            if save_game_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and menu == "settings":
                click2_sound.play()
                save_game()
                saved_text_delay = 1

    # update screen
    pygame.display.update()
    fps.tick(60)
