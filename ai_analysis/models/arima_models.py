#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:59:28 2019

@author: arlind
"""
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import ai_analysis.models.combination_helpers as ch
import ai_analysis.models.evaluations.evaluate_arima_model as eam
import ai_analysis.constans as const
def model_material(material,allData,show_components=False):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(material)    
    arima_order_int,seasonal_order_int=eam.get_best_param_from_results(material,const.internal_sales_SAP)
    arima_order_ext,seasonal_order_ext=eam.get_best_param_from_results(material,const.external_sales_IMS)
    arima_order_comp,seasonal_order_comp=eam.get_best_param_from_results(material,const.market_comp_sales_IMS)
    
    int_sales_forecast,conf_interval_int_sales=model_df(sales_data,show_components=show_components,arima_order=arima_order_int,seasonal_order=seasonal_order_int,title='Sales SAP')  
    ext_sales_forecast,conf_interval_ext_sales=model_df(market_data,show_components=show_components,arima_order=arima_order_ext,seasonal_order=seasonal_order_ext,title='Sales IMS',ims=True)
    competitor_sales_forecast,conf_interval_competitor=model_df(market_data_by_competitor.to_frame(),show_components=show_components,arima_order=arima_order_comp,seasonal_order=seasonal_order_comp,title='Sales Whole Market',ims=True)
    int_sales_by_comb=ch.int_sales_by_combination(int_sales_forecast,conf_interval_int_sales,ext_sales_forecast,conf_interval_ext_sales,competitor_sales_forecast,conf_interval_competitor,market_percentage)
    if show_components:
        plot_combined_data(sales_data[sales_data.columns[0]],int_sales_by_comb,'Combined prediction')
    return int_sales_forecast,ext_sales_forecast,competitor_sales_forecast,int_sales_by_comb

def model_df(df,show_components=False,arima_order=(2, 1, 2),seasonal_order=(0,0,0,12),title='',ims=False):
    try:
        df=df.drop(df.columns[1],axis=1)
    except:
        pass
    model = SARIMAX(df, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
    model_fit = model.fit(disp=0)
    results=model_fit.get_forecast(13)
    predictions=results.predicted_mean
    conf_interval=results.conf_int()
    if ims:
        predictions=predictions[-12:]
        conf_interval=conf_interval[-12:]
    else:
        predictions=predictions[:-1]
        conf_interval=conf_interval[:-1]
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
    
def plot_combined_data(df,results,title):
    fitted_values=df.append(results).to_frame()
    fig, ax = plt.subplots(figsize=(10,4))
    fitted_values.plot(ax=ax, label='SARIMA')
    ax.set_title(title)
    
    
