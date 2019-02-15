#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:11:48 2019

@author: arlind
"""
'''
creates a dictionary that contains as keys the old value of Material and as values the new value of Material
grouping by GMD FDF ID, Brand
'''
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_lineage_tools as dlt
import sys
def create_dict_to_replace(anagrafica_to_modify,unique_gmd):
    dict_to_return={}
    for mat in list(anagrafica_to_modify['Material']):
        try:
            dict_to_return[mat]=unique_gmd[(unique_gmd['GMD FDF ID']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['GMD FDF ID'].iloc[0])&(unique_gmd['Brand']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['Brand'].iloc[0])]['Material'].iloc[0]
        except:
            '''ignore for products that have changed id but are not in status 40 or 35'''
            pass
    return dict_to_return     

'''
creates a dictionary that contains as keys the old value of Material and as values the new value of Material
grouping by GMD AS ID, GMD Tot.pack size,Strength - Text,Brand,GMD Dosage Form
'''
def create_dict_to_replace_by_mol_pack_size(anagrafica_to_modify,unique_gmd):
    dict_to_return={}
    for mat in list(anagrafica_to_modify['Material']):
        try:
            dict_to_return[str(mat)]=str(unique_gmd[(unique_gmd['GMD AS ID']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['GMD AS ID'].iloc[0])&(unique_gmd['GMD Tot.pack size']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['GMD Tot.pack size'].iloc[0])&(unique_gmd['Brand']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['Brand'].iloc[0])&(unique_gmd['Strength - Text']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['Strength - Text'].iloc[0])&(unique_gmd['GMD Dosage Form']==anagrafica_to_modify[anagrafica_to_modify['Material']==mat]['GMD Dosage Form'].iloc[0])]['Material'].iloc[0])
        except:
            '''ignore for products that have changed id but are not in status 40 or 35'''
            pass
    return dict_to_return      

'''
the group by in this method is done using the following fields
GMD AS ID, GMD Tot.pack size,Strength - Text,Brand,GMD Dosage Form
'''
def add_history_sales_different_sku(sales_data,anagrafica):  
    anagrafica_dub=anagrafica[anagrafica.duplicated(subset=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'])][['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form']].drop_duplicates()
    anagrafica_to_modify=anagrafica[['Material','ECC - Local Product Status','GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','Descrizione','GMD Dosage Form']].merge(anagrafica_dub,on=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'],how='inner')
    unique_gmd=anagrafica_to_modify[(anagrafica_to_modify['ECC - Local Product Status']=='40')|(anagrafica_to_modify['ECC - Local Product Status']=='35')].groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','ECC - Local Product Status','GMD Dosage Form'],as_index=False)['Material'].min()
    unique_gmd=unique_gmd.merge(unique_gmd.groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','GMD Dosage Form'],as_index=False)['ECC - Local Product Status'].max())
    sales_to_return=sales_data.copy()
    sales_to_return['Material']=sales_to_return['Material'].replace(to_replace=create_dict_to_replace_by_mol_pack_size(anagrafica_to_modify,unique_gmd))
    return sales_to_return.groupby(['Material'],as_index=False).sum()

'''
the group by in this method is done using the following fields
GMD FDF ID, Brand
'''
def add_history_sales_different_sku_by_fdfid(sales_data,anagrafica):
    anagrafica_dub=anagrafica[anagrafica.duplicated(subset=['GMD FDF ID','Brand'])][['GMD FDF ID','Brand']].drop_duplicates()
    anagrafica_to_modify=anagrafica[['Material','GMD FDF ID','Brand','ECC - Local Product Status']].merge(anagrafica_dub,on=['GMD FDF ID','Brand'],how='inner')
    unique_gmd=anagrafica_to_modify[(anagrafica_to_modify['ECC - Local Product Status']=='40')|(anagrafica_to_modify['ECC - Local Product Status']=='35')].groupby(['GMD FDF ID','Brand','ECC - Local Product Status'],as_index=False)['Material'].min()
    unique_gmd=unique_gmd.merge(unique_gmd.groupby(['GMD FDF ID','Brand'],as_index=False)['ECC - Local Product Status'].max())
    sales_data['Material']=sales_data['Material'].replace(to_replace=create_dict_to_replace(anagrafica_to_modify,unique_gmd))
    return sales_data.groupby(['Material'],as_index=False).sum()


def create_lineage_csv(file_path=''):    
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
        
    dataframetosave=pd.DataFrame.from_dict(tosave_dict)
    dataframetosavewithdescription=dataframetosave.rename(columns={'old':'MaterialOld','new':'MaterialNew'}).merge(anagrafica[['Descrizione','Material','GMD FDF ID','Brand']].rename(columns={'Material':'MaterialOld','Descrizione':'DescrizioneOld','GMD FDF ID':'GMD FDF ID old','Brand':'Brand old'})).merge(anagrafica[['Descrizione','Material','GMD FDF ID','Brand']].rename(columns={'Material':'MaterialNew','Descrizione':'DescrizioneNew','GMD FDF ID':'GMD FDF ID new','Brand':'Brand New'}))
    dataframetosavewithdescripitonfiltered=dataframetosavewithdescription[(dataframetosavewithdescription['GMD FDF ID old']!=dataframetosavewithdescription['GMD FDF ID new'])]
    dataframetosavewithdescription.to_csv(path_or_buf=file_path+'AllTransformations.csv',sep=';')
    dataframetosavewithdescripitonfiltered.to_csv(path_or_buf=file_path+'ParticularCases.csv',sep=';')

if __name__ == "__main__":    
    path=''if len(sys.argv)<=1 else sys.argv[1]
    create_lineage_csv(file_path=path)

