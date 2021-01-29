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
