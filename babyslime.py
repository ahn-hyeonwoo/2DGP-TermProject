from pico2d import *

class BabySlime: 
    def __init__(self):
        self.image = load_image('babyslime_walk_1.png')
        self.x = 580 // 2
        self.y = 360 // 2
        
    def draw(self): 
        self.image.draw(self.x, self.y, 30, 22)
        
    def update(self, will_x, will_y): 
        x_dist = will_x - self.x
        y_dist = will_y - self.y
        if abs(x_dist) > abs(y_dist): 
            self.x += (x_dist / abs(x_dist)) * 0.1
        elif abs(x_dist) < abs(y_dist): 
            self.y += (y_dist / abs(y_dist)) * 0.1

