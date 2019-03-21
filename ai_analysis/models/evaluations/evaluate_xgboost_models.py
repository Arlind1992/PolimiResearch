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

def evaluate_model(X, eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec,number_of_splits=5,test_window=12,metric_func=mean_squared_error,series_len_min=20,training_percentage=0.6):
    if len(X)>=series_len_min:
        return __evaluate_model_more(X, eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec,training_percentage=training_percentage,test_window=test_window,metric_func=metric_func)
    else:
        return __evaluate_model_less(X, eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec,number_of_splits=number_of_splits,metric_func=metric_func)
def __evaluate_model_more(X, eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec,training_percentage=0.6,test_window=12,metric_func=mean_squared_error):
    error=[]
    train_set,test_set=X[:int(len(X)*training_percentage)],X[int(len(X)*training_percentage):]
    # prepare training dataset
    test_set=test_set[:int(len(test_set)/test_window)*test_window-1].append(test_set[len(test_set)-test_window-1:])
    history = train_set
    predictions = list()
    for t in range(int((len(test_set)/test_window))):
        error_to_add={'parames':(eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec),'metric':metric_func.__name__,'date':test_set[t*test_window:(t+1)*test_window].index[0]}
        
    reg =MultiOutputRegressor( xgb.XGBRegressor(n_estimators=1000,
                           learning_rate =eta,
                           max_depth=max_depth,
                           min_child_weight=min_child_weight,
                           gamma=gamma,
                           subsample=subsample,
                           colsample_bytree=colsample_bytree,
                           nthread=4,
                           seed=27))
    reg.fit(X_train, y_train)
    date_rng = pd.date_range(start=y_test.index[-1].date(), end=y_test.index[-1].date()+timedelta(days=365), freq='MS')
    date_rng=y_test.index
    Y_pred=[]
    for i in range(0,test_window):
        X_to_predict=fg.get_x_to_predict_all_data(last_X_int,last_X_ext,last_X_comp)
        X_to_predict=X_to_predict[X_test.columns]
        Y_pred_to_add=reg.predict(X_to_predict)
        last_X_int=fg.add_latest_month(last_X_int)
        last_X_int['t']=float(Y_pred_to_add[0][0])
        last_X_ext=fg.add_latest_month(last_X_ext)
        last_X_ext['t-1']=float(Y_pred_to_add[0][1])
        last_X_comp=fg.add_latest_month(last_X_comp)
        last_X_comp['t-1']=float(Y_pred_to_add[0][2])
        Y_pred.append(Y_pred_to_add[0][0])
        
    Y_pred=pd.Series(Y_pred).astype(float)
    Y_pred.index=date_rng
    
    mean_squared_error(Y_pred,y_test['t_int'])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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

def __evaluate_model_less(X, eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec,number_of_splits=5,metric_func=mean_squared_error):
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
def evaluate_xgboost_models(dataset,metric_func=mean_squared_error,test_window=12,training_percentage=0.6):
    dataset = dataset.astype('float32')
    eta_vec,min_child_weight_vec,max_depth_vec,gamma_vec,subsample_vec,colsample_bytree_vec=__get_xgboost_hyper_parameters()
    results=[]
    i=0
    for eta in eta_vec:
        for min_child_weight in min_child_weight_vec:
            for max_depth in max_depth_vec:
                for gamma in gamma_vec:
                    for subsample in subsample_vec:
                        for colsample_bytree in colsample_bytree_vec:                 
                            try:
                                mse_ls = evaluate_model(dataset, order,seasonal,test_window=test_window,training_percentage=training_percentage)
                                results.append(mse_ls)
                                print('IM ALIVE '+str(i))
                                i=i+1
                            except Exception as e: print(str(e))            
    return  results

def __get_xgboost_hyper_parameters():
    eta=[0.10, 0.15, 0.20, 0.25, 0.30 ]
    min_child_weight=[ 1, 3, 5, 7 ]
    max_depth=[3, 4, 5, 6, 8, 10]
    gamma=[ 0.0, 0.1, 0.2 , 0.3, 0.4 ]
    subsample=[ 0.3, 0.4, 0.5 , 0.7 ]
    colsample_bytree=[ 0.3, 0.4, 0.5 , 0.7 ]
    
    return eta,min_child_weight,max_depth,gamma,subsample,colsample_bytree
   

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