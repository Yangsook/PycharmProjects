from turtle import Turtle

STARTING_POSITION = (0, -250)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.go_to_start()
        self.x_move = 8
        self.y_move = 10


    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.go_to_start()
        self.bounce_y()
