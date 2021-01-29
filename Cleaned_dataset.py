import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#  read the new, decoded csv file
rounds = pd.read_csv('rounds_clean.csv', encoding='ISO-8859-1')
companies = pd.read_csv('companies_clean.csv', sep = '\t', encoding='ISO-8859-1')

# quickly verify that there are 66368 unique companies in both.
# and only the same 66368 are present in both files

# unique values
print(len(companies.permalink.unique()))
print(len(rounds.company_permalink.unique()))

# present in rounds but not in companies
print(len(rounds.loc[~rounds['company_permalink'].isin(companies['permalink']),:]))

# Missing value treatment
# Missing values in the companies df
print(companies.isnull().sum())

# missing values in rounds df
print(rounds.isnull().sum())

"""
Since there are no missing values in the permalink or company_permalink columns, let's merge the two and then 
work on the master dataframe
"""

#merging the two dfs
master = pd.merge(companies, rounds, how = 'inner', left_on= 'permalink', right_on= 'company_permalink')
print('Master dataset:',master.head(9))

# Since the columns company_permalink and permalink are the same, let's remove one of them.

print(master.columns) # Looking at the dataset columns

master = master.drop(['company_permalink'], axis=1) # Dropping the redundant column

print(master.columns)
# Let's look at the number of missing values in the master dataframe
print('\n The null values in your dataset:', master.isnull().sum(),'\n')

# Let's look at the fraction of missing values in the columns.
# summing up the missing values(column-wise) and displaying the fractions of NaNs.
print(round(100*(master.isnull().sum()/len(master.index)), 2))

"""
Clearly, the column funding_round_code is useless (with about 73% missing values). Also, for the business objectives given, the columns homepage_url, founded_at, state_code, region and city need not be used.

Thus, let's drop these columns.
"""
# dropping columns
master = master.drop(['funding_round_code', 'homepage_url', 'founded_at', 'state_code', 'region', 'city'], axis=1)
print(master.head())

# summing up the missing values (column-wise) and displaying fraction of NaNs
print(round(100*(master.isnull().sum()/len(master.index)), 2))

"""
Note that the column raised_amount_usd is an important column, since that is the number we want to analyse (compare, means, sum etc.). That needs to be carefully treated.

Also, the column country_code will be used for country-wise analysis, and category_list will be used to merge the dataframe with the main categories.

Let's first see how we can deal with missing values in raised_amount_usd.
"""