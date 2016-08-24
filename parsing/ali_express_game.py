# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import io
import sys


def init_driver():
    _driver = webdriver.Chrome(r'/home/methyst/Документы/chromedriver')
    #_driver = webdriver.PhantomJS(r'C:\Users\andreyev\Downloads\phantomjs-2.0.0-windows\bin\phantomjs.exe')
    _driver.wait = WebDriverWait(_driver, 10)
    return _driver

driver = init_driver()

# логинимся
driver.get('https://login.aliexpress.com/buyer_ru.htm')

login_box = driver.wait.until(EC.presence_of_element_located((By.NAME, "loginId")))
login_box.send_keys('email')

pass_box = driver.wait.until(EC.presence_of_element_located((By.NAME, "password")))
pass_box.send_keys('password')

pass_box.send_keys(Keys.ENTER)
# except Exception as e:
#     print(e)

time.sleep(5)
# переходим на страницу игры
driver.get('http://sale.aliexpress.com/ru/__pc/1111_coupon_alley.htm')

# нажать старт
start_game = driver.wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'start-btn clickable'))
start_game.click()

remaining_games = driver.wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'start-btn'))
open_card1 = driver.wait.until(EC.presence_of_element_located(By.XPATH, '/html/body/div[4]/redeem-intro/div[1]/div[2]/div[1]/div/div[2]/span[6]/span[1]'))
open_card1.click()
open_card2 = driver.wait.until(EC.presence_of_element_located(By.XPATH, '/html/body/div[4]/redeem-intro/div[1]/div[2]/div[1]/div/div[2]/span[7]/span[1]'))
open_card2.click()
open_card3 = driver.wait.until(EC.presence_of_element_located(By.XPATH, '/html/body/div[4]/redeem-intro/div[1]/div[2]/div[1]/div/div[2]/span[8]/span[1]'))
open_card3.click()

# играть снова
start_again = driver.wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'btn'))
start_game.click()

check_box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checkmark")))
check_box.click()