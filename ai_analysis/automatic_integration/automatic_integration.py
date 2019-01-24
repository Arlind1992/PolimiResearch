#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:28:05 2019

@author: arlind
"""
from openpyxl import load_workbook
import pandas as pd
import ai_analysis.anagrafica as an
import ai_analysis.data_market as md
import ai_analysis.automatic_integration.integration_utils as iu


wb=load_workbook(filename='ai_analysis/Integration.xlsx')
pack_dataframe_tct=iu.create_df_fromsheet(wb['Dosage Form'],1)
molecule_dataframe_tct=iu.create_df_fromsheet(wb['Molecule'],1)
molecule_dataframe_tct=molecule_dataframe_tct[ molecule_dataframe_tct['external'].notnull()][['external','internal']]
anagrafica=an.create_anagrafica(1, file='Supply&Demand/anagrafica_AI_moreInfo.xlsx',sheet_name='needed')
anagrafica=iu.transform_anagrafica(anagrafica)
market_data=md.create_market_data_from_csv(filepath='Market Data/OnlyNecDataSubsetMolecules.csv',separator=';')
market_data=iu.trasform_market_data(market_data)

anagrafica_external_mol=anagrafica.merge(molecule_dataframe_tct.rename(columns={'internal':'GMD AS ID'}),how='inner',on='GMD AS ID')
anagrafica_external_mol_pack=anagrafica_external_mol.merge(pack_dataframe_tct.rename(columns={'internal':'GMD Dosage Form'}),how='inner',on='GMD Dosage Form')

anagrafica_external_mol_pack['ContainerSize']=anagrafica_external_mol_pack.apply(lambda x: x.Nome[int(x.Nome.find(x.short))-2:int(x.Nome.find(x.short))].strip(),axis=1)

anagrafica_join_market=anagrafica_external_mol_pack.rename(columns={'external_x':'Molecule','external_y':'PackType'}).merge(market_data,how='inner',on=['Molecule','PackType'])
anagrafica_join_market=anagrafica_join_market[((anagrafica_join_market['Name Type']=='NOME AZIENDA+NOME MOLECOLA')&(anagrafica_join_market['Brand']==anagrafica_join_market['BrandOwner']))|(anagrafica_join_market['Name Type']!='NOME AZIENDA+NOME MOLECOLA')]
anagrafica_join_market_1=anagrafica_join_market[anagrafica_join_market.apply(lambda x: x.Size.replace('µg','Y') in x.PackSize and x.ContainerSize in x.PackSize,axis=1) ]

iu.save_to_csv(anagrafica_join_market_1)

anagrafica_join_market_2=iu.dataframe_differences(anagrafica_join_market,anagrafica_join_market_1['Material'],'Material')
anagrafica_join_market_2=anagrafica_join_market_2[anagrafica_join_market_2['ECC - Local Product Status']=='40']