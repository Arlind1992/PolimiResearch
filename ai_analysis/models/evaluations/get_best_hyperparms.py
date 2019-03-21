#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:55:39 2019

@author: arlind
"""

import pandas as pd
from os import listdir
from os.path import isfile, join
import ai_analysis.constans as const
from pandas import Timestamp 
material='44070378'
path_data='hyperparam_results'
algorithm=const.sarima
onlyfiles = [f for f in listdir(path_data) if isfile(join(path_data, f))]
series_type=const.internal_sales_SAP

hyperparams=pd.read_csv(path_data+'/'+onlyfiles[0],sep=';')
hyperparams=hyperparams[hyperparams['Number Of Data']>20]
hyperparams=hyperparams[(hyperparams['Series']==series_type)&(hyperparams['Material'].astype(str)==str(material))]
values=eval(hyperparams['Metric Values'].iloc[0])[0]
values_df=pd.DataFrame(values)


values_df_to_plot=values_df[['date','value']]
values_df_to_plot.index=values_df_to_plot['date']
values_df_to_plot=values_df_to_plot.drop(columns=['date'])
values_df_to_plot.index=pd.to_datetime(values_df_to_plot.index)
values_df_to_plot.plot()