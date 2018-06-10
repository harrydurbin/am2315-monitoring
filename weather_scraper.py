#!/usr/bin/python3
"""
Script to scrape weather data with selenium
Harry Durbin

Notes:
+ must install browser driver and update path below to allow selenium to run.
+ initialize an empty database by running init_sunnyportal_table.py in tests folder
"""

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import calendar
import datetime
from dateutil import parser

# pyvirtualdisplay settings
display = Display(visible=0, size=(800, 600))
display.start()


class Weather(object):

    # set variables
    BASE_URL = 'https://www.accuweather.com/en/us/san-jose-ca/95112/hourly-weather-forecast/39767_pc'

    # assigning web driver for selenium (download chrome driver and set path below)
    DRIVER_PATH = '/home/hd/Downloads/geckodriver'

    def __init__(self):
        self.DRIVER = self.get_driver()
        self.execute()

    def get_driver(self):
        DRIVER = webdriver.Firefox(executable_path = self.DRIVER_PATH)
        return DRIVER

    def go_to_site(self):
        self.DRIVER.get(self.BASE_URL)

    def get_temp(self):

        TEMPTABLE = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.CLASS_NAME, """hourly-table.overview-hourly""")))
        temp_html = TEMPTABLE.get_attribute('innerHTML')
        # print (temp_html)
    #     self.power = pd.read_html(power_html, header = 0)
        self.df = pd.read_html(temp_html,header=0)[0]
        self.df.to_csv('data_test.csv')
        # ORIGIN = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Origin"]')))
        # ORIGIN.send_keys(self.ORIGIN_CITY)
        # DESTINATION = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Destination"]')))
        # DESTINATION.send_keys(self.DESTINATION_CITY)
        print (self.df)
        return self.df

    def execute(self):
        print ('Accessing site...')
        self.go_to_site()
        self.get_temp()
        display.stop()



if __name__ == '__main__':
    Weather()
