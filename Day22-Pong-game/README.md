# Pong-game-project (day 22)
![day22-pong-game](https://user-images.githubusercontent.com/120784842/226108391-14600bf3-02b2-4ea1-ae14-3595189fe2b3.gif)

## 게임 방법
1. 테이블을 가로지르는 공이 한 개 있고, 두 명의 플레이어가 각각 패들을 움직이며 공을 주고 받습니다.
2. 만약 공을 놓치면 상대방이 득점합니다.
3. 공은 벽 또는 패들에 부딪히면서 점점 빨라집니다.

## 배운 점

### 작은 단위로 나눠보면
1. 스크린 만들기
2. 패들을 만들고 키보드로 움직이기
3. 다른 패들 만들기
4. 공 만들고 움직이게하기
5. 벽과 충돌했는지 알아내고 튕기기
6. 패들과 충돌했는지 알아내고 튕기기
7. 패들이 공을 놓친것을 알아내기
8. 점수 계산하기 


### 패들이 공을 받아낼 때마다, 공 속도 증가하기
- 공 속도를 조절하기 위해서는 while 반복문에 있는 지연 시간 설정이 핵심임. 지연 시간을 짧게할수록 빨라짐.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/94e7ee2ca6f8814bfc80a925cb135ec9257a2d1a/Day22-Pong-game/main.py#L27-L28

- 매번 ball_move_speed 값을 약간씩 작게 하되 음수가 되지 않게 해야함. 만약 음수가 되면 오류가 생김.

- 패들에 부딪혀 x_bounce를 할 때마다 0.8을 곱해주도록 하여 해결함.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/94e7ee2ca6f8814bfc80a925cb135ec9257a2d1a/Day22-Pong-game/ball.py#L23-L25

### 공이 패들 넘어가서도 공이 계속 튕기는 버그
1. [문제상황 - (이 링크에 이슈를 남기고 해결하였다.)](https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/issues/2)

특정 상황에서 공이 패들을 넘어가서도 계속해서 튕기는 문제가 발생했다. 

![day22-pong-game(error)](https://user-images.githubusercontent.com/120784842/226112044-3dc54ef9-de7c-4535-932a-cb9532f17e77.gif)

2. 원인


공이 패들과의 충돌을 알아내는 코드에서 공의 x좌표가  패들의 시작점을 넘어갔는지와 공과 패들과의 거리를 이용해서 충돌을 감지했는데 이렇게하면 공이 패들뒤로 넘어갔음에도 조건을 충족하여 계속해서 튕겨져 나갔다.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/94e7ee2ca6f8814bfc80a925cb135ec9257a2d1a/Day22-Pong-game/main.py#L36-L38

3. 해결방안


공과 패들과의 거리가 아니라 공의 x좌표와 패들의 x,y 좌표를 사용하여 정확히 충돌했을 때를 찾아냄.
패들의 위와 아래에 충돌했을 때도 튕겨져 나가도록 추가함.
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/94e7ee2ca6f8814bfc80a925cb135ec9257a2d1a/Day22-Pong-game/main.py#L39-L43

4. 결과


패들에 부딪혔을 때만 튕겨져 나가도록 수정함.
