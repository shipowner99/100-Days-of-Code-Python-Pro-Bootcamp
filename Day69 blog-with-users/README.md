# 블로그 사용자 추가하기

### 요구 사항 1 - 신규 사용자 등록
1. 어제 배운 내용을 활용하여 사용자가 /register 경로로 이동해서 블로그 웹 사이트에 등록할 수 있도록 합니다. forms.py에 RegisterForm이라는 WTForm을 만들고 플라스크 부트스트랩을 사용하여 wtf quick_form을 렌더링해야 합니다.

사용자가 입력한 데이터를 사용하여 User 테이블의 blog.db에 새 항목이 만들어져야 합니다.
```python
#forms.py
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")
```
```python
#register.html
{{ wtf.quick_form(form, novalidate=True, button_map={"submit": "primary"}) }}
```
```python
#main.py
#Import RegisterForm from forms.py
from forms import CreatePostForm,  RegisterForm

#Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    
# Create all the tables in the database
with app.app_context():
    db.create_all()

#Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form)
```

### 요구 사항 2 - 등록된 사용자 로그인
1. 성공적으로 등록이 완료된(데이터베이스의 사용자 테이블에 추가된) 사용자는 login 경로로 이동하여 자신의 크리덴셜(자격 증명 정보)을 사용하여 로그인할 수 있어야 합니다. 그러려면 Flask-Login 문서와 어제 배운 내용을 활용해야 합니다.
```python
#forms.py
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("SIGN ME UP!")
```
```python
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


```

2. /register 경로에 코드 한 줄을 추가해서 사용자 등록이 성공적으로 완료된 경우 해당 사용자를 다시 홈페이지로 보내 Flask-Login으로 로그인하도록 만들어보세요.
```python
login_user(new_user)
return redirect(url_for('get_all_posts'))
```

3. /register 경로에서 사용자가 데이터베이스에 이미 존재하는 이메일로 등록을 시도하는 경우, /login 경로로 리디렉션하고 해당 이메일로 로그인하라는 플래시 메시지가 표시되어야 합니다.

```python

#main.py
if User.query.filter_by(email=form.email.data).first():
    flash("You've already signed up with that email, log in instead!")
    return redirect(url_for('login'))
else: ## MORE CODE BELOW

#login.html
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto content">
            {% with messages = get_flashed_messages() %}
            {% if messages %}
            {% for message in messages %}
            <p>{{ message }}</p>
            {% endfor %}
            {% endif %}
            {% endwith %}
            {{ wtf.quick_form(form, novalidate=True, button_map={"submit": "primary"}) }}
        </div>
    </div>
</div>
```
4. /login 경로에서 사용자의 이메일이 데이터베이스에 존재하지 않거나 비밀번호가 check_password()를 사용하여 저장된 것과 일치하지 않을 경우, 다시 /login으로 리디렉션하고, 사용자에게 어떤 문제가 발생했는지 알리고 다시 시도하도록 요청하는 플래시 메시지가 표시되도록 해야 합니다.
```python

```


5. 어떻게 내비게이션 바를 업데이트하면 사용자가 로그인하지 않은 경우 다음과 같이 표시되도록 할 수 있는지 알아내 보세요.


단, 사용자가 등록 후 로그인/인증된 경우에는 내비게이션 바에 다음과 같이 표시되어야 합니다.


힌트: 내비게이션 바 코드는 header.html 안에 있습니다.

힌트: https://flask-login.readthedocs.io/en/latest/#login-example

해답



6. 사용자가 로그아웃 버튼을 클릭하면 로그아웃하고 홈페이지로 다시 이동하도록 /logout 경로를 코딩하세요.

다음과 같이 되어야 합니다.