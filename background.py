from pico2d import *
import server
import collision
import map

class Background:
    def __init__(self):
        self.image = load_image('objects/background/background.png')
        self.min_x, self.max_x = server.canvas_size.x // 12, server.canvas_size.x - server.canvas_size.x // 12
        self.min_y, self.max_y = server.canvas_size.y // 8, server.canvas_size.y - server.canvas_size.y // 8
        self.door_image = [None for _ in range(4)]
        self.door_image[0] = load_image('objects/door/up/door_up_1.png')
        self.door_image[1] = load_image('objects/door/down/door_down_1.png')
        self.door_image[2] = load_image('objects/door/left/door_left_1.png')
        self.door_image[3] = load_image('objects/door/right/door_right_1.png')

    def update(self):
        enter_map = map.is_will_enter_door(server.will.x, server.will.y)
        room_index = map.cur_x + map.cur_y*7
        if enter_map == 1 and map.Rooms[room_index].up_door == True: 
            map.cur_y += 1
            server.will.y = self.min_y + 15
        elif enter_map == 2 and map.Rooms[room_index].down_door == True: 
            map.cur_y -= 1
            server.will.y = self.max_y - 15
        elif enter_map == 3 and map.Rooms[room_index].left_door == True: 
            map.cur_x -= 1
            server.will.x = self.max_x - 15
        elif enter_map == 4 and map.Rooms[room_index].right_door == True: 
            map.cur_x += 1
            server.will.x = self.min_x + 15

    def draw(self):
        self.image.draw_to_origin(0, 0, server.canvas_size.x, server.canvas_size.y)
        # draw_rectangle(*self.get_bb())

        # min_x, max_x, min_y, max_y = server.background.min_x, server.background.max_x, server.background.min_y, server.background.max_y
        w, h = server.canvas_size.x, server.canvas_size.y
        x_gap, y_gap = self.min_x * 1.2, self.min_y * 1.5
        if map.Rooms[map.cur_x + map.cur_y*7].up_door: 
            self.door_image[0].draw(w//2, (self.max_y + h) // 2, 200, y_gap)
        if map.Rooms[map.cur_x + map.cur_y*7].down_door: 
            self.door_image[1].draw(w//2, (self.min_y + 0) // 2, 200, y_gap)
        if map.Rooms[map.cur_x + map.cur_y*7].left_door: 
            self.door_image[2].draw((self.min_x + 0) // 2, h//2, x_gap, 200)
        if map.Rooms[map.cur_x + map.cur_y*7].right_door: 
            self.door_image[3].draw((self.max_x + w) // 2, h//2, x_gap, 200)

    def get_bb(self):
        return self.min_x, self.min_y, self.max_x, self.max_y
