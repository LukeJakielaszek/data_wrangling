#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

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

# PDF Extraction
import PyPDF2
import urllib.request
import shutil
from wand.image import Image as IMG
import PIL
import PIL.Image
from pytesseract import image_to_string
import pytesseract

# state executive orders
michigan_exec_link = "https://www.michigan.gov/whitmer/0,9309,7-387-90499_90705---,00.html"

# output file
out_filename = "data/michigan_exec.csv"

# executive order PDF listings
michigan_alt_link = "http://www.legislature.mi.gov/(S(d3b0ixy34nwgszptpzq2e5ed))/mileg.aspx?page=executiveorders"

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

# Parses dates and summaries from PDF listing
def michigan_alt():
    # open the browser
    driver = chrome_instance(michigan_alt_link)

    # get the table of executive orders
    table = driver.find_element_by_xpath('//*[@id="frg_executiveorders_lblEOList"]/table/tbody')
    table = table.get_attribute('outerHTML')
    table = bs.BeautifulSoup(table,'html.parser')

    # per order dictionary
    orders = {}

    # loop through each executive order in the table
    for order in table.find_all("tr"):
        # get the title and description
        title, desc = order.find_all("td")

        # construct the link to the PDF
        link = "http://www.legislature.mi.gov/documents/" + title.find("a")['href']

        # construct the title of the executive order
        title = title.text.replace("E.O. NO.", "").strip()

        # get the summary listed for the executive order
        summary = desc.text.strip()

        # ensure titles are consistent across sources
        # converts order-1 to order-01
        year, issue = title.split("-")
        if(int(issue) < 10):
            title = year + "-0" + issue
        else:
            title = year + "-" + issue

        print()
        print(title)
        print(link)
        print(summary)

        # construct a dictionary for each order
        temp_dict = {}
        temp_dict["link"] = link
        temp_dict["summary"] = summary
        temp_dict["date"] = "" 

        # attempt to parse the PDF
        try:
            # download the pdf to local system
            download_page(link, "tmp/tmp.pdf")

            # convert the pdf to a png
            path = pdf_to_png("tmp/tmp.pdf")

            # extract the date from pdf using OCR
            date = get_text(path)
        
            print(date)

            # store the date in our dictionary
            temp_dict["date"] = date
            
        except:
            print("ERROR: Skipping " + str(title))

        # store the order in our dictionary
        orders[title] = temp_dict

    return orders

# download pdf to local system
# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
def download_page(url, file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        
# get the date from the last page of the PDF file
def get_text(path):
    # extract the text
    output = pytesseract.image_to_string(PIL.Image.open(path).convert("RGB"), lang='eng')

    # find the date index
    index = output.find('Date:')

    # parse the date
    output = output[index+6:]
    output = output.split()
    date = output[0] + " " + output[1] + " " + output[2]
    date = date.upper().strip()

    # return the date
    return(date)

# convert the downloaded pdf to a png
def pdf_to_png(path):
    pages = 0

    # download all pages
    # a resolution of about 300 allows almost all PDFs to be processed in memory
    # the higher we go, the more accurate our optical character recognition is
    with IMG(filename=path, resolution=300) as img:

        print('width =', img.width)
        print('height =', img.height)
        print('pages = ', len(img.sequence))

        # get the number of pages in PDF
        pages = len(img.sequence)
        
        print('resolution = ', img.resolution)

        # convert the PDF to a png
        with img.convert('png') as converted:
            converted.save(filename='tmp/sample.png')

    # return the last page file name
    return("tmp/sample-"+ str(pages-1) + ".png")
        
# scrape the page contents for ohio executive orders and save to CSV
def michigan_exec(orders):
    # open the browser
    driver = chrome_instance(michigan_exec_link)

    # get the list of executive orders
    ul = driver.find_element_by_xpath('//*[@id="comp_106314"]/ul')
    ul = ul.get_attribute('outerHTML')
    ul = bs.BeautifulSoup(ul,'html.parser')

    # prepare our output CSV
    with open(out_filename, "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["Executive Order", "Summary", "Date", "Link", "Covid Related", "Rescinded", "State of Emergency"])

        # loop through each executive order in the list
        for li in ul.find_all("li"):
            # initialize our booleans to false
            for_covid = False
            rescinded = False
            state_of_emergency = False

            # construct a link to the full text of the order
            link = "https://www.michigan.gov" + li.find("a")["href"]

            # Remove unneccessary text for each orders listing
            heading = li.text.replace("Executive Order", "").strip()

            # seperate the name of the order with additional meta data
            heading = heading.split(" - ")

            # get the title of the order
            title = heading[0]

            # check if the order has to do with COVID
            if("COVID-19" in title):
                title = title.split(" ")[0]
                for_covid = True

            # extract other metadata for order
            if(len(heading) == 2):
                # remove whitespace
                heading = heading[1].strip()

                # check if order is rescinded
                if("Rescinded" == heading):
                    rescinded = True

                # check if order involved in SOE
                if("Declaration of State of Emergency" in heading):
                    state_of_emergency = True

                # check if order involved with COVID
                if("COVID-19" in heading):
                    for_covid = True

            # display meta data
            print(title, "| COVID:", for_covid, " | rescinded:", rescinded,
                  " | soe:", state_of_emergency)

            # remove whitespace
            title = title.strip()

            # grab our extracted information from the PDF listing
            summary = ""
            date = ""

            # if our current order was scraped from the PDF
            if title in orders:

                # extract date and summary
                temp_dict = orders[title]
                summary = temp_dict["summary"]
                date = temp_dict["date"]
            else:
                # leave those fields blank
                print("Not in orders [" + str(title) + "]")
                summary = ""
                date = ""

            # write the data to csv
            writer.writerow([title, summary, date, link, for_covid, rescinded, state_of_emergency])
        
if __name__ == "__main__":
    # extract from PDF
    orders = michigan_alt()

    print(orders)

    # extract from website and save to CSV
    michigan_exec(orders)
