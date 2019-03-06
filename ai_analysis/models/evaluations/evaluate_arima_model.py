#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:11:30 2019

@author: arlind
"""

import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.model_selection import TimeSeriesSplit as tss
from sklearn.metrics import mean_squared_error
import numpy
import ai_analysis.data_loading.load_data_locally as ldl
from ast import literal_eval as make_tuple

def evaluate_model(X, arima_order,seasonal_order,number_of_splits=5,test_window=12,metric_func=mean_squared_error):
    error=0
    for train_index, test_index in tss(n_splits=number_of_splits).split(X):
        train_set,test_set=X[train_index],X[test_index]
        test_set=numpy.concatenate((test_set[:int(len(test_set)/test_window)*test_window-1],test_set[len(test_set)-test_window-1:]),axis=0)
        # prepare training dataset
        history = [x for x in train_set]
        predictions = list()
        for t in range(int((len(test_set)/test_window))):
        	model = SARIMAX(history, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
        	model_fit = model.fit(disp=0)
        	yhat = model_fit.forecast(steps=test_window)
        	predictions=predictions+(list(yhat))    
        	history = history+list(test_set[t*test_window:(t+1)*test_window])
        # calculate out of sample error
        error = metric_func(test_set, predictions)+error
    return float(error/number_of_splits)

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_arima_models(dataset,pdq,seasonal_pdq,metric_func=mean_squared_error):
    dataset = dataset.astype('float32')
    best_score, best_cfg, best_seasonal = float("inf"), None,None
    for order in pdq:
        for seasonal in seasonal_pdq:
            try:
                mse = evaluate_model(dataset, order,seasonal)
                if mse < best_score:
                    best_score, best_cfg ,best_seasonal= mse, order,seasonal
                print('ARIMA%s MSE=%.3f' % (order,mse))
            except Exception as e: print(str(e))
                
    print('Best SARIMA%s MSE=%.3f Seasonal %s' % (best_cfg, best_score,best_seasonal))
    return  best_score,(best_cfg,best_seasonal)
def get_arima_hyper_parameters():
    p_values = range(0,8)
    d_values = range(0,2)
    q_values = range(0,3)
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p_values, d_values, q_values))]
    pqd=list(itertools.product(p_values,d_values,q_values))
    return pqd,seasonal_pdq

def calculate_weights(allData,material,number_of_splits=5):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(material)
    arima_order,seasonal_order=get_best_param_from_results(material)
    weight=numpy.arange(0,1,0.05)
    possible_weights=[(x,y,z) for x in weight for y in weight for z in weight if x+y+z==1]
    best_weights=(0,0,0)
    best_score=float('inf')
    market_data=market_data[-len(sales_data)+1:]
    market_data=market_data[market_data.columns.values[0]]
    market_data_by_competitor=market_data_by_competitor[-len(sales_data)+1:]
    sales_data=sales_data[sales_data.columns.values[0]]
    mean_percentage=market_percentage[-6:].mean()
    for pw in possible_weights:
        error=0
        for train_index, test_index in tss(n_splits=number_of_splits).split(sales_data):
            train_set_internal,test_set_internal=sales_data[train_index],sales_data[test_index]
            train_set_external=market_data[train_index[train_index[:-1]]]
            train_set_competitor=market_data_by_competitor[train_index[train_index[:-1]]]
            model_internal = SARIMAX(train_set_internal, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
            model_fit_internal = model_internal.fit(disp=0)
            model_external = SARIMAX(train_set_external, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
            model_fit_external = model_external.fit(disp=0)
            model_market = SARIMAX(train_set_competitor, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
            model_fit_market = model_market.fit(disp=0)
            yhat_internal = model_fit_internal.forecast(steps=len(test_index))
            yhat_external = model_fit_external.forecast(steps=(len(test_index)+1))[1:]
            yhat_market = model_fit_market.forecast(steps=(len(test_index)+1))[1:]
            # calculate out of sample error
            error = mean_squared_error(test_set_internal, pw[0]*yhat_internal+pw[1]*yhat_external+pw[2]*yhat_market*mean_percentage )+error
        if error<best_score:
            best_score=error
            best_weights=pw
    return best_weights
    
    

def get_best_param_from_results(material):
    arima_order=(2, 1, 2)
    seasonal_order=(0,0,0,12)
    try:
        eval_results=ldl.load_evaluation_results()
        s_params_SARIMA=eval_results[(eval_results['Material'].astype(str)==str(material))&(eval_results['Algorithm']=='SARIMA')]['Best Param'].iloc[0]
        eval_results=make_tuple(s_params_SARIMA) 
        if eval_results:    
            arima_order=eval_results[0]
            seasonal_order=eval_results[1]
    except:
        pass
    return arima_order,seasonal_order    

'''pqd=[(1,0,2)]'''
'''
arima_order=pqd[0]
seasonal_order=seasonal_pdq[0]
evaluate_arima_model(X.values,pqd[0],seasonal_pdq[0])

evaluate_models(X.values, pqd,seasonal_pdq)'''