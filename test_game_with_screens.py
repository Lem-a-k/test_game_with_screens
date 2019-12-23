import pygame
import os
import sys
import argparse

BACKS = ["background1.jpg", "background2.jpg"]
PLAYER = "mario.png"


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()

def print_back(intro_text, pic=None):
    if pic is None:
        screen.fill((200, 100, 200))
    else:
        background = pygame.transform.scale(load_image(pic), screen_size)
        screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

def start_screen():
    print_back(["Это экран приветствия",
                  "Клавиатура - начать игру", "Мышка - настройки"], BACKS[0])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                return GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SETTINGS
        pygame.display.flip()
        clock.tick(FPS)

def settings_screen():
    print_back(["Это экран c настройками",
                  "Клавиатура - играть"], BACKS[1])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                return GAME
        pygame.display.flip()
        clock.tick(FPS)

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image(PLAYER)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


def game_screen(new_game=False):
    global hero

    if new_game:
        hero.kill()
        hero = Player(hero_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    hero.move(0, -10)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 10)
                elif event.key == pygame.K_LEFT:
                    hero.move(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    hero.move(10, 0)
                elif event.key == pygame.K_ESCAPE:
                    return RESULTS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SETTINGS
        print_back(["Это экран игры",
                    "Стрелки - играть",
                    "Мышка - настройки",
                    "Esc - результаты"])
        hero_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def results_screen():
    print_back(["Это экран с результатами",
                  "Клавиатура - сыграть снова", "Мышка - настройки"], BACKS[0])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GAME
                return NEW_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SETTINGS
        pygame.display.flip()
        clock.tick(FPS)


GREETING = 0
SETTINGS = 1
GAME = 2
RESULTS = 3
EXIT = 4
NEW_GAME = 5

todo = {GREETING: start_screen,
        SETTINGS: settings_screen,
        GAME: game_screen,
        NEW_GAME: lambda: game_screen(True),
        RESULTS: results_screen,
        EXIT: terminate}

pygame.init()
screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()


hero_group = pygame.sprite.GroupSingle()
hero = Player(hero_group)

state = GREETING
while True:
    state = todo[state]()
