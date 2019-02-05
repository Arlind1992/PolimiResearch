# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 14:35:44 2018

@author: RUFIAR1
"""
import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, "en_US.UTF-8") 

def plot_finance_data(finance_data):
    finance_data['All Data']=finance_data['Material'].astype('str')+','+finance_data['Fiscal year/period']
    tras_finance_data=finance_data.drop(['Fiscal year/period','Material'],axis=1).set_index('All Data').T
    tras_finance_data.index=pd.to_datetime(tras_finance_data.index,format='%b %Y')
    tras_finance_data=tras_finance_data.sort_index()
    tras_finance_data.plot.line(title='Finance data')
'''done'''
def plot_market_data(market_data):
    market_data['All Data']=market_data['Molecule']+','+market_data['Manufacturer']+','+market_data['Product']+','+market_data['Pack']
    market_data=market_data.drop(columns=['Molecule','Manufacturer','Product','Pack'])
    market_data=market_data.set_index("All Data").T
    market_data.index=pd.to_datetime(market_data.index,format='%d/%m/%Y')
    market_data=market_data.sort_index()
    market_data.sort_index().plot.line(title='Market data',subplots=True)
'''done'''
def plot_sales_data(sales_data):
    sales_data['All Data']=sales_data['Product'].astype('str')+','+sales_data['material'].astype('str')+','+ sales_data['CAUSALE']
    sales_data=sales_data.drop(columns=['CAUSALE','NOTE','material','Product','inc IMS','AVG VENDUTO 2018','AVG FCST Q1','%','%','Stock','LF2','LF2 YTG (from JULY)','TOTALE'])
    sales_data=sales_data.set_index("All Data").T
    sales_data.index=pd.to_datetime(sales_data.index,format='%b')
    sales_data.sort_index().plot.line(title='Sales data')
    
def plot_transformed_sales_data(transformed_data):
    transformed_data.index=pd.to_datetime(transformed_data.index,format='%b %Y')
    transformed_data.sort_index().plot.line(title='Sales data transformed')

'''done'''
def plot_forecast_data(forecast_data):
    forecast_data['All Data']=forecast_data['Material'].astype('str')
    forecast_data=forecast_data.drop(columns=['Material'])
    forecast_data=forecast_data.set_index("All Data").T
    forecast_data.index=pd.to_datetime(forecast_data.index)
    forecast_data.sort_index().plot.line(title='Forecast data')  