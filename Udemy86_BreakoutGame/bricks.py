from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "gray"]
X_LIST = [-340, -230, -120, -10, 100, 210, 320]
Y_LIST = [280, 255, 230, 205, 180]

class Bricks:

    def __init__(self):
        self.all_bricks = []


    def create_bricks(self):

        for i in X_LIST:
            for j in Y_LIST:
                new_brick = Turtle("square")
                new_brick.shapesize(stretch_wid=1, stretch_len=5)
                new_brick.penup()
                new_brick.color(random.choice(COLORS))
                new_brick.goto(i, j)
                self.all_bricks.append(new_brick)


