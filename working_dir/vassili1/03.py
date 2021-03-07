import pandas as pd


with open('working_dir/vassili1/bank leads emails md,va,dc - Sheet1.csv', 'r') as f:
    f = f.read()

f = f.replace('\n\n' , '\n')


df = pd.read_csv('working_dir/vassili1/bank leads emails md,va,dc - Sheet1.csv')

for i,k in df.iterrows():
    k[3] = k[3].split('\n\n')[-1]

df.to_excel('working_dir/vassili1/bank leads emails md,va,dc.xlsx')



df = pd.read_csv('working_dir/vassili1/bank leads ny email - Sheet1.csv')

for i,k in df.iterrows():
    k[3] = k[3].split('\n\n')[-1]

df.to_excel('working_dir/vassili1/bank leads ny email.xlsx')