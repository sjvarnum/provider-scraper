from datetime import datetime
import pandas as pd
import random
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import *
from time import sleep

service = Service('geckodriver.exe')
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
base_url = 'https://www.healthgrades.com/find-a-doctor'
driver = webdriver.Firefox(service=service, options=options)
# wait = WebDriverWait(driver, 10)
url = 'https://www.healthgrades.com/usearch?what=Pulmonary%20Disease&where=Albany%2C%20NY&pageNum=1&sort.provider=bestmatch'
driver.get(url)
sleep(10)

body = driver.page_source
html = HTML(html=body)
cards = html.find('.search-card__card-info')
provider_list = []
for card in cards:
    try:
        provider_name = card.find('h3.provider-details__provider-name', first=True)
        provider_name = provider_name.find('a', first=True).text
        print(provider_name)
    except:
        None
    try:
        provider_specialty = card.find('.provider-details__specialty', first=True).text
    except:
        None
    try:
        provider_address = card.find('.card-info__location-info', first=True).text.split('\n')[0]
        # provider_address = provider_location.split('\n')[0]
    except:
        None
    try:
        provider_city = card.find('.card-info__location-info', first=True).text.split('\n')[1].split(',')[0]
        # provider_city = provider_address.split('\n')[1].split(',')[0]
    except: 
        None
    try:
        provider_zip = card.find('.card-info__location-info', first=True).text.split('\n')[1].split(',')[1].split()[1]
    except:
        None

    data = {
            'Name': provider_name,
            'Specialty': provider_specialty,
            'Address': provider_address,
            'City': provider_city,
            'Zip': provider_zip
        }

    provider_list.append(data)    

    # n = random.randint(1, 5)
    # sleep(n)

print(provider_list)

driver.close()