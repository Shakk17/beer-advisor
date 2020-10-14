import pandas as pd

from bs4 import BeautifulSoup


with open('data/Products-2020-okt-05-091213.html', encoding='utf-8') as f:
    data = f.read()

print('File loaded.')

soup = BeautifulSoup(data, 'html.parser')
columns = ['number', 'id', 'item_number', 'name', 'name2', 'price_with_VAT', 'pant', 'volume_ml',
           'price_per_liter', 'start_sale', 'expired', 'item_group', 'type', 'style', 'packaging',
           'closing', 'origin', 'origin_country', 'producer', 'supplier', 'year_vintage', 'provadargang',
           'abv', 'assortment', 'assortment_text', 'ecologic', 'etical', 'etical_label', 'kosher', 'description']
rows = soup.find_all('tr')
beers_list = []

for i, row in enumerate(rows[1:]):
    beer = {}

    values = row.find_all('td')
    for j, column in enumerate(columns):
        beer[column] = values[j].text if values[j].text != '\xa0' else None

    beers_list.append(beer)

    progress = i / len(rows)
    if i % 100 == 0:
        print(f'{(progress * 100):.1f} %')

beers_df = pd.DataFrame(beers_list)
beers_df.to_csv('data/sysbo.csv')
