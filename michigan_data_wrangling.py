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
michigan_data_link = "https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html"

# output file
out_filename = "data/michigan_data.csv"


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
def michigan_data():
    # open the browser
    driver = chrome_instance(michigan_data_link)

    # find and click daily counts
    driver.find_element_by_xpath('//*[@id="comp_115181"]/ul/li[1]/span/span/span[2]/ul/li[1]/h4/strong/a').click()

    # wait for javascript
    driver.execute_script("return document.documentElement.outerHTML")

    # get the entire table
    table = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/div[1]/div/div/table[1]/tbody')
    table = table.get_attribute('innerHTML')
    table = bs.BeautifulSoup(table,'html.parser')

    # get all rows of the table
    rows = table.find_all("tr")

    # prepare output file
    with open(out_filename, "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["Date","Region 1","Region 2 North","Region 2 South","Region 3", "Region 5","Region 6","Region 7","Region 8","Unknown","Grand Total"])

        # for each row
        for i, tr in enumerate(rows):
            # skip the totals (last row)
            if(i == len(rows)-1):
                break

            # for each col
            cols = tr.find_all("td")
            for i,col in enumerate(cols):
                # get the text
                col = col.text.strip()

                # if a value is not entered, it should be 0
                if(col == ""):
                    col = "0"

                # save the parsed entry value
                cols[i] = col

            # get each entry for the row
            date, r1, r2_north, r2_south, r3, r5, r6, r7, r8, unknown, gt = cols

            # format the date consistently with our other data
            day, month = date.strip().split("-")
            if(month == "Mar"):
                month = "MARCH"
            elif(month == "Apr"):
                month = "APRIL"

            # reconstruct the date
            date = month + " " + day + ", 2020"
            
            # write the data to csv
            writer.writerow([date, r1, r2_north, r2_south, r3, r5, r6, r7, r8, unknown, gt])

if __name__ == "__main__":
    michigan_data()
