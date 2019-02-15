#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 12:31:53 2019

@author: arlind
"""
import pandas as pd
import ai_analysis.transform_data as td
import ai_analysis.data_market as dm

class AllData:
    '''
    integration_join_anagrafica=anagrafica.merge(integration,how='inner',on='Material')
    integration_join_anagrafica=integration_join_anagrafica[integration_join_anagrafica['ECC - Local Product Status']=='40']
    '''
    def __init__(self,anagrafica,sales_data,market_data,market_data_pb,integration_data,integration_probiotici,lineage,market_perimeter):
        self.anagrafica=anagrafica
        self.sales_data=sales_data
        self.market_data=dm.remove_dupplicates(market_data)
        self.integration=integration_data
        self.integration_probiotici=integration_probiotici
        self.market_data_pb=market_data_pb
        self.data_lineage=lineage
        self.market_perimeter=market_perimeter
        self.sales_data=self.add_history_sales_different_sku(self.sales_data)
        
    def plot_for_material_probiotico(self,material):
        sales_data_filtered_pb=self.sales_data[self.sales_data['Material']==str(material)]
        integration_filtered_pb=self.integration_probiotici[self.integration_probiotici['Material'].astype(str)==material]
        market_data_filtered_pb=self.market_data_pb[(self.market_data_pb['Company']=='SANDOZ-HEXAL') & (self.market_data_pb['Product']==integration_filtered_pb['QlikProduct'].iloc[0])]
        ts_sales_data_pb=td.tras_sales_data(sales_data_filtered_pb)
        ts_market_data_pb=td.tras_market_data_probiotici(market_data_filtered_pb)
        ts_market_data_pb[ts_market_data_pb.columns.values[0]]=ts_market_data_pb[ts_market_data_pb.columns.values[0]].apply(lambda x: float(str(x).replace(',','.')))
        market_data_pb_bymolecule=self.market_data_pb.drop(columns=['Company','Product','Brand']).sum()
        market_data_pb_bymolecule.index=pd.to_datetime(market_data_pb_bymolecule.index,format='%b-%Y')
        market_data_pb_bymolecule.sort_index().plot(title='Whole Market Data')
        ts_sales_data_pb.join(ts_market_data_pb).plot(title='Sales-Market')
    
    def remove_initial_zeros(self,series_tofilter):
        def get_first_non_zero_value(series_tocheck):
            for i in range(0,series_tocheck.size):
                try:
                    if series_tocheck.iloc[i]!=0:
                        return i
                except:
                    if series_tocheck.iloc[i][series_tocheck.columns[0]]!=0:
                        return i
            return i    
        return series_tofilter.iloc[get_first_non_zero_value(series_tofilter):]
    def plot_for_material(self,material):
        ts_market_data_by_molecule,ts_sales_data,ts_market_data,stock_changes=self.get_dataframes_for_material(material)
        '''stock_changes.plot(title='Stock changes')'''
        ts_market_data_by_molecule.plot(title='Whole market')
        ts_sales_data.join(ts_market_data).plot(title='Sales-Market')
    '''
    returns three different dataframes in correspondence with the material code received as input
    the dataframes are in the following order wholemarket, internalsales, externalsales
    '''
    def get_dataframes_for_material(self,material):
        sales_data_filtered=self.sales_data[self.sales_data['Material']==material]
        integration_filtered=self.integration[self.integration['Material'].astype(str)==material]
        market_data_filtered=self.market_data[(self.market_data['Manufacturer']=='SANDOZ') & (self.market_data['Product']==integration_filtered['Product'].iloc[0])& (self.market_data['Pack']==integration_filtered['Pack'].iloc[0])]
        ts_sales_data=td.tras_sales_data(sales_data_filtered)
        ts_market_data=td.tras_market_data(market_data_filtered).astype(float)
        ts_market_data_by_molecule=self.get_market_for_material(material)
        ts_market_data_by_molecule.index=pd.to_datetime(ts_market_data_by_molecule.index,format='%d/%m/%Y')
        stock_changes=ts_sales_data[ts_sales_data.columns[0]].subtract(ts_market_data[ts_market_data.columns[0]]).dropna()
        return self.remove_initial_zeros(ts_market_data_by_molecule.sort_index()),self.remove_initial_zeros(ts_sales_data),self.remove_initial_zeros(ts_market_data),stock_changes    
    
    def get_market_for_material(self,material):
        market_data_competitor=dm.get_market_competitor_data_by_material(material,self.market_data,self.integration,self.market_perimeter)
        market_data_by_molecule=market_data_competitor.drop(columns=['Manufacturer','Product','Pack','Anatomical Therapeutic Class 4','Molecule','Key'])
        market_data_by_molecule[market_data_by_molecule.columns]=market_data_by_molecule[market_data_by_molecule.columns].astype(float)
        market_data_by_molecule=market_data_by_molecule.sum()
        return market_data_by_molecule.T
    
    def plot_material(self,material):
        if(int(material) in list(self.integration_probiotici['Material'])):
            self.plot_for_material_probiotico(material)
        else:
            self.plot_for_material(material)
    
    def add_history_sales_different_sku(self,sales_data):  
        sales_data['Material']=sales_data['Material'].replace(to_replace=self.transform_data_lineage())
        return sales_data.groupby(['Material'],as_index=False).sum()
    
    def transform_data_lineage(self):
        return {str(row['MaterialOld']):str(row['MaterialNew']) for index,row in self.data_lineage.iterrows()}
    
    
    