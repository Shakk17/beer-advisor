import re
import string
from time import time, sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import logging

# Set up logging for errors.
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# Default value is 'sprit'.
trans = {
    'rott-vin': 'roda-viner',
    'vitt-vin': 'vita-viner',
    'mousserande-vin': 'mousserande-viner',
    'rosevin': 'roseviner',
    'ol': 'ol',
    'blandlador-vin': 'aperitif-dessert',
    'glogg-och-gluhwein': 'aperitif-dessert',
    'aperitif-och-dessert': 'aperitif-dessert',
    'sake': 'aperitif-dessert',
    'vermouth': 'aperitif-dessert',
    'bla-stilla': 'aperitif-dessert',
    'bla-mousserande': 'aperitif-dessert',
    'cider': 'cider-och-blanddrycker',
    'blanddrycker': 'cider-och-blanddrycker',
    'alkoholfritt': 'alkoholfritt',
    'presentforpackningar': 'presentartiklar',
    'dryckestillbehor': 'presentartiklar',
}


def get_attributes(soup):
    buttons = soup.find_all('button', {'class': 'cmp-keyword-description cmp-keyword-description-inside color-no-dash'})
    icons = [button.find('i').prettify() for button in buttons]
    texts = [button.find('div').text for button in buttons]
    attributes = ['Beska', 'Fyllighet', 'Sötma']
    values = {}
    for i in range(len(icons)):
        values[texts[i]] = re.search("icon-tasteclock-(.)", icons[i]).group(1) if texts[i] in attributes else 1
    return values


def get_time_left(start_time):
    time_passed = time() - start_time
    time_per_item = time_passed / (items_scraped + 1)
    remaining_items = n_items - i
    time_to_finish = time_per_item * remaining_items
    hrs_left = int(time_to_finish / 3600)
    min_left = int((time_to_finish - (hrs_left * 3600)) / 60)
    sec_left = int(time_to_finish % 60)
    return hrs_left, min_left, sec_left


sysbo_df = pd.read_csv('data/sysbo.csv', index_col='number')
try:
    new_sysbo_df = pd.read_csv('data/new_sysbo.csv', index_col='number')
except FileNotFoundError:
    new_sysbo_df = sysbo_df.copy()
n_items = sysbo_df.shape[0]

start_time = time()
items_scraped = 0

for number, item in new_sysbo_df.iterrows():
    try:
        if item['scraped'] == 1:
            print('Item already scraped.')
            continue
    except KeyError:
        # First element to scrape. Feature 'scraped' does not exist yet.
        pass
    i = int(item['Unnamed: 0'])

    # Remove punctuation.
    name = unidecode(item['name'].lower())
    name = name.translate(str.maketrans('', '', string.punctuation.replace('-', '')))
    name = name.replace(' ', '-').replace('--', '-').replace('--', '-')

    group = unidecode(item['item_group'].lower().replace(' ', '-'))

    old_url = f'https://www.systembolaget.se/dryck/{group}/{name}-{number}'

    group = trans.get(group, 'sprit')

    url = f'https://www.systembolaget.se/dryck/{group}/{name}-{number}'

    try:
        html = requests.get(url).text
    except Exception:
        print('Connection error.')
        continue

    soup = BeautifulSoup(html, 'html.parser')
    try:
        # If cannot get price, throw an error.
        price = soup.find('li', {'class': 'price'}).text
        # Get attributes.
        values = get_attributes(soup)
        # Update dataframe.
        new_sysbo_df.loc[number, 'scraped'] = 1
        for name, value in values.items():
            new_sysbo_df.loc[number, f'scraped_{name.lower()}'] = value
    except Exception:
        logging.error(f'NAME: {name}               OLD: {old_url}                 NEW: {url}')
        print(f'ERROR: {name}')
    finally:
        items_scraped += 1
        hrs_left, min_left, sec_left = get_time_left(start_time)
        print(f'{i / n_items * 100:.1f} % - TIME LEFT: {hrs_left}h {min_left}m {sec_left}s')
        # Save dataset every 500 items.
        if i % 50 == 0:
            print('Saving dataset.')
            new_sysbo_df.to_csv('data/new_sysbo.csv')
