#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 19:05:14 2019

@author: arlind
"""
import ai_analysis.data_loading.load_data_locally as ldl
from ast import literal_eval as make_tuple

def int_sales_by_combination(int_sales_forecast,conf_interval_int_sales,ext_sales_forecast,conf_interval_ext_sales,competitor_sales_forecast,conf_interval_competitor,market_percentage):
    std_deviation=(conf_interval_int_sales[conf_interval_int_sales.columns[1]]-conf_interval_int_sales[conf_interval_int_sales.columns[0]])/int_sales_forecast
    std_deviation_ext=(conf_interval_ext_sales[conf_interval_ext_sales.columns[1]]-conf_interval_ext_sales[conf_interval_ext_sales.columns[0]])/ext_sales_forecast    
    std_deviation_market=(conf_interval_competitor[conf_interval_competitor.columns[1]]-conf_interval_competitor[conf_interval_competitor.columns[0]])/competitor_sales_forecast    
    sum_alldev=std_deviation+std_deviation_ext+std_deviation_market    
    int_forecast=(std_deviation/sum_alldev)*int_sales_forecast+(std_deviation_ext/sum_alldev)*ext_sales_forecast+(std_deviation_market/sum_alldev)*competitor_sales_forecast*market_percentage[-6:].mean()
    return int_forecast

def get_best_weights(material,algorithm):
    pw=(0.3,0.3,0.4)
    try:
        weights_results=ldl.load_weight_results()
        weights=weights_results[(weights_results['Material'].astype(str)==str(material))&(weights_results['Model']==algorithm)]['Best Weights'].iloc[0]
        pw=make_tuple(weights)
    except:
        pass
    
    return pw