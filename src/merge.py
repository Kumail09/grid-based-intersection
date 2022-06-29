import pandas as pd

df1 = pd.read_csv('MergedAp.csv').drop(columns=['S.no'])

print(df1)
df1.drop_duplicates(inplace=True)
print(df1)


df2 = pd.read_csv('MergedGps.csv').drop(columns=['S.no'])
df2.drop_duplicates(inplace=True)


# def preprocess(x):
#     print('Processing')
#     x = x.drop(columns=['S.no'])
#     df2 = pd.merge(df1, x, on='index_right')
#     df2 = df2[['index_right', 'mac_address', 'trip_id']]
#     df2.to_csv("df3.csv", mode="a", header=False, index=False)


df3 = pd.merge(df1, df2, on='index_right')
df3 = df3[['index_right', 'mac_address', 'trip_id']]
df3.rename(columns={'index_right': 'cell_index'}, inplace=True)
df3.to_csv('Merged.csv', index=False)

# reader = pd.read_csv("MergedGps.csv", chunksize=1000)
#
# [preprocess(r) for r in reader]


