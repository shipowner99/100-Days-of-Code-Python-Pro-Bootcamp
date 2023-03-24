# 영화 웹사이트 베스트 10
## 요구 사항 1 - 영화 목록 항목을 볼 수 있을 것

1. SQL 알케미를 사용하여 SQ 라이트 데이터베이스를 만듭니다. 데이터베이스에는 'Movie'라는 이름의 표가 있어야 하며, 이 표에는 다음의 필드가 포함되어야 합니다.

id 
title 
year 
description 
rating 
ranking
review
img_url


2. 코드/DB Viewer를 사용하여 다음 값으로 데이터베이스에 새 항목을 추가합니다.

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
힌트: 코드를 한 번 실행한 후 2단계에서 추가 입력된 코드를 제거해야 합니다. 그렇지 않으면 다음과 같은 메시지가 뜰 수 있습니다.






3. 데이터베이스의 각 항목이 홈페이지에 올바르게 표시되도록 코드를 작성합니다.

각각의 데이터가 어떻게 표시되는지 확인하세요.

앞면:


뒷면:


## 요구 사항 2 - 영화 등급 및 리뷰를 수정할 수 있을 것
영화 카드 뒷면에는 수정 버튼이 있고, 이 버튼을 클릭하여 평점과 리뷰를 변경할 수 있어야 합니다.

예)




1. WTForms에 대해 배운 내용을 활용해서 RateMovieForm을 만들고 이를 사용하여 edit.html에서 렌더링할 Quick Form을 생성합니다.

참고: edit.html의 코드는 변경할 필요 없습니다. 학생들이 단순 HTML 양식을 작성하지 않도록 하기 위해, Quick Form을 렌더링하는 데 필요한 모든 것을 사전에 마련해 두었습니다.

WTForms 사용법을 잊어버린 경우 이전 수업으로 돌아가서 복습하거나 다음 링크의 문서를 참고하시기 바랍니다.

https://pythonhosted.org/Flask-Bootstrap/forms.html

https://wtforms.readthedocs.io/en/2.3.x/

https://flask-wtf.readthedocs.io/en/stable/



2. 폼을 제출하고 유효성을 검사한 다음에는 데이터베이스의 해당 영화 항목에 업데이트 사항을 추가합니다. SQL 알케미에 관한 보다 자세한 내용은 다음의 링크에서 확인할 수 있습니다.

https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application


