# Snake-game-project (day 20,21,24)
![day24-snake-game](https://user-images.githubusercontent.com/120784842/225862864-d367280a-3a77-4d14-ae5d-d634701def24.gif)


## 게임 방법
1. 뱀은 자동으로 앞으로 움직입니다. 움직이고 있는 뱀을 키보드 키로 방향을 조작합니다.
2. 뱀은 먹이를 먹고, 먹을수록 뱀은 점점 길어집니다.
3. 뱀이 혼자 엉키거나, 벽에 부딪히면 게임이 끝나고 자동으로 다시 시작합니다.
4. 오래 버티면서 먹이를 최대한 많이 먹는 것이 목표입니다.
5. 최고 점수는 저장됩니다.

## 배운 점

### 작은 단위로 나눠보면
1. 뱀의 몸통을 만들고 키보드로 움직이게 하기
2. 먹이 만들고 먹이를 먹었는지 알아내기
3. 벽에 부딪혔는지 알아내기
4. 뱀이 자기 꼬리와 부딪혔는지 알아내기
5. 게임 점수판만들어 점수 기록하기
6. 최대 점수 저장하고 불러내기


## Object Oriented Programming(OOP): 객체지향 프로그래밍
### Class Inheritance: 클래스 상속
- 기존 클래스에서 메소드과 속성을 상속받는 과정
- 클래스 이름 옆에 괄호 치고, 상속받고자 하는 클래스를 적는다. super 는 상위 클래스를 나타냄.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/4befbb27fd538267cec37e93ec91c43aeaf1c292/Day24-Snake-game/food.py#L5-L8
- 위 코드에서는 Food 클래스가 Turtle 클래스를 상속받음.
- 클래스 상속을 통해 메소드의 기능을 확장할 수도 있음.

>(예시 문제) 
>
>```
>  class Dog:
>    def bark(self):
>      print("Woof, woof")
>
>  class Labrador(Dog):
>    def bark(self):
>      super().bark()
>      print("Greetings, good sir. How do you do?")  
>```
>
> 일때 
> 
> ```
> sparky = Labrador()
> sparky.bark()
> ```
> 위의 코드가 출력하는 값은?
> 
>   정답:
>  ```
> Woof, woof!
> Greetings, good sir. How do you do?
>  ```

## 파일 열고 수정하는 방법 -open, with 키워드 사용 방법
1)read
- https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/4befbb27fd538267cec37e93ec91c43aeaf1c292/Day24-Snake-game/scoreboard.py#L11-L12

2)write
- https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/4befbb27fd538267cec37e93ec91c43aeaf1c292/Day24-Snake-game/scoreboard.py#L29-L30
- mode = "w" 로 바꿔줘야함.
- w 는 write. 다 지우고 새로 써줌. 
- a 는 append. 있는 것에 덧붙여써줌.

3)with키워드
- with 를 쓰면 data.close()를 하지 않아도 사용하고나서 자동으로 닫힘. 파일 닫는 것을 기억할 필요가 없음. 일을 끝냈다는 것을 알아채는 즉시 파일을 닫는다.
- 이 프로젝트에서는 처음 실행했을 때 data에 저장되어 있던 최고 점수를 불러내고 신기록 세우면 data에 점수를 덮어 씌우기할 때 사용함.

## 발전시키고 싶은 점
- 게임이 끝나고 자동으로 다시 시작하는 것이 아니라 키보드 아무 키나 눌렀을 때 다시 시작하게 하고 싶다.
