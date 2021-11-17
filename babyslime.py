from pico2d import *
import game_world

class BabySlime: 
    def __init__(self):
        self.image = list(range(5))
        for i in range(0, 5):
            self.image[i] = load_image('mobs/babyslime/walk/babyslime_walk_%d.png' % int(i+1)) 
        self.x = 580 // 2
        self.y = 360 // 2
        self.frame = 0
        
    def draw(self): 
        self.image[int(self.frame)].draw(self.x, self.y, 30, 22)
        
    def update(self):
        will_x = game_world.will_x
        will_y = game_world.will_y 
        x_dist = will_x - self.x
        y_dist = will_y - self.y
        if abs(x_dist) > abs(y_dist): 
            self.x += (x_dist / abs(x_dist)) * 1.4
        elif abs(x_dist) < abs(y_dist): 
            self.y += (y_dist / abs(y_dist)) * 1.4

        self.frame = (self.frame + 0.15) % 5
