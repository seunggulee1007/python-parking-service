from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class PlayMuseum:
    def __init__(self):
        self.driver = None

    def open_chrome(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def login(self):
        self.driver.get("https://nharmony.nhnent.com/user/hrms/bem/parking/parkingTicketTransferPop.nhn")
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys("")
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys("")
        password.send_keys(Keys.RETURN)

        self.driver.implicitly_wait(10)

    def request_parking(self):
        self.driver.find_element(By.XPATH, '//*[@id="pop_content"]/div/div[2]/div[2]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="req_parking_lot_type_cd_1"]').click()
        now_date = datetime.now()
        two_weeks_later = now_date + timedelta(weeks=2)

        # 2주 뒤 날짜의 '일자'만 추출 (day)
        day_only = two_weeks_later.day
        print(two_weeks_later)
        # datepicker 필드 찾기
        date_picker_field = self.driver.find_element(By.XPATH, "//tr[@id='req_ymd_0']//input[@name='transferYmd']")
        # datepicker 필드의 ID 또는 다른 속성 사용
        date_picker_field.click()

        # 원하는 날짜로 이동 (예: 15일 선택)
        # 여기서는 datepicker 내부의 'a' 태그가 날짜로 사용된다고 가정합니다.
        # Xpath로 날짜 선택 (원하는 날짜에 따라 '15' 부분을 변경)

        date_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{day_only}']"))
        )
        date_element.click()

        max_ymd = self.driver.find_element(By.XPATH, "//tr[@id='req_ymd_0']//input[@name='maxYmd']")
        max_ymd.click()
        date_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{day_only}']"))
        )

        date_element.click()

        select_hour_element = self.driver.find_element(By.XPATH, "//tr[@id='req_ymd_0']//input[@name='maxHh']")
        select_hour = Select(select_hour_element)
        select_hour.select_by_visible_text('10')
        select_minute_element = self.driver.find_element(By.XPATH, "//tr[@id='req_ymd_0']//input[@name='maxMm']")
        select_minute = Select(select_minute_element)
        select_minute.select_by_visible_text('00')

        self.driver.find_element(By.LINK_TEXT, '확인').click()

if __name__ == '__main__':
    play_museum = PlayMuseum()
    play_museum.open_chrome()
    play_museum.login()
    play_museum.request_parking()
