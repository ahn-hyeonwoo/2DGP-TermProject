from pico2d import *


def handle_events():
    global running
    global dir_updown
    global dir_side
    global direction
    global rolling; global roll_frame
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                dir_side += 1
                direction = 3 # see right
            elif event.key == SDLK_a:
                dir_side -= 1
                direction = 2 # see left
            elif event.key == SDLK_s:
                dir_updown += 1
                direction = 1 # see down
            elif event.key == SDLK_w:
                dir_updown -= 1
                direction = 0 # see up
            elif event.key == SDLK_SPACE:
                if not rolling:
                    rolling = True
                    roll_frame = 0
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                dir_side -= 1
            elif event.key == SDLK_a:
                dir_side += 1
            elif event.key == SDLK_s:
                dir_updown -= 1
            elif event.key == SDLK_w:
                dir_updown += 1


open_canvas(580, 360)
background = load_image('background.png')
character_stand = load_image('will_stand.png')
character_walk = load_image('will_walk.png')
character_roll = load_image('will_roll.png')

running = True
dir_updown = 0
dir_side = 0
walk_frame = 0
stand_frame = 0
direction = 1
rolling = False
roll_frame = 0

t = 0
x = 580//2
y = 360//2
while running:
    t += 1
    clear_canvas()
    background.draw(580//2, 360//2)

    if rolling:
        character_roll.clip_draw(roll_frame * 35, 35 * direction, 35, 35, x, y)
    elif dir_updown != 0 or dir_side != 0:
        character_walk.clip_draw(walk_frame * 35, 35 * direction, 35, 35, x, y)
    else: 
        character_stand.clip_draw(stand_frame * 35, 35 * direction, 35, 35, x, y)

    if rolling: 
        speed = 0
        if roll_frame < 1:
            speed = 0.15
        elif roll_frame < 5:
            speed = 0.35
        else:
            speed = 0.15
        if dir_side > 0:
            x += speed
        elif dir_side < 0:
            x -= speed
        if dir_updown > 0:
            y -= speed
        elif dir_updown < 0:
            y += speed
    else:
        if dir_side > 0:
            x += 0.25
        elif dir_side < 0:
            x -= 0.25
        if dir_updown > 0:
            y -= 0.25
        elif dir_updown < 0:
            y += 0.25

    if t > 50:
        if rolling:
            roll_frame += 1
            if roll_frame == 8:
                walk_frame = 0
                stand_frame = 0
                roll_frame = 0
                rolling = False
        elif dir_updown != 0 or dir_side != 0:
            walk_frame = (walk_frame + 1) % 8
            stand_frame = 0
        else:
            stand_frame = (stand_frame + 1) % 10
            walk_frame = 0
        t = 0
    update_canvas()
    handle_events()
    delay(0.0001)
    pass


close_canvas()