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
import pandas as pd

# state executive orders
ohio_data_link = "https://coronavirus.ohio.gov/static/COVIDSummaryData.csv"

# output file
out_filename = "data/ohio_data.csv"

def convert_date(val):
    month, day, year = val.split("/")
    if(month == "3"):
        month = "MARCH"
    elif(month == "4"):
        month = "APRIL"

    date = month + " " + day + ", " + year

    return date
    
# scrape the page contents for ohio executive orders
def ohio_data():
    # get the csv
    myfile = requests.get(ohio_data_link)

    # save it locally
    temp_file_name = "tmp/ohio_tmp_data.csv"
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(myfile.content)

    # replace all null with N/A
    df = pd.read_csv(temp_file_name)

    # drop totals at bottom
    df = df.drop(df.index[-1])

    # standardize onset date
    for i,val in enumerate(df["Onset Date"]):
        if(val != ""):
            df["Onset Date"][i] = convert_date(val)

    # standardize death date
    for i,val in enumerate(df["Date Of Death"]):
        if(str(val) != "nan" and val != "" and val != "Unknown"):
            df["Date Of Death"][i] = convert_date(val)

    # standardize admission date
    for i,val in enumerate(df["Admission Date"]):
        if(str(val) != "nan" and val != "" and val != "Unknown"):
            df["Admission Date"][i] = convert_date(val)
            
    # write it to csv
    df.to_csv(out_filename, index=False)

if __name__ == "__main__":
    ohio_data()
