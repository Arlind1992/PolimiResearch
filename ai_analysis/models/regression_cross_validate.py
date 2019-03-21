#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:55:01 2019

@author: arlind
"""
import ai_analysis.features.feature_gen as fg
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from datetime import timedelta 
def cross_validate(allData,material,regressior,time_window,metric_fun):
    ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock,market_percentage=allData.get_dataframes_for_material(str(material))
    df_market=fg.transform_time_series(ts_market_data_by_molecule[ts_market_data_by_molecule.columns[0]])
    df_internal=fg.transform_time_series(ts_sales_data[ts_sales_data.columns[0]])
    df_external=fg.transform_time_series(ts_market_data[ts_market_data.columns[0]])
    df_external=df_external.append(fg.add_latest_month(df_external))
    df_market=df_market.append(fg.add_latest_month(df_market))
    df_joined=df_internal.add_suffix('_int').join(df_external.drop(columns=['quarter','month','year','t']).add_suffix('_ext')).join(df_market.drop(columns=['quarter','month','year','t']).add_suffix('_comp'))
    X_test = df_joined[-time_window:]
    y_test=X_test[['t_int','t-1_ext','t-1_comp']]
    X_test=X_test.drop(columns=['t_int','t-1_ext','t-1_comp'])
    X_test=X_test.head(n=1)
    X_train=df_joined[:-time_window]
    y_train=X_train[['t_int','t-1_ext','t-1_comp']]
    X_train=X_train.drop(columns=['t_int','t-1_ext','t-1_comp'])        
    last_X_int=df_internal[:-time_window].tail(n=1)
    last_X_ext=df_external[:-time_window].tail(n=1)
    last_X_comp=df_market[:-time_window].tail(n=1)
    reg =MultiOutputRegressor(regressior)
    reg.fit(X_train, y_train)
    date_rng = pd.date_range(start=y_test.index[-1].date(), end=y_test.index[-1].date()+timedelta(days=365), freq='MS')
    date_rng=y_test.index
    Y_pred=[]
    for i in range(0,time_window):
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
    return metric_fun(X_test, Y_pred['t_int'])