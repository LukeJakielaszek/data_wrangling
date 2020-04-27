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

### Daily Counts

## Michigan
### Executive Orders

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
