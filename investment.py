import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


