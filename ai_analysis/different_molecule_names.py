#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 10:41:11 2019

@author: arlind
"""
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_market as dm

a=an.create_anagrafica(2, file='Supply&Demand/anagrafica_AI_moreInfo1.xlsx',sheet_name='report Bi')
a=a[a['ECC - Local Product Status']=='40']
molecules=pd.DataFrame(a['GMD AS ID'].unique())
molecules.columns=['Molecule']
molecules['Molecule1']=molecules['Molecule']

dt_market_data=dm.create_market_data_from_csv()
un_mol_market_data=pd.DataFrame(dt_market_data['Molecule'].unique())
un_mol_market_data.columns=['Molecule']
un_mol_market_data['Molecule1']=un_mol_market_data['Molecule']

diff=molecules.merge(un_mol_market_data,how='left',suffixes=('_internal','_external'),on=('Molecule'))
diff=diff[diff['Molecule1_external']==diff['Molecule1_internal']]


splitted_mol_an=molecules
splitted_mol_an['Molecule']=molecules['Molecule'].apply(lambda x: x.split(' ')[0])
splitted_mol_an['Molecule']=splitted_mol_an['Molecule'].apply(lambda x: x.split('+')[0])

diff_splitted=splitted_mol_an.merge(un_mol_market_data,how='left',suffixes=('_internal','_external'),on=('Molecule'))

diff_splitted=diff_splitted[diff_splitted['Molecule1_external']!=diff_splitted['Molecule1_internal']]

len(diff_splitted[diff_splitted['Molecule1_external']!=diff_splitted['Molecule']].index)