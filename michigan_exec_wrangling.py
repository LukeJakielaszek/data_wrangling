#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import bs4 as bs
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import pickle
import csv
import time

# state executive orders
michigan_exec_link = "https://www.michigan.gov/whitmer/0,9309,7-387-90499_90705---,00.html"

# output file
out_filename = "data/michigan_exec.csv"

# get a selenium chrome instance
def chrome_instance(webpage):
    # create a chrome instance
    driver = webdriver.Chrome()
    
    # get landing page of category
    driver.get(webpage)

    # wait for javascript
    driver.execute_script("return document.documentElement.outerHTML")
    
    return driver

# wait for the web page to load
def driver_wait(driver, class_a):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_a))
        )
    except:
        print("ERROR: Cards never loaded")

    return element

# scrape the page contents for ohio executive orders
def michigan_exec():
    # open the browser
    driver = chrome_instance(michigan_exec_link)

    # get the date of the order
    ul = driver.find_element_by_xpath('//*[@id="comp_106314"]/ul')

    ul = ul.get_attribute('outerHTML')
    ul = bs.BeautifulSoup(ul,'html.parser')

    for li in ul.find_all("li"):
        for_covid = False
        rescinded = False
        state_of_emergency = False
        heading = li.text.replace("Executive Order", "").strip()

        heading = heading.split(" - ")

        title = heading[0]
        if("COVID-19" in title):
            title = title.split(" ")[0]
            for_covid = True

        if(len(heading) == 2):
            heading = heading[1].strip()
            if("Rescinded" == heading):
                rescinded = True
            if("Declaration of State of Emergency" in heading):
                state_of_emergency = True

            if("COVID-19" in heading):
                for_covid = True

        
            
        print(title, "| COVID:", for_covid, " | rescinded:", rescinded, " | soe:",state_of_emergency)
        
if __name__ == "__main__":
    michigan_exec()
