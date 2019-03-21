#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 17:02:49 2019

@author: arlind
"""


import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
import ai_analysis.models.evaluations.evaluate_arima_model as evam
import ai_analysis.models.evaluations.evaluate_prophet_models as evpm
import pandas as pd
import ai_analysis.constans as const
import warnings
import datetime
import multiprocessing
from sklearn.metrics import mean_squared_error
def add_results(material,algorithm,series_name,number_ofdata,metric,metric_value,timestamp):
    dict_to_add=dict()
    dict_to_add['Material']=material
    dict_to_add['Algorithm']=algorithm
    dict_to_add['Series']=series_name
    dict_to_add['Number Of Data']=number_ofdata
    dict_to_add['Metric']=metric
    dict_to_add['Metric Values']=metric_value
    dict_to_add['Timestamp']=timestamp
    return dict_to_add
warnings.filterwarnings("ignore")
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
results=[]
pdq,seasonal_order=evam.get_arima_hyper_parameters()
changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list=evpm.get_hyper_parameter_values() 
timestamp=str(datetime.datetime.now())   
subset_sku=list(integration_data['Material'])
test_window=3
training_percentage=0.7
def calculate_arima(material):
    results_to_return=[]
    ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock,market_percentage=allData.get_dataframes_for_material(str(material))
    inputs=[(ts_market_data_by_molecule,pdq,seasonal_order,mean_squared_error,test_window,training_percentage),(ts_sales_data.iloc[:,0],pdq,seasonal_order,mean_squared_error,test_window,training_percentage),(ts_market_data[ts_market_data.columns[0]],pdq,seasonal_order,mean_squared_error,test_window,training_percentage)]
    toadd_info=[(const.market_comp_sales_IMS,len(ts_market_data_by_molecule)),(const.external_sales_IMS,len(ts_sales_data)),(const.internal_sales_SAP,len(ts_market_data))]
    pool_int=multiprocessing.Pool(3)
    results_int=zip(*pool_int.map(evam.evaluate_arima_models,inputs))
    for index,ri in enumerate(results_int):
        results_to_return.append(add_results(material,const.sarima,toadd_info[index][0],const.sarima,toadd_info[index][1],const.mean_squared,ri,timestamp))
    return results_to_return

pool = multiprocessing.Pool(30)
results_pool=zip(*pool.map(calculate_arima, subset_sku))
for rp in results_pool:
    results.extend(rp)
    
timestamp=str(datetime.datetime.now())     
df_results=pd.DataFrame(results)
df_results.to_csv('HyperparamResultsSARIMA_'+timestamp,sep=';',mode='a')
