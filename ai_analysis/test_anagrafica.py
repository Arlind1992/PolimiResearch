#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 09:49:13 2019

@author: arlind
"""
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_lineage_tools as dlt


anagrafica=an.create_anagrafica(3, file='AllData/anagrafica_AI.xlsx',sheet_name='report Bi')
anagrafica_dub=anagrafica[anagrafica.duplicated(subset=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'])][['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form']].drop_duplicates()
anagrafica_to_modify=anagrafica[['Material','ECC - Local Product Status','GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','Descrizione','GMD Dosage Form']].merge(anagrafica_dub,on=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'],how='inner')
unique_gmd=anagrafica_to_modify[(anagrafica_to_modify['ECC - Local Product Status']=='40')|(anagrafica_to_modify['ECC - Local Product Status']=='35')].groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','ECC - Local Product Status','GMD Dosage Form'],as_index=False)['Material'].min()
unique_gmd=unique_gmd.merge(unique_gmd.groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'],as_index=False)['ECC - Local Product Status'].max())
to_replace=dlt.create_dict_to_replace_by_mol_pack_size(anagrafica_to_modify,unique_gmd)
tosave_dict={'old':[''],'new':['']}

for x in to_replace.keys():
    tosave_dict['old'].append(x)
    tosave_dict['new'].append(to_replace[x])

if __name__ == "__main__":    
    dataframetosave=pd.DataFrame.from_dict(tosave_dict)
    dataframetosavewithdescription=dataframetosave.rename(columns={'old':'MaterialOld','new':'MaterialNew'}).merge(anagrafica[['Descrizione','Material','GMD FDF ID','Brand']].rename(columns={'Material':'MaterialOld','Descrizione':'DescrizioneOld','GMD FDF ID':'GMD FDF ID old','Brand':'Brand old'})).merge(anagrafica[['Descrizione','Material','GMD FDF ID','Brand']].rename(columns={'Material':'MaterialNew','Descrizione':'DescrizioneNew','GMD FDF ID':'GMD FDF ID new','Brand':'Brand New'}))
    dataframetosavewithdescripiton=dataframetosavewithdescription[(dataframetosavewithdescription['GMD FDF ID old']!=dataframetosavewithdescription['GMD FDF ID new'])]
    dataframetosavewithdescription.to_csv(path_or_buf='data_lineage/AllTransformations.csv',sep=';')
    dataframetosavewithdescripiton.to_csv(path_or_buf='data_lineage/ParticularCases.csv',sep=';')
