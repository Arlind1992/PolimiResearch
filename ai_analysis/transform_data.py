# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:59:48 2019

@author: RUFIAR1
"""
import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, "en_US.UTF-8") 
def tras_finance_data(finance_data):
    finance_data['All Data']=finance_data['Material'].astype('str')+','+finance_data['Fiscal year/period']
    tras_finance_data=finance_data.drop(['Fiscal year/period','Material'],axis=1).set_index('All Data').T
    tras_finance_data.index=pd.to_datetime(tras_finance_data.index,format='%b %Y')
    return tras_finance_data.sort_index()
'''done'''
def tras_market_data_manual(market_data):
    market_data['All Data']=market_data['Molecule']+','+market_data['Manufacturer']+','+market_data['Product']+','+market_data['Pack']+','+market_data['BRAND-INN']+','+market_data["GX-OX"]
    market_data=market_data.drop(columns=['Molecule','Molecule ADJ','Manufacturer','Product','Pack','BRAND-INN','GX-OX'])
    market_data=market_data.set_index("All Data").T
    market_data.index=pd.to_datetime(market_data.index,format='%d/%m/%Y')
    return market_data.sort_index()

'''done'''
def tras_market_data(market_data):
    market_data['All Data']=market_data['Molecule']+','+market_data['Manufacturer']+','+market_data['Product']+','+market_data['Pack']
    market_data=market_data.drop(columns=['Molecule','Manufacturer','Product','Pack'])
    try:
        market_data=market_data.drop(columns=['Anatomical Therapeutic Class 4'])
    except:
        pass
    market_data=market_data.set_index("All Data").T
    market_data.index=pd.to_datetime(market_data.index,format='%d/%m/%Y')
    return market_data.sort_index()

'''done'''
def tras_sales_data_manual(sales_data):
    sales_data['All Data']=sales_data['Product'].astype('str')+','+sales_data['material'].astype('str')+','+ sales_data['CAUSALE']
    sales_data=sales_data.drop(columns=['CAUSALE','NOTE','material','Product','inc IMS','AVG VENDUTO 2018','AVG FCST Q1','%','%','Stock','LF2','LF2 YTG (from JULY)','TOTALE'])
    sales_data=sales_data.set_index("All Data").T
    sales_data.index=pd.to_datetime(sales_data.index,format='%b')
    return sales_data.sort_index()
'''done'''
def tras_transformed_sales_data(transformed_data):
    transformed_data.index=pd.to_datetime(transformed_data.index,format='%b %Y')
    return transformed_data.sort_index()

'''done'''
def tras_sales_data(forecast_data):
    forecast_data['All Data']=forecast_data['Material'].astype('str')
    forecast_data=forecast_data.drop(columns=['Material'])
    forecast_data=forecast_data.set_index("All Data").T
    forecast_data.index=pd.to_datetime(forecast_data.index)
    return forecast_data.sort_index()  

'''done'''
def tras_market_data_probiotici(market_data):
    market_data['All Data']=market_data['Company']+','+market_data['Brand']+','+market_data['Product']
    market_data=market_data.drop(columns=['Company','Brand','Product'])
    market_data=market_data.set_index("All Data").T
    market_data.index=pd.to_datetime(market_data.index,format='%b-%Y')
    return market_data.sort_index()
