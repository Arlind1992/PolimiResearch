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
import ai_analysis.constans as const
import ai_analysis.data_loading.load_data_locally as ldl
from ast import literal_eval as make_tuple

def evaluate_model(X, arima_order,seasonal_order,number_of_splits=5,test_window=12,metric_func=mean_squared_error,series_len_min=20,training_percentage=0.6,last_year=False):
    if len(X)>=series_len_min:
        return __evaluate_model_more(X, arima_order,seasonal_order,training_percentage=training_percentage,test_window=test_window,metric_func=metric_func,last_year=last_year)
    else:
        return __evaluate_model_less(X, arima_order,seasonal_order,number_of_splits=number_of_splits,metric_func=metric_func)
def __evaluate_model_more(X, arima_order,seasonal_order,training_percentage=0.6,test_window=12,metric_func=mean_squared_error,last_year=False):
    error=[]
    if last_year:
        train_set,test_set=X[:-24],X[-24:-12]
    else:
        train_set,test_set=X[:int(len(X)*training_percentage)],X[int(len(X)*training_percentage):]
    # prepare training dataset
    test_set=test_set[:int(len(test_set)/test_window)*test_window-1].append(test_set[len(test_set)-test_window-1:])
    history = train_set
    predictions = list()
    for t in range(int((len(test_set)/test_window))):
        error_to_add={'parames':(arima_order,seasonal_order),'metric':metric_func.__name__,'date':test_set[t*test_window:(t+1)*test_window].index[0]}
        model = SARIMAX(history, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast(steps=test_window)
        predictions=predictions+(list(yhat))    
        history = history.append(test_set[t*test_window:(t+1)*test_window])
        # calculate out of sample error
        error_to_add['value']=metric_func(test_set[t*test_window:(t+1)*test_window], predictions[-test_window:])
        error_to_add['len']=len(history)        
        error.append(error_to_add)
    return error

def __evaluate_model_less(X, arima_order,seasonal_order,number_of_splits=5,metric_func=mean_squared_error):
    error=0
    for train_index, test_index in tss(n_splits=number_of_splits).split(X):
        train_set,test_set=X[train_index],X[test_index]
        model = SARIMAX(train_set, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast(steps=len(test_set))
        # calculate out of sample error
        error = metric_func(test_set, yhat)+error
    return float(error/number_of_splits)

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_arima_models(dataset,pdq,seasonal_pdq,metric_func=mean_squared_error,test_window=12,training_percentage=0.6,last_year=False):
    dataset = dataset.astype('float32')
    results=[]
    i=0
    for order in pdq:
        for seasonal in seasonal_pdq:
            try:
                mse_ls = evaluate_model(dataset, order,seasonal,test_window=test_window,training_percentage=training_percentage,last_year=last_year)
                results.append(mse_ls)
                print('IM ALIVE '+str(i))
                i=i+1
            except Exception as e: print(str(e))
                
    return  results
def get_arima_hyper_parameters():
    p_values = range(0,8)
    d_values = range(0,2)
    q_values = range(0,3)
    p_values_s=range(0,3)
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p_values_s, d_values, q_values))]
    pqd=list(itertools.product(p_values,d_values,q_values))
    return pqd,seasonal_pdq

def calculate_weights(allData,material,number_of_splits=5):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(str(material))
    arima_order,seasonal_order=get_best_param_from_results(str(material),const.internal_sales_SAP)
    arima_order_ext,seasonal_order_ext=get_best_param_from_results(material,const.external_sales_IMS)
    arima_order_comp,seasonal_order_comp=get_best_param_from_results(material,const.market_comp_sales_IMS)
    print(arima_order)
    print(arima_order_comp)
    print(arima_order_ext)
    weight=numpy.arange(0,1,0.01)
    possible_weights=[(x,y,z) for x in weight for y in weight for z in weight if x+y+z==1]
    best_weights=(0,0,0)
    best_score=float('inf')
    market_data=market_data[-len(sales_data)+1:]
    market_data=market_data[market_data.columns.values[0]]
    market_data_by_competitor=market_data_by_competitor[-len(sales_data)+1:]
    sales_data=sales_data[sales_data.columns.values[0]]
    mean_percentage=market_percentage[-6:].mean()
    error={}
    for pw in possible_weights:
        error[pw]=0
    for train_index, test_index in tss(n_splits=number_of_splits).split(sales_data):
        train_set_internal,test_set_internal=sales_data[train_index],sales_data[test_index]
        train_set_external=market_data[train_index[train_index[:-1]]]
        train_set_competitor=market_data_by_competitor[train_index[train_index[:-1]]]
        model_internal = SARIMAX(train_set_internal, order=arima_order,seasonal_order=seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
        model_fit_internal = model_internal.fit(disp=0)
        model_external = SARIMAX(train_set_external, order=arima_order_ext,seasonal_order=seasonal_order_ext,enforce_stationarity=False,enforce_invertibility=False)
        model_fit_external = model_external.fit(disp=0)
        model_market = SARIMAX(train_set_competitor, order=arima_order_comp,seasonal_order=seasonal_order_comp,enforce_stationarity=False,enforce_invertibility=False)
        model_fit_market = model_market.fit(disp=0)
        yhat_internal = model_fit_internal.forecast(steps=len(test_index))
        yhat_external = model_fit_external.forecast(steps=(len(test_index)+1))[1:]
        yhat_market = model_fit_market.forecast(steps=(len(test_index)+1))[1:]
        # calculate out of sample error
        for pw in possible_weights:
            error[pw]=mean_squared_error(test_set_internal, pw[0]*yhat_internal+pw[1]*yhat_external+pw[2]*yhat_market*mean_percentage )+error[pw]
    for err in error:        
        if error[err]<best_score:
            best_score=error[err]
            best_weights=err
    return best_weights
    
    

def get_best_param_from_results(material,series_type):
    arima_order=(2, 1, 2)
    seasonal_order=(0,0,0,12)
    try:
        eval_results=ldl.load_evaluation_results()
        s_params_SARIMA=eval_results[(eval_results['Material'].astype(str)==str(material))&(eval_results['Algorithm']==const.sarima)&(eval_results['Series']==series_type)]['Best Param'].iloc[0]
        eval_results=make_tuple(s_params_SARIMA) 
        if eval_results[0]:    
            arima_order=eval_results[0]
            seasonal_order=eval_results[1]
    except Exception as e:
        print(e)
    return arima_order,seasonal_order    


'''pqd=[(1,0,2)]'''
'''
arima_order=pqd[0]
seasonal_order=seasonal_pdq[0]
evaluate_arima_model(X.values,pqd[0],seasonal_pdq[0])

evaluate_models(X.values, pqd,seasonal_pdq)'''