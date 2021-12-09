import random
# import json
# import os

from pico2d import *
import game_framework
import game_world
import server

from will import Will
from background import Background
from babyslime import BabySlime


name = "MainState"


def enter():
    server.will = Will()
    game_world.add_object(server.will, 1)

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.babyslime = BabySlime()
    game_world.add_object(server.babyslime, 2)

def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.will.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






