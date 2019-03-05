#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:08:13 2019

@author: arlind
"""
from sklearn.model_selection import TimeSeriesSplit as tss
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
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