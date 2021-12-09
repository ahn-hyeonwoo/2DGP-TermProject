from random import randint
import server

class Room: 
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_door = False
        self.right_door = False
        self.up_door = False
        self.down_door = False
        self.enable = False
    
    def make_room(self, dir): 
        if dir == 0: 
            self.left_door = True
        elif dir == 1: 
            self.right_door = True
        elif dir == 2: 
            self.up_door = True
        else:
            self.down_door = True

Rooms = [Room() for _ in range(35)]
# 좌하단부터 0, 왼쪽으로 1씩 증가, 위쪽으로 7씩 증가, 최대 34

room_count = randint(10, 15)

start_x = randint(2, 4)
start_y = 0 
Rooms[start_x + start_y * 7].enable = True

cur_x = start_x
cur_y = start_y

while room_count > 0: 
    min_room = [float('inf') for _ in range(5)]
    max_room = [-1 for _ in range(5)]
    top_room = [-1 for _ in range(7)]
    bot_room = [float('inf') for _ in range(7)]

    for i in range(5): 
        for j in range(7): 
            if Rooms[i*7 + j].enable == True: 
                if j < min_room[i]: 
                    min_room[i] = j
                if j >= max_room[i]: 
                    max_room[i] = j
    
    for j in range(7): 
        for i in range(5): 
            if Rooms[i*7 + j].enable == True: 
                top_room[j] = i
                if i < bot_room[j]: 
                    bot_room[j] = i
    
    for i in range(5): 
        if min_room[i] != float('inf') and min_room[i] != 0: 
            if randint(0, 100) > 50: 
                Rooms[(i * 7 + min_room[i]) - 1].enable = True
                Rooms[(i * 7 + min_room[i]) - 1].right_door = True
                Rooms[((i * 7 + min_room[i]))].left_door = True
                room_count -= 1
                if room_count <= 0: break
        
        if max_room[i] != -1 and max_room[i] != 6: 
            if randint(0, 100) > 50:
                Rooms[(i * 7 + max_room[i]) + 1].enable = True
                Rooms[(i * 7 + max_room[i]) + 1].left_door = True
                Rooms[(i * 7 + max_room[i])].right_door = True
                room_count -= 1
                if room_count <= 0: break
    
    if room_count <= 0: break

    for j in range(7): 
        if top_room[j] != -1 and top_room[j] != 4: 
            if randint(0, 100) > 50:
                Rooms[(top_room[j] + 1) * 7 + j].enable = True
                Rooms[(top_room[j] + 1) * 7 + j].down_door = True
                Rooms[(top_room[j]) * 7 + j].up_door = True
                room_count -= 1
                if room_count <= 0: break
        
        if bot_room[j] != float('inf') and bot_room[j] != 0: 
            if randint(0, 100) > 50: 
                Rooms[(bot_room[j] - 1) * 7 + j].enable = True
                Rooms[(bot_room[j] - 1) * 7 + j].up_door = True
                Rooms[(bot_room[j]) * 7 + j].down_door = True
                room_count -= 1
                if room_count <= 0: break
    
    if room_count <= 0: break

if __name__ == '__main__': 
    for i in range(5): 
        for j in range(7): 
            print(' ', end='')
            if Rooms[i*7+j].down_door == True: 
                print('|', end='')
            else: print(' ', end='')
            print(' ', end='')
        print()
        for j in range(7): 
            if Rooms[i*7+j].enable == True: 
                if Rooms[i*7+j].left_door == True: 
                    print('-', end='')
                else: print(' ', end='')
                print('1', end='')
                if Rooms[i*7+j].right_door == True: 
                    print('-', end='')
                else: print(' ', end='')
            else: 
                print(' 0 ', end='')
        print()
        for j in range(7): 
            print(' ', end='')
            if Rooms[i*7+j].up_door == True: 
                print('|', end='')
            else: print(' ', end='')
            print(' ', end='')
        print()


def is_will_enter_door(x, y):
    w, h = server.canvas_size.x, server.canvas_size.y
    min_x, max_x = server.background.min_x, server.background.max_x
    min_y, max_y = server.background.min_y, server.background.max_y
    if x >= w//2 - 200 and x <= w//2 + 200: 
        if y >= max_y - 10 and y <= max_y: 
            return 1
        elif y >= min_y and y <= min_y + 10: 
            return 2
    elif x >= min_x and x <= min_x + 10: 
        if y >= h//2 - 200 and y <= h//2 + 200: 
            return 3
    elif x >= max_x - 10 and x <= max_x: 
        if y >= h//2 - 200 and y <= h//2 + 200: 
            return 4
    return 0