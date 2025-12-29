# Google Play Store Review Scraper

파이썬(Python)과 셀레니움(Selenium)을 사용하여 Google Play Store의 앱 리뷰를 자동으로 수집(크롤링)하고 엑셀 파일로 저장하는 스크립트입니다.

## 📌 주요 기능

* **자동화된 수집**: Chrome 브라우저를 제어하여 실제 사용자처럼 리뷰 페이지에 접속합니다.
* **전체 리뷰 로드**: '리뷰 모두 보기' 버튼을 자동으로 클릭하고, 스크롤을 내려 더 많은 리뷰를 로드합니다.
* **데이터 추출**: 작성자 별점, 리뷰 내용, 작성 날짜를 추출합니다.
* **엑셀 저장**: 수집된 데이터를 중복 제거 후 `.xlsx` 파일로 저장합니다.
* **탐지 우회**: 자동화 봇 탐지를 방지하기 위한 다양한 브라우저 옵션이 적용되어 있습니다.

## 🛠 사전 요구 사항 (Prerequisites)

이 프로젝트를 실행하려면 다음이 설치되어 있어야 합니다.

* **Python 3.8+**
* **Google Chrome 브라우저** (최신 버전)

### 라이브러리 설치

터미널(또는 CMD)에서 아래 명령어를 실행하여 필요한 패키지를 설치하세요.

```bash
pip install selenium webdriver-manager pandas tqdm openpyxl
```

## ⚙️ 설정 방법 (Configuration)

스크립트(`main.py` 또는 해당 소스 파일)를 열어 아래 두 변수를 본인의 환경에 맞게 수정해야 합니다.

### 1. 수집할 앱 URL 설정
`url` 변수에 크롤링하고 싶은 앱의 구글 플레이 스토어 주소를 입력하세요.

```python
# 예시
url = "[https://play.google.com/store/apps/details?id=com.sampleapp&hl=ko](https://play.google.com/store/apps/details?id=com.sampleapp&hl=ko)"
```

### 2. 저장 경로 설정
`save_path` 변수에 엑셀 파일이 저장될 경로를 입력하세요.

> **주의**: 윈도우 사용자의 경우 경로 앞에 `r`을 붙이거나 역슬래시(`\`)를 두 번 써야 오류가 발생하지 않습니다.

```python
# 예시 (Windows)
save_path = r"C:\Users\YourName\Desktop\reviews.xlsx"

# 예시 (Mac/Linux)
save_path = "./reviews.xlsx"
```

## 🚀 실행 방법 (Usage)

설정을 마친 후 터미널에서 스크립트를 실행합니다.

```bash
python main.py
```

실행하면 자동으로 크롬 브라우저가 열리며 수집이 진행됩니다. 수집이 완료되면 설정한 경로에 엑셀 파일이 생성됩니다.

## 📊 결과 데이터 예시

생성된 엑셀 파일은 다음과 같은 컬럼을 포함합니다.

| Rating | Review | Date |
| :--- | :--- | :--- |
| 5 | 앱이 정말 유용해요! 잘 쓰고 있습니다. | 2024년 1월 15일 |
| 1 | 업데이트 이후 자꾸 튕깁니다. 고쳐주세요. | 2024년 1월 10일 |
| ... | ... | ... |

## ⚠️ 주의사항 및 문제 해결

1.  **CSS 선택자 변경**: 구글 플레이 스토어는 웹페이지 구조(Class Name 등)를 자주 변경합니다. 만약 리뷰가 수집되지 않는다면 `review_selectors`, `text_selectors` 등의 변수에 있는 CSS 선택자를 개발자 도구(F12)를 통해 최신 값으로 업데이트해야 합니다.
2.  **페이지 로딩 속도**: 인터넷 환경에 따라 `time.sleep()` 시간을 늘려야 할 수도 있습니다.
3.  **과도한 요청 제한**: 너무 짧은 시간에 많은 요청을 보내면 일시적으로 차단될 수 있습니다.

## 📝 License

이 코드는 학습 및 연구 목적으로 작성되었습니다. 수집된 데이터의 상업적 이용에 대한 책임은 사용자에게 있습니다.
