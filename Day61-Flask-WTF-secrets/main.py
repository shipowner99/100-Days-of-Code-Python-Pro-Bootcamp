from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = StringField('Password')

app = Flask(__name__)
app.secret_key = "qwerasdf"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login")
def login():
    login_form = LoginForm(meta={'csrf': False})
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)