# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 18:15:55 2018

@author: RUFIAR1
"""
import ai_analysis.plot_data as plot_data
import ai_analysis.manual_integration.create_data as cd
import ai_analysis.transform_data as td

from openpyxl import load_workbook
from statsmodels.tsa.arima_model import ARIMA
import locale
locale.setlocale(locale.LC_TIME, "en_US.UTF-8") 
import numpy as np
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
''''''
def manual_integration(sheet_ranges):
    forcast=cd.create_forecast(sheet_ranges,4)
    market_data=cd.create_market_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Market Data')),int(cd.get_row_number(sheet_ranges,'Sales')))
    sales_data=cd.create_sales_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Sales')),int(cd.get_row_number(sheet_ranges,'Finance')))
    finance_data=cd.create_finance_data(sheet_ranges,int(cd.get_row_number(sheet_ranges,'Finance')),int(cd.get_row_number(sheet_ranges,'Finance'))+3)  
    td_market_data=td.tras_market_data(market_data)
    td_finance_data=td.tras_finance_data(finance_data)
    all_market=td_market_data.agg("sum", axis="columns")
    all_market.plot.line(title='All Market data')
    plot_data.plot_forecast_data(forcast)
    plot_data.plot_finance_data(finance_data)
    plot_data.plot_sales_data(sales_data)
    

wb = load_workbook(filename = 'ai_analysis/ManualIntegration.xlsx')
sheet_ranges = wb['LANSOPRAZOLO SDZ 15MG 14GRC V1']
anag=cd.create_anagrafica(sheet_ranges,1)
manual_integration(wb['LANSOPRAZOLO SDZ 15MG 14GRC V1'])