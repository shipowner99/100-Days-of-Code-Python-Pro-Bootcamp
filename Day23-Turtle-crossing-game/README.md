# Turtle crossing game project
![day23-turtle-crossing](https://user-images.githubusercontent.com/120784842/225292561-ea3d7f34-2687-4db2-a7e3-c1159a467bd1.gif)

## 게임 방법
1. 거북이는 키보드 ↑ 키를 누르면 앞으로 움직입니다. 뒤로 가거나, 왼쪽, 오른쪽으로 움직이지 않고, 앞으로만 움직입니다.
1. 자동차는 y축 범위 내에서 무작위로 생성되고, 화면의 오른쪽 가장자리에서 왼쪽 가장자리로 움직입니다.
1. 거북이가 화면의 제일 윗부분에 도착하면, 거북이는 원래 위치로 돌아가고 플레이어는 다음 레벨로 넘어갑니다. 다음 단계에서는 자동차의 속도가 빨라집니다.
1. 거북이가 자동차와 충돌하면, 게임 끝나고 멈춥니다.

## 생각할 점 및 배운 점
- 하나의 큰 프로젝트를 할 때는 어떻게 작은 단위로 나눌지 생각하기

### 작은 단위로 나눠보면
1. 키보드로 움직이는 플레이어(거북이)만들기
1. 장애물(자동차)만들기
1. 장애물 충돌 감지하기
1. 결승선 도달 감지하기
1. 게임 점수판만들기

## Object Oriented Programming(OOP): 객체지향 프로그래밍
↔ Prucedural Programming 절차지향프로그래밍: 위에서 아래로 
- 프로그래밍에서 여러 가지 관계가 복잡하게 얽혀있을 때 코드 안에서 관계들을 간소화하고 더 크고 복잡한 프로젝트로 확장할 수 있음.
- 각각의 코드 묶음들을 모듈로 만들어서 각각의 부분은 다른 사람이 만들수도 있음.
- 나중에 같은 기능이 필요할 때 재사용이 가능함.
 * Class : 청사진
   - 각 단어의 첫 글자는 대문자로 씀
   - 여기에서는 거북이, 장애물, 점수판을 각각 class 로 만듦.
 * Object : 청사진으로부터 만들어진 개별 객체
   - attributes(객체가 가진 것(have). 특정 객체가 가진 변수 등의 데이터) 
   - methods(객체가 하는 일(do). 객체의 function)
 * Constructor : 생성자. 청사진의 일부로 객체가 생성 될 때 무슨일이 일어나야하는지 명시.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/3386cbcdebbc395a17f0c3d33f6efb3313545850/Day23-Turtle-crossing-game/main.py#L15
 * initialize attributes ( initialize: 변수의 시작값을 정하는 것.)
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/3386cbcdebbc395a17f0c3d33f6efb3313545850/Day23-Turtle-crossing-game/player.py#L10-L16
   * self : class 내부에서 class로부터 만들어지는 객체를 지칭하는 것
 * initialize methods
 https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/3386cbcdebbc395a17f0c3d33f6efb3313545850/Day23-Turtle-crossing-game/player.py#L24-L28
-> 결승선에 도착했는지 확인하는 함수

### Function as Inputs
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/3386cbcdebbc395a17f0c3d33f6efb3313545850/Day23-Turtle-crossing-game/main.py#L20
변수 자리에 함수를 넣을수도 있음
    
### Higher Order Functions
다른 함수와 같이 작동하는 함수(여기선 onkey)
