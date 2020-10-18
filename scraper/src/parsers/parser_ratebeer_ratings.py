import pandas as pd


with open('data/ratebeer_ratings.txt', encoding='ISO-8859-1') as f:
    data = f.read()

rows = data.split('\n')

columns = ['beer_id', 'name', 'brewery', 'aroma', 'appearance', 'taste', 'palate', 'overall', 'my_score', 'comment',
           'review_date', 'country', 'state', 'city', 'style']

beers_list = []
for i, row in enumerate(rows[1:]):
    beer = {}
    values = row.split('|')
    for j, column in enumerate(columns):
        beer[column] = values[j]

    beers_list.append(beer)

    progress = i / len(rows)
    if i % 100 == 0:
        print(f'{(progress * 100):.1f} %')

beers_df = pd.DataFrame(beers_list)
beers_df.to_csv('data/ratebeer_ratings.csv')
