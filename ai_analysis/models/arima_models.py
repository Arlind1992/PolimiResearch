#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:59:28 2019

@author: arlind
"""
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt


def model_material(material,allData,arima_order=(2, 1, 2),seasonal_order=(0,0,0,12),show_components=False):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(material)
    int_sales_forecast,conf_interval_int_sales=model_df(sales_data,show_components,arima_order=arima_order,seasonal_order=seasonal_order,title='Sales SAP')  
    ext_sales_forecast,conf_interval_ext_sales=model_df(market_data,show_components,title='Sales IMS')
    competitor_sales_forecast,conf_interval_competitor=model_df(market_data_by_competitor.to_frame(),show_components,title='Sales Whole Market')
    return int_sales_forecast,ext_sales_forecast,competitor_sales_forecast

def model_df(df,show_components=False,arima_order=(2, 1, 2),seasonal_order=(0,0,0,12),title=''):
    try:
        df=df.drop(df.columns[1],axis=1)
    except:
        pass
    model = SARIMAX(df, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
    model_fit = model.fit(disp=0)
    results=model_fit.get_forecast(12)
    predictions=results.predicted_mean
    conf_interval=results.conf_int()
    if show_components:
        plot_data(df,model_fit,title)
    return predictions,conf_interval
    
def plot_data(df,model_fit,title):
    result=model_fit.get_forecast(12)
    predictions=result.predicted_mean
    conf_interval=result.conf_int()
    fitted_values=model_fit.fittedvalues.append(predictions).to_frame()
    fig, ax = plt.subplots(figsize=(10,4))
    df.plot(ax=ax, label='Observations')
    fitted_values.plot(ax=ax, label='SARIMA')
    ax.set_title(title)
    ax.fill_between( conf_interval.index,conf_interval.iloc[:, 0], conf_interval.iloc[:, 1], alpha=0.1)



    
