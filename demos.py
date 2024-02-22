# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:19:00 2023

@author: Bogdan Tudose
"""

#Power of Python Demo
import pandas as pd #data manipulation package
import plotly.express as px #visualization package
import requests #connecting to websites
#https://bogdan.streamlit.app/

#%% Aggregating Large Amounts of Data
    # Ontario Sunshine List
    # Data Source: https://www.ontario.ca/page/public-sector-salary-disclosure
    # Dashboard: https://on-sunshine.streamlit.app/
    # Code aggregates 25+ years of data from multiple excel files, 2,187,974 rows of data
        #247MB of data
    
    
# Alberta Sunshine List
# https://www.alberta.ca/salary-and-severance-disclosure-table.aspx
# https://open.alberta.ca/opendata/public-disclosure-of-salary-and-severance
url = "http://salaries.dataservices.alberta.ca/files/alberta-salary-disclosure.csv"
df = pd.read_csv(url)
df.info()
pivot = df.groupby(['Year'])['BaseSalary'].mean()
pivot2 = df.groupby(['Year','Ministry'])['BaseSalary'].mean().reset_index()
pivot3 = df.groupby(['Ministry','PositionClass'])['BaseSalary'].mean().reset_index()
pivot3.to_excel('Alberta Salaries.xlsx')


df.columns
#Visualizations
fig = px.bar(pivot, x=pivot.index, y='BaseSalary')
fig.write_html(file="AB Salaries.html",auto_open=True)

pivot2['Year'] = pivot2['Year'].astype(str)
# fig2 = px.bar(pivot2, x="Ministry", y='BaseSalary', color='Year', barmode='group') #stack
# fig2 = px.bar(pivot2, x="Ministry", y='BaseSalary', color='Year', barmode='stack') 
fig2 = px.bar(pivot2, x="Year", y='BaseSalary', color='Ministry', barmode='stack') 
fig2.write_html(file="AB Salaries by Ministry.html",auto_open=True)

#%% Complex Dashboards with Financial Analysis:
    # Beta Calculator
    # https://bogdan.streamlit.app/Stock_Beta_Calculator

#%% Options Calculator
    # https://bogdan.streamlit.app/Options_Calculator

#%% Industry Data Web API Examples

#%%%Air Passengers data

#%%% Top8 Airports Canada
# https://www.catsa-acsta.gc.ca/en/screened-passenger-data
url= "https://www.catsa-acsta.gc.ca/en/screened-passenger-data"
tables = pd.read_html(url)
df = tables[0]
dfTop8 = df.iloc[1:,0:6]
dfTop8['Date'] = pd.to_datetime(dfTop8['Year'] + '-2024') #convert to dates

years = [str(year) for year in range(2020,2025)]
for year in years:
    dfTop8[year] = pd.to_numeric(dfTop8[year])

#plotting series
dfTop8.plot(x='Date',y=years)
# dfTop8.plot(x='Date',y=['2020','2021','2023','2024',])

#calculated fields
dfTop8['YoY'] = dfTop8['2024'] / dfTop8['2023'] - 1
dfTop8['2024 YTD'] = dfTop8['2024'].cumsum()
dfTop8['2023 YTD'] = dfTop8['2023'].cumsum()
dfTop8['2024 YoY Cumul'] = dfTop8['2024 YTD'] / dfTop8['2023 YTD'] - 1

dfTop8.plot(x='Date',y='2024 YoY Cumul')

#Other plots
#histogram
dfTop8['2023'].plot(kind='hist')
dfTop8['2023'].plot(kind='hist',bins=30)

dfTop8['2023'].plot(kind='box')

#Stats
stats = dfTop8.describe()

#%%% Alberta Airports
# https://economicdashboard.alberta.ca/AirPassengers#type
#Air Passengers
# url = 'https://economicdashboard.alberta.ca/Download/DownloadFile?extension=JSON&requestUrl=https%3A%2F%2Feconomicdashboard.alberta.ca%2Fapi%2FAirPassengers'
df = pd.read_json(url)
df.info()
df['Date'] = pd.to_datetime(df['When'])
# figAir = px.line(df, x="Date", y='Alberta', color='Airport')
figAir = px.bar(df, x="Date", y='Alberta', color='Airport')
figAir.write_html(file="Alberta Airport Data.html",auto_open=True)


#%% API Alberta
"""
The total monthly number of passengers, including arrivals and departures, 
travelling through the Edmonton International (YEG) and 
Calgary International (YYC) airports. 
This includes domestic, transborder (Canada-U.S.), and international flights.
"""
# https://api.economicdata.alberta.ca/api/data?code=1c22431c-ad90-4614-a973-9c39f309d9c7
# url = "https://api.economicdata.alberta.ca/api/data?code=1c22431c-ad90-4614-a973-9c39f309d9c7"

codes = {'all':'1c22431c-ad90-4614-a973-9c39f309d9c7',
         'type':'82b15b0b-4475-4034-9ba4-f00188b3784e',
         'airport':'46f88a70-c204-4e15-9168-5366dc8bea6d'}

params = {'code': ''}
tables = {}
jsonFiles = {}
for dataType, code in codes.items():
    params['code'] = code
    response = requests.get('https://api.economicdata.alberta.ca/api/data', params=params)
    data = response.json()
    jsonFiles[dataType] = data #save down the json file
    df = pd.DataFrame(data)    
    df['Date'] = pd.to_datetime(df['Date'])
    tables[dataType] = df

#Passenger data by airport
dfAirport = tables['airport']
dfAll = tables['all']
figAll = px.bar(dfAll, x="Date", y='Value', title='All Alberta Airports')
figAll.write_html(file="Alberta Airport Data.html",auto_open=True)

figAir = px.line(dfAirport, x="Date", y='Value', color='Airport')
figAir.write_html(file="Airport Data by Airport.html",auto_open=True)
# df.plot(x='Date',y='Value')
dfAirport.to_excel('Airport Data.xlsx')
#See live app streamlit
    # https://albertaairports.streamlit.app/
#%%% Planes vs automobiles Emissions
    # Creator: Jamie Wilkie 
    # https://energyminuteplanesvsautos.streamlit.app/
    # Main Source: Canada Open APO
        #https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64

#%%% Alberta Electricity Generation
    # Creator: Jamie Wilkie 
    # https://energyminuteabpowergeneration.streamlit.app/
    # Data Source: http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet

# Other useful APIs
    # https://open.alberta.ca/interact/for-developers#:~:text=The%20Government%20of%20Alberta%20is,.ca%2Fapi%2F3


#%% Demo PDF Files
from tabula import read_pdf
url = "https://trreb.ca/files/market-stats/condo-reports/condo_report_Q3-2020.pdf"
df = read_pdf(url, pages=2, multiple_tables=True)


# url = "http://members.rebgv.org/news/REBGV-Stats-Pkg-October-2020.pdf"
url = "https://members.rebgv.org/news/REBGV-Stats-Pkg-Jan-2024.pdf"
dfs = read_pdf(url, pages=3, multiple_tables=True)

df = dfs[0]

#%% Bank of Canada API
url = 'https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json?start_date=2017-01-03'
resp = requests.get(url)
data = resp.json()
df = pd.DataFrame(data['observations'])
table = df[['d','FXUSDCAD','FXAUDCAD']].copy()
table['USDCAD'] = table['FXUSDCAD'].apply(lambda x: x['v']).astype(float)
table['AUDCAD'] = table['FXAUDCAD'].apply(lambda x: x['v']).astype(float)
table['Date'] = pd.to_datetime(table['d'])

table.plot(x='Date', y=['USDCAD','AUDCAD'])


#%% Upcoming sessions

# CFA Calgary
# CORE DATA ANALYSIS: PYTHON INTRODUCTORY WORKSHOP
# Tuesday, March 19, 2024
# 8:30 a.m. - 4:30 p.m. MST


# WEB SCRAPING WITH PYTHON (ADVANCED MODULE)
# Wednesday, March 20, 2024
# 1:30 p.m. - 5:00 p.m. MST


#CFA Vancouver
#Python 1 - April 9
#Python 2 - May 14
#Python 3 - June 11



