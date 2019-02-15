#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:53:27 2019

@author: arlind
"""

import ai_analysis.data_market as dm

import ai_analysis.data_loading.load_data_locally as ldl
import pandas as pd
sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()

an_active=anagrafica[(anagrafica['ECC - Local Product Status']=='40')]

latest_molecules=dm.remove_dupplicates(pd.read_csv('Market Data/laterstdataallmolecules.csv',sep=';'))
lms=latest_molecules[latest_molecules['Manufacturer']=='SANDOZ']
perimeter=ldl.load_market_perimeter_doc()

competitors=dm.get_market_competitor_data_by_material('44072410',market_data,integration_data,perimeter)
competitorson2009=competitors[competitors['01/08/2009']!=0]['01/08/2009']
competitorson2009A=competitors[competitors['01/9/2009']!=0]['01/9/2009']

latest_molecules=latest_molecules[(latest_molecules['Sell-in UN Month/10/2018']!='0')&(latest_molecules['Sell-in UN Month/8/2018']!='0')&(latest_molecules['Sell-in UN Month/9/2018']!='0')&(latest_molecules['Sell-in UN Month/11/2018']!='0')]
latest_molecules=latest_molecules[['Product','Manufacturer','Pack']]
perimeter_dup=perimeter.drop_duplicates()
latest_molecules['Key']=latest_molecules['Product']+' '+latest_molecules['Pack']

joined_data=latest_molecules.merge(perimeter_dup,on='Key',how='left')

missing=joined_data[joined_data['Molecola'].isnull()]
missing_sandoz=missing[missing['Manufacturer']=='SANDOZ']
s=sales_data['APR 2008']

pl=s.plot()

pl.figure()
type(pl)
data_lineage=ldl.load_data_lineage()
mp=dm.get_market_competitor_data_by_material('44070376',market_data,integration_data,perimeter)



integration_filtered=integration_data[integration_data['Material'].astype(str)==str('44070376')]
market_data_perimeter_filtered=perimeter[perimeter['Key']==(integration_filtered['Product'].iloc[0]+' '+integration_filtered['Pack'].iloc[0])]
if str(market_data_perimeter_filtered['Special Market'].iloc[0])!='nan':
   perimeter_to_join_by=perimeter[perimeter['Special Market']==perimeter['Special Market'].iloc[0]]
else:
   perimeter_to_join_by=perimeter[perimeter['Mkt Molecola']==perimeter['Mkt Molecola'].iloc[0]] 
perimeter_to_join_by_only_key=perimeter_to_join_by['Key'].to_frame()
market_data['Key']=market_data['Product']+' '+market_data['Pack']
hd= market_data.merge(perimeter_to_join_by_only_key,on='Key')    