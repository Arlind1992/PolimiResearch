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
def evaluate_model(X, changepoint_prior_scale_par,seasonality_prior_scale_par,fourier_order_par,number_of_splits=5,test_window=12,metric=mean_squared_error):
    error=0
    for train_index, test_index in tss(n_splits=number_of_splits).split(X):
        train_set,test_set=X[train_index],X[test_index]
        test_set=test_set[:int(len(test_set)/test_window)*test_window-1].append(test_set[len(test_set)-test_window-1:])
        # prepare training dataset
        history = train_set
        predictions = list()
        for t in range(int((len(test_set)/test_window))):
            model = Prophet( changepoint_prior_scale=changepoint_prior_scale_par,growth='linear').add_seasonality(name='yearly',period=365.25, prior_scale=seasonality_prior_scale_par,fourier_order=fourier_order_par)
            to_fit=history.to_frame()
            to_fit=to_fit.rename(columns={to_fit.columns[0]:'y'})
            to_fit['ds']=to_fit.index
            model_fit = model.fit(to_fit)
            future=model.make_future_dataframe(periods=12)
            yhat = model_fit.predict(future)['yhat'][-12:]
            predictions=predictions+(list(yhat))    
            history = history.append(test_set[t*test_window:(t+1)*test_window])
        # calculate out of sample error
        error = metric(test_set, predictions)+error
    return float(error/number_of_splits)
def evaluate_prophet_models(dataset,changepoint_prior_scale,seasonality_prior_scale,fourier_order,metric=mean_squared_error):
    dataset = dataset.astype('float32')
    best_score, best_changepoint, best_seasonal,best_fourier = float("inf"), None,None,None
    for changepoint in changepoint_prior_scale:
        for seasonal in seasonality_prior_scale:
            for fourier in fourier_order:
                try:
                    mse = evaluate_model(dataset, changepoint,seasonal,fourier)
                    if mse < best_score:
                        best_score, best_changepoint ,best_seasonal,best_fourier= mse, changepoint,seasonal,fourier
                    print('PROPHET changepoint=%s seasonal= %s fourier=%s MSE=%.3f' % (best_changepoint,best_seasonal,best_fourier,mse))
                except Exception as e: print(str(e))				
    print('Best PROPHET changepoint=%s seasonal= %s fourier=%s MSE=%.3f' % (best_changepoint,best_seasonal,best_fourier,mse))
    return mse,(best_changepoint,best_seasonal,best_fourier)

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
    fourier_order=10
    changepoint_prior_scale= 0.5
    seasonality_prior_scale=100
    try:
        eval_results=ldl.load_evaluation_results()
        s_params_SARIMA=eval_results[(eval_results['Material'].astype(str)==str(material))&(eval_results['Algorithm']=='PROPHET')]['Best Param'].iloc[0]
        eval_results=make_tuple(s_params_SARIMA) 
        if eval_results:    
            fourier_order=eval_results[0]
            changepoint_prior_scale=eval_results[1]
            seasonality_prior_scale=eval_results[2]
    except:
        pass
    return fourier_order,changepoint_prior_scale,seasonality_prior_scale        



def get_hyper_parameter_values():
    '''
    fourier_order_list =[10,15,20,25]
    changepoint_prior_scale_list=[0.05, 0.5, 0.001]
    seasonality_prior_scale_list=[100, 10, 1]
    '''
    fourier_order_list =[10,15]
    changepoint_prior_scale_list=[0.05, 0.5]
    seasonality_prior_scale_list=[100]
    return changepoint_prior_scale_list,seasonality_prior_scale_list,fourier_order_list