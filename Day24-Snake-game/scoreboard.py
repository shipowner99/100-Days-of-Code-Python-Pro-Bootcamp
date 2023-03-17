from turtle import Turtle
ALIGNMENT = "center"
FONT = ('Arial', 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0

        with open("data.txt", mode="r") as data:
            self.high_score =int(data.read())

        self.pencolor("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 250)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(arg=f"Score : {self.score} High Score : {self.high_score}", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.update_scoreboard()
        with open("data.txt", mode="w") as data:
            data.write(f"{self.high_score}")

    # def gameover(self):
    #     self.goto(0, 0)
    #     self.write(arg="GAME OVER", align=ALIGNMENT, font=FONT)


    def add_score(self):
        self.clear()
        self.score += 1
        self.update_scoreboard()

