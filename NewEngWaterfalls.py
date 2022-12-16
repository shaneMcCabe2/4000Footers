import gspread # handling google sheets
import pandas as pd
import numpy as np
import googlemaps
from geopy.geocoders import GoogleV3 # handling geocode in python
import sqlite3

# reference sites: 
# https://pyshark.com/geocoding-in-python/
# https://newenglandwaterfalls.com/4000footers.php


# credentials for connecting to google sheets API
gc = gspread.service_account(filename='credentials.json')

# open a workbook from URL
wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/11lX-31JNouPS3rKwE0axZrrz-x0dbob-MfSOvBs6X84/edit#gid=1296847477')

# open specific worksheet
ws = wb.worksheet('OG')

# add google sheet table to dataframe
df = pd.DataFrame(ws.get_all_records())

# add names column to enable google maps search
df['Name'] = 'Mount ' + df['Mountain'] + ', NH'
# manipulate individual cell that was causing issues
df.at[29,'Name'] = 'Bondcliff, Lincoln, NH'

# initialize arrays tp pull in data from Google
add_arr = []
lat_arr = []
long_arr = []

# set up geocoder with our api key
API = 'AIzaSyCGNHGc871PGzHefCygn7v3P-0zhfxGc0Q'
geolocator = GoogleV3(api_key=API)

# iterate through the name column to get location data of each MT from Google
for item in df['Name']:
    location = geolocator.geocode(item)
    if location is None:
        add_arr = np.append(add_arr, '')
        lat_arr = np.append(lat_arr, '')
        long_arr = np.append(long_arr, '')
    else:
        add_arr = np.append(add_arr, location.address)
        lat_arr = np.append(lat_arr, location.latitude)
        long_arr = np.append(long_arr, location.longitude)

# create new columns in df from arrays        
df['Address'] = add_arr
df['Latitude'] = lat_arr
df['Longitude'] = long_arr

# clean Name column after google search
df['Name'] = df['Name'].str[:-4]

# connect to SQLite database
conn = sqlite3.connect(r'footers.db')

# write the data to a sqlite table
df.to_sql('footers', conn, if_exists='replace', index=False)

# create a cursor object
cur = conn.cursor()
# fetch and display result
for row in cur.execute('SELECT * FROM footers'):
    print(row)
# close connection to SQLite database
conn.close()







