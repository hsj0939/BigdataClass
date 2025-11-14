import pandas as pd

file_name = './survey_raw.csv'
df_raw = pd.read_csv(file_name)

column_AGE = 'Age'

print('-'*50)
print(df_raw.head())

print('-'*50)
print(df_raw['Age'])

sr_age = df_raw['Age']

print('-'*50)
print(sr_age.unique())

print('-'*50)
print(sr_age.drop_duplicates())

print('-'*50)
print(df_raw.groupby([column_AGE]))