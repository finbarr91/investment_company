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

# summary stats of raised_amount_usd
print(master['raised_amount_usd'].describe())

"""
The mean is somewhere around USD 10 million, while the median is only about USD 1m. The min and max values are also miles apart.

In general, since there is a huge spread in the funding amounts, it will be inappropriate to impute it with a metric such as median or mean. Also, since we have quite a large number of observations, it is wiser to just drop the rows.

Let's thus remove the rows having NaNs in raised_amount_usd.
"""

# removing NaNs in raised_amount_usd
master = master[~np.isnan(master['raised_amount_usd'])]
print(round(100*(master.isnull().sum()/len(master.index)), 2))

# Let's now look at the column country_code. To see the distribution of the values for categorical variables, ' \
# it is best to convert them into type 'category'.

country_codes = master['country_code'].astype('category')
print(country_codes)
# displaying frequencies of each category
print(country_codes.value_counts())

"""
By far, the most number of investments have happened in American countries. 
We can also see the fractions.
"""
# viewing fractions of counts of country_codes
print(100*(master['country_code'].value_counts()/len(master.index)))

"""
Now, we can either delete the rows having country_code missing (about 6% rows), or we can impute them by USA. Since the number 6 is quite small, and we have a decent amount of data, it may be better to just remove the rows.

Note that np.isnan does not work with arrays of type 'object', it only works with native numpy type (float). Thus, you can use pd.isnull() instead.

"""

# removing rows with missing country_codes
master = master[~pd.isnull(master['country_code'])]

# look at missing values
round(100*(master.isnull().sum()/len(master.index)), 2)

"""
Note that the fraction of missing values in the remaining dataframe has also reduced now - only 0.65% in category_list. Let's thus remove those as well.
Note Optionally, you could have simply let the missing values in the dataset and continued the analysis. There is nothing wrong with that. But in this case, since we will use that column later for merging with the 'main_categories', removing the missing values will be quite convenient (and again - we have enough data).
"""

# removing rows with missing category_list values
master = master[~pd.isnull(master['category_list'])]
# look at missing values
print(round(100*(master.isnull().sum()/len(master.index)), 2))

# writing the clean dataframe to an another file
master.to_csv("master_df.csv", sep=',', index=False)

# look at the master df info for number of rows etc.
master.info()

# after missing value treatment, approx 77% observations are retained
100*(len(master.index) / len(rounds.index))


