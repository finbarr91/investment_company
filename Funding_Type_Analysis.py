
"""Funding Type Analysis
Let's compare the funding amounts across the funding types. Also, we need to impose the constraint that the investment amount should be between 5 and 15 million USD. ' \
We will choose the funding type such that the average investment amount falls in this range"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("master_df.csv", sep=",", encoding="ISO-8859-1")
print(df.head())
# first, let's filter the df so it only contains the four specified funding types
df = df[(df.funding_round_type == "venture") |
        (df.funding_round_type == "angel") |
        (df.funding_round_type == "seed") |
        (df.funding_round_type == "private_equity") ]
print(df.columns)
print(df.head(10))

# distribution of raised_amount_usd
sns.boxplot(y=df['raised_amount_usd'])
plt.yscale('log')
plt.show()

# summary metrics
df['raised_amount_usd'].describe()

# comparing summary stats across four categories
sns.boxplot(x='funding_round_type', y='raised_amount_usd', data=df)
plt.yscale('log')
plt.show()

# compare the mean and median values across categories
print(df.pivot_table(values='raised_amount_usd', columns='funding_round_type', aggfunc=[np.median, np.mean]))

# compare the median investment amount across the types
df.groupby('funding_round_type')['raised_amount_usd'].median().sort_values(ascending=False)

# filter the df for private equity type investments
df = df[df.funding_round_type=="venture"]

"""Country Analysis
Let's now compare the total investment amounts across countries. 
Note that we'll filter the data for only the 'venture' type investments 
and then compare the 'total investment' across countries."""
# group by country codes and compare the total funding amounts
country_wise_total = df.groupby('country_code')['raised_amount_usd'].sum().sort_values(ascending=False)
print(country_wise_total)

# top 9 countries
top_9_countries = country_wise_total[:9]
print(top_9_countries)

# filtering for the top three countries
df = df[(df.country_code=='USA') | (df.country_code=='GBR') | (df.country_code=='IND')]
print(df.head())

# filtered df has about 38800 observations
print(df.info())

# boxplot to see distributions of funding amount across countries
plt.figure(figsize=(10, 10))
sns.boxplot(x='country_code', y='raised_amount_usd', data=df)
plt.yscale('log')
plt.show()

"""Sector Analysis
First, we need to extract the main sector using the column category_list. The category_list column contains values such as 'Biotechnology|Health Care' - in this, 'Biotechnology' is the 'main category' of the company, which we need to use.

Let's extract the main categories in a new column."""

# extracting the main category
df.loc[:, 'main_category'] = df['category_list'].apply(lambda x: x.split("|")[0])
print(df.head())

# drop the category_list column
df = df.drop('category_list', axis=1)
print(df.head())

# read mapping file
mapping = pd.read_csv("mapping.csv", sep=",")
print(mapping.head())

# missing values in mapping file
print(mapping.isnull().sum())

# remove the row with missing values
mapping = mapping[~pd.isnull(mapping['category_list'])]
print(mapping.isnull().sum())

# Now, since we need to merge the mapping file with the main dataframe (df),
# let's convert the common column to lowercase in both.

# converting common columns to lowercase
mapping['category_list'] = mapping['category_list'].str.lower()
df['main_category'] = df['main_category'].str.lower()

# look at heads
print(mapping.head())

print(df.head())

# Let's have a look at the category_list column of the mapping file.
# These values will be used to merge with the main df.

print(mapping['category_list'])

"""
To be able to merge all the main_category values with the mapping file's category_list column, all the values in the main_category column should be present in the category_list column of the mapping file.

Let's see if this is true.
"""

# values in main_category column in df which are not in the category_list column in mapping file
print(df[~df['main_category'].isin(mapping['category_list'])])

# values in the category_list column which are not in main_category column
print(mapping[~mapping['category_list'].isin(df['main_category'])])

"""If you see carefully, you'll notice something fishy - there are sectors named alter0tive medicine, a0lytics, waste ma0gement, veteri0ry, etc. This is not a random quality issue, but rather a pattern. In some strings, the 'na' has been replaced by '0'. This is weird - maybe someone was trying to replace the 'NA' values with '0', and ended up doing this.

Let's treat this problem by replacing '0' with 'na' in the category_list column."""
# replacing '0' with 'na'
mapping['category_list'] = mapping['category_list'].apply(lambda x: x.replace('0', 'na'))
print(mapping['category_list'])

# merge the dfs
df = pd.merge(df, mapping, how='inner', left_on='main_category', right_on='category_list')
print(df.head())

# let's drop the category_list column since it is the same as main_category
df = df.drop('category_list', axis=1)
print(df.head())

# look at the column types and names
print(df.info())

# store the value and id variables in two separate arrays

# store the value variables in one Series
value_vars = df.columns[9:18]

# take the setdiff() to get the rest of the variables
id_vars = np.setdiff1d(df.columns, value_vars)

print(value_vars, "\n")
print(id_vars)

# convert into long
long_df = pd.melt(df,
        id_vars=list(id_vars),
        value_vars=list(value_vars))

print(long_df.head())

# remove rows having value=0
long_df = long_df[long_df['value']==1]
long_df = long_df.drop('value', axis=1)

# look at the new df
print(long_df.head())
print(len(long_df))

# renaming the 'variable' column
long_df = long_df.rename(columns={'variable': 'sector'})
# info
print(long_df.info())

"""
The dataframe now contains only venture type investments in countries USA, IND and GBR, and we have mapped each company to one of the eight main sectors (named 'sector' in the dataframe).

We can now compute the sector-wise number and the amount of investment in the three countries.
"""

# summarising the sector-wise number and sum of venture investments across three countries

# first, let's also filter for investment range between 5 and 15m
df = long_df[(long_df['raised_amount_usd'] >= 5000000) & (long_df['raised_amount_usd'] <= 15000000)]

# groupby country, sector and compute the count and sum
df.groupby(['country_code', 'sector']).raised_amount_usd.agg(['count', 'sum'])

# plotting sector-wise count and sum of investments in the three countries
plt.figure(figsize=(16, 14))

plt.subplot(2, 1, 1)
p = sns.barplot(x='sector', y='raised_amount_usd', hue='country_code', data=df, estimator=np.sum)
p.set_xticklabels(p.get_xticklabels(),rotation=30)
plt.title('Total Invested Amount (USD)')
plt.tight_layout()

plt.subplot(2, 1, 2)
q = sns.countplot(x='sector', hue='country_code', data=df)
q.set_xticklabels(q.get_xticklabels(),rotation=30)
plt.title('Number of Investments')
plt.tight_layout()
plt.show()


