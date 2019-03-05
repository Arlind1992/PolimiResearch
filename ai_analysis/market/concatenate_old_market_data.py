#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:30:27 2019

@author: arlind
"""
import ai_analysis.market.data_market as dm
import pandas as pd

'''code to save all merge and save all market data archives and also add to them the latest data'''
df=dm.create_all_old_market_data('Market Data/Ginecologia')

all_data_market=pd.read_csv('AllData/AllDataIMS.csv',sep=';')

all_data_market=all_data_market.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
df_columns=df.columns.values.tolist()
df_columns=df_columns[6:]
for index, row in df.iterrows():
    for column in df_columns:
        print(index)
        all_data_market.loc[(all_data_market['Manufacturer']==row['Manufacturer'])&(all_data_market['Product']==row['Product'])&(all_data_market['Pack']==row['Pack'])&(all_data_market['Molecule']==row['Molecule']),column]=row[column]


all_data_market.to_csv(path_or_buf='Market Data/Ginecology updated.csv',sep=';')

df.to_csv(path_or_buf ='Market Data/AllOldDataGinecologia.csv',sep=';')
