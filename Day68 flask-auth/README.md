# 플라스크를 이용한 인증

### 신규 사용자 등록
신규 사용자를 등록하려면 register.html에 입력한 정보를 가져와 users.db에 저장할 email, name, password를 사용하여 신규 User 객체를 만들어야 합니다.
사용자 등록이 완료되면 바로 secrets.html 페이지로 이동할 겁니다.
secrets.html 페이지에 'Hello <insert name>'이 표시되고, 여기에 등록 양식에 입력한 이름이 나타나야 합니다.
```python
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        new_user = User(
            email=data.get('email'),
            password=data.get('password'),
            name=data.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("secrets.html", name=request.form.get('name'))
    return render_template("register.html")
```
```python
  <h1 class="title">Welcome, {{name}}!</h1>
```

### 파일 다운로드하기
사용자가 secrets.html 페이지에 접속하면 기밀 파일을 다운로드할 수 있어야 합니다. 참고로 기밀 파일은 시작 프로젝트의 static > files > cheat_sheet.pdf에 있습니다.

이 문제를 해결하려면 send_from_directory()라는 플라스크의 메소드를 사용해야 합니다.

1. 먼저 secrets.html 페이지로 이동하여 앵커 태그가 /download 경로에서 서버에 GET 요청을 하도록 합니다.
```python
  <a href="{{ url_for('download') }}">Download Your File</a>

```
2. 다운로드 경로에서 사용자가 '파일 다운로드(Download Your File)' 버튼을 클릭하면, send_from_directory()에 대한 문서를 사용하여 cheat_sheet.pdf 파일을 다운로드합니다.

https://flask.palletsprojects.com/en/2.2.x/api/#flask.send_from_directory
```python
@app.route('/download')
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf")
```

### Werkzeug를 사용하여 비밀번호 해싱하기
이 시점에서 사용자의 비밀번호는 데이터베이스에 일반 텍스트로 저장됩니다:

1. 데이터베이스에서 해시되지 않은 이전 항목을 삭제하세요.

비밀번호를 저장하기 전에 해시를 통해 사용자의 비밀번호를 보호합니다.

이를 위해서는 벡자이크(Werkzeug)의 헬퍼 함수 generate_password_hash()를 사용합니다.

2. 다음 링크의 문서를 사용하여 사용자 비밀번호를 해싱 및 솔트하는 방법을 알아내 보세요.
https://werkzeug.palletsprojects.com/en/2.2.x/utils/#module-werkzeug.security

pbkdf2:sha256을 사용하여 비밀번호를 해시하고

솔트 길이(salt length) 8을 추가하세요.
```python
from werkzeug.security import generate_password_hash

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        hash_and_salted_password = generate_password_hash(
            data.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=data.get('email'),
            password=hash_and_salted_password,
            name=data.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("secrets.html", name=request.form.get('name'))
```

### Flask_Login 패키지로 사용자 인증하기
현재는 /secrets으로 이동하면 기밀 페이지와 다운로드 링크가 표시되며, 인증 장벽이 없습니다. 등록/로그인한 사용자만 해당 페이지를 보고 파일을 다운로드할 수 있도록 하려면 어떻게 해야 할까요?

서버의 특정 경로를 보호하고 인증된 사용자만 접근할 수 있도록 해야 합니다.

이를 위해 대다수의 플라스크 개발자는 Flask_Login 패키지를 사용합니다.

고난이도 과제:

Flask_Login 문서를 사용하여 /login 경로를 만들어보세요. /secrets 경로는 로그인한 사용자만 접근할 수 있도록 보호되어야 합니다.

```python
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    pass


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
        return render_template("secrets.html", name=user.name)
    return render_template("login.html")

@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name)

@login_required
@app.route('/download')
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

```
### 플라스크 플래시 메시지
사용자가 수행한 작업에 대한 피드백을 제공하고자 하는 경우가 생길 수 있습니다. 예를 들어 '로그인에 문제가 있었나요?', '잘못된 비밀번호를 입력했거나 이메일이 존재하지 않습니까?'와 같은 피드백을 전달하고 싶은 상황에서 로그인 페이지로 계속 리디렉션하는 대신 무엇이 잘못되었는지 알려준다면 좋은 사용자 경험을 제공할 수 있을 것입니다.

이를 위한 가장 쉬운 방법은 플라스크 플래시(Flask Flash) 메시지를 사용하는 것입니다. 이는 템플릿으로 전송되어 한 번만 표시되는 메시지로, 페이지를 새로고침하면 사라집니다.

https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

1. 아래 예시와 같이 사용자의 이메일이 데이터베이스에 없는 경우, 사용자에게 플래시 메시지를 보내 이를 알리고 로그인 경로로 다시 리디렉션하도록 로그인 경로를 업데이트하세요. 예)
```python
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user is None:
            error = "The email does not exist. Please try again."
            return render_template("login.html", error=error)
```

2. 아래 예시와 같이 check_password 함수가 False를 반환하면 사용자를 다시 로그인 페이지로 리디렉션할 때 플래시 메시지를 보내도록 로그인 경로를 업데이트하세요.
```python
        elif check_password_hash(user.password, password):
            login_user(user)
            return render_template("secrets.html", name=user.name)
        else:
            error = "Password incorrect. Please try again."
            return render_template("login.html", error=error)
```

3. 아래 예시와 같이 사용자가 입력한 이메일이 데이터베이스에 이미 존재할 경우 로그인 페이지로 리디렉션하고 이미 등록된 사용자임을 알리는 플래시 메시지가 표시되도록 /register 경로를 업데이트하세요.
```python
        if User.query.filter_by(email=data.get('email')).first():
            error = "You've already signed up with that email. Log in instead!"
            return render_template("login.html", error=error)
```
### 인증상태를 템플릿에 전달하기
사용자가 로그인할 때 홈페이지에 로그인/등록 버튼이 보이면 안 됩니다. 내비게이션 바에도 등록 또는 로그인이 보이면 안 됩니다.

이렇게 되도록 base.html과 index.html에서 코드를 바꿀 수 있는지 시도해 보세요.

이전 수업에서 base.html이 모든 페이지가 만들어지는 레이아웃 템플릿이라고 배웠던 것을 기억하세요.
```python
#base.html
        {% if not logged_in: %}
      <li class="nav-item">
        <a class="nav-link" href="{{ url_for('login') }}">Login</a>
      </li>
        <li class="nav-item">
        <a class="nav-link" href="{{ url_for('register') }}">Register</a>
      </li>
        {% endif %}
```
```python
#index.html
    {% if not logged_in: %}
    <a href="{{ url_for('login') }}" class="btn btn-primary btn-block btn-large">Login</a>
    <a href="{{ url_for('register') }}" class="btn btn-secondary btn-block btn-large">Register</a>
    {% endif %}
```
```python
#main.py
logged_in=current_user.is_authenticated
# 위 코드를 페이지(홈페이지, register, secret) 렌더링 하는 곳에 넣어준다.
```

## 참고 자료
- Flask-Login
https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
- mixin classes in python
https://www.thedigitalcatonline.com/blog/2020/03/27/mixin-classes-in-python/
- Flask-Message Flashing
https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/