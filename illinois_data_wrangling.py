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
import json
from io import StringIO

# state executive orders
illinois_data_link = "https://dph.illinois.gov/sitefiles/COVIDHistoricalTestResults.json?nocache=1"

# output file
out_filename = "data/illinois_data.csv"

# scrape the page contents for ohio executive orders
def illinois_data():
    # get the json data
    myfile = requests.get(illinois_data_link)

    # save it locally
    temp_file_name = "tmp/illinois_tmp_data.json"
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(myfile.content)

    # load the json file
    with open(temp_file_name, "rb") as temp_file:
        json_data = json.load(temp_file)

    # get the historical time-series data
    county_data = json_data['historical_county']["values"]

    print("county data " + str(len(county_data)))

    # prepare output file
    with open(out_filename, "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["Date", "County", "Confirmed Cases", "Total Tested", "Negative", "Deaths"
                         , "Lat", "Lon"])

        # loop over each date
        for obj in county_data:
            date = obj['testDate']

            # loop over each county
            for county_data in obj['values']:
                # extract the data
                county = county_data["County"]
                confirmed_cases = county_data["confirmed_cases"]
                total_tested = county_data["total_tested"]
                negative = county_data["negative"]
                deaths = county_data["deaths"]

                # fill bad lats and lon
                lat = "N/A"
                lon = "N/A"
                try:
                    lat = county_data["lat"]
                    lon = county_data["lon"]
                except:
                    print("ERROR: Skipping " + county + " coords")

                # write the data to csv
                writer.writerow([date, county, confirmed_cases, total_tested,
                                 negative, deaths, lat, lon])

if __name__ == "__main__":
    illinois_data()
