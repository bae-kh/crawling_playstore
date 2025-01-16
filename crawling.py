from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# ChromeDriver 초기화
service = Service(ChromeDriverManager().install())

# 저장 경로 설정
save_path = r"C:\Users\qorkd\OneDrive\바탕 화면\google_play_reviews.xlsx"

# review_data 변수를 전역 범위에서 초기화
review_data = []

with webdriver.Chrome(service=service, options=options) as driver:
   # URL 설정 및 페이지 접속
   url = "https://play.google.com/store/apps/details?id=com.sampleapp&hl=ko"
   driver.set_page_load_timeout(30)
   driver.get(url)
   
   time.sleep(10)  # 초기 페이지 로딩 대기 시간
   
   driver.save_screenshot("debug_screenshot.png")
   print("스크린샷이 저장되었습니다.")
   
   wait = WebDriverWait(driver, 30)
   
   try:
       xpaths = [
           '//button[span[contains(text(), "리뷰 모두 보기")]]',
           '//button[.//span[contains(text(), "리뷰")]]',
           '//button[contains(@aria-label, "리뷰")]',
           '//div[contains(@role, "button")][.//span[contains(text(), "리뷰")]]'
       ]
       
       found = False
       for xpath in xpaths:
           try:
               show_all_button = wait.until(
                   EC.element_to_be_clickable((By.XPATH, xpath))
               )
               show_all_button.click()
               found = True
               print(f"리뷰 버튼을 찾았습니다: {xpath}")
               break
           except:
               continue
               
       if not found:
           raise TimeoutException("모든 XPATH 시도 실패")
           
       time.sleep(5)
       
   except TimeoutException as e:
       print("리뷰 모두 보기 버튼을 찾을 수 없습니다:", e)
       print("\n현재 페이지 소스:")
       print(driver.page_source[:1000])
       exit()

   print("리뷰 로딩 중...")
   
   # 리뷰 컨테이너의 CSS 선택자 수정
   review_selectors = [
       'div[class*="RHo1pe"]',
       'div[jscontroller="H6eOGe"]',
       'div[jsname="P8xhZc"]',
       'div[class*="d15Mdf"]'
   ]
   
   found_selector = None
   for selector in review_selectors:
       try:
           wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
           review_blocks = driver.find_elements(By.CSS_SELECTOR, selector)
           if len(review_blocks) > 0:
               found_selector = selector
               print(f"리뷰 블록을 찾았습니다. 선택자: {selector}")
               break
       except:
           continue
   
   if not found_selector:
       print("리뷰 블록을 찾을 수 없습니다.")
       exit()

   print("리뷰 로딩 중...")
   SCROLL_PAUSE_TIME = 1  # 대기 시간 1초로 감소
   scroll_attempts = 0
   max_scroll_attempts = 300
   last_review_count = 0
   no_new_reviews_count = 0

   while scroll_attempts < max_scroll_attempts:
       try:
           # 현재 리뷰 수 확인
           current_reviews = []
           for selector in review_selectors:
               current_reviews.extend(driver.find_elements(By.CSS_SELECTOR, selector))
           current_review_count = len(current_reviews)
           print(f"현재 로드된 리뷰 수: {current_review_count}")

           # JavaScript로 스크롤 실행 - 스크롤 값 증가
           driver.execute_script("""
               var elements = document.getElementsByClassName('fysCi');
               if(elements.length > 0) {
                   elements[0].scrollBy({
                       top: 5000,  
                       behavior: 'auto'  
                   });
               }
           """)
           time.sleep(SCROLL_PAUSE_TIME)

           # 첫 번째 스크롤 방식이 실패할 경우의 대체 스크롤 코드도 더 크게
           if current_review_count == last_review_count:
               driver.execute_script("""
                   var dialogContent = document.querySelector('[role="dialog"] > div');
                   if(dialogContent) {
                       dialogContent.scrollBy(0, 5000);
                   }
               """)
               time.sleep(SCROLL_PAUSE_TIME)

           # 새로운 리뷰가 로드되었는지 확인
           if current_review_count > last_review_count:
               print(f"새로운 리뷰 {current_review_count - last_review_count}개 로드됨")
               last_review_count = current_review_count
               no_new_reviews_count = 0
           else:
               print(f"새로운 리뷰가 로드되지 않음 (현재: {current_review_count}개)")
               no_new_reviews_count += 1

           scroll_attempts += 1
           print(f"스크롤 진행: {scroll_attempts}/{max_scroll_attempts}")

           if no_new_reviews_count >= 7:  # 7번 연속으로 새로운 리뷰가 없으면 종료
               print("더 이상 새로운 리뷰를 불러올 수 없습니다.")
               break

       except Exception as e:
           print(f"스크롤 중 오류 발생: {e}")
           time.sleep(1)
           continue

   print("리뷰 요소 찾는 중...")
   # 모든 리뷰 블록 수집
   review_blocks = []
   for selector in review_selectors:
       review_blocks.extend(driver.find_elements(By.CSS_SELECTOR, selector))
   print(f"찾은 리뷰 블록 수: {len(review_blocks)}")
   
   if len(review_blocks) > 0:
       for block in tqdm(review_blocks, desc="리뷰 수집 중"):
           try:
               # 별점 찾기
               rating = None
               try:
                   rating_element = block.find_element(By.CSS_SELECTOR, 'div[role="img"]')
                   if rating_element:
                       rating_text = rating_element.get_attribute('aria-label')
                       if rating_text and "별표" in rating_text:
                           rating = rating_text.split("에 ")[1].split("개")[0]
               except Exception as e:
                   print(f"별점 추출 중 오류 발생: {e}")
                   rating = None

               # 리뷰 텍스트 찾기
               text_selectors = [
                   '.h3YV2d',
                   '.UD7Dzf',
                   '.review-body',
                   'span[jsname="fbQN7e"]',
                   'span[jsname="bN97Pc"]'
               ]
               
               review_text = None
               for selector in text_selectors:
                   try:
                       element = block.find_element(By.CSS_SELECTOR, selector)
                       review_text = element.text
                       if review_text:
                           break
                   except:
                       continue
               
               # 날짜 찾기
               date_selectors = [
                   '.bp9Aid',
                   'span[class*="bp9"]',
                   'span[class*="review-date"]'
               ]
               
               review_date = None
               for selector in date_selectors:
                   try:
                       element = block.find_element(By.CSS_SELECTOR, selector)
                       review_date = element.text
                       if review_date:
                           break
                   except:
                       continue
               
               if review_text and review_date:
                   review_data.append({
                       "Rating": rating,
                       "Review": review_text,
                       "Date": review_date
                   })
                   print(f"수집된 리뷰: {review_text[:50]}...")
                   
           except Exception as e:
               print(f"개별 리뷰 수집 중 오류: {e}")
               continue

       if not review_data:
           print("\n페이지 소스 확인:")
           print(driver.page_source[:1000])
           
   else:
       print("리뷰 블록을 찾을 수 없습니다.")

if review_data:
   df = pd.DataFrame(review_data)
   df = df.drop_duplicates()
   df.to_excel(save_path, index=False)
   print(f"\n크롤링 완료! {len(df)}개의 리뷰가 {save_path} 경로에 저장되었습니다.")
else:
   print("\n수집된 리뷰가 없습니다.")
