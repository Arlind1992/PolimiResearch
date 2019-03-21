#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:52:16 2019

@author: arlind
"""


import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
import pandas as pd
import warnings
from sklearn.model_selection import GridSearchCV
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf


def model_material(material,allData,show_components=False):
    market_data_by_competitor,sales_data,market_data,stock=allData.get_dataframes_for_material(material)
    int_sales_forecast,conf_interval_int_sales=model_df(sales_data,show_components,title='Sales SAP')  
    ext_sales_forecast,conf_interval_ext_sales=model_df(market_data,show_components,title='Sales IMS')
    competitor_sales_forecast,conf_interval_competitor=model_df(market_data_by_competitor.to_frame(),show_components,title='Sales Whole Market')
    return int_sales_forecast,ext_sales_forecast,competitor_sales_forecast


def model_df(df,material,type_series,show_components=False,title=''):
    eta,min_child_weight,max_depth,gamma,subsample,colsample_bytree=get_best_param_from_results()
    try:
        df=df.drop(df.columns[1],axis=1)
    except:
        pass
    df_tomodel=transform_time_series(df)
    X_test = df_tomodel[-12:]
    y_test=X_test[0]
    X_test=X_test.drop(columns=[0])
    X_train=df_tomodel[:-12]
    y_train=X_train[0]
    X_train=X_train.drop(columns=[0])        
    reg = xgb.XGBRegressor(n_estimators=1000,
                           learning_rate =eta,
                           max_depth=max_depth,
                           min_child_weight=min_child_weight,
                           gamma=gamma,
                           subsample=subsample,
                           colsample_bytree=colsample_bytree,
                           nthread=4,
                           seed=27)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            early_stopping_rounds=50, #stop if 50 consequent rounds without decrease of error
            verbose=False)
    reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        early_stopping_rounds=50, #stop if 50 consequent rounds without decrease of error
        verbose=False)
    date_rng = pd.date_range(start='01/01/2019', end='12/01/2019', freq='MS')
    X_to_pred_series=pd.Series(date_rng)
    X_to_pred_series.index=date_rng
    X_to_pred_series=transform_time_series(X_to_pred_series)
    X_to_pred_series=X_to_pred_series.drop(columns=0)
    Y_pred = reg.predict(X_to_pred_series)
    Y_pred=pd.Series(Y_pred).astype(float)
    Y_pred.index=date_rng
    
    conf_interval=results.conf_int()
    if show_components:
        plot_data(df,model_fit,title)
    return Y_pred,conf_interval

def get_best_param_from_results(material,ts_type):
    eta=0.1
    min_child_weight=1
    max_depth=6
    gamma=0
    subsample=1
    colsample_bytree=1
    '''
    try:
        eval_results=ldl.load_evaluation_results()
        s_params_SARIMA=eval_results[(eval_results['Material'].astype(str)==str(material))&(eval_results['Algorithm']=='SARIMA')]['Best Param'].iloc[0]
        eval_results=make_tuple(s_params_SARIMA) 
        if arima_order:    
            arima_order=eval_results[0]
            seasonal_order=eval_results[1]
    except:
        pass
    '''
    return eta,min_child_weight,max_depth,gamma,subsample,colsample_bytree

def plot_data(df,model_fit,title):
    result=model_fit.get_forecast(12)
    predictions=result.predicted_mean
    conf_interval=result.conf_int()
    fitted_values=model_fit.fittedvalues.append(predictions).to_frame()
    fig, ax = plt.subplots(figsize=(10,4))
    df.plot(ax=ax, label='Observations')
    fitted_values.plot(ax=ax, label='SARIMA')
    ax.set_title(title)
    ax.fill_between( conf_interval.index,conf_interval.iloc[:, 0], conf_interval.iloc[:, 1], alpha=0.1)


