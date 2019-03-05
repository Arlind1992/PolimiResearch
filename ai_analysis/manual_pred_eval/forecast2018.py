#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:57:43 2019

@author: arlind
"""

import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
import ai_analysis.models.arima_models as am
import ai_analysis.models.prophet_models as pm
import pandas as pd
import warnings
from ast import literal_eval as make_tuple

evaluation_results=ldl.load_evaluation_results()
internal_results=evaluation_results[(evaluation_results['Series']=='Internal Sales')&(evaluation_results['Metric Value'].astype(str)!='inf')]
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
allForecasts=pd.DataFrame()
for material in internal_results['Material']:
    s_params_SARIMA=internal_results[(internal_results['Material'].astype(str)==str(material))&(internal_results['Algorithm']=='SARIMA')]['Best Param'].iloc[0]
    params_SARIMA=make_tuple(s_params_SARIMA)
    ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock=allData.get_dataframes_for_material(str(material))
    if len(ts_sales_data) <20:
        pass
    train=ts_sales_data[:-12]    
    test=ts_sales_data[-12:]
    forecast=am.model_df(train,arima_order=params_SARIMA[0],seasonal_order=params_SARIMA[1])
    traslated=forecast.to_frame().T
    traslated['Material']=material
    traslated['Type']='Forecast'
    allForecasts=allForecasts.append(traslated)
    traslated_test=test.T
    traslated_test['Material']=material
    traslated_test['Type']='Actual'
    allForecasts=allForecasts.append(traslated_test)

allForecasts.to_csv('ARIMA_FORECASTS.csv',sep=';')
