import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

#화면 만들기
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.title("거북이 길건너기 게임")

#각각 class마다 object 생성
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()


screen.listen()
screen.onkey(player.up, "Up")
game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    #충돌 감지
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    #건너기 성공
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

#클릭 하면 나가기
screen.exitonclick()