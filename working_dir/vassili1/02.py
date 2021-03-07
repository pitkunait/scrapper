import pandas as pd
import json
import collections

with open('working_dir/vassili1/all.json', 'r') as f:
    corps = json.load(f)

for i in corps:
    i['addresses'] = i['addresses'][0]

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

hui = []

for i in corps:
   hui.append(flatten(i))



with open("data3.csv", "w") as f:
    f.write(','.join(hui[0].keys()) + '\n')
    for i in hui[150000:]:
        f.write(','.join([str(dd) for dd in i.values()]) + '\n')


df = pd.DataFrame(hui[:50000])
df.to_excel('data1.xlsx')

df1 = pd.DataFrame(hui[50000:100000])
df1.to_excel('data2.xlsx')


df2 = pd.DataFrame(hui[100000:150000])
df2.to_excel('data3.xlsx')


df3 = pd.DataFrame(hui[150000:])
df3.to_excel('data4.xlsx')


