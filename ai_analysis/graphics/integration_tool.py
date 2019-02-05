#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:58:13 2019

@author: arlind
"""
import ai_analysis.join_data_different_sources as ds
import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QInputDialog,QListWidget
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        
        self.title = 'Integration tests'
        self.width = 540
        self.height = 500
        self.material=''
        self.initUI()
    
    def plot_diagram(self,item):       
        ds.plot_material(item.text().split('-')[0].strip()) 
            
    def initUI(self):
        self.setWindowTitle(self.title)
        list_w=QListWidget(self)
        to_add_items=ds.integration['Material'].apply(lambda x:str(x)+'-' )+ds.integration['Product'].apply(lambda x:str(x)+'-' ) +ds.integration['Pack']
        to_add_items_prob=ds.integration_probiotici['Material'].apply(lambda x:str(x)+'-' )+ds.integration_probiotici['QlikProduct']
        list_w.addItems(list(to_add_items))
        list_w.addItems(list(to_add_items_prob))
        list_w.itemClicked.connect(self.plot_diagram)
        list_w.resize(400,600)
        '''
        button = QPushButton('Show material', self)
        button.setToolTip('Add material')
        button.move(0,0)
        button.resize(140,100)
        button.clicked.connect(self.showDialog)
        '''
        self.resize(400,600)
        self.show()
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    


'''
materials=['44068397','44083137','44058838']'''