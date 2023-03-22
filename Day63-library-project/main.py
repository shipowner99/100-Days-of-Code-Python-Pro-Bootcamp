from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

##데이터베이스 만들기
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)


##표만들기
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        #레코드 만들기
        added_book = request.form
        data = added_book.to_dict()
        new_book = Book(title=data["title"], author=data["author"], rating=data["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

