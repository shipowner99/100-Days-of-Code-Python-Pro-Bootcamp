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
