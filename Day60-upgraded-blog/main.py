from flask import Flask, render_template, request
import requests
import smtplib

MY_EMAIL = "vivathink99@gmail.com"
MY_PASSWORD = "zzbfplpesxpairrs"


app = Flask(__name__)

response = requests.get("https://api.npoint.io/c30ea4f6d9c5343811cb")
data = response.json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=data)

@app.route('/about')
def about():
    return render_template("about.html", posts=data)

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["username"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route('/post/<int:num>')
def post(num):
    return render_template("post.html", number=num, posts=data)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)



if __name__ == "__main__":
    app.run(debug=True)