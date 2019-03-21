#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:17:53 2019

@author: arlind
"""

import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
from sklearn.model_selection import TimeSeriesSplit as tss
import ai_analysis.models.combination_helpers as ch
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
import ai_analysis.models.evaluations.evaluate_prophet_models as epm
import ai_analysis.constans as const

def model_material(material,allData,show_components=False):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(material)
    int_sales_forecast=model_internal_sales(sales_data,material,show_components)  
    ext_sales_forecast=model_external_sales(market_data,material,show_components)
    competitor_sales_forecast=model_market_by_competitor(market_data_by_competitor,material,show_components)
    int_sales_forecast.index=int_sales_forecast['ds']
    ext_sales_forecast.index=ext_sales_forecast['ds']
    competitor_sales_forecast.index=competitor_sales_forecast['ds']
    combined_int_sales=ch.int_sales_by_combination(int_sales_forecast['yhat'][-12:],__trasform_forecast_conf_int(int_sales_forecast),ext_sales_forecast['yhat'][-12:],__trasform_forecast_conf_int(ext_sales_forecast),competitor_sales_forecast['yhat'][-12:],__trasform_forecast_conf_int(competitor_sales_forecast),market_percentage)
    if show_components:
        sales_data[sales_data.columns[0]].append(combined_int_sales).plot()
    return int_sales_forecast,ext_sales_forecast,competitor_sales_forecast,combined_int_sales

def __trasform_forecast_conf_int(forecast_result):
    to_return=forecast_result[['ds','yhat_lower','yhat_upper']][-12:]
    to_return.index=to_return['ds']
    to_return=to_return.drop(columns='ds')
    return to_return

def model_internal_sales(sales_data,material,show_compontents=False):
    try:
        sales_data=sales_data.drop(sales_data.columns[1],axis=1)
    except:
        pass
    fourier_order,changepoint_prior_scale,seasonality_prior_scale=epm.get_best_param_from_results(material,const.prophet)
    sales_data=sales_data.rename(columns={sales_data.columns[0]:'y'})
    sales_data['ds']=sales_data.index
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(sales_data)
    future = m.make_future_dataframe(periods=12,freq='MS')
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'SAP Sales')
    return forecast

def model_external_sales(market_data,material,show_compontents=False):
    market_data=market_data.rename(columns={market_data.columns[0]:'y'})
    market_data['ds']=market_data.index
    
    fourier_order,changepoint_prior_scale,seasonality_prior_scale=epm.get_best_param_from_results(material,const.prophet)
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(market_data)
    future = m.make_future_dataframe(periods=13,freq='MS')
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'External Sales')
    return forecast


def model_market_by_competitor(market_data_by_competitor,material,show_compontents=False):
    try:
        market_data_by_competitor=market_data_by_competitor.to_frame()
    except:
        pass
    market_data_by_competitor=market_data_by_competitor.rename(columns={market_data_by_competitor.columns[0]:'y'})
    market_data_by_competitor['ds']=market_data_by_competitor.index
    fourier_order,changepoint_prior_scale,seasonality_prior_scale=epm.get_best_param_from_results(material,const.prophet)
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(market_data_by_competitor)
    future = m.make_future_dataframe(periods=13,freq='MS')
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'Whole market')
    return forecast

def plot_forecast(forecast,prophet,title):
    prophet.plot(forecast,xlabel=title)
    
