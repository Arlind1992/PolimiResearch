#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:17:53 2019

@author: arlind
"""

import ai_analysis.join_data_different_sources as dds
from fbprophet import Prophet
market_data_by_mol,market_data,sales_data=dds.get_dataframes_for_material('982566')
sales_data=sales_data.drop(sales_data.columns[1],axis=1)
sales_data=sales_data.rename(columns={sales_data.columns[0]:'y'})
sales_data['ds']=sales_data.index
m = Prophet(yearly_seasonality=True,seasonality_prior_scale=0.1)
m.fit(sales_data)
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
