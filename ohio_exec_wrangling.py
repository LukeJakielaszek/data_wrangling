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
ohio_exec_link = "https://governor.ohio.gov/wps/portal/gov/governor/media/executive-orders/"

# output file
out_filename = "data/ohio_exec.csv"

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
def ohio_exec():
    # open the browser
    driver = chrome_instance(ohio_exec_link)

    # let it load
    elem = driver_wait(driver, "odx-section-resources-cards-list")
    
    # get only the cards section
    cards = elem.get_attribute('innerHTML')
    cards = bs.BeautifulSoup(cards,'html.parser')

    print("GETTING CARDS")

    # prepare output file
    with open(out_filename, "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["Executive Order", "Summary", "Date", "Link"])

        # get each orders data
        for card in cards.find_all("section", {"class":"ohio-card-content"}):
            # get the brief summary
            summary = card.find("p", {"class": "ohio-card-content-summary"}).text
            # extract the order's title
            title = card.find("h3", {"class": "ohio-card-content-header"}).text
            title = title.replace("Executive Order", "").strip()
            
            # get the link to a page with detailed contents
            link = ohio_exec_link + card.find("a", {"class": "ohio-card-wrapper-anchor"})['href'].split("/")[-1]

            # load the page
            driver.get(link)
            
            # wait for javascript
            driver.execute_script("return document.documentElement.outerHTML")

            # get the date of the order
            date = driver.find_element_by_xpath('//*[@id="odx-main-content"]/article/div/div[1]/div/span[1]')
            
            date = date.get_attribute('innerHTML')
            date = bs.BeautifulSoup(date,'html.parser').text.strip()

            # display to console
            print()
            print(title)
            print(summary)
            print(link)
            print(date)

            # write the data to csv
            writer.writerow([title, summary, date, link])

        
if __name__ == "__main__":
    ohio_exec()
