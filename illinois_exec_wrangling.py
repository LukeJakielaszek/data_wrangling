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
import requests
import pickle
import csv

# state executive orders
illinois_exec_link = "https://www2.illinois.gov/sites/coronavirus/Resources/Pages/ExecutiveOrders.aspx"

out_filename = "data/illinois_exec.csv"

def chrome_instance(webpage):
    # create a chrome instance
    driver = webdriver.Chrome()
    
    # get landing page of category
    driver.get(webpage)

    # wait for javascript
    driver.execute_script("return document.documentElement.outerHTML")

    return driver

def illinois_exec():
    driver = chrome_instance(illinois_exec_link)
    
    # get the executive order list
    elem = driver.find_element_by_xpath('/html/body/form/div[4]/div[2]/div/main/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/ul')
    
    # read only the single ul of executive orders
    html = elem.get_attribute('outerHTML')

    # parse into a bs object
    soup = bs.BeautifulSoup(html,'html.parser')

    with open(out_filename, "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["Executive Order", "Brief Summary", "Long Summary", "Issued Date", "Filed Date", "Link"])
        for i,li in enumerate(soup.find_all("li")):
            # get each executive order by section
            title_p, summary_p, date_p = li.find_all("p")

            # get the title
            title = date_p.find("a").text.replace("(HTML)", "").replace("Executive Order", "").strip()
            print(title)
            
            # get summaries of executive order
            summary_p = summary_p.text
            brief_sum = ""
            long_sum = ""
            try:
                brief_sum, long_sum = summary_p.split("—")
            except:
                sums = summary_p.split("-")
                brief_sum = sums[0]
                for i,sum_a in enumerate(sums[1:]):
                    if i != 0:
                        long_sum += "-"
                    long_sum += sum_a
                
            brief_sum = brief_sum.strip()
            long_sum = long_sum.strip()
            
            print(brief_sum)
            
            print(long_sum)
            
            # get the more detailed page
            link = "https://www2.illinois.gov" + date_p.find("a")["href"]                
            driver.get(link)
            
            # wait for javascript
            driver.execute_script("return document.documentElement.outerHTML")

            cur_page = driver.page_source

            # parse into a bs object
            cur_page = bs.BeautifulSoup(cur_page,'html.parser')
                
            # get the date section
            dates = str(cur_page.find_all("p")[-1]).replace("<p>", "").replace("</p>", "").upper()

            # get both the issued and filing dates
            issued, filed = dates.split("<BR/>")
            issued = issued.replace("ISSUED BY THE GOVERNOR", "").strip()
            filed = filed.replace("FILED BY THE SECRETARY OF STATE", "").strip()
                
            print(issued)
            print(filed)

            # write the data to csv
            writer.writerow([title, brief_sum, long_sum, issued, filed, link])
            
if __name__ == "__main__":
    illinois_exec()
