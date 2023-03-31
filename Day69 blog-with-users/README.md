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