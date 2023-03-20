# Make POST Requests with Flask and HTML Froms

## 플라스크 서버로 POST 요청 처리하기
### 1. HTML `<form>` 양식에 입력된 데이터를 POST 방식으로 서버로 제출하기
#### 1) HTML `<form>` `method` 속성
form-data를 보내는 방법을 지정합니다.

URL variables(with `method="get"`) 또는 HTTP post transaction(with `method="post"`)으로 보낼 수 있습니다.

>##### GET
> - name/value 쌍의 URL에 form-data를 추가합니다.
> - 길이 제한 있음(약 3000자)
> - url에 표시됨(민감한 데이터 보내지 말 것.)

>##### POST
> - HTTP 요청 본문 내부에 form-data를 추가합니다.(URL에 표시되지 않음)
> - 크기 제한 없음
> - 북마크할 수 없음
  
  
#### 2) HTML `<form>` `action` 속성
form이 제출될 때 form-data를 보낼 위치를 지정합니다.

이때, url_for 를 사용하여 동적으로 생성하는 것이 좋음. 서버가 호스트 되는 장치에 따라 경로가 바뀌지 않기 때문.

  예) 
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/eadf4c713b55f4b7d1f157ddb5b7379304e7f962/Day60-Make-POST-Requests-with-Flask-and-HTML-Forms/templates/index.html#L10
  
  
### 2.`<input>`양식의 각 입력 값에 `name` 속성이 있어야 함.
  https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/eadf4c713b55f4b7d1f157ddb5b7379304e7f962/Day60-Make-POST-Requests-with-Flask-and-HTML-Forms/templates/index.html#L11-L12

### 3. Flask 서버에서 HTML의 POST 요청을 받아서 처리하기
#### HTTP Methods(데코레이터를 main.py 에 만들기)
`route()` 데코레이터의 `methods` 인수를 사용하여 다른 HTTP 매서드를 처리할 수 있음.
`methods` 매개 변수는 딕셔너리 형으로 쓸 수 있으므로 하나의 제출 경로에 메소드 방식은 여러 개 있을 수 있음.

예)` @app.route("/contact", methods=["GET", "POST"]`

https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/eadf4c713b55f4b7d1f157ddb5b7379304e7f962/Day60-Make-POST-Requests-with-Flask-and-HTML-Forms/main.py#L11
  
#### flask 모듈에 있는 Request Object
서버로 전송된 요청 매개 변수를 활용할 수 있는 객체
  
##### 1) `method` 속성(`request.method`)
현재 request method를 지정함.(GET, POST... 이런 것)

예) `request.method = 'POST'`

##### 2) `form` 속성(`request.form`)
form-data(POST 또는 PUT request에서 전송된 데이터)를 딕셔너리 형태로 줌.

request.form gives us the data the user entered in the form as a dictionary
  
https://github.com/shipowner99/100-Days-of-Code-Python-Pro-Bootcamp/blob/eadf4c713b55f4b7d1f157ddb5b7379304e7f962/Day60-Make-POST-Requests-with-Flask-and-HTML-Forms/main.py#L11-L15
  
