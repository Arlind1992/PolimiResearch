# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 10:40:00 2019

@author: RUFIAR1
"""
from openpyxl import load_workbook
import pandas as pd
import ai_analysis.manual_integration.create_data as cd
import re
from os import listdir
from os.path import isfile, join
def create_market_data_complete(file='Market Data/2018.10 RETAIL - Download 20 sample molecule - 2018.12.20 - Copy.xlsx',sheet_name='2018.10 RETAIL - Download 20 sa'):    
    wb = load_workbook(filename = file)
    intrested_sheet=wb[sheet_name]
    market_data=cd.create_market_data(intrested_sheet,0,intrested_sheet.max_row)
    market_data['All Data']=market_data['Molecule']+','+market_data['Manufacturer']+','+market_data['Product']+','+market_data['Pack']+','+market_data['BRAND-INN']+','+market_data["GX-OX"]
    market_data=market_data.drop(columns=['Molecule','Molecule ADJ','Manufacturer','Product','Pack','BRAND-INN','GX-OX'])
    market_data=market_data.set_index("All Data")
    return market_data

def create_market_data_from_csv(filepath='Market Data/All Market Data Sandoz 2.csv',separator=','):
    dt=pd.read_csv(filepath,sep=separator,decimal=",")
    col_names=list(dt)
    pattern=re.compile('^Sell-in (.*?)/')
    for colname in col_names:
        if pattern.match(colname):
            dt=dt.rename(columns = {colname: re.sub(pattern, '01/', colname)})
    return dt
    ddd=create_market_data_from_csv()
def create_all_old_market_data(path_data):
    onlyfiles = [f for f in listdir(path_data) if isfile(join(path_data, f))]
    df=create_market_data_from_csv(filepath=path_data+'/'+onlyfiles[0],separator=';')
    for f_pos in range(1,len(onlyfiles)):
        df=df.merge(create_market_data_from_csv(filepath=path_data+'/'+onlyfiles[f_pos],separator=';'), how='outer',on=['Manufacturer','Name Type','Product','Pack','Molecule'] )    
    return df
path_data='Market Data/All old data'
onlyfiles = [f for f in listdir(path_data) if isfile(join(path_data, f))]
df_csv=create_market_data_from_csv(filepath=path_data+'/'+onlyfiles[2],separator=';')
df_c=pd.read_csv(path_data+'/'+onlyfiles[0],sep=';')
def add_latest_data(latest_data_path,old_data_path):
    latest_data=create_market_data_from_csv(filepath=latest_data_path,separator=';')
    df=create_market_data_from_csv(filepath=old_data_path, separator=';')
    for col_name in list(latest_data.columns.values):
        if '01' in col_name:
            try:
                df=df.drop(columns=col_name, axis=1)
            except:
                pass
    toreturn=df.merge(latest_data, how='outer',on=['Manufacturer','Name Type','Product','Pack','Molecule'] )    
    return toreturn    

def get_market_data():
    return create_market_data_from_csv(filepath='AllData/AllDataWithMoleculeSubset.csv',separator=';').drop(columns='Unnamed: 0.1',axis=1)
'''
path_data='Market Data/All old data'
code to save all merge and save all market data archives and also add to them the latest data
df=create_all_old_market_data('Market Data/All old data')
df.to_csv(path_or_buf ='Market Data/AllOldData.csv',sep=';',decimal=',')
toreturn=add_latest_data('Market Data/OnlyNecDataSubsetMolecules.csv','Market Data/AllOldData.csv')
toreturn.to_csv(path_or_buf ='Market Data/AllDataWithMoleculeSubset.csv',sep=';')
'''

