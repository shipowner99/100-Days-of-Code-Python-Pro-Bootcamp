# 가상 책장 만들기

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
제목 또는 다른 속성별 특정 값을 조회하여 삭제할 수도 있습니다.

## doc 읽기 위해 따로 공부한 것..
### instance folder
- Flask 에서 민감한 정보를 포함한 변수를 정의해야 할 때 사용
- config.py 로 분리하여 저장.
- database password나 API key 같은 것들 숨길 때 사용.
-애플리케이션의 레포지토리 루트의 하위 디렉토리로, 이 애플리케이션의 인스턴스를 위한 구성 파일을 포함합니다. 이를 사용하면 데이터베이스 비밀번호, API 키와 같은 비밀 정보를 숨길 수 있습니다. 이 폴더는 버전 관리에 포함되지 않아야 합니다.

- Flask에서 instance folder를 사용하면 애플리케이션의 루트 디렉토리 외부에 위치하므로 로컬 데이터를 저장할 수 있습니다. 이 폴더는 버전 관리에 포함되지 않아야 하며, Flask는 이 폴더를 자동으로 생성하지 않습니다.

### query 란
질문, 문의하다란 뜻

데이터베이스에게 특정한 데이터를 보여달라는 클라이언트의 요청을 말함. 

쿼리문을 작성한다는 말은 데이터베이스에서 원하는 정보를 가져오는 코드를 작성한다는 뜻.
데이터베이스를 사용하려면 SQL이라는 구조화된 질의를 작성하고 실행해야 하는 등 복잡한 과정이 필요함.

### 데이터베이스 개념
https://www.oracle.com/kr/database/what-is-database/
데이터베이스는 구조화된 정보 또는 데이터의 조직화된 모음으로서 일반적으로 컴퓨터 시스템에 전자적으로 저장됩니다 데이터베이스는 일반적으로 데이터베이스 관리 시스템(DBMS)에 의해 제어됩니다. 연결된 애플리케이션과 함께 데이터와 DBMS를 하나로 묶어 데이터베이스 시스템이라고 하며 단축하여 데이터베이스라고도 합니다.

오늘날 운영되고 있는 가장 일반적인 유형의 데이터베이스에서 데이터는 일반적으로 처리 및 데이터 쿼리를 효율적으로 수행하기 위해 일련의 테이블에서 행과 열로 모델링됩니다. 그러면 데이터에 쉽게 액세스하고 관리, 수정, 업데이트, 제어 및 구성할 수 있습니다. 대부분의 데이터베이스는 데이터 작성 및 쿼리에 SQL(Structured Query Language)을 사용합니다.

### SQL(Structured Query Language)
SQL은 데이터를 쿼리, 조작 및 정의하고 액세스 제어를 제공하기 위해 거의 모든 관계형 데이터베이스에서 사용되는 프로그래밍 언어입니다. 

### 관계형 데이터베이스
관계형 데이터베이스는 1980년대를 지배했습니다. 관계형 데이터베이스의 항목은 열과 행이 있는 테이블 집합으로 구성됩니다. 관계형 데이터베이스 기술은 정형 정보에 액세스하는 가장 효율적이고 유연한 방법을 제공합니다.
데이터베이스의 유형 중 하나.

### ORM(object relatinal mapping)
개발자가 쿼리를 직접 작성하지 않아도 데이터베이스의 데이터를 처리할 수 있음.
즉, 데이터베이스에 데이터를 저장하는 테이블을 파이썬 클래스로 만들어 관리하는 기술!
- 장점: 데이터베이스의 종류에 상관 없이 일관된 코드를 유지할 수 있어서 프로그램을 유지.보수하기가 편리하다. 또한 내부에서 안전한 SQL쿼리를 자동으로 생성해주므로 개발자가 달라도 통일된 쿼리를 작성할 수 있고 오류 발생률도 줄일 수 있다. 
파이썬 ORM 라이브러리 중 가자 많이 사용하는 것이 SQLAlchemy 임.

#### model
데이터를 다룰 목적으로 만든 파이썬 클래스이다. 데이터를 관리하는 데 사용하는 ORM 클래스를 모델이라고 한다. 모델을 사용하면 내부에서 SQL을 자동으로 생성해주므로 직접 작성하지 않아도 된다.



### 데이터베이스 소프트웨어(DBMS) 
데이터베이스 소프트웨어는 "데이터베이스 관리 시스템"(DBMS)이라고도 합니다.데이터베이스 소프트웨어는 사용자가 데이터를 구조화된 형태로 저장한 다음 액세스할 수 있도록 하여 데이터 관리를 간소화합니다. 일반적으로 데이터를 생성하고 관리하는 데 도움이 되는 그래픽 인터페이스가 있으며 경우에 따라 사용자는 데이터베이스 소프트웨어를 사용하여 데이터베이스를 구성합니다.인기 데이터베이스 소프트웨어 또는 DBMS로는 MySQL, Microsoft Access, Microsoft SQL Server, FileMaker Pro, Oracle Database 및 dBASE가 있습니다.




### CLI(Command Line Interface)란?
명령 줄 인터페이스(CLI, Command line interface) 또는 명령어 인터페이스는 텍스트 터미널을 통해 사용자와 컴퓨터가 상호 작용하는 방식을 뜻한다. 즉, 작업 명령은 사용자가 컴퓨터 키보드 등을 통해 문자열의 형태로 입력하며, 컴퓨터로부터의 출력 역시 문자열의 형태로 주어진다. ( - 위키백과 - )
Windows 사용자들이 접하게 되는 CMD 창과 Mac OS 사용자들이 접하게 되는 Terminal 창이 바로 명령 줄 인터페이스를 제공하는 프로그램이다. 이제 이 프로그램을 어떻게 사용 해야 되는 지에 대해 알아보자. 우리는 이런 입출력이 가능하게 해주는 소프트웨어나 하드웨어를 터미널(terminal)이라고 한다. 또한, 사용자가 입력한 명령어를 해석해 주는 소프트웨어를 셸(shell)이라고 한다.