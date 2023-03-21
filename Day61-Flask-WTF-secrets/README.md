# 61일차: 고급 입력양식 만들기(Flask-WTF)
## 목표:비밀 키가 있는 웹사이트 만들기
지난번에는 플라스크 서버로 HTML입력양식을 동작하도록하여, 사용자가 양식에 입력한 데이터를 가져와봤다.

이번에는 플라스크 확장 모듈 Flask-WTF를 사용하여 입력양식을 만들 예정이다. 비밀키가 있는 웹사이트 만들기
사용자 이름과 비밀번호를 정확하게 입력해야만 비밀키를 가진 페이지에 접근 할 수 있다.

## Flask-WTF
https://flask-wtf.readthedocs.io/en/1.0.x/form/
## Flask-WTF 의 장점 3가지
1) 쉬운 유효성 검증
  - 사용자가 필수 입력 항목에 올바른 형식으로 데이터를 입력했는지 검증
  - 예) 이메일 주소에 '@', '.' 의 포함 여부 확인.
  - 유효성 검증을 위한 코드를 직접 작성할 필요가 없다.
2) 코드 라인 감소
  - 웹사이트에 입력양식을 많이 사용한다면, 플라스크 입력양식 모듈을 사용하면 작성(혹은 복사 및 붙여넣기)해야 하는 코드의 양을 획기적으로 줄일 수 있다.
3) CSRF 보호 기능 내장
  - 사이트 간 요청 위조(Cross Site Request Forgery), 줄여서 CSRF
  - https://owasp.org/www-community/attacks/csrf
  - 모르는 사람에게 돈을 송금하는 등 사용자가 자신의 의지와는 무관한 행동을 하게 하는 공격
  - 이런 공격은 웹사이트의 보안을 해침.
  - 웹사이트의 입력양식을 만들 때 보통 Flask-WTF 를 사용하지만 실제로 HTML 입력양식으로 만든 프로젝트도 있끼 때문에 두 가지 방법의 동작원리를 이해하는 것이 중요함.
## Flask-WTF 설치
  - 터미널에서 `pip install Flask-WTF`

## 입력 양식 만들기

- import 모듈:
- ```python
  #main.py
  from flask_wtf import FlaskForm
  from wtforms import StringField
  ```
- FlaskForm 이용하여 form 만들기:
- ```python
  #main.py
  class LoginForm(FlaskForm):
      email = StringField('Email')
      password = StringField('Password')
  ```
- form 사용하기:
- ```python
  #main.py
  @app.route("/login")
    def login():
      login_form = LoginForm(meta={'csrf': False})
      return render_template('login.html', form=login_form)
  ```
- CSRF 보호 기능 넣기:
- ```python
  #login.html  
  {{form.csrf_token }}
  #main.py
  app.secret_key = "some secret string"
  ```
- rendering 하기:
- ```python 
  #login.html
  <form method="POST" action="{{url_for('login')}}">
  {{ form.csrf_token }}
  {{ form.email.label }} {{ form.email(size=30) }}
  {{ form.password.label }} {{ form.password(size=30) }}
  <input type="submit"  value="Log In">
  ```
## 유효성 검사 추가하기
### 1. validator 객체 추가하기
- ```python
  #main.py
  from wtforms.validators import DataRequired
  
  #main.py
  email = StringField(label='Email', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired()])
  ```
- `validators` 매개변수는 validator 객체의 리스트
- DataRequired : 데이터를 필수로 입력해야함. 사용자가 아무것도 입력하지 않을 경우, 오류가 발생
- 입력양식이 제출된 후 오류가 많으면 `errors` 리스트가 생성되어 오류를 발생시킨 필드의 프로퍼티로 HTML에 전달됨
- 예) `form.<field>.errors`
### 2. 오류 발생시, 반복문을 사용하여 이 오류들을 텍스트로 보여줄 수 있음.
https://wtforms.readthedocs.io/en/2.3.x/crash_course/#displaying-errors
- ```python
  {{ form.email.label }} <br> {{ form.email(size=30) }}
  {% for error in form.email.errors: %}
  <span style="color:red">{{error}}</span>
  {% endfor %}
  ```
  
### 3. 사용자가 제출 버튼을 눌렀을 때 입력 값의 유효성을 검증하기.
- 기존 코드를 수정하여 `POST`요청에 응답 후 데이터를 `validate_on_submit()`으로 검증할 수 있어야 함.
- ```python
  @app.route("/login", methods=["GET", "POST"])
  def login():
    login_form = LoginForm()
    login_form.validate_on_submit()
      return render_template('login.html', form=login_form)
  ```
- 이 동작은 WTForm의 유효성 검증이 아니라, 브라우저에 내장된 검증 방법으로 브라우저마다 다르다.
- 사용자가 인터넷 익스플로러를 사용한다면, 별도의 검증 방법이 없음.

### 4. 모든 사용자가 입력창의 유효성 검증을 받도록 입력 양식에 `novalidate`라는 속성으로 브라우저 검증을 꺼야 함.
- ```python
  #login.html
  <form method="POST" action="{{url_for('login')}}" novalidate>
  ```
## WTForms로 폼 데이터 수신하기
- HTML 에서는 플라스크의 request객체 사용
- WTForms 에서는 `<form_object>.<form_filed>.data` 사용
- https://wtforms.readthedocs.io/en/2.3.x/crash_course/#how-forms-get-data
- 단, 필드 데이터를 인쇄하기 전에 폼이 제출된 것인지(POST 요청) 아니면 해당 폼이 렌더링 될 때 GET 요청된 것인지 여부를 확인해야함
- 앞에서는 `if request.method == "POST`를 사용함.
- 이번에는 `validate_on_submit()`의 반환 값을 확인해볼텐데, 이 반환값은 사용자가 폼을 제출한 후 유효성 검증이 성공한 경우 `True`, 실패한 경우 `False`가 됨.


## Jinja2로 템플릿 상속하기
- 진자를 사용하여 웹 사이트를 템플릿화 할 수 있음
- ```python
  #hearder.html footer.html 을 삽입하는 코드
    {% include "header.html%}
    웹 페이지 컨텐츠
    {% include "footer.html%}
  ```
### 템플릿 상속
- 실제 전체 웹 사이트에 동일한 디자인 템플릿을 사용하고 싶지만 헤더나 푸터의 일부 코드를 변경해야 하는 때 사용
- 클래스 상속과 유사해서 상위 템플릿을 가져와 하위 웹 페이지에서 스타일을 확장할 수 있음.
```python
#base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```
이 템플릿을 상속하는 하위 웹페이지에 의해 새 콘텐츠를 삽입할수 있는 미리 정의된 블록이 있음.
1) success.html 페이지를 base.html 템플릿으로부터 상속하기
```python
#success.html
#1.
{% extends "base.html" %}
#2.
{% block title %}Success{% endblock %}
#3.
{% block content %}
   <div class="container">
      <h1>Top Secret </h1>
      <iframe src="https://giphy.com/embed/Ju7l5y9osyymQ" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
      <p><a href="https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ">via GIPHY</a></p>
   </div>
{% endblock %}
```
(#1) 이 라인은 템플릿 엔진(진자)이 'base.html'을 이 페이지의 템플릿으로 사용하도록 명령

(#2) 이 블록은 템플릿의 헤더에 사용자 정의된 제목을 삽입함.

(#3) 이 블록은 웹 사이트의 콘텐츠를 제공하며, 해당 부분은 웹 페이지마다 달라짐.

2) success.html 에 적용하면..
```python
#success.html
{% extends "base.html" %}
{% block title %}Success{% endblock %}
{% block content %}
   <div class="container">
      <h1>Top Secret </h1>
      <iframe src="https://giphy.com/embed/Ju7l5y9osyymQ" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
      <p><a href="https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ">via GIPHY</a></p>
   </div>
{% endblock %}
```

3) base.html에 배경 추가하면..
```python
<style>
{% block styling %}
body{
    background: purple;
}
{% endblock %}
</style>
```
success.html과 denied.html 모두 보라색 배경이됨.

4) denied.html 에서만 글자 색 추가로 바꾸기
```python
#denied.html
{% block styling %}
   {{ super() }}
   h1 {
      color:red;
   }
{% endblock %}
```

## 플라스크 부트스트랩을 상속된 템플릿으로 사용하기
1) 설치
`pip install Flask-Bootstrap`
2) 문서에 따라 파일 수정
https://pythonhosted.org/Flask-Bootstrap/basic-usage.html

## WTForms를 지원하는 플라스크 부트스트랩
- WTForms로 폼을 만드는 가장 편리한 방법
- `{{wtf.quick_form(form)}}`을 사용하면 한 줄의 코드로 간단하게 폼을 만들 수 있음.
- 탬플릿에 상속된 WTForms 객체(`form`)를 가져옴으로써 폼에 대한 모든 레이블, 입력, 버튼, 스타일을 생성함.
- 전체 요소를 삭제하고, 부트스트랩으로부터 wtf 지원을 상속하기위한 줄을 추가한 다음 `quick_form()`을 사용하기만 하면 간단하게 나만의 `form`을 생성할 수 있음.
- ```python
    {% import "bootstrap/wtf.html" as wtf %}
  ...
    {{wtf.quick_form(form, novalidate=True) }}
  ```


## requirements.txt
- 필요한 라이브러리(프로젝트에 필요한 설치 패키지들)와 버전을 명시할 수 있다.
- 필요한 패키지를 포함하지 않고 프로젝트를 공유할 수 있으므로 프로젝트 파일의 크기가 훨씬 줄어든다.
- 프로젝트를 다운로드했을 때, 코드 편집기에서 requirement.txt 파일에 있는 필요 패키지들을 설치하라고 한다.
- https://docs.google.com/document/d/e/2PACX-1vRIW_TuZ6z0ASjAoxgJgmzjGYLCDx019tKvphaTwK_Za7fnMKywUuXI0-s5wr0nQI_gprm6J6y7L9rL/pub

### requirements.txt 파일을 만드는 방법
- 환경을 일관되게 유지하려면 환경 패키지의 현재 상태를 고정하는 것이 좋다.
`$ pip freeze > requirements.txt`
- 이렇게 하면 현재 환경의 모든 패키지와 해당 버전의 간단한 목록이 포함된 requirements.txt 파일이 생성됨
- `pip list`를 사용하여 요구 사항 형식 없이 패키지 목록을 볼 수 있음.(?)
- freeze 하기 전에 virtualenv 를 활성화 해야함.

### requirements.txt 파일을 사용하는 방법
- 나중에 다른 개발자(또는 환경을 다시 만들어야 하는 경우)가 동일한 버전을 사용하여 동일한 패키지를 설치하는 것이 더 쉽다.
- `$ pip3 install -r requirements.txt`
- 설치, 배포 및 개발자 간에 일관성을 보장하는데 도움이 된다.
- github 리포지토리에서 requirements.txt 파일을 실행하려면?
- 1) 복제 또는 다운로드한 리포지토리의 마스터 폴더 내에 새 가상 환경을 설정한다.(python3로 새 가상 환경 만들기-https://docs.google.com/document/d/1g6A5vbniN2ZoFUWaHJD35t9qiXS9raJ14hlzK4qot7g/edit)
- 2) 해당 virtualenv를 활성화한다.
- 3) 표시된 `pip3 install` 명령을 실행한다. 각 패키지의 올바른 버전 번호를 사용하여 requirements.txt 파ㅣㄹ에 나열된 모든 항목을 설치합니다.