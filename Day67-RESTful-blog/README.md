#
### 요구 사항 1 - 블로그 게시물 항목을 가져올 수 있을 것
시작 프로젝트에 포함된 posts.db SQLite 데이터베이스에서 게시물을 가져오세요.
```python
#main.py - 데이터베이스 생성
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##CONNECT TO DB
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#table 구성
with app.app_context():
    db.create_all()

##DB 사용하여 post 렌더링하기
@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)
```

### 요구 사항 2 - 신규 블로그 게시물을 게시할 수 있을 것
플라스크 서버에 /new-post라는 새 POST 경로를 만드세요.

1. '새 게시물 작성(Create New Post)' 버튼을 클릭하면 make-post.html 페이지가 표시되어야 합니다.
```python
#index.html
<a class="btn btn-primary float-right" href="{{url_for('add_new_post')}}">Create New Post</a>
```
```python
#main.py
@app.route("/new_post", methods=["POST", "GET"])
def new_post():
    form = CreatePostForm()
    return render_template("make-post.html", form=form)
```
플라스크 CKEditor 패키지를 사용하여 WTForm의 블로그 콘텐츠(body)를 전체 CKEditor로 입력하는 방법을 알아야 합니다.
```python
from flask_ckeditor import CKEditor, CKEditorField

#Notice body's StringField changed to CKEditorField
body = CKEditorField("Blog Content", validators=[DataRequired()])
```
```python
# make-post.html -Add import for bootstrap wtf quickform support
{% import "bootstrap/wtf.html" as wtf %}
#Load ckeditor
{{ ckeditor.load() }}

#Configure the ckeditor to tell it which field in WTForm will need to be a CKEditor.
{{ ckeditor.config(name='body') }}

#Add WTF quickform and Make it blue
{{ wtf.quick_form(form, novalidate=True, button_map={"submit":"primary"}) }}
```
2. 사용자가 모든 필드를 입력하면 폼의 데이터를 posts.db에 BlogPost 객체로 저장해야 합니다.
게시물이 저장되면 사용자는 홈페이지로 리디렉션되어야 하며, 저장 프로세스가 성공적으로 이루어진 경우 새 게시물이 표시되어야 합니다.
```python
#main.py 
from datetime import date

@app.route("/new_post", methods=["POST", "GET"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
        title = form.title.data,
        subtitle = form.subtitle.data,
        date = date.today().strftime("%B %d, %Y"),
        body = form.body.data,
        author = form.author.data,
        img_url = form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)
```

### 요구 사항 3 - 기존 블로그 게시물을 편집할 수 있을 것
홈페이지에서 각 블로그 게시물을 클릭하면 해당 블로그 게시물의 post.html 페이지로 이동해야 합니다. 
또한 게시물 끝에는 게시물 수정 버튼이 표시되며, 이 버튼을 클릭하면 make-post.html 페이지로 이동해야 합니다.

1. 새로운 경로 /edit-post/<post_id>를 생성합니다.

사용자가 블로그 게시물(post.html 페이지) 하단에 있는 '게시물 수정(Edit Post)' 버튼을 클릭하면 이 경로로 GET 요청이 이루어져야 합니다. 여기서 post_id는 읽고 있던 게시물의 id입니다.

사용자가 '새 게시물 작성(Create New Post)'에서 온 경우, <h1>은 '새 게시물(New Post)'을 읽어 들여야 하지만 사용자가 특정 블로그 게시물을 수정하려고 온 경우에는 '게시물 수정(Edit Post)'을 읽어 들여야 합니다.
```python
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm()
    return render_template("make-post.html", form=edit_form, is_edit=True)
```
```python
<h1>{{line}}</h1>
```


2. make-post.html로 이동하면 블로그 게시물의 데이터로 WTForm의 필드가 자동으로 채워져야 합니다. 이렇게 하면 사용자가 블로그 게시물을 다시 입력할 필요가 없습니다.
```python
@app.route("/edit-post/<post_id>")
def edit_post(post_id):
    line = "Edit Post"
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title= post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    return render_template("make-post.html", line=line, form=edit_form)

```

3. 사용자가 WTForm에서 수정을 마치고 '게시물 제출(Submit Post)'을 클릭하면 데이터베이스에서 게시물이 업데이트되어야 하며, 사용자는 해당 블로그 게시물의 post.html 페이지로 리디렉션되어야 합니다.
```python
@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    line = "Edit Post"
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title= post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", line=line, form=edit_form)
```

### 요구 사항 4- 블로그 게시물을 삭제할 수 있을 것
1. index.html에서 각 게시물 옆에 ✘ 표시만 보여지는 앵커 태그를 만듭니다. (이 문서에 있는 ✘ 표시를 복사하여 넣어도 됩니다).

해당 표시를 클릭하면 데이터베이스에서 게시물이 삭제되고, 사용자가 홈페이지로 리디렉션되어야 합니다.

/delete/<post_id> 경로에 DELETE 경로를 생성해야 합니다.
```python
            <a href="{{ url_for('delete_post', post_id=post.id) }}">✘</a>
```
```python
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

```
# 유용한 문서

https://flask-ckeditor.readthedocs.io/en/latest/basic.html

https://pythonhosted.org/Flask-Bootstrap/forms.html

https://flask-wtf.readthedocs.io/en/stable/
- 시간 가져오기 <월(완전한 명칭)> <일>, <년>
- 문서:https://www.w3schools.com/python/python_datetime.asp
- CKEditorField의 데이터는 HTML로 저장되며, 여기에는 블로그 게시물의 모든 구조와 스타일이 포함됩니다. 
블로그 게시물의 post.html 페이지로 이동했을 때 이러한 구조가 반영되도록 하려면 Jinja safe() filter를 추가해야 합니다.
이렇게 하면 진자(Jinja)가 post.html 템플릿을 렌더링할 때 HTML을 텍스트로 처리하지 않게 됩니다.
진자 필터를 적용하려면 파이프 기호 '|'가 필요하며, 이 기호는 진자 표현식과 진자 필터 사이에 들어갑니다.
- 예) `{{post.body|safe}}`
https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.safe
- Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.
- 참고: HTML 폼(WTForms 포함)은 PUT, PATCH 또는 DELETE 메소드를 허용하지 않습니다. 따라서 이는 일반적으로 PUT 요청(기존 데이터 교체)이지만, HTML 폼에서 오는 요청이므로 수정된 게시물을 POST 요청으로 받아들여야 합니다.

