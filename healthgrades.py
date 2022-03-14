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
driver = webdriver.Firefox(service=service, options=options)
# wait = WebDriverWait(driver, 10)


def get_cities():
    base_url = 'https://www.healthgrades.com'
    cities_url = 'https://www.healthgrades.com/find-a-doctor/new-york'
    driver.get(cities_url)
    sleep(10)
    body = driver.page_source
    html = HTML(html=body)

    city_links = []
    city_element = html.find('ul.link-column > li')
    for link in city_element:
        link = link.find('a', first=True).links.pop()
        link = f'{base_url}{link}'
        city_links.append(link)


def get_specialty():
    specialty_element = html.find('ul.link-column > li')
    pages = 1
    specialty_list = []
    specialty_links = []
    for specialty in specialty_element:
        specialty = specialty.text
        link = f'https://www.healthgrades.com/usearch?what={specialty}&where={city}%2C%20NY&distances=100&pageNum={pages}&sort.provider=bestmatch'
        specialty_list.append(specialty)
        specialty_links.append(link)
    # print(specialty_links)

    specialty = specialty_list[6] # <-- change to select individual specialty

    specialty_url = specialty_links[6] # <-- change to select individual specialty
    print(specialty)
    print(specialty_url)

    driver.get(specialty_url)
    sleep(5)
    body = driver.page_source
    html = HTML(html=body)

    pages = html.find('.results__pagination p', first=True).text.split()[-1]
    if int(pages) > 100:
        pages = '99'
    print(f'{pages} pages')





if __name__ == '__main__':
    city_link = city_links[0] # <-- change to select individual city
    print(city_link)

    city = city_link.split('/')[-1]
    print(city)


    driver.get(city_link)
    sleep(4)
    body = driver.page_source
    html = HTML(html=body)

    
provider_list = []

for page in range(1, int(pages)+1):
# for page in range(1, 4):
    print(f'Processing page {page} of {pages} pages for {specialty}.')
    url = f'https://www.healthgrades.com/usearch?what={specialty}&where={city}%2C%20NY&distances=100&pageNum={page}&sort.provider=bestmatch'
    driver.get(url)
    sleep(5)

    body = driver.page_source
    html = HTML(html=body)
    
    cards = html.find('.search-card__card-info')
    for card in cards:
        try:
            provider_name = card.find('h3.provider-details__provider-name', first=True)
            provider_name = provider_name.find('a', first=True).text
            if 'Dr.' in provider_name and 'Jr.' in provider_name:
                provider_name = provider_name.split('.')[1].split(',')[0].strip()
            elif 'Dr.' in provider_name:
                provider_name = provider_name.split('.')[1].split(',')[0].strip()
            else:
                provider_name = provider_name.split(',')[0].strip()
        except:
            None
        try:
            provider_title = card.find('h3.provider-details__provider-name', first=True)
            provider_title = provider_title.find('a', first=True).text
            if 'Dr.' in provider_title and 'Jr.' in provider_title:
                provider_title = provider_title.split(',')[1].strip()
            elif 'Dr.' in provider_title:
                provider_title = provider_title.split(',')[1].strip()
            elif ',' not in provider_title:
                provider_title = None
            else:
                provider_title = provider_title.split(',')[1].strip()
        except:
            None
        try:
            provider_specialty = card.find('.provider-details__specialty', first=True).text
        except:
            None
        try:
            provider_address = card.find('.card-info__location-info', first=True).text.split('\n')[0]
        except:
            None
        try:
            provider_city = card.find('.card-info__location-info', first=True).text.split('\n')[1].split(',')[0]
        except: 
            None
        try:
            provider_state = card.find('.card-info__location-info', first=True).text.split('\n')[1].split(',')[1].split()[0]
        except: 
            None
        try:
            provider_zip = card.find('.card-info__location-info', first=True).text.split('\n')[1].split(',')[1].split()[1]
        except:
            None
        try:
            provider_phone = card.find('.booking-options__booking-phone', first=True)
            provider_phone = provider_phone.find('a', first=True).text
        except:
            None

        data = {
                'Name': provider_name,
                'Title': provider_title,
                'Specialty': provider_specialty,
                'Address': provider_address,
                'City': provider_city,
                'State': provider_state,
                'Zip': provider_zip,
                'Phone': provider_phone
            }

        provider_list.append(data)    

    n = random.randint(1, 5)
    sleep(n)

    # driver.close()

    df = pd.DataFrame(provider_list)
    filename = f'ny_{city}_{specialty}'
    filename = filename.replace(' ', '_').lower()
    filename = f'{filename}.csv'
    df.to_csv(filename, index=False)