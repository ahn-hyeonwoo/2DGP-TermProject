import game_framework
from pico2d import *

import game_world
import server
import collision

# Boy Run Speed
# PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
# RUN_SPEED_KMPH = 20.0  # Km / Hour
# RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
# RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
# RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
RUN_SPEED_PPS = server.canvas_size.x // 6

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


W_DOWN, W_UP, A_DOWN, A_UP, S_DOWN, S_UP, D_DOWN, D_UP, SPACE, ESCAPE_TO_IDLE, ESCAPE_TO_WALK, J_DOWN = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_w): W_DOWN,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYDOWN, SDLK_s): S_DOWN,
    (SDL_KEYDOWN, SDLK_d): D_DOWN, 
    (SDL_KEYDOWN, SDLK_j): J_DOWN, 
    (SDL_KEYUP, SDLK_w): W_UP, 
    (SDL_KEYUP, SDLK_a): A_UP, 
    (SDL_KEYUP, SDLK_s): S_UP, 
    (SDL_KEYUP, SDLK_d): D_UP, 
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class IdleState:

    def enter(will, event):
        if event == D_DOWN:
            will.velocity_x += 1
            will.dir = 3
        elif event == A_DOWN:
            will.velocity_x -= 1
            will.dir = 2
        elif event == W_DOWN: 
            will.velocity_y += 1
            will.dir = 0
        elif event == S_DOWN: 
            will.velocity_y -= 1
            will.dir = 1
        elif event == D_UP:
            will.velocity_x -= 1
        elif event == A_UP:
            will.velocity_x += 1
        elif event == W_UP: 
            will.velocity_y -= 1
        elif event == S_UP: 
            will.velocity_y += 1

    def exit(will, event):
        will.frame = 0
        if event == SPACE: 
            will.timer = 8 / (2 * FRAMES_PER_ACTION * ACTION_PER_TIME) + 0.01
        elif event == J_DOWN: 
            will.timer = 8 / (2 * FRAMES_PER_ACTION * ACTION_PER_TIME) + 0.01

    def do(will):
        will.frame = (will.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

    def draw(will):
        w, h = server.will_size.w, server.will_size.h
        if will.dir > 1: 
            will.image_idle[will.dir][int(will.frame)].draw(will.x, will.y, w, h)
        else: 
            will.image_idle[will.dir][int(will.frame)].draw(will.x, will.y, w - (w // 5), h)


class WalkState:

    def enter(will, event):
        if event == D_DOWN:
            will.velocity_x += 1
            will.dir = 3
        elif event == A_DOWN:
            will.velocity_x -= 1
            will.dir = 2
        elif event == W_DOWN: 
            will.velocity_y += 1
            will.dir = 0
        elif event == S_DOWN: 
            will.velocity_y -= 1
            will.dir = 1
        elif event == D_UP:
            will.velocity_x -= 1
        elif event == A_UP:
            will.velocity_x += 1
        elif event == W_UP: 
            will.velocity_y -= 1
        elif event == S_UP: 
            will.velocity_y += 1

    def exit(will, event):
        if event is SPACE: 
            will.frame = 0
            will.timer = 8 / (2 * FRAMES_PER_ACTION * ACTION_PER_TIME) + 0.01
        elif event is J_DOWN: 
            will.frame = 0
            will.timer = 8 / (2 * FRAMES_PER_ACTION * ACTION_PER_TIME) + 0.01
        elif event is ESCAPE_TO_IDLE: 
            will.frame = 0

    def do(will):
        will.frame = (will.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if will.velocity_x != 0 or will.velocity_y != 0: 
            if will.velocity_x > 0: 
                if will.velocity_y > 0:         will.degree = 45
                elif will.velocity_y < 0:       will.degree = 315
                else:                           will.degree = 0
            elif will.velocity_x < 0: 
                if will.velocity_y > 0:         will.degree = 135
                elif will.velocity_y < 0:       will.degree = 225
                else:                           will.degree = 180
            else: 
                if will.velocity_y > 0:         will.degree = 90
                elif will.velocity_y < 0:       will.degree = 270
            
            r = RUN_SPEED_PPS * game_framework.frame_time
            will.x += r * math.cos(will.degree/360*2*math.pi)
            will.y += r * math.sin(will.degree/360*2*math.pi)
            will.x = clamp(server.background.min_x, will.x, server.background.max_x)
            will.y = clamp(server.background.min_y, will.y, server.background.max_y)
        else: 
            will.add_event(ESCAPE_TO_IDLE)

    def draw(will):
        w, h = server.will_size.w, server.will_size.h
        if will.dir > 1: 
            will.image_walk[will.dir][int(will.frame)].draw(will.x, will.y, w, h)
        else: 
            will.image_walk[will.dir][int(will.frame)].draw(will.x, will.y, w - (w // 5), h)


class RollState:

    def enter(will, event):
        if event == D_DOWN:
            will.velocity_x += 1
        elif event == A_DOWN:
            will.velocity_x -= 1
        elif event == W_DOWN: 
            will.velocity_y += 1
        elif event == S_DOWN: 
            will.velocity_y -= 1
        elif event == D_UP:
            will.velocity_x -= 1
        elif event == A_UP:
            will.velocity_x += 1
        elif event == W_UP: 
            will.velocity_y -= 1
        elif event == S_UP: 
            will.velocity_y += 1

    def exit(will, event):
        if event == ESCAPE_TO_WALK: 
            will.timer = 0
            will.frame = 0

    def do(will):
        will.frame = (will.frame + 2 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        
        r = RUN_SPEED_PPS * game_framework.frame_time * 1.75
        will.x += r * math.cos(will.degree/360*2*math.pi)
        will.y += r * math.sin(will.degree/360*2*math.pi)
        will.x = clamp(server.background.min_x, will.x, server.background.max_x)
        will.y = clamp(server.background.min_y, will.y, server.background.max_y)

        will.timer -= game_framework.frame_time
        if will.timer <= 0: 
            will.add_event(ESCAPE_TO_WALK)

    def draw(will):
        w, h = server.will_size.w, server.will_size.h
        if will.dir > 1: 
            will.image_roll[will.dir][int(will.frame)].draw(will.x, will.y, w, h)
        else: 
            will.image_roll[will.dir][int(will.frame)].draw(will.x, will.y, w - (w//5), h)


class AttackState:

    def enter(will, event):
        if event == D_DOWN:
            will.velocity_x += 1
        elif event == A_DOWN:
            will.velocity_x -= 1
        elif event == W_DOWN: 
            will.velocity_y += 1
        elif event == S_DOWN: 
            will.velocity_y -= 1
        elif event == D_UP:
            will.velocity_x -= 1
        elif event == A_UP:
            will.velocity_x += 1
        elif event == W_UP: 
            will.velocity_y -= 1
        elif event == S_UP: 
            will.velocity_y += 1

    def exit(will, event):
        if event == ESCAPE_TO_WALK: 
            will.timer = 0
            will.frame = 0
            # Do Attack
            # for obj in game_world.all_objects(): 

        elif event == SPACE: 
            will.timer = 0
            will.timer = 8 / (2 * FRAMES_PER_ACTION * ACTION_PER_TIME) + 0.01

    def do(will):
        will.frame = (will.frame + 2 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        
        # r = RUN_SPEED_PPS * game_framework.frame_time * 1.75
        # will.x += r * math.cos(will.degree/360*2*math.pi)
        # will.y += r * math.sin(will.degree/360*2*math.pi)
        # will.x = clamp(server.background.min_x, will.x, server.background.max_x)
        # will.y = clamp(server.background.min_y, will.y, server.background.max_y)

        will.timer -= game_framework.frame_time
        if will.timer <= 0: 
            will.add_event(ESCAPE_TO_WALK)

    def draw(will):
        w, h = server.will_size.w, server.will_size.h
        if will.dir > 1: 
            will.image_spear[will.dir][int(will.frame)].draw(will.x, will.y, w, h)
        else: 
            will.image_spear[will.dir][int(will.frame)].draw(will.x, will.y, w - (w//5), h)


next_state_table = {
    IdleState: {W_UP: WalkState, A_UP: WalkState, S_UP: WalkState, D_UP: WalkState, 
                W_DOWN: WalkState, A_DOWN: WalkState, S_DOWN: WalkState, D_DOWN: WalkState, 
                SPACE: RollState, ESCAPE_TO_WALK: IdleState, ESCAPE_TO_IDLE: IdleState, 
                J_DOWN: AttackState},
    WalkState: {W_UP: WalkState, A_UP: WalkState, S_UP: WalkState, D_UP: WalkState, 
                W_DOWN: WalkState, A_DOWN: WalkState, S_DOWN: WalkState, D_DOWN: WalkState, 
                SPACE: RollState, ESCAPE_TO_IDLE: IdleState, ESCAPE_TO_WALK: IdleState, 
                J_DOWN: AttackState},
    RollState: {W_UP: RollState, A_UP: RollState, S_UP: RollState, D_UP: RollState, 
                W_DOWN: RollState, A_DOWN: RollState, S_DOWN: RollState, D_DOWN: RollState, 
                SPACE: RollState, ESCAPE_TO_WALK: WalkState, ESCAPE_TO_IDLE: WalkState, 
                J_DOWN: RollState}, 
    AttackState:    {W_UP: AttackState, A_UP: AttackState, S_UP: AttackState, D_UP: AttackState, 
                    W_DOWN: AttackState, A_DOWN: AttackState, S_DOWN: AttackState, D_DOWN: AttackState, 
                    SPACE: RollState, ESCAPE_TO_WALK: WalkState, ESCAPE_TO_IDLE: WalkState, 
                    J_DOWN: AttackState}
}

class Will:

    def __init__(self):
        self.x, self.y = server.canvas_size.x // 2, server.canvas_size.y // 2
        # 0: up, 1: down, 2: left, 3: right
        self.image_idle = [[None for _ in range(10)] for _ in range(4)]
        for i in range(10): self.image_idle[0][i] = load_image('will/will_idle/up/will_idle_up_%d.png' % int(i+1))
        for i in range(10): self.image_idle[1][i] = load_image('will/will_idle/down/will_idle_down_%d.png' % int(i+1))
        for i in range(10): self.image_idle[2][i] = load_image('will/will_idle/left/will_idle_left_%d.png' % int(i+1))
        for i in range(10): self.image_idle[3][i] = load_image('will/will_idle/right/will_idle_right_%d.png' % int(i+1))
        self.image_walk = [[None for _ in range(8)] for _ in range(4)]
        for i in range(8): self.image_walk[0][i] = load_image('will/will_walk/up/will_walk_up_%d.png' % int(i+1))
        for i in range(8): self.image_walk[1][i] = load_image('will/will_walk/down/will_walk_down_%d.png' % int(i+1))
        for i in range(8): self.image_walk[2][i] = load_image('will/will_walk/left/will_walk_left_%d.png' % int(i+1))
        for i in range(8): self.image_walk[3][i] = load_image('will/will_walk/right/will_walk_right_%d.png' % int(i+1))
        self.image_roll = [[None for _ in range(8)] for _ in range(4)]
        for i in range(8): self.image_roll[0][i] = load_image('will/will_roll/up/will_roll_up_%d.png' % int(i+1))
        for i in range(8): self.image_roll[1][i] = load_image('will/will_roll/down/will_roll_down_%d.png' % int(i+1))
        for i in range(8): self.image_roll[2][i] = load_image('will/will_roll/left/will_roll_left_%d.png' % int(i+1))
        for i in range(8): self.image_roll[3][i] = load_image('will/will_roll/right/will_roll_right_%d.png' % int(i+1))
        self.image_spear = [[None for _ in range(8)] for _ in range(4)]
        for i in range(8): self.image_spear[0][i] = load_image('will/will_attack/spear/up/Will_SpearCombo_Animation_Up_%d.png' % int(i+1))
        for i in range(8): self.image_spear[1][i] = load_image('will/will_attack/spear/down/Will_SpearCombo_Animation_Down_%d.png' % int(i+1))
        for i in range(8): self.image_spear[2][i] = load_image('will/will_attack/spear/left/Will_SpearCombo_Animation_Left_%d.png' % int(i+1))
        for i in range(8): self.image_spear[3][i] = load_image('will/will_attack/spear/right/Will_SpearCombo_Animation_Right_%d.png' % int(i+1))
        self.dir = 1 # 0: up, 1: down, 2: left, 3: right
        self.velocity_x = 0
        self.velocity_y = 0
        self.degree = 270 # degree of will's actual moving direction
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.hp = 100

    def get_bb(self):
        w, h = server.will_size.w, server.will_size.h
        return self.x - w//2, self.y - h//2, self.x + w//2, self.y + h//2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 45, self.y + 50, '(HP: %d)' % self.hp, (255, 255, 0))

        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)