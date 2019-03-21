#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:15:13 2019

@author: arlind
"""


import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl

import ai_analysis.models.evaluations.evaluate_prophet_models as epm
import ai_analysis.models.prophet_models as pm
import pandas as pd
from ast import literal_eval as make_tuple
import ai_analysis.constans as const
import ai_analysis.models.combination_helpers as ch

evaluation_results=ldl.load_evaluation_results()
internal_results=evaluation_results[(evaluation_results['Series']==const.internal_sales_SAP)&(evaluation_results['Metric Value'].astype(str)!='inf')]
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
allForecasts=pd.DataFrame()
subset=[44070378,44070396,44070376,999144,44001187,982475,44038591,999145,44000736]
timewindow=6
for material in subset:
    ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock,market_percentage=allData.get_dataframes_for_material(str(material))
    if len(ts_sales_data) <20:
        continue
    fourier_order_int,changepoint_prior_scale_int,seasonality_prior_scale_int=epm.get_best_param_from_results(material,const.internal_sales_SAP)
    fourier_order_ext,changepoint_prior_scale_ext,seasonality_prior_scale_ext=epm.get_best_param_from_results(material,const.external_sales_IMS)
    fourier_order_comp,changepoint_prior_scale_comp,seasonality_prior_scale_comp=epm.get_best_param_from_results(material,const.market_comp_sales_IMS)
    test=ts_sales_data[-12:]
    forecast=pd.Series()
    for i in range(0,13-timewindow):    
        if i==0:
            int_sales_forecast=pm.model_internal_sales(ts_sales_data[:-12],material)  
            '''ext_sales_forecast,conf_interval_ext_sales=pm.model_external_sales(ts_market_data[:-12],fourier_order=fourier_order_ext,changepoint_prior_scale=changepoint_prior_scale_ext,seasonality_prior_scale=seasonality_prior_scale_ext,title='Sales IMS',ims=True)
            competitor_sales_forecast,conf_interval_competitor=pm.model_market_by_competitor(ts_market_data_by_molecule.to_frame()[:-12],fourier_order=fourier_order_comp,changepoint_prior_scale=changepoint_prior_scale_comp,seasonality_prior_scale=seasonality_prior_scale_comp,title='Sales Whole Market',ims=True)
            weights=ch.get_best_weights(str(material),const.sarima)
            mean_percentage=market_percentage[-6:].mean()'''
            '''
            to_append=ch.int_sales_by_combination(int_sales_forecast[:3],conf_interval_int_sales[:3],ext_sales_forecast[:3],conf_interval_ext_sales[:3],competitor_sales_forecast[:3],conf_interval_competitor[:3],market_percentage)
            forecast=forecast.append(weights[0]*int_sales_forecast[:3]+weights[1]*ext_sales_forecast[:3]+weights[2]*competitor_sales_forecast[:3]*mean_percentage)'''
            int_sales_forecast.index=int_sales_forecast['ds']
            to_append=int_sales_forecast['yhat'][-12:][:-12+timewindow]
            forecast=forecast.append(to_append)
        else:
            int_sales_forecast=pm.model_internal_sales(ts_sales_data[:-12+i],material)  
            '''ext_sales_forecast,conf_interval_ext_sales=pm.model_external_sales(ts_market_data[:-12+i],fourier_order=fourier_order_ext,changepoint_prior_scale=changepoint_prior_scale_ext,seasonality_prior_scale=seasonality_prior_scale_ext,title='Sales IMS',ims=True)
            competitor_sales_forecast,conf_interval_competitor=pm.model_market_by_competitor(ts_market_data_by_molecule.to_frame()[:-12+i],material,title='Sales Whole Market',ims=True)
            weights=ch.get_best_weights(str(material),const.sarima)
            mean_percentage=market_percentage[-6:].mean()'''
            '''
            to_append=(weights[0]*int_sales_forecast[2]+weights[1]*ext_sales_forecast[2]+weights[2]*competitor_sales_forecast[2]*mean_percentage)
            '''
            int_sales_forecast.index=int_sales_forecast['ds']
            to_append=(int_sales_forecast['yhat'].iloc[-13+timewindow])
            
            to_append=pd.Series([to_append])
            to_append.index=[int_sales_forecast.index[-13+timewindow]]
            '''
            to_append=ch.int_sales_by_combination(int_sales_forecast[2],conf_interval_int_sales.iloc[2].to_frame().T,ext_sales_forecast[2],conf_interval_ext_sales.iloc[2].to_frame().T,competitor_sales_forecast[2],conf_interval_competitor.iloc[2].to_frame().T,market_percentage)
            '''
            forecast=forecast.append(to_append)
    traslated=forecast.to_frame().T
    traslated['Material']=material
    traslated['Type']='Forecast'
    allForecasts=allForecasts.append(traslated)
    '''traslated_test=test.T
    traslated_test['Material']=material
    traslated_test['Type']='Actual
    allForecasts=allForecasts.append(traslated_test)'''

allForecasts.to_csv('Prophet6monthrolling.csv',sep=';',decimal=',',float_format='%.2f')