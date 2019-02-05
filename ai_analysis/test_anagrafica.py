#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 09:49:13 2019

@author: arlind
"""
import ai_analysis.anagrafica as an
 
anagrafica=an.create_anagrafica(3, file='AllData/anagrafica_AI.xlsx',sheet_name='report Bi')

onlyneededcolumns=a[['GMD FDF ID','Brand','Descrizione','Material','GMD AS ID','GMD Tot.pack size','Ind. Std Desc.','Strength - Text']]
onlyneededcolumnscon=onlyneededcolumns.groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand']).apply(lambda x: x.sum())

onlyneededcolumnsfil=onlyneededcolumnscon[onlyneededcolumnscon['GMD FDF ID'].apply(lambda x: len(str(x))>6)]

onlyv1=onlyneededcolumns[onlyneededcolumns['Descrizione'].apply(lambda x: 'V1'in x)]

joined=onlyneededcolumns.merge(onlyv1,how='inner',suffixes=('_x', '_y'),on=['GMD FDF ID','Brand'])

gmd1=joined.groupby(['GMD FDF ID','Brand'],as_index=False).count()

tocheck=gmd1[gmd1['Descrizione_x']==1]


mol_dosage=a[['GMD AS ID','GMD Dosage Form']].drop_duplicates()

dosage_form=pd.DataFrame(a[a['ECC - Local Product Status']=='40']['GMD Dosage Form'].unique())


a=a.sort_values(by='Material')
subset=a[a.duplicated(subset=['GMD FDF ID','Brand'])]

subt=subset[(subset['Material']=='44062070') | (subset['Material']=='44067807') | (subset['Material']=='44070378') | (subset['Material']=='44057383') | (subset['Material']=='44000735') | (subset['Material']=='44058951') | (subset['Material']=='44012619' )|  (subset['Material']=='44060859')]



anagrafica_dub=anagrafica[anagrafica.duplicated(subset=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand'])][['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand']].drop_duplicates()
anagrafica_to_modify=anagrafica[['Material','ECC - Local Product Status','GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','Descrizione']].merge(anagrafica_dub,on=['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand'],how='inner')
unique_gmd=anagrafica_to_modify[(anagrafica_to_modify['ECC - Local Product Status']=='40')|(anagrafica_to_modify['ECC - Local Product Status']=='35')].groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand','ECC - Local Product Status'],as_index=False)['Material'].min()
unique_gmd=unique_gmd.merge(unique_gmd.groupby(['GMD AS ID', 'GMD Tot.pack size','Strength - Text','Brand'],as_index=False)['ECC - Local Product Status'].max())
sales_data['Material']=sales_data['Material'].replace(to_replace=create_dict_to_replace(anagrafica_to_modify,unique_gmd))
    return sales_data.groupby(['Material'],as_index=False).sum()