# 가상 책장 만들기

## 목표
- SQ 라이트 데이터베이스 생성하는 방법
- 데이터베이스에서 데이터를 생성, 읽기, 업데이트, 삭제하는 방법
- 필요할 때마다 데이터를 제공할 수 있도록 데이터베이스를 Flask 애플리케이션과 연결하기

## SQ 라이트

### 데이터베이스 만들기
1. 새 프로젝트를 만들고 main.py 파일 내에서 sqlite3 모듈을 가져옵니다.

`import sqlite3`

2. 이제 새 데이터베이스에 대한 연결을 생성합니다(데이터베이스가 존재하지 않는 경우 생성됨).
```python
db = sqlite3.connect("books-collection.db")
```
3. main.py를 실행하면 books-collection.db라는 새 파일이 파이참에 표시되어야 합니다.

4. 다음에는 데이터베이스를 제어하는 커서를 만들어야 합니다.

`cursor = db.cursor()
`

커서는 마우스 또는 포인터라고도 합니다. SQ 라이트 데이터베이스를 수정할 때 커서가 필요합니다.


### 데이터베이스에 표 만들기

5. 표를 하나 만들어 봅시다. 앞서 작성한 모든 줄 아래에 다음과 같은 코드를 추가합니다.
```python
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
```

하나씩 살펴보겠습니다.

>cursor - 4단계에서 생성한 커서는 데이터베이스의 마우스 포인터로서 모든 작업을 수행하게 됩니다.

>.execute() - 이 메소드는 커서가 작업을 실행하도록 명령합니다. SQ 라이트 데이터베이스의 모든 작업은 구조화 질의어(SQL, Structured Query Language)라는 명령어로 표현되는데, 이는 키워드가 모두 대문자로 쓰인 영어 문장과 비슷합니다. 

>CREATE TABLE -  - 데이터베이스에 새 표를 생성하는 키워드로 이 뒤에 표 이름이 오게 됩니다.
>관련 문서: https://www.w3schools.com/sql/sql_ref_create_table.asp

>books -  생성 중인 새 표에 우리가 부여한 이름입니다.

>() -  CREATE TABLE books ( ) 다음의 괄호 안에 들어가는 부분은 이 표의 필드입니다. 또는 엑셀 시트의 열 제목이라고 생각하면 됩니다.


>id INTEGER PRIMARY KEY - 'id'라고 불리는 첫 번째 필드로서 데이터 유형이 INTEGER이고 이 표의 PRIMARY KEY가 됩니다. 기본키(primary key)는 표에서 이 레코드를 고유하게 식별하는 데이터 중 일부입니다. 예를 들어 한 국가 내에서 동일한 여권 번호를 가진 사람은 없기 때문에 사람의 기본 키는 여권 번호가 될 수 있습니다.

>title varchar(250) NOT NULL UNIQUE - 두 번째 필드로 '제목(title)'이라고 합니다. 문자로 구성된 가변 길이 문자열이 허용되며, 괄호 안의 250은 최대 텍스트 길이입니다. NOT NULL은 값이 있어야 하며 비워 둘 수 없음을 의미합니다. 또한, UNIQUE는 이 표의 두 레코드가 동일한 제목을 가질 수 없음을 의미합니다.

>author varchar(250) NOT NULL - author라고 불리는 필드로 최대 250자의 작성자 가변 길이 문자열이 허용되며 비워 둘 수 없습니다.

>rating FLOAT NOT NULL - rating이라는 필드로 실수형(FLOAT) 데이터 유형 숫자가 허용되며 비워 둘 수 없습니다.


6. 5단계에서 작성한 코드를 실행해도 눈에 띄는 변화는 없을 것입니다. 데이터베이스를 보려면 몇 가지 특수한 소프트웨어를 다운로드해야 합니다.

https://sqlitebrowser.org/dl/

7. DB Browser를 다운로드 및 설치했으면 해당 브라우저를 열고 '데이터베이스열기(Open Database)'를 클릭합니다.


8. 프로젝트 위치(PyCharm Projects라는 폴더에 있어야 함)로 이동하여 books-collection.db를 엽니다.


이때 4개의 필드가 포함된 books라는 표가 표시되어야 합니다.


이게 우리가 만든 데이터베이스입니다.

9. 데이터를 표에 추가하려면 main.py로 돌아가서 다음의 코드를 작성하면 됩니다.
```python
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()
```
그러면 books 표에 '해리 포터'라는 새 항목이 생성되고 변경 사항이 데이터베이스에 적용됩니다.

10. 이제 books라는 표가 생성된 이전 코드 라인을 주석 처리합니다. 그렇지 않으면 `sqlite3.OperationalError: table books already exists`라는 오류 메시지가 뜨게 됩니다.



11. 그런 다음 '데이터베이스 닫기(Close Database)'를 클릭하여 DB Browser에서 데이터베이스를 닫습니다. 그렇지 않을 경우 파이참에서 데이터베이스로 작업할 때 database locked 이라는 경고가 표시됩니다.


12. 이제 main.py에서 코드를 실행하고, DB Browser에서 데이터베이스를 다시 열어서 업데이트된 books 표를 확인합니다. 다음과 같이 표시되어야 합니다.


SQL 쿼리는 오타에 매우 민감합니다. 만약 다음과 같이 작성하지 않고,

`cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()`
아래와 같이 작성한다면,

`cursor.execute("INSERT INTO books VALUE(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()`
코드가 실행되지 않습니다(코드에서 차이점을 발견하셨나요?)

하지만 다행히 파이썬 프로젝트에서 SQ 라이트로 작업할 때 오류가 발생하기 쉬운 이러한 SQL 명령어 대신 사용할 수 있는 훨씬 좋은 방법이 있습니다. 바로 SQL 알케미(SQLAlchemy)라는 도구를 사용하여 파이썬 코드를 작성하는 거죠. 그럼 다음 수업에서 함께 작성해보겠습니다!

## SQLAlchemy
보셨듯이 SQL 명령어 작성은 복잡하며 오류가 발생하기 쉽습니다. 이럴 때 파이썬 코드를 작성하고 컴파일러가 코드상의 오타와 오류를 찾아낼 수 있도록 도와주는 무언가가 있으면 훨씬 편리하겠죠. 그래서 만들어진 것이 바로 SQLAlchemy입니다.
파이썬 문법만으로도 데이터베이스를 다룰 수 있다. ORM을 이용하면 개발자가 쿼리를 직접 작성하지 않아도 데이터베이스를 처리할 수 있다.

- 객체 관계형 매핑(ORM, Object Relational Mapping) 라이브러리라고 정의되는데, 이는 데이터베이스의 관계를 객체에 매핑할 수 있다는 뜻입니다. 이때 필드는 객체 속성이 되고, 표는 별도의 클래스, 데이터의 각 행은 새 개체로 정의될 수 있습니다. 
1. SQ 라이트3 모듈을 사용하여 SQ 라이트 데이터베이스를 직접 생성한 기존 코드를 모두 주석 처리합니다.

2. 필요한 패키지인 flask 및 flask_sqlalchemy를 설치하고 각각에서 Flask와 SQLAlchemy 클래스를 임포트합니다.
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
```

도전 과제: 주석 처리된 코드에서 수행한 모든 작업을 SQL 알케미로 수행하는 방법을 SQL알케미 문서를 활용하여 찾아보세요.

### document
#### Configure(구성하다) the Extension(확장): 새 데이터베이스 만들기
The only required Flask app config is the `SQLALCHEMY_DATABASE_URI` key. That is a connection string that tells SQLAlchemy what database to connect to.

Create your Flask application object, load any config, and then initialize the SQLAlchemy extension class with the application by calling `db.init_app`. This example connects to a SQLite database, which is stored in the app’s instance folder.
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)
```

The db object gives you access to the db.Model class to define models, and the db.session to execute queries.

See Configuration for an explanation of connections strings and what other configuration keys are used. The SQLAlchemy object also takes some arguments to customize the objects it manages.

#### Define Models : 새 표 만들기(1)
Subclass `db.Model` to define a model class. The `db` object makes the names in `sqlalchemy` and `sqlalchemy.orm` available for convenience, such as `db.Column`. The model will generate a table name by converting the `CamelCase` class name to `snake_case`.
```python
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
```
The table name "user" will automatically be assigned to the model’s table.
#### Create the Tables : 새 표 만들기(2)
After all models and tables are defined, call S`QLAlchemy.create_all()` to create the table schema in the database. This requires an application context. Since you’re not in a request at this point, create one manually.
```python
with app.app_context():
    db.create_all()
```
If you define models in other modules, you must import them before calling create_all, otherwise SQLAlchemy will not know about them.

create_all does not update tables if they are already in the database. If you change a model’s columns, use a migration library like Alembic with Flask-Alembic or Flask-Migrate to generate migrations that update the database schema.

#### Query the Data
Within a Flask view or CLI command, you can use `db.session` to execute queries and modify model data.

SQLAlchemy automatically defines an` __init__` method for each model that assigns any keyword arguments to corresponding database columns and other attributes.

`db.session.add(obj)` adds an object to the session, to be inserted. Modifying an object’s attributes updates the object. `db.session.delete(obj)` deletes an object. Remember to call `db.session.commit()` after modifying, adding, or deleting any data.

```python
new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
db.session.add(new_book)
db.session.commit()
```

## SQLAlchemy를 사용한 CRUD 작업
### CRUD란?
- Create
- Read
- Update
- Delete

### 새 레코드 만들기
```python
new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
db.session.add(new_book)
db.session.commit()
# 새 레코드를 만들 때 기본 키 필드는 선택사항이며, 다음과 같이 작성할 수도 있음.
new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
```
### 모든 레코드 읽기
`all_books = session.query(Book).all()`

### 쿼리별 레코드 업데이트하기
https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter_by
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