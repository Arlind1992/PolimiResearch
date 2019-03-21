#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:39:54 2019

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
warnings.filterwarnings("ignore")
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
 
timestamp=str(datetime.datetime.now())   
subset_sku=list(integration_data['Material'])

results_weights=[]

for material in subset_sku:
    results_weights.append({'Material':material,'Best Weights':evam.calculate_weights(allData,str(material)),'Model':const.sarima})
    results_weights.append({'Material':material,'Best Weights':evpm.calculate_weights(allData,str(material)),'Model':const.prophet})

pd.DataFrame(results_weights).to_csv('ResultsWeights',sep=';',mode='a')