#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:07:22 2019

@author: arlind
"""

import ai_analysis.join_data_different_sources as ds
import ai_analysis.data_loading.load_data_locally as ldl

sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
perimeter=ldl.load_market_perimeter_doc()
dat_lineage=ldl.load_data_lineage()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,dat_lineage,perimeter)

material='44083137'
market,int_sales,ext_sales=allData.get_dataframes_for_material(material)
stock_changes=int_sales[int_sales.columns[0]].subtract(ext_sales[ext_sales.columns[0]]).dropna()
stock_changes.plot()

stock_toframe=stock_changes.to_frame()
stock_toframe=stock_toframe.rename(columns={stock_toframe.columns[0]:'stock'})
alljoined=stock_toframe.join(int_sales).join(ext_sales).join(market.to_frame())

co=alljoined.corr()

allsaleshist=allData.sales_data_fullhistory

hist=dlt.add_history_sales_different_sku(sales_data,anagrafica)


materials=['44068397','44083137','44058838']

allData.plot_material(material)
        