import collections
import os
import json

import pandas as pd

data_files = os.listdir('working_dir/vassili/dnb/emails/data')
email_files = os.listdir('working_dir/vassili/dnb/emails/emails')

emails = {}
data = []

for em in email_files:
    with open(f'working_dir/vassili/dnb/emails/emails/{em}', 'r') as f:
        f = json.load(f)
        emails[f['id']] = f

for da in data_files:
    with open(f'working_dir/vassili/dnb/emails/data/{da}', 'r') as f:
        f = json.load(f)
        for i in f:
            emai = emails.get(i.get('id'))
            if emai:
                i['email'] = emai
            else:
                print(i['id'], 'has no email')
            data.append(i)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for aa in range(len(v)):
                if isinstance(v[aa], dict):
                    items.append((f"{k}_{aa}", flatten(v[aa])))
                else:
                    items.append((f"{k}_{aa}", v[aa]))

        else:
            items.append((new_key, v))
    return dict(items)

new_data = [flatten(i) for i in data]
new_data = [flatten(i) for i in new_data]


df = pd.DataFrame(new_data)

df.to_csv('data.csv')