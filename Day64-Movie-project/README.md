# 영화 웹사이트 베스트 10
## 목표: Flask/WTForms/SQLite/SQLAlchemy 등을 사용하여 역대 최고의 영화 10편을 꼽는 웹사이트 만들기
앞으로 보는 영화를 목록에 업데이트하고 사람들에게 추천할 영화를 관리하기
### 요구 사항 1 - 영화 목록 항목을 볼 수 있을 것

1. SQL 알케미를 사용하여 SQ 라이트 데이터베이스를 만듭니다. 데이터베이스에는 'Movie'라는 이름의 표가 있어야 하며, 이 표에는 다음의 필드가 포함되어야 합니다.
```python
id 
title 
year 
description 
rating 
ranking
review
img_url
```
```python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-best10.db"
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(250))
    year = db.Column(db.Text)
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.Text)
    img_url = db.Column(db.Text)

with app.app_context():
    db.create_all()
```
2. 코드/DB Viewer를 사용하여 다음 값으로 데이터베이스에 새 항목을 추가합니다.
```python
with app.app_context():
    new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
    db.session.add(new_movie)
    db.session.commit()
```

### 요구 사항 2 - 영화 등급 및 리뷰를 수정할 수 있을 것
영화 카드 뒷면에는 'Update' 버튼이 있고, 이 버튼을 클릭하여 평점과 리뷰를 변경할 수 있어야 합니다.
```python
#index.html
<a href="{{url_for('edit', id=movie.id)}}" class="button">Update</a>
```
1. WTForms을 활용하여 RateMovieForm을 만들고 이를 사용하여 edit.html에서 렌더링할 Quick Form을 생성합니다.
```python
#main.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
class MovieRatingForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField("Done")
```
```python
#edit.html
{{wtf.quick_form(form, novalidate=True) }}
```

2. 폼을 제출하고 유효성을 검사한 다음에는 데이터베이스의 해당 영화 항목에 업데이트 사항을 추가합니다.

https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application

```python
#main.py
@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = MovieRatingForm()
    table_id = request.args.get('id')
    movie_seleted = Movie.query.get(table_id)
    if form.validate_on_submit():
        movie_to_update = Movie.query.get(table_id)
        movie_to_update.rating = float(form.rating.data)
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie = movie_seleted, form=form)
```
### 요구 사항 3 - 데이터베이스에서 영화를 삭제할 수 있을 것
1. 각 영화 카드의 뒷면에는 삭제 버튼도 있어야 하며, 이 버튼을 클릭하면 데이터베이스에서 영화 항목을 삭제할 수 있어야 합니다.
```python
#index.html
<a href="{{url_for('delete', id=movie.id)}}" class="button delete-button">Delete</a>
```
```python
#main.py
@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_seleted = Movie.query.get(movie_id)
    db.session.delete(movie_seleted)
    db.session.commit()
    return redirect(url_for('home'))
```

### 요구 사항 4 - 페이지 추가를 통해 새 영화를 추가할 수 있을 것
앞에서는 하드코딩된 코드 조각이나 DB 뷰어를 사용하여 데이터베이스에 새 항목을 추가했으나, 이번에는 이러한 작업을 수행할 수 없는 사용자를 위해 add페이지를 작동시킴으로써 영화를 추가하고 API를 사용하여 포스터 이미지, 출시 연도, 영화 설명을 가져올 수 있도록 해야 합니다.

1. 홈페이지에서 ‘영화 추가(Add Movie)’ 버튼을 클릭하면 add 페이지가 렌더링되도록 합니다. add 페이지에는 영화 제목이라는 1개의 필드만 포함된 WTF quick form이 표시되어야 합니다.
```python
#index.html
<a href="{{url_for('add')}}" class="button">Add Movie</a>
```
```python
#main.py
class MovieAddingForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField("Add movie")
    
@app.route('/add', methods=["POST", "GET"])
def add():
    form = MovieAddingForm()
    return render_template('add.html', form=form)
```
```python
#add.html
{{wtf.quick_form(form, novalidate=True) }}
```
2. 사용자가 영화 제목을 입력하고 'Add Movie'버튼을 클릭하면 플라스크 서버가 해당 영화 제목을 수신해야 합니다. 그런 다음 requests 라이브러리를 사용하여 해당 제목과 일치하는 모든 영화에 대해 The Movie Database API를 요청 및 검색해야 합니다.
```python
#main.py
@app.route('/add', methods=["POST", "GET"])
def add():
    form = MovieAddingForm()
    if form.validate_on_submit():
        parameters = {
            "api_key": API_KEY,
            "query": form.title.data,
            "language" : 'ko-KR'
        }
        response = requests.get(url=SEARCH_URL, params=parameters)
        response.raise_for_status()
        data = response.json()["results"]

        return render_template('select.html', data=data)
    return render_template('add.html', form=form)
```

검색 쿼리를 만들어 영화 데이터를 요청하는 방법은 영화 데이터베이스에 있는 문서를 참고하세요.

https://developers.themoviedb.org/3/search/search-movies


API에서 얻은 데이터를 사용하여 select.html 페이지를 렌더링하고 모든 영화 제목과 개봉 연도를 페이지에 추가해야 합니다. 이런 방법으로 사용자는 추가할 영화를 선택할 수 있는데, 보통 비슷한 제목의 영화가 여러 편 있습니다.
```python
#select.html
{% block content %}
<div class="container">
    <h1 class="heading">Select Movie</h1>
        {% for movie in data: %}
  <p>
      <a href=" {{ url_for('get_movie', movie_id = movie['id']) }} "> {{movie["title"]}} - {{movie["release_date"]}}</a>
  </p>
        {% endfor %}


</div>
{% endblock %}
```

3. 사용자가 select.html 페이지에서 특정 영화를 선택하면 해당 영화 ID를 사용하여 영화 데이터베이스 API의 다른 경로가 요청되어 해당 영화에 대한 모든 데이터(예: 포스터 이미지 URL)를 가져올 수 있어야 합니다.

get-movie-details 경로를 요청하기 위해 사용자가 선택한 영화의 id를 사용합니다.

https://developers.themoviedb.org/3/movies/get-movie-details

API에서 얻은 데이터는 데이터베이스를 새 항목으로 채우는 데 사용되어야 하며, 채워야 하는 속성은 다음과 같습니다.
```python
제목 (title)

이미지 URL (img_url)

개봉연도 (year)

설명 (description)`
```

항목이 추가되면 홈페이지로 리디렉션되며 새 영화가 카드로 표시되어야 합니다. 일부 누락된 데이터가 있을 텐데 괜찮습니다.
```python
#select.html
<a href=" {{ url_for('get_movie', movie_id = movie['id']) }} "> {{movie["title"]}} - {{movie["release_date"]}}</a>
```
```python
#main.py
@app.route('/get_movie', methods=["GET", "POST"])
def get_movie():
    movie_api_id = request.args.get('movie_id')
    if movie_api_id:
        parameters = {
            "api_key": API_KEY,
            "language": 'ko-KR'
        }
        response = requests.get(url=f"{INFO_URL}/{movie_api_id}", params=parameters)
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
```

4. 올바른 영화를 찾은 다음에는 영화 항목에서 평점과 리뷰가 누락되었으므로 홈페이지로 리디렉션하는 대신 edit.html 페이지로 리디렉션합니다. 수정 페이지 폼에는 이 두 필드가 포함되도록 하고, 새로운 데이터로 데이터베이스의 영화 항목을 업데이트합니다.
```python
        return redirect(url_for('edit', id=new_movie.id))
```

### 요구 사항 5 - 영화를 평점별로 정렬하고 순위를 매길 수 있을 것
현재 영화 카드의 앞면에는 ‘None’이라고 큰 글씨로 쓰여 있습니다.

 이 부분에 'None'이 아닌 평점에 따른 영화의 순위를 표시하고자 합니다.

이후 추가한 다른 영화가 가장 높은 평점을 받은 경우 해당 평점에 따라 순위가 매겨져야 합니다.
```python
#main.py
@app.route("/")
def home():
    #This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()

    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies)-i
    db.session.commit()
    return render_template("index.html", movies=all_movies)
```


### 강의 내용 이외에 내가 추가로 해본 것:
1. edit에서 포스터 그림이 같이 뜨게 해서 내가 고른 영화가 맞는지 확인할 수 있게 하기
```python
#edit.html
<div style="text-align : center">
    <img src="{{movie['img_url']}}" alt="Poster" width="200">
</div>
<div style="margin-left: 100px;">
    {{wtf.quick_form(form, novalidate=True) }}
</div>
```

2. 영화를 보여줄 때, 평점이 높은 것부터 내림차순으로 정렬하고 순위를 매기려면??
```python
#main.py
@app.route("/")
def home():
    #This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()

    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = i+1
    db.session.commit()
    return render_template("index.html", movies=all_movies)
```

