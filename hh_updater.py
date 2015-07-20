from time import sleep
import sys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

# from selenium.webdriver.common.keys import Keys  # заимодействие с командами клавиатуры

""" 0. http://selenium-python.readthedocs.org/en/latest/installation.html
    1. pip install selenium
    2.1 use phantomJS as default browser if you dont wanna open "real" browser while doing your tests.
    2.2 You need to make sure the standalone ChromeDriver binary (which is different than the Chrome browser binary)
    is either in your path or available in the webdriver.chrome.driver environment variable
    https://sites.google.com/a/chromium.org/chromedriver/downloads
"""


def init_driver():
    _driver = webdriver.Chrome()
    # _driver = webdriver.PhantomJS(r'C:\Users\andreyev\Downloads\phantomjs-2.0.0-windows\bin\phantomjs.exe')
    _driver.wait = WebDriverWait(_driver, 10)
    return _driver


def login(_driver, _login, _pswd):
    _driver.get("https://hh.ru/account/login")
    try:
        login_box = _driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        password_box = _driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "password")))

        login_box.send_keys(_login)
        password_box.send_keys(_pswd)

    except:
        print("another exception", sys.exc_info()[0])
    try:
        login_button = _driver.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div/form/div[3]/input")))
        login_button.submit()

    except TimeoutException as TE:
        print("Button not found in {}".format(_driver.current_url), TE)
    except WebDriverException as wbe:
        print("another exception", wbe, sys.exc_info()[0])
    except:
        print("login error", sys.exc_info()[0])
    return 0


def update_resume(_driver, _resume_url):
    _driver.get(_resume_url)
    try:
        update_button = _driver.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'update__status')))
        update_button.click()

    except TimeoutException:
        print("Update button not found", sys.exc_info()[0])
    except WebDriverException as wbe:
        print("too early: ", datetime.utcnow())
    except:
        print(sys.exc_traceback)
    else:
        print("resume updated: ", datetime.utcnow())
    return 0


def start_timer(_driver, _resume_id):
    _time = 0
    delay = timedelta(0, 4*3600)
    try:
        _time = datetime.utcnow()
        update_resume(_driver, 'http://hh.ru/resume/'+_resume_id)
    except:
        print('some_error', sys.exc_info()[0])

    while True:
        if datetime.utcnow() < _time + delay:
            # todo проверку сколько осталось до обновления резюме
            # print("sleep", (_time + delay - datetime.utcnow()).seconds)
            sleep(3600)
        else:
            update_resume(_driver, 'http://hh.ru/resume/'+_resume_id)
            _time += delay
            continue
    return 0

if __name__ == "__main__":
    my_login = "mylogin"
    my_password = 'mypass'
    resume_id = 'cvID'
    try:
        driver = init_driver()
        login(driver, my_login, my_password)
        #update_resume(driver, 'http://hh.ru/resume/' + resume_id)
        start_timer(driver, resume_id)
        # TODO проверку что резюме обновлено
        print("update finished", datetime.utcnow())

    except:
        print("updater errors", sys.exc_info()[0])
    finally:
        # sleep(5)
        driver.quit()