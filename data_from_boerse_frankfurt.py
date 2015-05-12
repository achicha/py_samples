# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import io
import sys

"""
download tick quotes for current day, if we know IHE codes of instruments,
from http://www.boerse-frankfurt.de/,
using Selenium web driver
"""


def init_driver():
    #_driver = webdriver.Chrome(r'C::\folder\chromedriver.exe')
    _driver = webdriver.PhantomJS(r'C:\Users\andreyev\Downloads\phantomjs-2.0.0-windows\bin\phantomjs.exe')
    _driver.wait = WebDriverWait(_driver, 10)
    return _driver


def read_names_from_file():
    instrument_list = []
    with io.open('stock_names.txt', 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            instrument_list.append(line.strip())
    print(instrument_list)
    return instrument_list


def get_links(_instruments):
    link_container = []
    driver.get('http://www.boerse-frankfurt.de/en/equities')

    for instr in _instruments:
        search_box = driver.wait.until(EC.presence_of_element_located((By.NAME, "name_isin_wkn")))
        search_box.send_keys(instr)
        search_button = driver.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bttn-arrow")))
        search_button.click()
        driver.wait.until(EC.presence_of_element_located((By.NAME, "name_isin_wkn")))
        link_container.append(driver.current_url + '/price+turnover+history/tick+data#page=1')
        #print(driver.current_url + '/price+turnover+history/tick+data#page=1')
    print(link_container)
    return link_container


def save_result_to_file():
    with io.open('{}.txt'.format(link.split('/')[5].split('+')[-1]), 'w', encoding='utf-8', errors='ignore') as v:
        for key in sorted(timestamp_dict.keys()):
            v.write(key)
            v.write(',')
            v.write(timestamp_dict[key])
            v.write(';')
    return print("saved to file: {}".format(v))


if __name__ == "__main__":
    driver = init_driver()
    #link = 'http://www.boerse-frankfurt.de/en/equities/indices/dax+kursindex+DE0008467440/price+turnover+history/tick+data#page=582'
    instrument_codes = read_names_from_file()
    links = get_links(instrument_codes)

    timestamp_dict = {}
    try:
        for link in links:
            try:
                driver.get(link)
                old_link = 0
                for i in range(1000):
                    print('_____________________')
                    print(driver.current_url)

                    # if last page -> then stop
                    if old_link == int(driver.current_url.split('=')[1]):
                        print(old_link, int(driver.current_url.split('=')[1]))
                        break

                    else:
                        old_link = int(driver.current_url.split('=')[1])
                        try:
                            #for i in driver.find_element(By.XPATH, '//*[@class="fullbox list_component"]//tr'):
                            driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='fullbox list_component']//tr")))
                            for y in driver.find_elements_by_xpath("//*[@class='fullbox list_component']//tr"):
                                try:
                                    data = y.text.split(' ')
                                    timestamp_dict['{}'.format(data[0])] = '{}'.format(data[1:])
                                except:
                                    print("text error", sys.exc_info()[0])

                        except:
                            print('xpath error', sys.exc_info()[0])

                        try:
                            next_button = driver.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))#//*[@id="tick_data_PREKOP236ba85162707bf423d82cef6c30c7e16f0"]/div/div[2]/a[15]')))
                            #for next_button in driver.find_elements_by_class_name('bttn-prevnext-mid-sub'):
                            next_button.click()
                            time.sleep(3)

                        except:
                            print("next error", sys.exc_info()[0])
            except:
                print('xz', sys.exc_info()[0])
            finally:
                time.sleep(5)
                save_result_to_file()
                time.sleep(5)
    except:
        print('xz1', sys.exc_info()[0])
    finally:
        driver.quit()
