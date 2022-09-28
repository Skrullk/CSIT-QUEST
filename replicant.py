import pygame as pg
from pygame.locals import *
import os
import random as rng


class State:
    pass


def center_place(screen_w, screen_h, surf):
    surf_w, surf_h = surf.get_size()
    return (
        (screen_w - surf_w) // 2,
        (screen_h - surf_h) // 2,
    )


def load_fonts(folder):
    fonts = []
    for fontname in os.listdir(folder):
        font = pg.font.Font(f"{folder}/{fontname}", font_size)
        fonts.append(font)
    return fonts


def negative_color(color):
    return Color(255 - color.r, 255 - color.g, 255 - color.b)



def test_screen(screen, state):
    bg = negative_color(bg_color) if state.negative else bg_color
    screen.fill(bg)

    if state.font_index == None:
        render_font = main_font
    else:
        render_font = rofl_fonts[state.font_index]

    if state.answer == RIGHT:
        text_str = "ПРАВИЛЬНО"
        text_color = GREEN
    else:
        text_str = "НЕПРАВИЛЬНО"
        text_color = RED

    if state.swap:
        text_color = GREEN if text_color == RED else RED
    text_color = negative_color(text_color) if state.negative else text_color

    if state.waiting:
        text = render_font.render("СЛУШАЙ", True, BLUE)
    else:
        text = render_font.render(text_str, True, text_color)
    text_place = center_place(*size, text)

    screen.blit(text, text_place)


def start_screen(screen, state):
    screen.fill(WHITE)

    text = main_font.render("ТЕСТ РЕПЛИКАНТА", True, BLACK)
    text_place = center_place(*size, text)
    screen.blit(text, text_place)

pg.init()
#  w, h = size = 1440, 900
#  screen = pg.display.set_mode(size, FULLSCREEN)
#  font_size = 170
w, h = size = 800, 600
screen = pg.display.set_mode(size)
font_size = 80

BLACK = Color("black")
RED = Color(200, 0, 0)
GREEN = Color(0, 200, 0)
BLUE = Color(0, 0, 200)
WHITE = Color("white")

RIGHT = 0
WRONG = 1

SCREEN_START = 0
SCREEN_TEST = 1

main_font = pg.font.Font("OpenGostTypeA.ttf", font_size)
rofl_fonts = load_fonts("fonts")

bg_color = WHITE

state = State()
def reset(state):
    state.screen = SCREEN_START
    state.answer = RIGHT
    state.font_index = None
    state.negative = False
    state.swap = False
    state.waiting = True
    state.timing = 0
reset(state)

running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                if state.waiting:
                    state.answer = rng.choice([RIGHT, WRONG])
                    state.waiting = False
                else:
                    state.waiting = True
            if event.key == K_s:
                state.screen = SCREEN_TEST
            if event.key == K_r:
                reset(state)
                state.screen = SCREEN_START
            if event.key == K_n:
                state.negative = not state.negative
            if event.key == K_b:
                state.swap = not state.swap
            if event.key == K_RIGHT:
                if state.font_index is None:
                    state.font_index = 0
                else:
                    state.font_index += 1
                    if state.font_index == len(rofl_fonts):
                        state.font_index = None
            if event.key == K_LEFT:
                if state.font_index is None:
                    state.font_index = len(rofl_fonts) - 1
                else:
                    state.font_index -= 1
                    if state.font_index == -1:
                        state.font_index = None

    screen.fill(BLACK)

    if state.screen == SCREEN_START:
        start_screen(screen, state)
    elif state.screen == SCREEN_TEST:
        test_screen(screen, state)

    pg.display.flip()

