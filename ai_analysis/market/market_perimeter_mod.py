#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:15:49 2019

@author: arlind
"""

import ai_analysis.data_loading.load_data_locally as ldl
import pandas as pd
perimeter=ldl.load_market_perimeter_doc()

market_form=pd.read_csv('Market Data/MarketPerimeterHelpers/maybyethisisit.csv',sep=';')
market_form_nec_mol=market_form[(market_form['Molecule'].str.contains('PRAZOLE'))|(market_form['Molecule']=='RAMIPRIL')|(market_form['Molecule']=='AMPLODIPINE')|(market_form['ATC1'].str.startswith("C "))]
market_form_nec_mol['Pack Size']=market_form_nec_mol['Pack'].apply(lambda x: str(x.split()[-1]))
market_form_nec_mol['Key']=market_form_nec_mol['Product']+' '+market_form_nec_mol['Pack']
market_form_nec_mol_per_mol=market_form_nec_mol.merge(perimeter[['Key','Mkt Molecola']])

forms=market_form_nec_mol_per_mol['FORM'].drop_duplicates()

market_form_nec_mol_per_mol['NEW CODE']= market_form_nec_mol_per_mol['FORM'].apply(lambda x :str(x.split()[-1]))

market_form_nec_mol_per_mol['Special Market']=market_form_nec_mol_per_mol['Mkt Molecola']+' '+market_form_nec_mol_per_mol['NEW CODE']+' '+market_form_nec_mol_per_mol['Pack Size']
try:
    perimeter=perimeter.drop(columns='Unnamed: 0').drop_duplicates()
except:
    pass

for index, row in market_form_nec_mol_per_mol.iterrows():
    perimeter.loc[(perimeter['Key']==row['Key']),'Special Market']=row['Special Market']


perimeter.to_csv('MarketPerimeterPack.csv',sep=';')