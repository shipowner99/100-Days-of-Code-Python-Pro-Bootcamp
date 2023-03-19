# us-states-game-project (day 25)


## 게임 방법
1. 미국 지도에서 빈칸으로 되어 있는 50개의 모든 주를 맞추면 됩니다.
1. 정답창에 "Exit"을 치면 게임을 끝낼 수 있고 CSV 파일이 생겨서 그 안에 50개 중에 맞추지 못했던 주를 확인할 수 있습니다.  
## 배운 점

## Working with CSV files
### CSV 
표 형태로 된 데이터를 대표하는 일반적인 방식(comma seperated Values)

## Analysing Data with Pandas
https://pandas.pydata.org/docs/index.html

### 판다스의 주요 데이터 구조 2가지
#### data frame
전체 표와 같은 것
L10 복붙
to.dict() : 각 열에 독립된 딕셔너리를 만들어줌.
L11 복붙
#### series
일종의 리스트로 표에서 한 열column(세로)을 말함.

to_list() : 리스트로 만들어줌.

### Get Data in columns
>```
>data.["condition"]
또는
>```
>data.condition

### Get data in row
>```
>data[data.day == "Monday"]
>data[data.temp == data.temp.max()]
전체 데이터[데이터.열 == 특정 열] 

또는 전체 데이터[데이터.열 == 특정 값]
L29 복붙
#### Create a dataframe from scratch
>```
>data_dict = {
>    "students": ["Amy", "James", "Angela"],
>    "scores": [76, 56, 65]
>}
>data = pandas.DataFrame(data_dict)
>```
>데이터 프레임을 csv파일로 변환하려면?
> ```
> data.to_csv(파일을 저장할 경로)
> ```
> L21-L22 복붙
