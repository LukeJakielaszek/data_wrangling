# data_wrangling

## Overview

Data was scraped from a total of 7 sources (2 for Illinois, 2 for Ohio, and 2 for Michigan). Each state has a csv file with scraped executive order information and another csv with general Covid-19 related counts. Unlisted / unobtainable data for an entry is left empty (null) in a CSV cell as not every source has complete information for each day. Dates are all caps in the form of "MONTH day, year". All csv are stored in the data directory. CSVs corresponding to executive orders are denoted with _exec.csv and CSVs corresponding to general counts are denoted with _data.csv. All scripts can be run together from the data_wrangling directory using the command "sh run_all.sh". Each script can also be run individually using "python3 script_name.py"<br/>

## Illinois
### Executive Orders
The following information regarding Illinois executive orders was obtained:<br/>
<br/>
Executive Order - The name of the order<br/>
Brief Summary - A short description (around 4 words / keywords) of the order<br/>
Long Summary - A longer description (around a paragraph) describing the order<br/>
Issued Date - The date the Governor issued the order<br/>
Filed Date - The date the Secretary filed the order<br/>
Link - A url to the full HTML version of the order<br/>
<br/>
Note: All issued dates and filed dates are the same for this dataset. I chose to keep them seperate in case this script is run in the future and something changes.<br/>
<br/>
Information was obtained by scraping the page "https://www2.illinois.gov/sites/coronavirus/Resources/Pages/ExecutiveOrders.aspx" to get a listing of all orders and summary information. The "Executive Order 2020-XX (HTML)" page for each order was also scraped to grab the date information. <br/>

### Daily Counts
The following information regarding Illinois Daily Covid-19 counts was obtained.<br/>
<br/>
Date - The date of the record<br/>
County - The county of the record (Illinois is listed within County which is the aggregation of the state counts)<br/>
Confirmed Cases - The number of cumulative confirmed cases for the county<br/>
Total Tested - The cumulative number of tested individuals for the county<br/>
Negative - The cumulative number of negative tests for the county<br/>
Deaths - The cumulative number of deaths for the county<br/>
Lat - The latitiude of the county<br/>
Lon - The longitude of the county<br/>
<br/>
Information was obtained by catching the JSON data transfer over the network on "https://dph.illinois.gov/covid19/covid19-statistics". When following the historical tests source to "https://dph.illinois.gov/sitefiles/COVIDHistoricalTestResults.json?nocache=1", A JSON object with LastUpdateDate, Characteristics_by_county, demographics, historical_county, and state_testing_results is found. Only the historical county and state_testing_results contain information with time-series data. state_testing_results is a subset of data of the historical_county (only listing the aggregate Illinois state information). As we are interested in time-series data, only the historical county key was retrieved.<br/>

## Ohio
### Executive Orders
The following information regarding Ohio executive orders was obtained:<br/>
<br/>
Executive Order - The name of the order<br/>
Summary - A description (around a sentence) describing the order<br/>
Date - The date the order was signed by the governor of Ohio<br/>
Link - A url to the full HTML version of the order<br/>
<br/>
Information was obtained by scraping all cards on the page "https://governor.ohio.gov/wps/portal/gov/governor/media/executive-orders/" to get a listing of all orders and summary information. The link that each card points to was also scraped to grab the date information. <br/>

### Daily Counts

County - County of record <br/>
Sex - sex of record <br/>
Age Range - Range of ages for the record <br/>
Onset Date - Date of Covid-19 onset for the record <br/>
Date of Death - The date that individuals died (this will be empty unless the death count is > 0 <br/>
Admission Date - The date that individuals were admitted to the hospital (this will be empty unless the Hospitalized count > 0) <br/>
Case Count - The number of cases for the county / sex / age range on a single day <br/>
Death Count - The number of deaths for the county / sex / age range from the origional case count <br/>
Hospitalized Count - The number of hospitalized individuals for the county / sex / age range from the origional case count <br/>
 <br/>
Note: All data is dependent on the Case Count. That is the death count is the number of deaths from the case count per row in the table. Similarly, the hospitalized count is the number of hospitalized individuals from the case count per row in the table. The only way death count or hospitalized count can be greater than 1 is if two of the origional people were hospitalized or died on the same day. Otherwise, they are seperated into another entry in the table. Please view the sample below: <br/>
<br/>
![Ohio Data Explained](https://github.com/LukeJakielaszek/data_wrangling/blob/master/ohio_data_explained.PNG)
<br/>
Information was obtained by downloading the CSV file located at "https://coronavirus.ohio.gov/static/COVIDSummaryData.csv". After downloading, I dropped the total row at the bottom of the table as it lacks a timestamp and standardized the dates according to my selected formatting. Otherwise, this data required no further modificatio.<br/>

## Michigan
### Executive Orders
The following information regarding Michigan executive orders was obtained:<br/>
<br/>
Executive Order - The name of the order<br/>
Summary - A description (around a sentence) describing the order<br/>
Date - The date the order was signed by the governor<br/>
Link - A url to the full HTML version of the order<br/>
Covid Related - A boolean stating if the order is involved with the Covid Pandemic
Rescinded - A boolean if the order had been rescinded
State of Emergency - A boolean stating if the order declared a state of emergency

<br/>
Information was obtained by scraping the page "https://www.michigan.gov/whitmer/0,9309,7-387-90499_90705---,00.html" for the names of orders, covid relatedness, if it was rescinded, and whether it declared a state of emergency. Unfortunately, the dates of the orders and a short summary of each order was typically unavailable on the governors website. Therefore, the secondary source "http://www.legislature.mi.gov/(S(ryjl4kptgnu3sbx2uogeebw0))/mileg.aspx?page=executiveorders" was scraped for the year of 2020 to obtain summary information and dates for each order. To obtain the date of the order, I used optical character recognition on the final page of the scanned PDF files and extracted the dates. Finally, I went through at the end and looked for non-date extracted text, quickly fixing them manually. As this I only scraped this secondary site for the year of 2020, all orders from 2019 in my final dataset lack a summary and date.

### Daily Counts

## sources
### Illinois
#### Executive Orders
https://www2.illinois.gov/sites/coronavirus/Resources/Pages/ExecutiveOrders.aspx

#### Daily Counts
https://dph.illinois.gov/covid19/covid19-statistics


### Ohio 

#### Counts
https://coronavirus.ohio.gov/static/COVIDSummaryData.csv

#### Executive Orders
https://governor.ohio.gov/wps/portal/gov/governor/media/executive-orders/

### Michigan

#### daily counts
https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html

#### Executive Orders
https://www.michigan.gov/whitmer/0,9309,7-387-90499_90705---,00.html
http://www.legislature.mi.gov/(S(d3b0ixy34nwgszptpzq2e5ed))/mileg.aspx?page=executiveorders
