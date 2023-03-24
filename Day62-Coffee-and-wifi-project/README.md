# Coffee and wifi project
https://user-images.githubusercontent.com/120784842/227081182-61606893-41ed-4cb0-baa9-43549719b10b.mp4

## 목표
플라스크 WTF, 플라스크 부트스트랩, 부트스트랩 클래스에 숙달하고 csv조작을 약간 수정하는 것

## 요구사항
- css/styles.css 파일을 사용
- /cafes 경로는 cafes.html 파일을 렌더링해야하며, 이 파일에는 cafe-data.csv의 모든 데이터를 표시하는 부트스트랩 표가 포함되어야 함.
- Location URL은 표 안에 전체 링크 대신 앵커 태그 `<a>`로 렌더링 되어야 합니다. 'Maps Link'라는 링크 텍스트가 있어야 하고 href가 실제 링크여야 함.
- 홈페이지의 '보기(Show ME!)' 버튼을 클릭하면 cafes.html 페이지로 이동
- 버튼은 없지만 아는 사람은 접근할 수 있는 '/add' 비밀 경로가 있어야 하며, 이를 클릭할 경우 add.html 파일로 이동해야 함.
- WTForms에 대해 배운 내용을 활용하여 add.html 페이지에 아래 데모에서 볼 수 있는 모든 필드가 포함된 `quick_form`을 만들기.
- 입력한 데이터가 유효한 URL인지 확인하는 유효성 검증 규칙이 위치 URL 필드에 포함되어야 함.
- 사용자가 성공적으로 add.html에 양식을 제출할 경우 데이터가 cafe-data.csv에 추가될 수 있도록 함. csv파일의 끝에 추가되어야 하며, 각 필드의 데이터는 cafe-data.csv의 다른 모든 데이터 라인과 마찬가지로 쉼표로 구분되어야 함.
- 웹 사이트의 모든 탐색 링크가 제대로 작동할 수 있도록 함.
