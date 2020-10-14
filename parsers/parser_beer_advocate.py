import pandas as pd
import re

with open('data/beer.json') as f:
    read_data = f.read()
    # Split data.
    items = read_data.split('\n')

beers_list = []
for i, item in enumerate(items):
    try:
        beer = {'review_appearance_score': re.search("'review/appearance': (.+?), '", item).group(1)
                if re.search("'review/appearance': (.+?), '", item) is not None else None,
                'beer_style': re.search("'beer/style': (.+?), '", item).group(1)
                if re.search("'beer/style': (.+?), '", item) is not None else None,
                'review_palate_score': re.search("'review/palate': (.+?), '", item).group(1)
                if re.search("'review/palate': (.+?), '", item) is not None else None,
                'review_taste_score': re.search("'review/taste': (.+?), '", item).group(1)
                if re.search("'review/taste': (.+?), '", item) is not None else None,
                'beer_name': re.search("'beer/name': (.+?), '", item).group(1)
                if re.search("'beer/name': (.+?), '", item) is not None else None,
                'review_time': re.search("'review/timeUnix': (.+?), '", item).group(1)
                if re.search("'review/timeUnix': (.+?), '", item) is not None else None,
                'user_gender': re.search("'user/gender': (.+?), '", item).group(1)
                if re.search("'user/gender': (.+?), '", item) is not None else None,
                'user_birthday': re.search("'user/birthdayUnix': (.+?), '", item).group(1)
                if re.search("'user/birthdayUnix': (.+?), '", item) is not None else None,
                'beer_ABV': re.search("'beer/ABV': (.+?), '", item).group(1)
                if re.search("'beer/ABV': (.+?), '", item) is not None else None,
                'beer_id': re.search("'beer/beerId': (.+?), '", item).group(1)
                if re.search("'beer/beerId': (.+?), '", item) is not None else None,
                'review_overall_score': re.search("'review/overall': (.+?), '", item).group(1)
                if re.search("'review/overall': (.+?), '", item) is not None else None,
                'review_text': re.search("'review/text': (.+?), '", item).group(1)
                if re.search("'review/text': (.+?), '", item) is not None else None,
                'review_user': re.search("'user/profileName': (.+?), '", item).group(1)
                if re.search("'user/profileName': (.+?), '", item) is not None else None,
                'review_aroma_score': re.search("'review/aroma': (.+?)}", item).group(1)
                if re.search("'review/aroma': (.+?)}", item) is not None else None}
        beers_list.append(beer)
        progress = i / len(items)
        if i % 10000 == 0:
            print(f'{(progress * 100):.1f} %')
    except AttributeError:
        print(item)
        # AAA, ZZZ not found in the original string
        found = ''  # apply your error handling
beers_df = pd.DataFrame(data=beers_list)
beers_df.info()
print(f'There are {len(beers_df["beer_name"].unique())} different beers in this dataset.')
beers_df.to_csv('data/beers.csv')
