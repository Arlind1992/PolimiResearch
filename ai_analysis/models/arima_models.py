#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:59:28 2019

@author: arlind
"""
import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
 

sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,lineage,perimeter)
material='44070378'
ts_market_data_by_molecule,ts_sales_data,ts_market_data=allData.get_dataframes_for_material(material)
ts_market_data_by_molecule.plot()
def model_material(material,allData):
    ts_market_data_by_molecule,ts_sales_data,ts_market_data=allData.get_dataframes_for_material(material)    
    model = ARIMA(ts_market_data_by_molecule, order=(6,0,6))
    model_fit = model.fit(disp=0)
    # plot residual errors
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    residuals.plot(kind='kde')

autocorrelation_plot(ts_market_data_by_molecule)
pyplot.show()

allData.remove_initial_zeros(ts_market_data_by_molecule)
