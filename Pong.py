# Implementation of classic arcade game Pong

import simplegui
from random import randrange

# the dimensions of the screen
WIDTH = 600
HEIGHT = 400       

# the radius of the ball
BALL_RADIUS = 20

# the dimensions of the pads
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# the variable for the paddle positions and velocities
paddle1_pos = [0, 240]
paddle2_pos = [0, 240]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

# the variables which control the direction of the ball initally
LEFT = False
RIGHT = True

# the vectors for the balls position and velocity
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# the variables for keeping the score of each player
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    HDir = randrange(2, 4)
    VDir = randrange(1, 3)
    
    if direction == RIGHT:
        ball_vel = [HDir, VDir]
    elif direction == LEFT:
        ball_vel = [-HDir, VDir]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2

    score1 = 0
    score2 = 0
    spawn_ball(False)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]

    # collision and reflection from upper and lower walls
    if (ball_pos[1] + BALL_RADIUS) == HEIGHT:
        ball_vel[1] = -ball_vel[1]
    elif (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1] 

    # collision with gutters and paddles
    if (ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH):
        if (paddle2_pos[1] - PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1]):
            # change direction and increase velocity by 10%
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score1 += 1
            spawn_ball(False)
    elif (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        if (paddle1_pos[1] - PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1]):
            # change direction and increase velocity by 10%
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score2 += 1
            spawn_ball(True) 
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen

    # to prevent the pad from going above the actual screen
    if paddle1_pos[1] >= HEIGHT and paddle1_vel[1] > 0:
        paddle1_pos[1] = HEIGHT
    # to prevent the pad from going below the actual screen
    elif paddle1_pos[1] <= PAD_HEIGHT and paddle1_vel[1] < 0:
        paddle1_pos[1] = PAD_HEIGHT
    # translate the pad accordingly
    else:
        paddle1_pos[1] += paddle1_vel[1]

    if paddle2_pos[1] >= HEIGHT and paddle2_vel[1] > 0:
        paddle2_pos[1] = HEIGHT
    # to prevent the pad from going below the actual screen
    elif paddle2_pos[1] <= PAD_HEIGHT and paddle2_vel[1] < 0:
        paddle2_pos[1] = PAD_HEIGHT
    # translate the pad accordingly
    else:
        paddle2_pos[1] += paddle2_vel[1]

    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos[1]), (PAD_WIDTH, paddle1_pos[1]), (PAD_WIDTH, paddle1_pos[1] - PAD_HEIGHT), (0, paddle1_pos[1] - PAD_HEIGHT)], 1, "White", "White")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos[1]), (WIDTH, paddle2_pos[1]), (WIDTH, paddle2_pos[1] - PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos[1] - PAD_HEIGHT)], 1, "White", "White")
    
    # draw scores
    canvas.draw_text(str(score2), (450, 50), 36, "White")
    canvas.draw_text(str(score1), (150, 50), 36, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel[1] = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel[1] = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel[1] = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle1_vel[1] = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    paddle1_vel[1] = 0
    paddle2_vel[1] = 0

def restart():
    new_game()

def exit():
    frame.stop()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)
frame.add_button("Exit ",exit,100)

# start frame
new_game()
frame.start()
