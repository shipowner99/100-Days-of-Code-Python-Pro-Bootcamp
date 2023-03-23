# 가상 책장 만들기
Uploading Library - 프로필 2 - Microsoft​ Edge 2023-03-23 12-02-59.mp4…

## 목표
- 플라스크 웹 사이트에 SQLite 데이터베이스 구축하기
- 추가한 모든 책이 데이터베이스에 저장될 수 있도록 하고, 
- 데이터베이스의 전체 CRUD 기능을 활용하기 위한 몇 가지 추가 기능을 만들어보세요.

## 웹사이트 과제 요구사항
- /add 경로를 통해 새 책을 추가하고, 책이 데이터베이스에 성공적으로 추가되면 홈페이지로 리디렉션되어야 합니다.
- 홈페이지에 데이터베이스의 모든 책이 표시되어야 합니다:
- 각각의 도서 <li>에 평점 수정(Edit Rating) 앵커 태그를 추가합니다. 버튼을 누르면 사용자가 해당 책에 대한 새로운 평점을 입력할 수 있는 평점 수정 페이지로 이동할 수 있어야 합니다. 그런 다음 '평점 변경'을 클릭하면 홈페이지로 돌아가고 책 옆에 새로운 평점이 표시되어야 합니다.
- 각 도서 목록 <li>에 삭제(Delete) 앵커 태그를 추가하여, 클릭 시 데이터베이스에서 책을 삭제하고 홈페이지로 다시 리디렉션되도록 합니다.

### SQLAlchemy로 데이터베이스 만들기
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
# initialize the app with the extension
db.init_app(app)
```
### SQLAlchemy로 Table만들기
```python
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
```
```python
with app.app_context():
    db.create_all()
```
#### Query the Data
##### 새 레코드 만들기
```python
added_book = request.form
data = added_book.to_dict()
new_book = Book(title=data["title"], author=data["author"], rating=data["rating"])
db.session.add(new_book)
db.session.commit()
```
#### 모든 레코드 읽기
`all_books = db.session.query(Book).all()`

#### 쿼리별 레코드 업데이트하기
```python
book_to_update = Book.query.filter_by(title="Harry Potter").fisrt()
book_to_update.title = "Harry Potter and the Chamber of Secrets"
db.session.commit()
```
### 기본키로 레코드 업데이트하기
https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.get
```python
book_id = 1
book_to_update = Book.query.get(book_id)
book_to_update.title = "Harry Potter and the Goblet if Fire"
db.session.commit()
```
### 기본키로 특정 레코드 삭제하기
```python
book_id = 1
book_to_delete = Book.query.get(book_id)
db.session.delete(book_to_delete)
db.session.commit()
```

### Edit Rating-평점 수정 페이지를 표시하기 위한 GET 요청 시 책 ID를 매개변수로 전달하는 방법
1. a태그에서 url_for로 GET 요청과 동시에 매개변수도 같이 보낼 수 있음.
```python 
# index.html
<a href="{{ url_for('edit', id=book.id) }}">Edit Rating</a>
```
2. GET 요청은 자동으로 받아짐. 매개 변수는 request.args.get('파라미터') 로 받을 수 있음.
```python
# main.html
def edit():
    id = request.args.get('id')
    book_selected = Book.query.get(id)
    return render_template('edit.html', book=book_selected)
```
3. form 으로 POST 요청을 보낼 수 있음.
```python
# edit.html
<form action="{{ url_for('edit') }}" method="POST">
<input hidden="hidden" name="id" value="{{book.id}}">
<input name="rating" type="text" placeholder="New Rating">
<button type="submit">Change Rating</button>
```
 
3. POST 요청은 request.method=="POST" 로 받기. 매개변수는 request.form["name"] 으로 받을 수 있음.
```python
# main.html
@app.route("/edit", methods=['GET', 'POST'])
def edit():
if request.method == "POST":
    #UPDATE RECORD
    book_id = request.form["id"]
    book_to_update = Book.query.get(book_id)
    book_to_update.rating = request.form["rating"]
    db.session.commit()
    return redirect(url_for('home'))
```
### Delete에서 요청과 파라미터 보내고 받는 방법
1. a태그로 GET 요청과 파라미터 보냄
` <a href="{{ url_for('delete', id=book['id']) }}">Delete</a>
2.main.html 에서 delete 함수를 만들어서 GET 요청 받고, request.args.get 으로 파라미터 받기. 
```python
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
```


