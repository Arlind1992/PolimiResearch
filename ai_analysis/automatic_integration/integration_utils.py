#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:22:05 2019

@author: arlind
"""
import re
import pandas as pd
def create_df_fromsheet(sheet,row_supply):
    to_return={}
    index_row=sheet[row_supply]
    for index_cells in index_row:
        if(index_cells.value):
            to_return[index_cells.value]=[sheet[index_cells.column+str(x)].value for x in range(row_supply+1,sheet.max_row)]
    return pd.DataFrame.from_records(to_return)

'''method to do the set difference between a dataframe and a series'''
def dataframe_differences(materialsdf,data_to_remove,column_to_filter_by):
    materials_to_remove_set=data_to_remove.unique().astype(int)
    return materialsdf[materialsdf[column_to_filter_by].apply(lambda x: int(x) not in materials_to_remove_set)]

def save_to_csv(df_int):
    df_int[['Material','Brand','Nome','Molecule','Product','Pack']].to_csv(path_or_buf ='integration.csv',sep=';')

def trasform_market_data(market_data):
    market_data=market_data[['Manufacturer','Name Type','Product','Pack','Molecule']][market_data['Manufacturer']=='SANDOZ']
    market_data['PackSize']=market_data['Pack'].apply(lambda x: x[-1 if not re.search('\d',x) else re.search('\d',x).start():].replace(' ',''))
    market_data['PackType']=market_data['Pack'].apply(lambda x: x[:-1 if not re.search('\d',x) else re.search('\d',x).start()])
    market_data['BrandOwner']=market_data['Product'].apply(lambda x: x.split(' ')[-1].replace('SAN','Sandoz').replace('HEX','Hexal'))
    return market_data

def transform_anagrafica(anagrafica):
    anagrafica=anagrafica[['GMD Bulk ID','Material','Brand','ECC - Local Product Status','GMD AS ID','Nome','GMD Dosage Form']]
    anagrafica['Size']=anagrafica['GMD Bulk ID'].apply(lambda x: x[-1 if not re.search('\d',x) else re.search('\d',x).start():].replace(' ',''))
    return anagrafica


        