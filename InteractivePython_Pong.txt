# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
COLOR1 = "White"
COLOR2 = "Yellow"

PADDLE_VELOCITY = 10
PLAYFIELD = [PAD_WIDTH + BALL_RADIUS, 
             WIDTH - (PAD_WIDTH + BALL_RADIUS), 
             BALL_RADIUS, 
             HEIGHT - BALL_RADIUS]

score1 = 0
score2 = 0
paddle1_pos = 100
paddle1_vel = 0
paddle2_pos = 100
paddle2_vel = 0

ball_color = COLOR1
paddle_hits = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global paddle_hits
    paddle_hits = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(3,6), -random.randrange(3,6)]
    if direction == LEFT:
        ball_vel[0] *= -1


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)
    

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global ball_color, paddle_hits
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    # if ball hits the wall, then reverse its velocity
    ball_pos = [a+b for a,b in zip(ball_pos,ball_vel)]
    
    # check for collision
    if ball_pos[0] < PLAYFIELD[0]: #left
        if ((ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS) and 
            (ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS)):
            ball_pos[0] = PLAYFIELD[0]
            ball_vel[0] *= -1.1
            paddle_hits += 1
        else:
            score2 += 1
            ball_color = COLOR2
            spawn_ball(RIGHT)
    elif ball_pos[0] > PLAYFIELD[1]: #right
        if ((ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS) and 
            (ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS)):
            ball_pos[0] = PLAYFIELD[1]
            ball_vel[0] *= -1.1
            paddle_hits += 1
        else:
            score1 += 1
            ball_color = COLOR1
            spawn_ball(LEFT)
    elif ball_pos[1] < PLAYFIELD[2]: #top
        ball_pos[1] = PLAYFIELD[2]
        ball_vel[1] *= -1
    elif ball_pos[1] > PLAYFIELD[3]: #bottom
        ball_pos[1] = PLAYFIELD[3]
        ball_vel[1] *= -1
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, ball_color, ball_color)
    c.draw_text("%02d" % paddle_hits, [ball_pos[0]-10,ball_pos[1]+6], 20, "Black")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos - HALF_PAD_HEIGHT < 0:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle1_pos + HALF_PAD_HEIGHT > HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    paddle2_pos += paddle2_vel
    if paddle2_pos - HALF_PAD_HEIGHT < 0:
        paddle2_pos = HALF_PAD_HEIGHT
    if paddle2_pos + HALF_PAD_HEIGHT > HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    
    # draw paddles
    c.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], 
                    [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                    [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                    [0, paddle1_pos + HALF_PAD_HEIGHT]], 2, COLOR1, COLOR1)

    c.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                    [WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                    [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                    [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 2, COLOR2, COLOR2)
    
    # draw scores
    c.draw_text(str(score1), [100, 40], 40, COLOR1)
    c.draw_text(str(score2), [WIDTH - 125, 40], 40, COLOR2)

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['W']:
        paddle1_vel = -PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['S']:
        paddle1_vel = PADDLE_VELOCITY
   
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = PADDLE_VELOCITY
        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['W']:
        if paddle1_vel < 0: paddle1_vel = 0
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['S']:
        if paddle1_vel > 0: paddle1_vel = 0
   
    if key == simplegui.KEY_MAP['up']:
        if paddle2_vel < 0: paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        if paddle2_vel > 0: paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
