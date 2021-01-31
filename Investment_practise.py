import pandas as pd
import math
import dis
dataframe = pd.DataFrame({ 'column_1' : [1,2,3,4,5,6],
                           'column_2' : ['this', 'column', 'contains', 'strings', 'in', 'it'],
                           'float_column': [1.00,2.00,3.00,4.00,5.00,6.03],
                           'boolean_column' :[True, False, True, False, True, False]

})

dataframe2 = pd.DataFrame({'siblings': ['Chisom', 'KC', 'Afoma', 'Muoma', 'Ogooo']})

dataframe3 = pd.concat([dataframe,dataframe2],axis=1)

print(dataframe3.head(6))
print(dataframe3.isnull().sum())

print(dataframe3[~pd.isnull(dataframe3['siblings'])])

set = {1,1,3,4,'Oge','Ifeoma',22,90,677}
print(set)
def f1():
    return list()


def f2():
    return []

print(dis.dis(f1))

print(dis.dis(f2))