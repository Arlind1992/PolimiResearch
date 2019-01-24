#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 12:31:53 2019

@author: arlind
"""
from openpyxl import load_workbook
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_market as md
import ai_analysis.automatic_integration.integration_utils as iu
import ai_analysis.sales_data as sd
import ai_analysis.transform_data as td
sales_data=sd.get_sales_data()
market_data=md.get_market_data().drop(columns='Name Type',axis=1).fillna(0)
market_data=market_data.drop(columns='Unnamed: 0')
anagrafica=an.create_anagrafica(2, file='AllData/anagrafica_AI.xlsx')
anagrafica['Material']=anagrafica['Material'].astype(int)
integration=pd.read_csv('AllData/crtSAPIMS.csv',sep=';')
integration_join_anagrafica=anagrafica.merge(integration,how='inner',on='Material')
integration_join_anagrafica=integration_join_anagrafica[integration_join_anagrafica['ECC - Local Product Status']=='40']
material='44058838'
def plot_for_material(material):
    sales_data_filtered=sales_data[sales_data['Material']==material]
    integration_filtered=integration[integration['Material'].astype(str)==material]
    market_data_filtered=market_data[(market_data['Manufacturer']=='SANDOZ') & (market_data['Product']==integration_filtered['Product'].iloc[0])& (market_data['Pack']==integration_filtered['Pack'].iloc[0])]
    ts_sales_data=td.tras_sales_data(sales_data_filtered)
    ts_market_data=td.tras_market_data(market_data_filtered).astype(float)
    ts_sales_data.sort_index().plot(title='Sales')
    ts_market_data.sort_index().apply(lambda x: x*1000).plot(title='Market Data Sandoz')

plot_for_material('44058838')    
