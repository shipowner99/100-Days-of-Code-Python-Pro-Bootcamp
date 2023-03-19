import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("50_states.csv")
all_states = data["state"].to_list()
guessed_states = []
while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 Guess the State",
                                    prompt="What's another state's name?")
    titled_answer_state = answer_state.title()

    if titled_answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        #맞추지 못한 것들 dataframe으로 바꾸고 csv 파일로 만들기
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break
    if titled_answer_state in all_states:
        guessed_states.append(titled_answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        #정답 row(이름,x,y) 가져오기
        state_data = data[data.state == titled_answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(titled_answer_state)

screen.exitonclick()
