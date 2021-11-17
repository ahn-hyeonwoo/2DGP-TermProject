from pico2d import *
import math
import time

import game_world
import babyslime




class Will:
    def __init__(self):
        self.image_stand = load_image('will_stand.png')
        self.image_walk = load_image('will_walk.png')
        self.image_roll = load_image('will_roll.png')
        self.stand_frame_max = 10
        self.walk_frame_max = 8
        self.roll_frame_max = 8
        self.x = 580 // 2
        self.y = 360 // 2
        self.direction = 0
        self.dir_side = 0
        self.dir_updown = 0
        self.walking = False
        self.rolling = False
        self.frame = 0
    
    def draw(self):
        if self.rolling:
            self.image_roll.clip_draw(int(self.frame) * 35, 35 * self.direction, 35, 35, self.x, self.y)
        elif self.walking:
            self.image_walk.clip_draw(int(self.frame) * 35, 35 * self.direction, 35, 35, self.x, self.y)
        else:
            self.image_stand.clip_draw(int(self.frame) * 35, 35 * self.direction, 35, 35, self.x, self.y)
    
    def frame_update(self):
        max = 10
        if self.walking or self.rolling: max = 8
        # self.frame = (self.frame + 1) % max
        self.frame = (self.frame + 0.2)
        if self.rolling and self.frame >= 8: 
            self.rolling = False
        self.frame = self.frame % max

    def update(self):
        if self.dir_side != 0 or self.dir_updown != 0: self.walking = True
        else: self.walking = False

        s = 0
        noDir = False
        if self.dir_side > 0:
            s = 0
            if self.dir_updown > 0:
                s = 315
            elif self.dir_updown < 0:
                s = 45
        elif self.dir_side < 0:
            s = 180
            if self.dir_updown > 0:
                s = 225
            elif self.dir_updown < 0:
                s = 135
        else:
            if self.dir_updown > 0:
                s = 270
            elif self.dir_updown < 0:
                s = 90
            else: 
                noDir = True
            pass
        
        r = 3.2 # 0.25
        if not noDir:
            if self.rolling:
                if self.frame < 1:
                    r = 2.56
                elif self.frame < 7:
                    r = 5.12
                else:
                    r = 2.56
                self.x += r * math.cos(s/360*2*math.pi)
                self.y += r * math.sin(s/360*2*math.pi)
            elif self.walking:
                self.x += r * math.cos(s/360*2*math.pi)
                self.y += r * math.sin(s/360*2*math.pi)


def handle_events():
    global will
    global running
    global t
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                will.dir_side += 1
                will.direction = 3 # see right
            elif event.key == SDLK_a:
                will.dir_side -= 1
                will.direction = 2 # see left
            elif event.key == SDLK_s:
                will.dir_updown += 1
                will.direction = 1 # see down
            elif event.key == SDLK_w:
                will.dir_updown -= 1
                will.direction = 0 # see up
            elif event.key == SDLK_SPACE:
                if not will.rolling:
                    will.rolling = True
                    will.frame = 0
                    will.roll_count = 0
                    will.fchange = 25
                    t = 0
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                will.dir_side -= 1
            elif event.key == SDLK_a:
                will.dir_side += 1
            elif event.key == SDLK_s:
                will.dir_updown -= 1
            elif event.key == SDLK_w:
                will.dir_updown += 1


open_canvas(580, 360, True)
background = load_image('background.png')
will = Will()
running = True

babyslime_test = babyslime.BabySlime()
game_world.add_object(babyslime_test, 1)

frame_time = time.time()
current_time = time.time() - frame_time
while running: 
    clear_canvas()
    background.draw(580//2, 360//2)

    will.draw()

    will.update()

    will.frame_update()
    
    # MOBS
    game_world.will_pos_update(will.x, will.y)
    for game_object in game_world.all_objects(): 
        game_object.update()
        game_object.draw()

    update_canvas()
    handle_events()

    frame_time = time.time() - current_time
    current_time += frame_time


close_canvas()