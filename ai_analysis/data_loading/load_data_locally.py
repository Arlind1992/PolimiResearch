#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:32:40 2019

@author: arlind
"""
import ai_analysis.sales_data as sd
import ai_analysis.anagrafica as an
import ai_analysis.market.data_market as md
import pandas as pd
import ai_analysis.manual_integration.create_data as cd
from openpyxl import load_workbook
def load_data():
    sales_data=sd.get_sales_data()
    anagrafica=an.create_anagrafica(3, file='AllData/anagrafica_AI.xlsx')
    market_data=md.get_market_data().drop(columns='Name Type',axis=1).fillna(0)
    market_data=md.remove_dupplicates(market_data.drop(columns='Unnamed: 0'))
    anagrafica['Material']=anagrafica['Material'].astype(int)
    integration=pd.read_csv('AllData/crtSAPIMS.csv',sep=';')
    market_data_pb=md.get_probiotici_csv()
    integration_probiotici=pd.read_csv('AllData/crtSAPQlik.csv',sep=';')
    return sales_data,anagrafica,market_data,market_data_pb,integration,integration_probiotici
def load_market_perimeter_doc():
    try:
        market_data_perimeter=pd.read_excel('AllData/MarketPerimeter.xlsx').drop_duplicates()
    except:
        market_data_perimeter=pd.read_csv('AllData/MarketPerimeter.csv',sep=';').drop_duplicates()
    return market_data_perimeter

def load_data_lineage():
    data_lineage=pd.read_csv('AllData/dataLineage.csv',sep=';')
    return data_lineage

def load_market_data():
    market_data=md.get_market_data().drop(columns='Name Type',axis=1).fillna(0)
    market_data=md.remove_dupplicates(market_data.drop(columns='Unnamed: 0'))
    return market_data

def load_evaluation_results():
    return pd.read_csv('Results',sep=';')


def load_weight_results():
    return pd.read_csv('ResultsWeights',sep=';')

def load_anagrafica():
    return an.create_anagrafica(3, file='AllData/anagrafica_AI.xlsx')

def load_sales_data():
    return  sd.get_sales_data()

def load_price_and_discounts():
    work_book=load_workbook('Finance/finance_data.xlsx')
    sheet_ph=work_book['Other']
    sheet_wh=work_book['WHS']
    sheet_other=work_book['PHS']
    return pd.read_excel('Finance/finance_data.xlsb')


