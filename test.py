from config import Config
from datetime import datetime, time, timedelta
from pages import Dashboard, Login, PaidTimeOff, Question
from utility import Database
from selenium.webdriver import Chrome



config = Config()

# Instantiate the driver
driver = Chrome()
driver.implicitly_wait(config.get_implicit_wait())

login = Login(config, driver)
dash = Dashboard(driver)
pto = PaidTimeOff(driver)
quest = Question(config, driver)

login.login()

if quest.is_on_question_page():
    quest.answer_question()

dash.go_to_pto()

pto.is_pto_day(datetime.now())
