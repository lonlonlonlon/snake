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
cyan = (0, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
yellow = (200, 200, 0)
purple = (200, 0, 200)
orange = (200, 100, 0)
black = (0, 0, 0)
dark_grey = (80, 80, 80)
grey = (110, 110, 110)
light_grey = (160, 160, 160)
white = (255, 255, 255)
color_order = [blue, purple, red, orange, yellow, green, cyan]
color_state = 0
color_assignment = {'r': dark_grey, 's': white, 'h': black, 'f': green}
rect_size = screen_width/rows
orientation_no_go_dict = {'up':'down','down':'up','left':'right','right':'left'}
already_turned_head = False
food_location = ()
food_color_rotation = [dark_grey, grey, light_grey, grey]
rect_size_ciel = math.ceil(rect_size)
width_draw_unit = screen_width / 40
height_draw_unit = screen_height / 40
title_text_size = math.floor(screen_width / 20)
medium_text_size = math.floor(screen_width / 23)
small_text_size = math.floor(screen_width / 30)
play_rect = pygame.Rect
death_menue_rect = pygame.Rect
options_rect = pygame.Rect
# r = Rand
# h = Hintergrund
# s = Schlangenkopf
# b = snake Body
# f = food


def init_snake():
    global draw_array
    draw_array = []
    for x in range(rows):
        tmp = []
        for y in range(cols):
            tmp.append('h')
        draw_array.append(tmp)
    for x in range(rows):
        for y in range(cols):
            if x == 0 or x == rows-1 or y == 0 or y == cols-1 or y == 1 or y == cols-2:
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
    rnd = random.randint(1, rows-2), random.randint(1, cols-2)
    while draw_array[rnd[0]][rnd[1]] != 'h':
        rnd = random.randint(1, rows-2), random.randint(1, cols-2)
    draw_array[rnd[0]][rnd[1]] = 'f'
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
    col = food_color_rotation.pop(0)
    pygame.draw.rect(screen, col, pygame.Rect(math.floor(food_location[0] * rect_size), math.floor(food_location[1] * rect_size), rect_size_ciel, rect_size_ciel))
    food_color_rotation.append(col)


def draw_text_overlay():
    set_text("score: " + str(score), math.floor(rows/2 * rect_size), rect_size, small_text_size, white)


def draw():
    for x_d in range(rows):
        for y_d in range(cols):
            color = get_color(x_d, y_d)
            pygame.draw.rect(screen, color, pygame.Rect(math.floor(x_d * rect_size), math.floor(y_d * rect_size), rect_size_ciel, rect_size_ciel))
    redraw_snake()
    redraw_food()
    draw_text_overlay()
    pygame.display.flip()


def death_screen():
    global screen
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
                        menue()
                    if death_exit_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()


def die():
    death_screen()

def next_color():
    global color_state
    global color_order
    if color_state == len(color_order):
        color_state = 0
    ret = color_order[color_state]
    color_state += 1
    return ret



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
        score += 1
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
    snake_direction = direction
    already_turned_head = True



def game_loop():
    global FPS
    global already_turned_head
    while True:
        clock.tick(FPS)  # updates the screen, the amount of times it does so depends on the FPS
        do_movement()
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
    pass


def process_menue_mouse_click():
    pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(pos):
        init_snake()
        game_loop()
        return
    if options_rect.collidepoint(pos):
        options_menue()
        return


def draw_menue():
    global play_rect
    global options_rect
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

menue()

#------------------------#
# 1 - left click
# 2 - middle click
# 3 - right click
# 4 - scroll up
# 5 - scroll down
#------------------------#