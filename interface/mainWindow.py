from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import vtk
import os
import sys
import networkx as nx 
from interface.txtTab import TextEditor
from interface.vtkTab import VTKGraph

class TableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = TextEditor(self)
        self.tab2 = VTKGraph(self)
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Text Editor")
        self.tabs.addTab(self.tab2,"Graph Visualisation")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)

        self.tab1.setLayout(self.tab1.tl)

        #self.tab2.layout.addWidget(self.tab2.frame)
        self.tab2.setLayout(self.tab2.vl)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)






        

