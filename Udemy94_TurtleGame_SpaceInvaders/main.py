# Import modules
import turtle
import time
import random
import winsound

# Functions
player_dx = 15

def move_left():
    x = player.xcor() - player_dx
    if x < -190:     # boundary / boarder is (-200, -200)
        x = -190      # rocket cannot go out of the boundary
    player.setx(x)

def move_right():
    x = player.xcor() + player_dx
    if x > 190:
        x = 190
    player.setx(x)

def fire_bullet():
    x = player.xcor()
    y = player.ycor()
    bullet.setposition(x, y + 20)
    bullet.showturtle()


# set up window
wn = turtle.Screen()
wn.setup(width=540, height=540)
wn.bgcolor('Black')
wn.title("Space invader")

# register shapes
turtle.register_shape('alien.gif')
turtle.register_shape('rocket.gif')

# Draw border, 400x400 square
border = turtle.Turtle()
border.speed(0)
border.color('gray')
border.up()  # Raise the pen so it does not draw anything)
border.setposition(-200, -200) # The center is (0,0) and Now we move our pen to the bottom.
border.down()
border.pensize(3) # Thickness of the pen
for side in range(4):
    border.forward(400)
    border.lt(90)  # Turn left 90 degree
    # now our space ship cannot go outside of the border.
border.hideturtle() # Cursor / Turtle is gone


# Score
# Set score to be 0 initially
score = 0

# Draw score board
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.up()
score_pen.setposition(-200, 210)
score_pen.write('Score: %s' % score)
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.shape('rocket.gif')
player.up() # in order to move again,we need to raise the pen
player.speed(0)
player.setposition(0, -180)
player.setheading(90) # turtle is looking at 90 degree

# Create player's bullet
bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('circle')
bullet.up()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

# create invader turtle
invader = turtle.Turtle()
invader.shape('alien.gif')
invader.up()
invader.speed(0)
invader.setposition(180, 180)
# invader.setheading(180)

# Create invader's bullet
invader_bullet = turtle.Turtle()
invader_bullet.color('red')
invader_bullet.shape('circle')
invader_bullet.up()
invader_bullet.speed(0)
invader_bullet.setheading(-90)
invader_bullet.shapesize(0.5, 0.5)
invader_bullet.hideturtle()


# Create keyboard binding
turtle.listen()
turtle.onkey(move_left, 'Left')   # call the function, move by 15 pixel
turtle.onkey(move_right, 'Right')
turtle.onkey(fire_bullet, 'space')

invader_speed = 5
bullet_speed = 10

while True:
    invader.forward(invader_speed)

    random_chance = random.randint(1, 200)
    if random_chance == 1:
        x = invader.xcor()
        y = invader.ycor()
        # invader_bullet.setposition(x, y - 20)
        # invader_bullet.setheading(-90)
        # invader_bullet.forward(bullet_speed)
        # invader_bullet.showturtle()

        new_laser = turtle.Turtle()
        new_laser.shape('triangle')
        new_laser.color('white')
        new_laser.penup()
        new_laser.setheading(-90)
        new_laser.shapesize(0.2, 0.2)
        new_laser.goto(x, y)
        new_laser.fd(bullet_speed)


    # check border
    if invader.xcor() > 190 or invader.xcor() < -190:
        invader.right(180) # Flip the invader angel 180 degrees
        invader.forward(invader_speed) # invader can move

    # fire the bullet
    bullet.forward(bullet_speed)


    # check for collision
    if abs(bullet.xcor() - invader.xcor()) < 15 and abs(bullet.ycor() - invader.ycor()) < 15:

        # update the score
        score = score + 1
        score_pen.clear()
        score_pen.write('Score: %s' % score)

        # reset invader and player
        bullet.hideturtle()
        invader.hideturtle()
        time.sleep(1) # 2 seconds later, new invader will show up

        invader.showturtle()
        x = random.randint(-180, 180)
        invader.setposition(x, 180)

        player.setposition(0, -180)