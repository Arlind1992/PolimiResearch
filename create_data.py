# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 14:39:47 2018

@author: RUFIAR1
"""
import pandas as pd
import datetime

def create_anagrafica(sheet,row_supply):
    to_return={}
    index_row=sheet[row_supply+1]
    for index_cells in index_row:
        if(index_cells.value):
            to_return[index_cells.value]=[sheet[index_cells.column+str(index_cells.row+1)].value]
    return pd.DataFrame.from_records(to_return)
        
def create_forecast(sheet,row_supply):
    to_return={}
    index_row=sheet[row_supply+1]
    for index_cells in index_row:
        if(index_cells.value and('2' in index_cells.value or 'Material'==index_cells.value)):
            to_return[index_cells.value]=[sheet[index_cells.column+str(index_cells.row+1)].value,sheet[index_cells.column+str(index_cells.row+2)].value]
    dt_to_return=pd.DataFrame.from_records(to_return)
    return dt_to_return

def create_sales_data(sheet,row_begin,row_end):
    to_return={}
    index_row=sheet[row_begin+1]
    now = datetime.datetime.now()
    for index_cells in index_row:
        if(index_cells.value):
            to_return[index_cells.value]=[sheet[index_cells.column+str(x)].value or 0 for x in range(row_begin+2,row_end)]
    dataframe_to_ret=pd.DataFrame.from_records(to_return)
    dataframe_to_ret=dataframe_to_ret[(dataframe_to_ret['CAUSALE']==('Forecast '+str(now.year+1))) | (dataframe_to_ret['CAUSALE']==('Forecast '+str(now.year)))|((dataframe_to_ret['CAUSALE'].str.contains('History'))) ]
    return dataframe_to_ret

def create_finance_data(sheet,row_begin,row_end):
    to_return={}
    index_row=sheet[row_begin+1]
    for index_cells in index_row:
        if(index_cells.value):
            to_return[index_cells.value]=[sheet[index_cells.column+str(x)].value or 0 for x in range(row_begin+2,row_end)]
    return pd.DataFrame.from_records(to_return)

def create_market_data(sheet,row_begin,row_end):
    to_return={}
    index_row=sheet[row_begin+1]
    for index_cells in index_row:
        if(index_cells.value):
            to_return[str(index_cells.value).replace('Sell-in UN Month','01')]=[sheet[index_cells.column+str(x)].value for x in range(row_begin+2,row_end)]
    return pd.DataFrame.from_records(to_return)

def get_row_number(sheet,name):
    first_column=sheet['A0']
    for cell in first_column:
        if(cell.value==name):
            return cell.coordinate[1:]
        
