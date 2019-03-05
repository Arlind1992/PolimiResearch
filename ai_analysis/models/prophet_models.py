#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:17:53 2019

@author: arlind
"""

import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
from sklearn.model_selection import TimeSeriesSplit as tss
import numpy
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
'''
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
material=
fourier order =10 : 25
'''

def model_material(material,allData,show_components=False):
    market_data_by_competitor,sales_data,market_data,stock=allData.get_dataframes_for_material(material)
    int_sales_forecast=model_internal_sales(sales_data,show_components)  
    ext_sales_forecast=model_external_sales(market_data,show_components)
    competitor_sales_forecast=model_market_by_competitor(market_data_by_competitor,show_components)
    return int_sales_forecast,ext_sales_forecast,competitor_sales_forecast

def model_internal_sales(sales_data,show_compontents=False):
    try:
        sales_data=sales_data.drop(sales_data.columns[1],axis=1)
    except:
        pass
    sales_data=sales_data.rename(columns={sales_data.columns[0]:'y'})
    sales_data['ds']=sales_data.index
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(sales_data)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'SAP Sales')
    return forecast

def model_external_sales(market_data,show_compontents=False):
    market_data=market_data.rename(columns={market_data.columns[0]:'y'})
    market_data['ds']=market_data.index
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(market_data)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'External Sales')
    return forecast


def model_market_by_competitor(market_data_by_competitor,show_compontents=False):
    try:
        market_data_by_competitor=market_data_by_competitor.to_frame()
    except:
        pass
    market_data_by_competitor=market_data_by_competitor.rename(columns={market_data_by_competitor.columns[0]:'y'})
    market_data_by_competitor['ds']=market_data_by_competitor.index
    m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
    m.fit(market_data_by_competitor)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    if show_compontents:
        plot_forecast(forecast,m,'Whole market')
    return forecast

def plot_forecast(forecast,prophet,title):
    prophet.plot(forecast,xlabel=title)
    prophet.plot_components(forecast)
    