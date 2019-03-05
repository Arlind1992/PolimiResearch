#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 12:32:08 2019
script to launch the grid search for all the Algorithms and for all SKU gives as output a csv file containing best parameters for each 
series 
@author: arlind
"""

import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
import ai_analysis.models.evaluations.evaluate_arima_model as evam
import ai_analysis.models.evaluations.evaluate_prophet_models as evpm
import pandas as pd
import warnings

def add_results(material,algorithm,best_param,series_name,number_ofdata,metric,metric_value):
    dict_to_add=dict()
    dict_to_add['Material']=material
    dict_to_add['Algorithm']=algorithm
    dict_to_add['Best Param']=best_param
    dict_to_add['Series']=series_name
    dict_to_add['Number Of Data']=number_ofdata
    dict_to_add['Metric']=metric
    dict_to_add['Metric Value']=metric_value
    return dict_to_add
warnings.filterwarnings("ignore")
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
results=[]
pdq,seasonal_order=evam.get_arima_hyper_parameters()
changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list=evpm.get_hyper_parameter_values()    
for material in integration_data['Material']:
    dict_to_add=dict()
    ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock=allData.get_dataframes_for_material(str(material))
    if len(ts_sales_data)<20:
        pass
    '''mse_competitor,param_competitor=evam.evaluate_arima_models(ts_market_data_by_molecule,pdq,seasonal_order)
    results.append(add_results(material,'SARIMA',param_competitor,'Whole market',len(ts_market_data_by_molecule),'MSE',mse_competitor))'''
    mse_competitor,param_competitor=evam.evaluate_arima_models(ts_sales_data.iloc[:,0],pdq,seasonal_order)
    results.append(add_results(material,'SARIMA',param_competitor,'Internal Sales',len(ts_sales_data),'MSE',mse_competitor))
    '''mse_competitor,param_competitor=evam.evaluate_arima_models(ts_market_data[0].iloc[:,0],pdq,seasonal_order)
    results.append(add_results(material,'SARIMA',param_competitor,'Market Sales',len(ts_market_data),'MSE',mse_competitor))   
    mse_competitor,param_competitor=evpm.evaluate_prophet_models(ts_market_data_by_molecule,changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list)
    results.append(add_results(material,'Prophet',param_competitor,'Whole market',len(ts_market_data_by_molecule),'MSE',mse_competitor))
    mse_competitor,param_competitor=evpm.evaluate_prophet_models(ts_sales_data.iloc[:,0],changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list)
    results.append(add_results(material,'Prophet',param_competitor,'Internal Sales',len(ts_sales_data),'MSE',mse_competitor))
    mse_competitor,param_competitor=evpm.evaluate_prophet_models(ts_market_data[0].iloc[:,0],changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list)
    results.append(add_results(material,'Prophet',param_competitor,'Market Sales',len(ts_market_data),'MSE',mse_competitor))
    '''

df_results=pd.DataFrame(results)
df_results.to_csv('Results',sep=';')