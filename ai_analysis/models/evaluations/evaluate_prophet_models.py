#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:08:13 2019

@author: arlind
"""
from sklearn.model_selection import TimeSeriesSplit as tss
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
import ai_analysis.data_loading.load_data_locally as ldl
from ast import literal_eval as make_tuple
import numpy
import ai_analysis.constans as const
def evaluate_model(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=5,test_window=12,metric=mean_squared_error,series_len_min=20,training_percentage=0.7):
    if len(X)>=series_len_min:
        return __evaluate_model_more(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=number_of_splits,test_window=test_window,metric=mean_squared_error,training_percentage=training_percentage)
    else:
        return __evaluate_model_less(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=number_of_splits,test_window=test_window,metric=mean_squared_error)


def __evaluate_model_more(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=5,test_window=12,metric=mean_squared_error,training_percentage=0.7):
    error=[]
    train_set,test_set=X[:int(len(X)*training_percentage)],X[int(len(X)*training_percentage):]
    test_set=test_set[:int(len(test_set)/test_window)*test_window-1].append(test_set[len(test_set)-test_window-1:])
    # prepare training dataset
    history = train_set
    predictions = list()
    for t in range(int((len(test_set)/test_window))):
        error_to_add={'params':(fourier_order_par,changepoint_prior_scale_par,seasonality_prior_scale_par),'metric':metric.__name__,'date':test_set[t*test_window:(t+1)*test_window][0]}    
        model = Prophet( changepoint_prior_scale=changepoint_prior_scale_par,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale_par,fourier_order=fourier_order_par)
        to_fit=history.to_frame()
        to_fit=to_fit.rename(columns={to_fit.columns[0]:'y'})
        to_fit['ds']=to_fit.index
        model_fit = model.fit(to_fit)
        future=model.make_future_dataframe(periods=test_window)
        yhat = model_fit.predict(future)['yhat'][-test_window:]
        predictions=predictions+(list(yhat))    
        history = history.append(test_set[t*test_window:(t+1)*test_window])
    # calculate out of sample error
        error_to_add['value']=metric(test_set[t*test_window:(t+1)*test_window], predictions[-test_window:])
        error_to_add['len']=len(history)
        error.append(error_to_add)
    return error

def __evaluate_model_less(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=5,test_window=12,metric=mean_squared_error):
    error=0
    for train_index, test_index in tss(n_splits=number_of_splits).split(X):
        train_set,test_set=X[train_index],X[test_index]
        model = Prophet( changepoint_prior_scale=changepoint_prior_scale_par,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale_par,fourier_order=fourier_order_par)
        to_fit=train_set.to_frame()
        to_fit=to_fit.rename(columns={to_fit.columns[0]:'y'})
        to_fit['ds']=to_fit.index
        model_fit = model.fit(to_fit)
        future=model.make_future_dataframe(periods=len(test_set))
        yhat = model_fit.predict(future)['yhat'][-len(test_set):]
        # calculate out of sample error
        error = metric(test_set, yhat)+error
    return float(error/number_of_splits)



def evaluate_prophet_models(dataset,changepoint_prior_scale,seasonality_prior_scale,fourier_order,metric=mean_squared_error,test_window=12):
    dataset = dataset.astype('float32')
    results=[]
    for changepoint in changepoint_prior_scale:
        for seasonal in seasonality_prior_scale:
            for fourier in fourier_order:
                try:
                    mse = evaluate_model(dataset, changepoint,seasonal,fourier,test_window=test_window)
                    results.append(mse)
                except Exception as e: print(str(e))				
    return results

def calculate_weights(allData,material,number_of_splits=5,metric=mean_squared_error):
    market_data_by_competitor,sales_data,market_data,stock,market_percentage=allData.get_dataframes_for_material(material)
    fourier_order,changepoint_prior_scale,seasonality_prior_scale=get_best_param_from_results(material,const.internal_sales_SAP)
    fourier_order_ext,changepoint_prior_scale_ext,seasonality_prior_scale_ext=get_best_param_from_results(material,const.external_sales_IMS)
    fourier_order_comp,changepoint_prior_scale_comp,seasonality_prior_scale_comp=get_best_param_from_results(material,const.market_comp_sales_IMS)
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
        model_internal = Prophet(changepoint_prior_scale=changepoint_prior_scale,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale,fourier_order=fourier_order)
        to_fit_internal=train_set_internal.to_frame()
        to_fit_internal=to_fit_internal.rename(columns={to_fit_internal.columns[0]:'y'})
        to_fit_internal['ds']=to_fit_internal.index
        model_fit_internal = model_internal.fit(to_fit_internal)
        
        model_external = Prophet(changepoint_prior_scale=changepoint_prior_scale_ext,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale_ext,fourier_order=fourier_order_ext)
        to_fit_external=train_set_external.to_frame()
        to_fit_external=to_fit_external.rename(columns={to_fit_external.columns[0]:'y'})
        to_fit_external['ds']=to_fit_external.index
        model_fit_external = model_external.fit(to_fit_external)
        
        model_market = Prophet(changepoint_prior_scale=changepoint_prior_scale_comp,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale_comp,fourier_order=fourier_order_comp)
        to_fit_market=train_set_competitor.to_frame()
        to_fit_market=to_fit_market.rename(columns={to_fit_market.columns[0]:'y'})
        to_fit_market['ds']=to_fit_market.index
        model_fit_market = model_market.fit(to_fit_market)
        
        future_internal=model_internal.make_future_dataframe(periods=len(test_index),freq='MS')
        future_external=model_external.make_future_dataframe(periods=len(test_index)+1,freq='MS')
        future_market=model_market.make_future_dataframe(periods=len(test_index)+1,freq='MS')
        
        yhat_internal = model_fit_internal.predict(future_internal)['yhat'][-len(test_index):]
        yhat_external = model_fit_external.predict(future_external)['yhat'][-len(test_index):]
        yhat_market = model_fit_market.predict(future_market)['yhat'][-len(test_index):]
        
        for pw in possible_weights:
            error[pw]=metric(test_set_internal, pw[0]*yhat_internal+pw[1]*yhat_external+pw[2]*yhat_market*mean_percentage )+error[pw]
    for err in error:        
        if error[err]<best_score:
            best_score=error[err]
            best_weights=err
    return best_weights


def get_best_param_from_results(material,series_type):
    fourier_order=10
    changepoint_prior_scale= 0.5
    seasonality_prior_scale=100
    try:
        eval_results=ldl.load_evaluation_results()
        s_params_SARIMA=eval_results[(eval_results['Material'].astype(str)==str(material))&(eval_results['Algorithm']==const.prophet)&(eval_results['Series']==series_type)]['Best Param'].iloc[0]
        eval_results=make_tuple(s_params_SARIMA) 
        if eval_results:    
            fourier_order=eval_results[2]
            changepoint_prior_scale=eval_results[0]
            seasonality_prior_scale=eval_results[1]
    except:
        pass
    return fourier_order,changepoint_prior_scale,seasonality_prior_scale        



def get_hyper_parameter_values():
    fourier_order_list =[10,15,20]
    changepoint_prior_scale_list=[0.05, 0.5, 0.001]
    seasonality_prior_scale_list=[100, 10, 1]
    '''
    fourier_order_list =[10,15]
    changepoint_prior_scale_list=[0.05, 0.5]
    seasonality_prior_scale_list=[100]
    '''
    return changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list