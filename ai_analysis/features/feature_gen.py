#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:03:44 2019

@author: arlind
"""
import pandas as pd
from dateutil.relativedelta import relativedelta

def transform_time_series(ts):
   
    dataframe=pd.DataFrame()
    for i in range(12,0,-1):
        dataframe['t-'+str(i)] = ts.shift(i)
        dataframe['t'] = ts.values 
        
    dataframe['Date']=dataframe.index
    dataframe['quarter'] = dataframe['Date'].astype('datetime64').dt.quarter
    dataframe['month'] = dataframe['Date'].dt.month
    dataframe['year'] = dataframe['Date'].dt.year
    dataframe=dataframe.drop(columns=['Date'])
    
    return dataframe[dataframe['t-12'].notnull()]

def add_latest_month(df):
    df_to_append=get_x_to_predict(df)
    df_to_append['t']=None
    return df_to_append

def get_x_to_predict(df_tomodel):
    to_modify=df_tomodel.tail(n=1)
    to_modify=to_modify.drop(columns=['quarter','month','year','t-12'])
    to_modify_ren=to_modify.rename(columns={'t':'t-1','t-1':'t-2','t-2':'t-3','t-3':'t-4','t-4':'t-5','t-5':'t-6','t-6':'t-7','t-7':'t-8','t-8':'t-9','t-9':'t-10','t-10':'t-11','t-11':'t-12'})
    to_modify_ren=to_modify_ren.rename(index={to_modify_ren.index[0]:to_modify_ren.index[0]+ relativedelta(months=1)})
    to_modify_ren['Date']=to_modify_ren.index
    to_modify_ren['quarter'] = to_modify_ren['Date'].astype('datetime64').dt.quarter
    to_modify_ren['month'] = to_modify_ren['Date'].astype('datetime64').dt.month
    to_modify_ren['year'] = to_modify_ren['Date'].astype('datetime64').dt.year
    to_modify_ren=to_modify_ren.drop(columns=['Date'])
    to_modify_ren=to_modify_ren[['t-12', 't-11', 't-10', 't-9', 't-8', 't-7', 't-6', 't-5', 't-4', 't-3', 't-2', 't-1', 'quarter', 'month', 'year']]
    return to_modify_ren

def get_x_to_predict_all_data(df_internal,df_external,df_market):
    X_to_predict_int=get_x_to_predict(df_internal)
    X_to_predict_ext=get_x_to_predict(df_external).drop(columns=['t-1'])
    X_to_predict_comp=get_x_to_predict(df_market).drop(columns=['t-1'])
    X_to_predict=X_to_predict_int.add_suffix('_int').join(X_to_predict_ext.drop(columns=['quarter','month','year']).add_suffix('_ext')).join(X_to_predict_comp.drop(columns=['quarter','month','year']).add_suffix('_comp'))
    return X_to_predict
