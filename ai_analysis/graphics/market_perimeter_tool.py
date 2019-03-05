#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:27:01 2019

@author: arlind
"""
   
    
import ai_analysis.join_data_different_sources as ds
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QInputDialog,QListWidget
from PyQt5.QtWidgets import QGridLayout, QDesktopWidget
from PyQt5.QtGui import QIcon
 
 
import ai_analysis.data_loading.load_data_locally as ldl

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Market Parameter Tool'
        self.width = 540
        self.height = 500
        self.material=''
        self.dialogs = list()
        self.initUI()
    
    def divide_market_by_product(self,market):
        divided_market=market.drop(columns=['Pack','Anatomical Therapeutic Class 4','Molecule','Key'])
        divided_market.index=divided_market['Product']+'-'+divided_market['Manufacturer']
        divided_market=divided_market.drop(columns=['Product','Manufacturer'])
        divided_market[divided_market.columns]=divided_market[divided_market.columns].astype(float)
        divided_market=divided_market.groupby(divided_market.index).sum()
        self.divided_market=divided_market
        
    def get_perimeter_for_key(self,market_data,perimeter,key):
        market_data['Key']=market_data['Product'] + ' '+market_data['Pack']
        market_data_perimeter_filtered=market_data.merge(perimeter[perimeter['Key']==key],how='inner',on='Key')
        market_by_molecule=perimeter[(perimeter['Mkt Molecola']==market_data_perimeter_filtered['Mkt Molecola'].iloc[0])]
        if str(market_data_perimeter_filtered['Special Market'].iloc[0])!='nan':
           perimeter_to_join_by=perimeter[perimeter['Special Market']==market_data_perimeter_filtered['Special Market'].iloc[0]]
        else:
           perimeter_to_join_by=perimeter[(perimeter['Mkt Molecola']==market_data_perimeter_filtered['Mkt Molecola'].iloc[0])&(perimeter['Special Market'].isnull())] 
        to_return=market_data.merge(perimeter_to_join_by['Key'].to_frame(),how='inner',on='Key')
        by_molecule=market_data.merge(market_by_molecule['Key'].to_frame(),how='inner',on='Key')
        return to_return,by_molecule
    
    def show_products(self,item):
        self.divide_market_by_product(self.selected_market)
        window=QMainWindow()
        list_w=QListWidget(window)
        list_w.addItems(list(self.divided_market.index))  
        list_w.resize(400,600)
        list_w.itemClicked.connect(self.plot_diagram_product)
        window.resize(400,600)
        self.dialogs.append(window)
        divided_market_to_plot=self.divided_market.T
        divided_market_to_plot.index=pd.to_datetime(divided_market_to_plot.index,format='%d/%m/%Y')
        divided_market_to_plot.plot()
        window.show()
    def plot_diagram_product(self,item):       
        divided_market_to_plot=self.divided_market.T
        divided_market_to_plot.index=pd.to_datetime(divided_market_to_plot.index,format='%d/%m/%Y')
        df=divided_market_to_plot[item.text().strip()].to_frame()
        df.plot()
    
    def plot_diagram(self,item):       
        to_return,bymolecule=self.get_perimeter_for_key(self.market_data,self.perimeter,item.text().strip())
        self.selected_market=to_return
        to_return=to_return.drop(columns=['Manufacturer','Product','Pack','Anatomical Therapeutic Class 4','Molecule','Key'])
        to_return[to_return.columns]=to_return[to_return.columns].astype(float)
        to_return=to_return.sum()
        to_return=to_return.T
        to_return.index=pd.to_datetime(to_return.index,format='%d/%m/%Y')
        to_return.sort_index().plot(title='Market by perimeter')
        bymolecule=bymolecule.drop(columns=['Manufacturer','Product','Pack','Anatomical Therapeutic Class 4','Molecule','Key'])
        bymolecule[bymolecule.columns]=bymolecule[bymolecule.columns].astype(float)
        bymolecule=bymolecule.sum()
        bymolecule=bymolecule.T
        bymolecule.index=pd.to_datetime(to_return.index,format='%d/%m/%Y')
        new_series_toprint=bymolecule.sort_index().copy()
        new_series_toprint.plot(title='Market by molecule')
        self.show_products(item)
        
    def initUI(self):
        self.setWindowTitle(self.title)
        list_w=QListWidget(self)
        self.market_data=ldl.load_market_data()
        self.perimeter=ldl.load_market_perimeter_doc()
        market_data_sandoz=self.market_data[(self.market_data['Manufacturer']=='SANDOZ')&(self.market_data['01/9/2018']!=0)&(self.market_data['01/10/2018']!=0)&(self.market_data['01/11/2018']!=0)]   
        to_add_items=(market_data_sandoz['Product']+ ' '+market_data_sandoz['Pack'])
        list_w.addItems(list(to_add_items.sort_values()))
        list_w.itemClicked.connect(self.plot_diagram)
        list_w.resize(400,600)
        self.resize(400,600)
        self.show()
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())