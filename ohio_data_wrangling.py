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
    #df = df.fillna("N/A")

    # write it to csv
    df.to_csv(out_filename, index=False)

if __name__ == "__main__":
    ohio_data()
