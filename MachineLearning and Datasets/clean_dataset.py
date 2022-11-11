import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# LIMIT QUANTILE FOR OUTLITERS
def outliers(df, column):  
    # Defining outliters
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    higher_bound = Q3 + 1.5 * IQR

    ls = data.index[(data[column] < lower_bound) | (data[column] > higher_bound)]
    
    return ls

def variants(df, x, y):
    # Defining data affected by covid 19 variants (Delta, Omicron)
    positivityStart = 0.01
    positivityEnd = 0.045
    casesLimit = 750
    
    index_name = df.index[(df[y] > casesLimit) & ((df[x] > positivityStart) & (df[x] < positivityEnd))]
    ls = sorted(set(index_name))
    df = df.drop(ls)
    return df

def remove_outliers(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df

#### LOAD DATA ####
data = pd.read_csv('covid19_toClean.csv', sep = ',')
data = data[['Daily New Cases', 'Positivity Rate']]

#### Drops the empty entries and remove variant (omicorn and delta) & outliers ####
data = data.dropna()
data = variants(data, 'Positivity Rate', 'Daily New Cases')
outliers_list = []
outliers_list.extend(outliers(data, 'Daily New Cases'))
data = remove_outliers(data, outliers_list)

#### Saving Data ####
data.to_csv('covid19_clean.csv', index=False)