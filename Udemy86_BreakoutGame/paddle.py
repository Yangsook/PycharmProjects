from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)

    def go_right(self):
        if self.xcor() <= 350:
            self.goto(self.xcor() + 20, self.ycor())

    def go_left(self):
        if self.xcor() >= -350:
            self.goto(self.xcor() - 20, self.ycor())

