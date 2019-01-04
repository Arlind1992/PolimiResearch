# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:06:02 2018

@author: RUFIAR1
"""

import pandas as pd


def filter_and_tras_market_data(ex_data,filter_by={}):
    ex_data['All Data']=ex_data['Molecule']+','+ex_data['Manufacturer']+','+ex_data['Product']+','+ex_data['Pack']+','+ex_data['BRAND-INN']+','+ex_data["GX-OX"]
    for key, value in filter_by.items():
        ex_data=ex_data[ex_data[key]==value]    
    ex_data=ex_data.drop(columns=['Molecule','Molecule ADJ','Manufacturer','Product','Pack','BRAND-INN','GX-OX'])
    ex_data=ex_data.set_index("All Data").T
    return ex_data

ex_data = pd.read_excel('Market Data/TestWithoutPivo.xlsx')
ex_data=filter_and_tras_market_data(ex_data,filter_by={'Molecule':'ACETILCISTEINA','Manufacturer':'SANDOZ'})   
ex_data.plot.line() 