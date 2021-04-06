import collections
import json
import os

PATH = 'working_dir/vassili/dnb/data'
files = os.listdir(PATH)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

data = []
count = 1

for file in files:
    with open('working_dir/vassili/dnb/data/' + file, 'r') as f:
        fil = json.load(f)
        for rec in fil:
            data.append(rec)
        if len(data) > 50000:
            print(count)
            with open(f'working_dir/vassili/dnb/proc_data.nosync/{count}.json', 'w') as f:
                json.dump(data, f)
                data = []
                count += 1

