# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 18:15:55 2018

@author: RUFIAR1
"""
import ai_analysis.plot_data as plot_data
import ai_analysis.manual_integration.create_data as cd
import ai_analysis.transform_data as td
import ai_analysis.anagrafica as an
from openpyxl import load_workbook
from statsmodels.tsa.arima_model import ARIMA

import numpy as np
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot

def manual_integration(sheet_ranges):
    anagrafica=an.create_anagrafica()
    forcast=cd.create_forecast(sheet_ranges,4)
    market_data=cd.create_market_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Market Data')),int(cd.get_row_number(sheet_ranges,'Sales')))
    sales_data=cd.create_sales_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Sales')),int(cd.get_row_number(sheet_ranges,'Finance')))
    finance_data=cd.create_finance_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Finance')),int(cd.get_row_number(sheet_ranges,'Finance'))+3)  
    td_market_data=td.tras_market_data(market_data)
    td_sales_data=td.tras_sales_data(sales_data)
    td_finance_data=td.tras_finance_data(finance_data)
    plot_data.plot_forecast_data(forcast)
    plot_data.plot_market_data(market_data)
    plot_data.plot_finance_data(finance_data)
    plot_data.plot_sales_data(sales_data)
    plot_data.plot_transformed_sales_data(cd.transform_sales_data(sales_data))

sales_data['All Data']=sales_data['Product'].astype('str')+','+sales_data['material'].astype('str')+','+ sales_data['CAUSALE']
sales_data=sales_data.drop(columns=['CAUSALE','NOTE','material','Product','inc IMS','AVG VENDUTO 2018','AVG FCST Q1','%','%','Stock','LF2','LF2 YTG (from JULY)','TOTALE'])
sales_data=sales_data.set_index("All Data").T

sales_dict=sales_data.to_dict()
tras=cd.transform_sales_data(sales_data)
plot_data.plot_transformed_sales_data(tras)
sales_data.rows


wb = load_workbook(filename = 'ai_analysis/ManualIntegration.xlsx')
sheet_ranges = wb['BUSETTE 10MCG H 4TTSM IT']
anag=cd.create_anagrafica(sheet_ranges,1)
manual_integration(wb['ZIPRASIDONE SDZ 20MG 56HGC V1'])    
manual_integration(wb['RAMIPRIL HCT HEX 5 25MG 14TAB'])
manual_integration(wb['BISOPROLOLO SDZ 5MG 28FCT V1 IT'])
manual_integration(wb['ALPRAZOLAM SDZ 1MG 20TAB IT'])
manual_integration(wb['ACETILCISTEIN HEX 300MG 3ML V1'])
manual_integration(wb['AMLODIPINA SDZ 5MG 28TAB V1 IT'])
manual_integration(wb['BUSETTE 10MCG H 4TTSM IT'])  
manual_integration(wb['LANSOPRAZOLO SDZ 15MG 14GRC V1'])