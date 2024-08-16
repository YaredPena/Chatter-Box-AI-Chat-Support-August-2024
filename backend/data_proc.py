import numpy as np
import pandas as pd
import os

df=pd.read_csv('data/sample.csv') #load df
print(df.shape)

print(df.columns)
print(df[['tweet_id','in_response_to_tweet_id']])

response_dict={}
print(119237 in df['tweet_id'].values) #test if i located right
for index, row in df.iterrows():
    if row['in_response_to_tweet_id'] in df['tweet_id'].values:
        response_dict[row['text']]=df.loc[df['tweet_id'] == row['in_response_to_tweet_id'], 'text'].iloc[0] #filter if the response is in the array. 
        #the returned dctionary is in question: response format
print(len(response_dict.keys()))# length of our dictionary
data= { 'complaints': response_dict.values(),
        'responses': response_dict.keys() }
output=pd.DataFrame.from_dict(data=data)
print(output)

file_name = 'out.csv'
df.to_csv(file_name, index=False)