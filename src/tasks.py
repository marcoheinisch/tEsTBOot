import os
import requests
import datetime
from bs4 import BeautifulSoup
from firebase import Firebase

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
FIREBASE_DB_URL = os.getenv('FIREBASE_DB_URL')
WOF_URL = os.getenv('WOF_URL')


def __get_wof_soup() -> BeautifulSoup:
    """Request Website with gym utilization data"""

    url = ()
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def __get_wof_value(wof_soup):
    """Get gym utilization data"""

    data = []
    table = wof_soup.find('table')
    table_body = table.find('tbody')

    table_rows = table_body.find_all('tr')
    for table_row in table_rows:
        table_tds = table_row.find_all('td')
        for table_td in table_tds:
            divs = table_td.find_all("div")
            value = [div.text.strip() for div in divs]

        data.append([v for v in value if v]) # Get rid of empty values

    data_wof1 = int(data[0][0].replace('%',''))

    return data_wof1

def do_request_and_save():
    data_wof1 = -1
    try:
        soup = __get_wof_soup()
        data_wof1 = __get_wof_value(soup)
    except Exception:
        print("Error: get_wof failed!")
        
    now = datetime.datetime.today()
    date_str = str(now.date())
    time_str = str(now.time())[:8]

    config = {
    'apiKey': str(FIREBASE_API_KEY),
    'authDomain': "",
    'databaseURL': str(FIREBASE_DB_URL),
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': ""
    }

    firebase = Firebase(config)
    db = firebase.database()
    
    db.child("datapoints").update({date_str+"/"+time_str : data_wof1})
