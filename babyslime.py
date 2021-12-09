import game_framework
from pico2d import *
import server


FRAMES_PER_ACTION = 5
ACTION_PER_TIME = 1


class BabySlime: 

    def __init__(self):
        self.image = [None for _ in range(5)]
        for i in range(5): 
            self.image[i] = load_image('mobs/babyslime/walk/babyslime_walk_%d.png' % int(i+1))
        self.x = server.canvas_size.x // 2
        self.y = server.canvas_size.y // 2
        self.degree = 0
        self.speed = 100
        self.frame = 0
        self.hp = 50
        self.font = load_font('ENCR10B.TTF', 16)
    
    def get_bb(self): 
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self): 
        self.dir = math.atan2(server.will.y - self.y, server.will.x - self.x)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir)* game_framework.frame_time
        self.y += self.speed * math.sin(self.dir)* game_framework.frame_time

    def draw(self): 
        self.image[int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 45, self.y + 50, '(HP: %d)' % self.hp, (255, 255, 0))

    def handle_event(self): 
        pass