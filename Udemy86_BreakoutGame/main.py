import time
from turtle import Screen
from bricks import Bricks
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Breakout Game")
screen.tracer(0)

bricks = Bricks()
ball = Ball()
paddle = Paddle((0,-250))
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(paddle.go_right, "Right")
screen.onkeypress(paddle.go_left, "Left")

bricks.create_bricks()
scoreboard.update_scoreboard()


game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    ball.move()

    #Detect collision with wall
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    #Detect collision with paddle
    # if ball.distance(paddle) < 50 : #and ball.ycor() < -250:
    if (-240 <= ball.ycor() <= -230) and (
        paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60) and ball.y_move < 0:
        ball.bounce_y()
        print('paddle')

    # Detect collision with bricks
    for brick in bricks.all_bricks:
        # if ball.distance(brick) < 45:
        if brick.ycor() - 20 <= ball.ycor() <= brick.ycor() + 20 and (
                brick.xcor() - 60 < ball.xcor() < brick.xcor() + 60) and ball.y_move > 0:

            print(ball.distance(brick))
            brick.goto(1000, 1000)
            ball.bounce_y()
            bricks.all_bricks.remove(brick)
            scoreboard.increase_score()

    # Game over
    if len(bricks.all_bricks) < 0 or ball.ycor() < -300:
        ball.goto(1000, 1000)
        game_is_on = False
        scoreboard.game_over()


screen.exitonclick()
