from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

scoreboard = Scoreboard()
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))

ball = Ball()

screen.listen()
screen.onkey(r_paddle.up, "Up")
screen.onkey(r_paddle.down, "Down")

screen.onkey(l_paddle.up, "w")
screen.onkey(l_paddle.down, "s")
game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    # 위아래 벽에 부딪히면
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # 패들에 부딪히면
    # (기존 강의 코드)
    # if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
    #     ball.bounce_x()
    # (버그 고친 코드)
    if -370 < ball.xcor() < -330 and l_paddle.ycor() + 70 > ball.ycor() > l_paddle.ycor() - 70 or 370 > ball.xcor() > 330 and r_paddle.ycor() + 70 > ball.ycor() >r_paddle.ycor() - 70:
        ball.bounce_y()
    if ball.xcor() == -330 and l_paddle.ycor() + 70 > ball.ycor() > l_paddle.ycor() - 70 or ball.xcor()==330 and r_paddle.ycor() + 70 > ball.ycor() >r_paddle.ycor() - 70:
        ball.bounce_x()

    # 공이 끝으로 빠지면
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()
