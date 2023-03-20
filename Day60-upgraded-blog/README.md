# 블로그 웹사이트에 배운 내용 적용하기

## contact.html 
- `name` attributes added to `<input>` elements.
- ```python
    <input type="email" name="email" class="form-control" placeholder="Email Address" id="email" required data-validation-required-message="Please enter your email address.">
- `action` and `method` attributes set on `<form>` element.
- ```python
    <form name="sentMessage" id="contactForm" action="{{ url_for('contact') }}" method="post" novalidate>
## main.py
- `contact` route updated.
- ```python
  @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            data = request.form
            print(data["name"])
            print(data["email"])
            print(data["phone"])
            print(data["message"])
        return render_template("contact.html")
    return render_template("contact.html")
  ```

## 문의가 잘 제출되면 웹에서 성공 메시지 출력하기

- IF/ELSE statement added to contact.html using Jinja2 formatting:
- ```python
  #contact.html
  
  {% if msg_sent: %}
            <h1>Successfully sent your message</h1>
            {% else: %}
            <h1>Contact Me</h1>
            {% endif %}
  ```
- `msg_sent` variable snet to template when rendering contact.html
- ```python
  @app.route("/contact", methods=["GET", "POST"])
    def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)
    ```

## smtplib로 이메일 전송하기
사용자가 문의하기를 원할 때, 실제로 관리자에게 이메일을 보내어 문의 기능 완성하기
- ```python
    import smtplib

    MY_EMAIL = "mail"
    MY_PASSWORD = "password"
  
    @app.route('/contact', methods=["POST", "GET"])
    def contact():
        if request.method == "POST":
            data = request.form
            send_email(data["username"], data["email"], data["phone"], data["message"])
            return render_template("contact.html", msg_sent=True)
        return render_template("contact.html", msg_sent=False)

    def send_email(name, email, phone, message):
        email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)
    ```