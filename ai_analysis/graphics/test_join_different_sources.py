#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:40:02 2019

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
import pandas as pd

sales_data,anagrafica, market_data,market_data_pb, integration_data,integration_probiotici=ldl.load_data()
data_lineage=ldl.load_data_lineage()
perimeter=ldl.load_market_perimeter_doc()
allData=ds.AllData(anagrafica,sales_data, market_data,market_data_pb, integration_data,integration_probiotici,data_lineage,perimeter)


dpb=allData.market_data_pb.drop(columns=['Company','Product','Brand']).sum()
dpb.index=pd.to_datetime(dpb.index,format='%b-%Y')


t=allData.get_market_for_material('44070376')

t2=allData.get_market_for_material('44070376')

allData.plot_material('44070376')        