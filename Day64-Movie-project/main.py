from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)


db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-best10.db"
db.init_app(app)

app.config['SECRET_KEY'] = 'abx'
Bootstrap(app)

API_KEY = "d7d8a72794a94b94c2d1378231b1f9f0"
SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

class MovieRatingForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField("Done")

class MovieAddingForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField("Add movie")

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
    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()


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

    # all_movies = db.session.query(Movie).all()
    # for movie in all_movies:
    #     movie.ranking = db.session.query(Movie).order_by(Movie.rating)
    #     db.session.commit()
    # return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["POST", "GET"])
def rate_movie():
    form = MovieRatingForm()
    table_id = request.args.get('id')
    movie_seleted = Movie.query.get(table_id)
    if form.validate_on_submit():
        movie_to_update = Movie.query.get(table_id)
        movie_to_update.rating = float(form.rating.data)
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie_seleted, form=form)

@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_seleted = Movie.query.get(movie_id)
    db.session.delete(movie_seleted)
    db.session.commit()
    return redirect(url_for('home'))

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
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('rate_movie', id=new_movie.id))






if __name__ == '__main__':
    app.run(debug=True)
