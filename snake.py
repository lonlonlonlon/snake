# To install pygame, type 'pip install pygame' in the
# windows powershell or the os terminal

# To create a blank screen as a setup for a game, use:
import math
import os
import random
import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

FPS = 15  # How many times the screen will update per second

screen_width = 1000  # How wide the window will be
screen_height = 1000  # how high the window will be
rows = 60  # x
cols = 60  # y

screen = pygame.display.set_mode((screen_width, screen_height))  # creates the screen
draw_array = []
for x in range(rows):
    tmp = []
    for y in range(cols):
        tmp.append('h')
    draw_array.append(tmp)
for x in range(rows):
    for y in range(cols):
        if x == 0 or x == rows-1 or y == 0 or y == cols-1 or x == 1 or x == rows-2 or y == 1 or y == cols-2:
            draw_array[x][y] = 'r'

draw_array[int(rows/2)][int(cols/2)] = 's'  # set snake start position
snake_head = (int(rows/2), int(cols/2))
snake_body = []
snake_body_color = []
score = 0
snake_length = 6
snake_direction = 'up'
blue = (0, 0, 200)
light_blue = (100, 100, 255)
dark_blue = (0, 0, 80)
cyan = (0, 200, 200)
green = (0, 200, 0)
light_green = (100, 255, 100)
dark_green = (0, 80, 0)
red = (200, 0, 0)
light_red = (255, 100, 100)
dark_red = (80, 0, 0)
yellow = (200, 200, 0)
purple = (80, 0, 80)
orange = (200, 100, 0)
black = (0, 0, 0)
dark_grey = (80, 80, 80)
grey = (110, 110, 110)
light_grey = (160, 160, 160)
white = (255, 255, 255)
small_rainbow_color_order = [blue, purple, red, orange, yellow, green, cyan]
large_rainbow_color_order = [light_blue, blue, dark_blue, purple, dark_red, red, light_red,
                             orange, yellow, light_green, green, dark_green, cyan]
color_order = small_rainbow_color_order
color_order_string = "smoll-rainbow"
color_order_dict = {"smoll-rainbow": small_rainbow_color_order, "grosse-rainbow": large_rainbow_color_order}
color_state = 0
color_assignment = {'r': dark_grey, 's': white, 'h': black, 'f': green, '5': light_green, 'l': light_blue}
rect_size = screen_width/rows
orientation_no_go_dict = {'up':'down','down':'up','left':'right','right':'left'}
already_turned_head = False
food_location = ()
food_type = ''
food_ttl = 0
food_color_rotation = [dark_grey, grey, light_grey, grey]
food_5_color_rotation = [yellow, white, yellow, light_green]
rect_size_ciel = math.ceil(rect_size)
width_draw_unit = screen_width / 40
height_draw_unit = screen_height / 40
title_text_size = math.floor(screen_width / 20)
medium_text_size = math.floor(screen_width / 23)
small_text_size = math.floor(screen_width / 30)
play_rect = pygame.Rect
death_menue_rect = pygame.Rect
options_rect = pygame.Rect
exit_rect = pygame.Rect
options_speed_up_rect = pygame.Rect
options_speed_down_rect = pygame.Rect
options_color_order_change_rect = pygame.Rect
options_back_rect = pygame.Rect
hit_sound = pygame.mixer.Sound(os.getcwd() + "/hit.wav")
select_1_sound = pygame.mixer.Sound(os.getcwd() + "/blipSelect.wav")
select_2_sound = pygame.mixer.Sound(os.getcwd() + "/blipSelect2.wav")
small_food_sound = pygame.mixer.Sound(os.getcwd() + "/small_food.wav")
blip_sounds = [select_2_sound, select_1_sound]
power_up_sound = pygame.mixer.Sound(os.getcwd() + "/powerUp.wav")
# pygame.mixer.music.load(os.getcwd() + "/MagicHappensSong.flac") // windows hat trouble mit flac
snake_turn_sound = pygame.mixer.Sound(os.getcwd() + "/snake_turn.wav")
sound_enabled = True
# pygame.mixer.music.play(-1)
# r = Rand
# h = Hintergrund
# s = Schlangenkopf
# b = snake Body
# f = food
# 5 = special food (5% chance of spawning instead of norm. food, gives 5 length and 3 pts) || has ttl of 350 Frames
# // planned ----------
# l = Lurchgeschwindigkeit!!!!! // powerup zeitbegrenzt erhöhte geschwindigkeit und mehr punkte!

# PIPELINE FÜR KEY INPUTS; JEDEN FRAME EINS NEHMEN UND ENTFERNEN (max 3)
# bei score 100 dicken Apfel aus mehreren essen spawnen und hoher speed mit unverwundbarkeit (alles zeitbegrenzt)

def play_blip_sound():
    rnd = random.randint(0, len(blip_sounds) -1)
    pygame.mixer.Sound.play(blip_sounds[rnd])

def get_color(x, y):
    color = draw_array[x][y]
    if color == 'b':
        return red
    else:
        return color_assignment[color]

# def get_color(x, y): # freaky
#     color = draw_array[x][y]
#     if color == 'b':
#         return next_color()
#     else:
#         return color_assignment[color]


def spawn_food():
    global draw_array
    global food_location
    global food_type
    global food_ttl
    rnd = random.randint(1, rows-2), random.randint(1, cols-2)
    while draw_array[rnd[0]][rnd[1]] != 'h':
        rnd = random.randint(1, rows-2), random.randint(1, cols-2)
    if random.randint(0, 9) == 1:
        draw_array[rnd[0]][rnd[1]] = '5'
        food_type = '5'
        food_ttl = 100
    else:
        draw_array[rnd[0]][rnd[1]] = 'f'
        food_type = 'f'
        food_ttl = -1
    food_location = rnd


def redraw_snake():
    global snake_body
    global snake_body_color
    global rect_size
    global screen
    for i in range(len(snake_body)):
        pos = snake_body[i]
        col = snake_body_color[i]
        pygame.draw.rect(screen, col, pygame.Rect(pos[0] * rect_size, pos[1] * rect_size, rect_size_ciel, rect_size_ciel))


def redraw_food():
    global food_location
    global rect_size
    global screen
    global food_5_color_rotation
    if food_type == 'f':
        col = food_color_rotation.pop(0)
        pygame.draw.rect(screen, col, pygame.Rect(math.floor(food_location[0] * rect_size), math.floor(food_location[1] * rect_size), rect_size_ciel, rect_size_ciel))
        food_color_rotation.append(col)
    if food_type == '5':
        col = food_5_color_rotation.pop(0)
        pygame.draw.rect(screen, col, pygame.Rect(math.floor(food_location[0] * rect_size), math.floor(food_location[1] * rect_size), rect_size_ciel, rect_size_ciel))
        food_5_color_rotation.append(col)


def draw_text_overlay():
    set_text("score: " + str(score), math.floor(rows/2 * rect_size), rect_size, small_text_size, white)


def draw_border_markings():
    global snake_head
    x = snake_head[0]
    y = snake_head[1]
    if x == food_location[0]:
        pygame.draw.rect(screen, dark_green, pygame.Rect(math.floor(x * rect_size), math.floor(2 * rect_size), rect_size_ciel, rect_size_ciel))
        pygame.draw.rect(screen, dark_green, pygame.Rect(math.floor(x * rect_size), math.floor((cols - 2) * rect_size), rect_size_ciel, rect_size_ciel))
    else:
        pygame.draw.rect(screen, dark_red, pygame.Rect(math.floor(x * rect_size), math.floor(2 * rect_size), rect_size_ciel, rect_size_ciel))
        pygame.draw.rect(screen, dark_red, pygame.Rect(math.floor(x * rect_size), math.floor((cols - 2) * rect_size), rect_size_ciel, rect_size_ciel))
    if y == food_location[1]:
        pygame.draw.rect(screen, dark_green, pygame.Rect(math.floor(0 * rect_size), math.floor(y * rect_size), rect_size_ciel, rect_size_ciel))
        pygame.draw.rect(screen, dark_green, pygame.Rect(math.floor((rows - 1) * rect_size), math.floor(y * rect_size), rect_size_ciel, rect_size_ciel))
    else:
        pygame.draw.rect(screen, dark_red, pygame.Rect(math.floor(0 * rect_size), math.floor(y * rect_size), rect_size_ciel, rect_size_ciel))
        pygame.draw.rect(screen, dark_red, pygame.Rect(math.floor((rows - 1) * rect_size), math.floor(y * rect_size), rect_size_ciel, rect_size_ciel))


def draw():
    for x_d in range(rows):
        for y_d in range(cols):
            color = get_color(x_d, y_d)
            pygame.draw.rect(screen, color, pygame.Rect(math.floor(x_d * rect_size), math.floor(y_d * rect_size), rect_size_ciel, rect_size_ciel))
    redraw_snake()
    redraw_food()
    draw_border_markings()
    draw_text_overlay()
    pygame.display.flip()


def reset_game():
    global draw_array
    draw_array = []
    for x in range(rows):
        tmp = []
        for y in range(cols):
            tmp.append('h')
        draw_array.append(tmp)
    for x in range(rows):
        for y in range(cols):
            if x == 0 or x == rows - 1 or y == 0 or y == cols - 1 or y == 1 or y == cols - 2 or y == 2:
                draw_array[x][y] = 'r'

    draw_array[int(rows / 2)][int(cols / 2)] = 's'  # set snake start position
    global snake_head
    snake_head = (int(rows / 2), int(cols / 2))
    global snake_body
    snake_body = []
    global snake_body_color
    snake_body_color = []
    global score
    score = 0
    global snake_length
    snake_length = 6
    global snake_direction
    snake_direction = 'up'
    global color_state
    color_state = 0
    global already_turned_head
    already_turned_head = False
    global food_location
    food_location = ()
    spawn_food()


def death_screen():
    global screen
    global death_menue_rect
    while True:
        clock.tick(60)  # updates the screen, the amount of times it does so depends on the FPS
        pos = pygame.mouse.get_pos()
        screen.fill(black)
        set_text("OOPS, u ded :(", width_draw_unit * 20,
                 height_draw_unit * 8, medium_text_size, orange)
        set_text("score: " + str(score), width_draw_unit * 20,
                 height_draw_unit * 12, medium_text_size, blue)
        death_menue_rect = set_text("-> Main Menue", width_draw_unit * 20,
                 height_draw_unit * 17, medium_text_size, green)
        if death_menue_rect.collidepoint(pos):
            death_menue_rect = set_text("-> Main Menue", width_draw_unit * 20,
                                        height_draw_unit * 17, medium_text_size, red)
        death_exit_rect = set_text("-> brEXXIT Oo", width_draw_unit * 20,
                                    height_draw_unit * 20, medium_text_size, green)
        if death_exit_rect.collidepoint(pos):
            death_exit_rect = set_text("-> brEXXIT Oo", width_draw_unit * 20,
                                       height_draw_unit * 20, medium_text_size, red)
        pygame.display.flip()
        for event in pygame.event.get():  # Allows you to add various events
            if event.type == pygame.QUIT:  # Allows the user to exit using the X button
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if death_menue_rect.collidepoint(pos):
                        play_blip_sound()
                        reset_game()
                        menue()
                    if death_exit_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()


def play_hit_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(hit_sound)


def die():
    play_hit_sound()
    death_screen()

def next_color():
    global color_state
    global color_order
    if color_state == len(color_order):
        color_state = 0
    ret = color_order[color_state]
    color_state += 1
    return ret


def play_small_food_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(small_food_sound)


def play_power_up_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(power_up_sound)


def try_move_snake(x, y):
    global snake_head
    global snake_body
    global draw_array
    global snake_length
    global score
    if x > rows or x < 0 or y > cols or y < 0:
        die()
    if draw_array[x][y] == 'r' or draw_array[x][y] == 'b':
        die()
    if draw_array[x][y] == 'f':
        snake_length += 1
        play_small_food_sound()
        score += 1
        spawn_food()
    if draw_array[x][y] == '5':
        snake_length += 5
        play_power_up_sound()
        score += 3
        spawn_food()
    snake_body.append(snake_head)
    snake_body_color.append(next_color())
    snake_head = (x, y)
    draw_array[x][y] = 's'


def do_movement():
    global snake_head
    global snake_body
    if snake_direction == 'up':
        try_move_snake(snake_head[0], snake_head[1] + 1)
    if snake_direction == 'down':
        try_move_snake(snake_head[0], snake_head[1] - 1)
    if snake_direction == 'left':
        try_move_snake(snake_head[0] - 1, snake_head[1])
    if snake_direction == 'right':
        try_move_snake(snake_head[0] + 1, snake_head[1])
    if len(snake_body) > snake_length:
        pos = snake_body.pop(0)
        snake_body_color.pop(0)
        draw_array[pos[0]][pos[1]] = 'h'
    for pos in snake_body:
        draw_array[pos[0]][pos[1]] = 'b'


def change_snake_direction(direction):
    global snake_direction
    global already_turned_head
    if already_turned_head:
        return
    if orientation_no_go_dict[snake_direction] == direction:
        return
    # pygame.mixer.Sound.play(snake_turn_sound)
    snake_direction = direction
    already_turned_head = True


def item_logic_cycle():
    global food_ttl
    food_ttl -= 1
    if food_ttl == 0:
        draw_array[food_location[0]][food_location[1]] = 'h'
        spawn_food()


def game_loop():
    global FPS
    global already_turned_head
    while True:
        clock.tick(FPS)  # updates the screen, the amount of times it does so depends on the FPS
        do_movement()
        item_logic_cycle()
        draw()
        already_turned_head = False
        for event in pygame.event.get():  # Allows you to add various events
            if event.type == pygame.QUIT:  # Allows the user to exit using the X button
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    change_snake_direction('down')
                if event.key == pygame.K_s:
                    change_snake_direction('up')
                if event.key == pygame.K_a:
                    change_snake_direction('left')
                if event.key == pygame.K_d:
                    change_snake_direction('right')


def set_text(string, coordx, coordy, fontSize, color): #Function to set text
    global screen
    font = pygame.font.Font(os.getcwd() + '/04B_30__.TTF', fontSize)
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, color)
    textRect = text.get_rect()
    textRect.center = (coordx, coordy)
    screen.blit(text, textRect)
    return textRect


def options_menue():
    global screen
    global options_speed_up_rect
    global options_speed_down_rect
    global FPS
    global options_color_order_change_rect
    global color_order
    global color_order_string
    global color_order_dict
    global options_back_rect
    while True:
        clock.tick(60)  # updates the screen, the amount of times it does so depends on the FPS
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(black)
        set_text("Optionen der Snake", width_draw_unit * 20, height_draw_unit * 4, title_text_size, cyan)
        set_text("Schlang-schpeed: " + str(FPS), width_draw_unit * 17, height_draw_unit * 8, small_text_size,
                green)
        set_text("Schlang-farb: " + color_order_string, width_draw_unit * 17, height_draw_unit * 10, small_text_size,
                 green)
        options_back_rect = set_text("-> Bekk", width_draw_unit * 20, height_draw_unit * 35, small_text_size,
                 green)
        if options_back_rect.collidepoint(mouse_pos):
            options_back_rect = set_text("-> Bekk", width_draw_unit * 20, height_draw_unit * 35, small_text_size,
                                         red)
        options_speed_up_rect = set_text(">", width_draw_unit * 34,
                                         height_draw_unit * 8, medium_text_size, green)
        if options_speed_up_rect.collidepoint(mouse_pos):
            options_speed_up_rect = set_text(">", width_draw_unit * 34,
                                             height_draw_unit * 8, medium_text_size, red)
        options_speed_down_rect = set_text("<", width_draw_unit * 32,
                                         height_draw_unit * 8, medium_text_size, green)
        if options_speed_down_rect.collidepoint(mouse_pos):
            options_speed_down_rect = set_text("<", width_draw_unit * 32,
                                             height_draw_unit * 8, medium_text_size, red)
        options_color_order_change_rect = set_text(">", width_draw_unit * 34,
                                           height_draw_unit * 10, medium_text_size, green)
        if options_color_order_change_rect.collidepoint(mouse_pos):
            options_color_order_change_rect = set_text(">", width_draw_unit * 34,
                                                       height_draw_unit * 10, medium_text_size, red)

        pygame.display.flip()
        for event in pygame.event.get():  # Allows you to add various events
            if event.type == pygame.QUIT:  # Allows the user to exit using the X button
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if options_speed_up_rect.collidepoint(mouse_pos):
                        if FPS != 100:
                            play_blip_sound()
                            FPS += 1
                        else:
                            play_hit_sound()
                    if options_speed_down_rect.collidepoint(mouse_pos):
                        if FPS != 3:
                            play_blip_sound()
                            FPS -= 1
                        else:
                            play_hit_sound()
                    if options_color_order_change_rect.collidepoint(mouse_pos):
                        play_blip_sound()
                        temp = list(color_order_dict.items())
                        index = [idx for idx, key in enumerate(temp) if key[0] == color_order_string][0]
                        if index + 1 > len(color_order_dict) -1:
                            index = 0
                        else:
                            index += 1
                        keys = list(color_order_dict.keys())
                        color_order_string = keys[index]
                        color_order = color_order_dict[keys[index]]
                    if options_back_rect.collidepoint(mouse_pos):
                        play_blip_sound()
                        menue()



def process_menue_mouse_click():
    global exit_rect
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    if play_rect.collidepoint(pos):
        play_blip_sound()
        game_loop()
        return
    if options_rect.collidepoint(pos):
        play_blip_sound()
        options_menue()
        return
    if exit_rect.collidepoint(pos):
        pygame.quit()
        sys.exit()


def draw_menue():
    global play_rect
    global options_rect
    global exit_rect
    screen.fill((0, 0, 0))
    set_text("Die Snake geht WiLd!", width_draw_unit * 20, height_draw_unit * 4, title_text_size, cyan)
    play_rect = set_text("-> Schlange spielen", width_draw_unit * 20, height_draw_unit * 14, medium_text_size, green)
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos):
        play_rect = set_text(
            "-> Schlange spielen", width_draw_unit * 20, height_draw_unit * 14, medium_text_size, red)
    options_rect = set_text("-> Schlangenoptionen", width_draw_unit * 20,
                            height_draw_unit * 17, medium_text_size, green)
    if options_rect.collidepoint(mouse_pos):
        options_rect = set_text("-> Schlangenoptionen", width_draw_unit * 20,
                                height_draw_unit * 17, medium_text_size, red)
    exit_rect = set_text("-> brEXXIT oO", width_draw_unit * 20,
                            height_draw_unit * 20, medium_text_size, green)
    if exit_rect.collidepoint(mouse_pos):
        exit_rect = set_text("-> brEXXIT oO", width_draw_unit * 20,
                                height_draw_unit * 20, medium_text_size, red)
    pygame.display.flip()


def menue():
    global screen
    screen.fill((0, 0, 0))
    while True:
        draw_menue()
        clock.tick(60)  # updates the screen, the amount of times it does so depends on the FPS
        for event in pygame.event.get():  # Allows you to add various events
            if event.type == pygame.QUIT:  # Allows the user to exit using the X button
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    process_menue_mouse_click()

reset_game()
menue()

#------------------------#
# 1 - left click
# 2 - middle click
# 3 - right click
# 4 - scroll up
# 5 - scroll down
#------------------------#