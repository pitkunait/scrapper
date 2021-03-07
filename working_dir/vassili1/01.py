import json
import os

list = []

for i in os.listdir('working_dir/vassili'):
    if i.startswith('data') and 'list' not in i:
        with open(f'working_dir/vassili/{i}', 'r') as f:
            l = json.load(f)
            list = list + l

with open('working_dir/vassili1/all.json', 'w') as f:
    json.dump(list, f)
