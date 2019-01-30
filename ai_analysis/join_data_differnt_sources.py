#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 12:31:53 2019

@author: arlind
"""
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_market as md
import ai_analysis.automatic_integration.integration_utils as iu
import ai_analysis.sales_data as sd
import ai_analysis.transform_data as td

def add_history_sales_different_sku(sales_data,anagrafica):    
    anagrafica_dub=anagrafica[anagrafica.duplicated(subset=['GMD FDF ID','Brand'])][['GMD FDF ID','Brand']].drop_duplicates()
    anagrafica_to_modify=anagrafica[['Material','GMD FDF ID','Brand','ECC - Local Product Status']].merge(anagrafica_dub,on=['GMD FDF ID','Brand'],how='inner')
    unique_gmd=anagrafica_to_modify[anagrafica_to_modify['ECC - Local Product Status']=='40'].groupby(['GMD FDF ID','Brand','ECC - Local Product Status'],as_index=False)['Material'].min()
    sales_data['Material']=sales_data['Material'].replace(to_replace=create_dict_to_replace(anagrafica_to_modify,unique_gmd))
    return sales_data.groupby(['Material'],as_index=False).sum()
def create_dict_to_replace(anagrafica_to_modify,unique_gmd):
    dict_to_return={}
    for mat in list(anagrafica_to_modify['Material']):
        dict_to_return[mat]=unique_gmd[(unique_gmd['GMD FDF ID']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['GMD FDF ID'].iloc[0])&(unique_gmd['Brand']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['Brand'].iloc[0])]['Material'].iloc[0]
    return dict_to_return        
sales_data=sd.get_sales_data()
anagrafica=an.create_anagrafica(2, file='AllData/anagrafica_AI.xlsx')
sales_data=add_history_sales_different_sku(sales_data,anagrafica)
market_data=md.get_market_data().drop(columns='Name Type',axis=1).fillna(0)
market_data=market_data.drop(columns='Unnamed: 0')
anagrafica['Material']=anagrafica['Material'].astype(int)
integration=pd.read_csv('AllData/crtSAPIMS.csv',sep=';')

not_integrated=iu.dataframe_differences(anagrafica,integration['Material'],'Material')

not_integrated_40=not_integrated[not_integrated['ECC - Local Product Status']!='40']
anagrafica_40=anagrafica[anagrafica['ECC - Local Product Status']=='40']

market_data_by_molecule=market_data.drop(columns=['Manufacturer','Product','Pack']).set_index('Molecule')
market_data_by_molecule[market_data_by_molecule.columns]=market_data_by_molecule[market_data_by_molecule.columns].astype(float)

market_data_by_molecule=market_data_by_molecule.groupby(market_data_by_molecule.index).sum()

integration_join_anagrafica=anagrafica.merge(integration,how='inner',on='Material')
integration_join_anagrafica=integration_join_anagrafica[integration_join_anagrafica['ECC - Local Product Status']=='40']
market_data_pb=md.get_probiotici_csv()
integration_probiotici=pd.read_csv('AllData/crtSAPQlik.csv',sep=';')
material='44083137'
def plot_for_material_probiotico(material):
    sales_data_filtered_pb=sales_data[sales_data['Material']==material]
    integration_filtered_pb=integration_probiotici[integration_probiotici['Material'].astype(str)==material]
    market_data_filtered_pb=market_data_pb[(market_data_pb['Company']=='SANDOZ-HEXAL') & (market_data_pb['Product']==integration_filtered_pb['QlikProduct'].iloc[0])]
    ts_sales_data_pb=td.tras_sales_data(sales_data_filtered_pb)
    ts_market_data_pb=td.tras_market_data_probiotici(market_data_filtered_pb)
    ts_market_data_pb[ts_market_data_pb.columns.values[0]]=ts_market_data_pb[ts_market_data_pb.columns.values[0]].apply(lambda x: float(str(x).replace(',','.')))
    ts_sales_data_pb.sort_index().plot(title='Sales')
    ts_market_data_pb.sort_index().plot(title='Market Data Sandoz')
    ts_sales_data_pb.join(ts_market_data_pb).plot(title='Sales-Market')
    
def plot_for_material(material):
    ts_market_data_by_molecule,ts_sales_data,ts_market_data=get_dataframes_for_material(material)
    ts_market_data_by_molecule.sort_index().plot(title='Whole market for molecule')
    '''ts_sales_data.plot(title='Sales')
    ts_market_data.apply(lambda x: x*1000).plot(title='Market Data Sandoz')'''
    ts_sales_data.join(ts_market_data).plot(title='Sales-Market')

def get_dataframes_for_material(material):
    sales_data_filtered=sales_data[sales_data['Material']==material]
    integration_filtered=integration[integration['Material'].astype(str)==material]
    market_data_filtered=market_data[(market_data['Manufacturer']=='SANDOZ') & (market_data['Product']==integration_filtered['Product'].iloc[0])& (market_data['Pack']==integration_filtered['Pack'].iloc[0])]
    ts_sales_data=td.tras_sales_data(sales_data_filtered)
    ts_market_data=td.tras_market_data(market_data_filtered).astype(float)
    ts_market_data_by_molecule=market_data_by_molecule[market_data_by_molecule.index==integration_filtered['Molecule'].iloc[0]].T
    ts_market_data_by_molecule.index=pd.to_datetime(ts_market_data_by_molecule.index,format='%d/%m/%Y')
    return ts_market_data_by_molecule,ts_sales_data,ts_market_data
    

    
def plot_material(material):
    if(material in integration_probiotici['Material']):
        plot_for_material_probiotico(material)
    else:
        plot_for_material(material)
        
materials=['44068397','44083137','44058838']
