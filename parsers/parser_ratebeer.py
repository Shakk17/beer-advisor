import pandas as pd
import re

with open('data/ratebeer.txt', encoding='ISO-8859-1') as f:
    data = f.read()

print('File loaded.')

items = data.split('\n\n')
beers_list = []
for i, item in enumerate(items):
    try:
        beer = {'beer_name': re.search("beer/name: (.+?)\n", item).group(1)
                if re.search("beer/name: (.+?)\n", item) is not None else None,
                'beer_id': re.search("beer/beerId: (.+?)\n", item).group(1)
                if re.search("beer/beerId: (.+?)\n", item) is not None else None,
                'brewer_id': re.search("beer/brewerId: (.+?)\n", item).group(1)
                if re.search("beer/brewerId: (.+?)\n", item) is not None else None,
                'beer_ABV': re.search("beer/ABV: (.+?)\n", item).group(1)
                if re.search("beer/ABV: (.+?)\n", item) is not None else None,
                'beer_style': re.search("beer/style: (.+?)\n", item).group(1)
                if re.search("beer/style: (.+?)\n", item) is not None else None,
                'review_appearance': re.search("review/appearance: (.+?)\n", item).group(1)
                if re.search("review/appearance: (.+?)\n", item) is not None else None,
                'review_aroma': re.search("review/aroma: (.+?)\n", item).group(1)
                if re.search("review/aroma: (.+?)\n", item) is not None else None,
                'review_palate': re.search("review/palate: (.+?)\n", item).group(1)
                if re.search("review/palate: (.+?)\n", item) is not None else None,
                'review_taste': re.search("review/taste: (.+?)\n", item).group(1)
                if re.search("review/taste: (.+?)\n", item) is not None else None,
                'review_overall': re.search("review/overall: (.+?)\n", item).group(1)
                if re.search("review/overall: (.+?)\n", item) is not None else None,
                'review_time': re.search("review/time: (.+?)\n", item).group(1)
                if re.search("review/time: (.+?)\n", item) is not None else None,
                'review_user': re.search("review/profileName: (.+?)\n", item).group(1)
                if re.search("review/profileName: (.+?)\n", item) is not None else None,
                'review_text': item.split('review/text: ')[1]
                if 'review/text: ' in item else None}
        beers_list.append(beer)
        progress = i / len(items)
        if i % 10000 == 0:
            print(f'{(progress * 100):.1f} %')
    except AttributeError:
        print(item)
        # AAA, ZZZ not found in the original string
        found = ''  # apply your error handling
beers_df = pd.DataFrame(data=beers_list)
beers_df.to_csv('data/ratebeer.csv')
