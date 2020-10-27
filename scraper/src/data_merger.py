import string
import itertools
from time import time
import pandas as pd

from editdistance import eval as lev_distance
from sklearn.metrics.pairwise import cosine_similarity


def get_time_left(start, n_items, items_done):
    time_passed = time() - start
    time_per_item = time_passed / (items_done + 1)
    remaining_items = n_items - items_done
    time_to_finish = time_per_item * remaining_items
    hrs_left = int(time_to_finish / 3600)
    min_left = int((time_to_finish - (hrs_left * 3600)) / 60)
    sec_left = int(time_to_finish % 60)
    return hrs_left, min_left, sec_left


# Import datasets.
ratebeer_df = pd.read_csv('data/ratebeer.csv')
print('Loaded ratebeer.csv')

beeradvocate_df = pd.read_csv('data/beeradvocate.csv')
print('Loaded beeradvocate.csv')

sysbo_df = pd.read_csv('data/sysbo.csv')
print('Loaded new_sysbo.csv')


rb_names = ratebeer_df['beer_name'].dropna()
sb_names = sysbo_df['name'].dropna()

# Export for Google Colab.
rb_names.to_csv('rb_names.csv')
sb_names.to_csv('sb_names.csv')

# GOOGLE COLAB PART.

n = len(rb_names) * len(sb_names)
print(f'TOTAL: {n}')

# Comparison.
vals = []
i = 0
comb = itertools.product(rb_names, sb_names)
start_time = time()
for (x, y) in comb:
    if i % 1000000 == 0:
        hrs_left, min_left, sec_left = get_time_left(start_time, n, i)
        print(f'PROGRESS: {i / n * 100:.2f} % - TIME LEFT: {hrs_left}h {min_left}m {sec_left}s')
    dist = lev_distance(x, y)
    vals.append((x, y, dist))
    i += 1

