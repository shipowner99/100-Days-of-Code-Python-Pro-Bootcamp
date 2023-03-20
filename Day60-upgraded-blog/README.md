# 블로그 웹사이트에 배운 내용 적용하기

## contact.html
- `name` attributes added to `<input>` elements.
- `<input type="email" name="email" class="form-control" placeholder="Email Address" id="email" required data-validation-required-message="Please enter your email address.">`
- `action` and `method` attributes set on `<form>` element.
- `<form name="sentMessage" id="contactForm" action="{{ url_for('contact') }}" method="post" novalidate>`
## main.py
- `contact` route updated.
- `코드 따오기`

