#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 14:26:53 2019

@author: arlind
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:58:13 2019

@author: arlind
"""
import ai_analysis.join_data_different_sources as ds
import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QInputDialog,QListWidget
from PyQt5.QtWidgets import QGridLayout, QDesktopWidget
from PyQt5.QtGui import QIcon
 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import ai_analysis.data_loading.load_data_locally as ldl
import ai_analysis.models.prophet_models as pm
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Integration tests'
        self.width = 540
        self.height = 500
        self.material=''
        self.initUI()
    
    def plot_diagram(self,item):       
        pm.model_material(item.text().split('-')[0].strip(),self.allData,show_components=True)    
    def initUI(self):
        self.setWindowTitle(self.title)
        list_w=QListWidget(self)
        sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
        data_lineage=ldl.load_data_lineage()
        perimeter=ldl.load_market_perimeter_doc()
        self.allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,data_lineage,perimeter)
        to_add_items=self.allData.integration['Material'].apply(lambda x:str(x)+'-' )+self.allData.integration['Product'].apply(lambda x:str(x)+'-' ) +self.allData.integration['Pack']
        to_add_items_prob=self.allData.integration_probiotici['Material'].apply(lambda x:str(x)+'-' )+self.allData.integration_probiotici['QlikProduct']
        list_w.addItems(list(to_add_items))
        list_w.addItems(list(to_add_items_prob))
        list_w.itemClicked.connect(self.plot_diagram)
        list_w.resize(400,600)
        self.resize(400,600)
        self.show()
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
