import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# Let's look at the dataset
companies = pd.read_csv('companies.txt', sep='\t', encoding= 'ISO-8859-1')
rounds = pd.read_csv('rounds2.csv', encoding = 'ISO-8859-1')

# Looking at the dataset head
print(rounds.head())
print(rounds.info(), '\n')
print(rounds.shape)

# Lets look at the companies head
print(companies.head())
print(companies.info())
print(companies.shape)

# identify the unique number of permalinks in companies
print(len(companies.permalink.unique()))

# Also let's convert all the entries to lowercase (or uppercase) for uniformity.
# converting all permalinks to lowercase.

companies['permalink'] = companies['permalink'].str.lower()
print(companies.head())


# let's look at the unique values again
print(len(companies['permalink'].unique()))

# lets look at the unique names in round df
# Note that the column name in rounds file is different(company_permalink)
print(len(rounds['company_permalink'].unique()))

# converting column to lowercase
rounds['company_permalink']= rounds['company_permalink'].str.lower()
print(rounds.head())

# Let's look at the unique values again
print(len(rounds.company_permalink.unique()))

# companies present in round file but not in company file
print(rounds.loc[~rounds['company_permalink'].isin(companies['permalink']), :])

# looking at the indices with weird characters
rounds_original = pd.read_csv('rounds2.csv', encoding='ISO-8859-1')
print(rounds_original.iloc[[29597, 31863, 45176, 58473],:])

rawdata= open('rounds2.csv', 'rb').read()
result = chardet.detect(rawdata)
charenc = result['encoding']
print(charenc)
print('Result:', result)

# trying different encodings
# throws an error
# encoding = 'cp1254'
# rounds_original = pd.read_csv('rounds2.csv', encoding='cp1254')
# print(rounds_original.iloc[[29597, 31863, 45176] ,:])

rounds['company_permalink'] = rounds.company_permalink.str.encode('utf-8').str.decode('ascii','ignore')
print(rounds.loc[~rounds['company_permalink'].isin(companies['permalink']), :])

# Look at unique values again
print(len(rounds.company_permalink.unique()))

# companies present in companies df but not in rounds df
print(companies.loc[~companies['permalink'].isin(rounds['company_permalink']), :])

# remove encoding from companies df
companies['permalink'] = companies.permalink.str.encode('utf-8').str.decode('ascii', 'ignore')

# companies present in companies df but not in rounds df
print(companies.loc[~companies['permalink'].isin(rounds['company_permalink']), :])

# write rounds file
rounds.to_csv("rounds_clean.csv", sep=',', index=False)

# write companies file
companies.to_csv("companies_clean.csv", sep='\t', index=False)

# Now that we have treated the encoding problems (caused by special characters). let's complete the data cleaning 
# process by treating missing values.
# We will read the clean csv files we created in th previous exercise














