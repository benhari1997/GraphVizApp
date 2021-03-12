import vtk
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from tools.txtToVtk import fromFileToNetwork
from tools.drawGraph import draw3Dgraph, draw2Dgraph

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

class VTKGraph(QWidget):
    
    def __init__(self, parent, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.frame = QFrame()
 
        self.vl = QGridLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)

        self.filters = QGroupBox("Filters :")
        filterLayout = QVBoxLayout()
        ##
        self.searchGroup = QGroupBox("Search by word :")
        searchBoxLayout = QVBoxLayout()

        searchBar = QLineEdit()
        searchBoxLayout.addWidget(searchBar)

        searchButton = QPushButton("Search")
        searchBoxLayout.addWidget(searchButton)
        searchButton.clicked.connect(self.searchNode)

        self.searchGroup.setLayout(searchBoxLayout)

        ##
        self.dispMGroup = QGroupBox("Select Display Method :")
        dispMBoxLayout = QHBoxLayout()

        dispMbutton1 = QRadioButton("Planar")
        dispMBoxLayout.addWidget(dispMbutton1)

        dispMbutton2 = QRadioButton("Spring")
        dispMBoxLayout.addWidget(dispMbutton2)

        dispMbutton3 = QRadioButton("Atlas")
        dispMBoxLayout.addWidget(dispMbutton3)

        dispMbutton4 = QRadioButton("Kamada-ka")
        dispMBoxLayout.addWidget(dispMbutton4)

        self.dispMGroup.setLayout(dispMBoxLayout)

        ## 
        self.dispTGroup = QGroupBox("Select Display type :")
        dispTBoxLayout = QHBoxLayout()

        dispTButton1 = QRadioButton("Non oriented - Scaled")
        dispTBoxLayout.addWidget(dispTButton1)

        dispTButton2 = QRadioButton("Oriented - Unscaled")
        dispTBoxLayout.addWidget(dispTButton2)

        self.dispTGroup.setLayout(dispTBoxLayout)

        ###
        filterLayout.addWidget(self.searchGroup)
        filterLayout.addWidget(self.dispMGroup)
        filterLayout.addWidget(self.dispTGroup)

        self.filters.setLayout(filterLayout)
        #
        ###

        self.stats = QGroupBox("Statistics :")
        statsBoxLayout = QVBoxLayout()

        ##
        figure = Figure()
        canvas = FigureCanvas(figure)
        statsBoxLayout.addWidget(canvas)

        
        #####################

        data = [random.random() for i in range(10)]

        # create an axis
        ax = figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        canvas.draw()

        #####################
        self.stats.setLayout(statsBoxLayout)
        #
        ###
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.filters)
        vLayout.addWidget(self.stats)

        self.vl.addLayout(vLayout, 0, 0, 2, 2)
        self.vl.addWidget(self.vtkWidget, 0, 3, 1, 1)

        # Create renderer and interactor
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source & actors
        self.source = fromFileToNetwork(dim=3, words=["brain", "motion", "domain"])
        self.actors = draw3Dgraph(self.source)

        # Add Actors to renderer
        self.ren.AddActor(self.actors[0])
        self.ren.AddActor(self.actors[1])
 
        self.ren.ResetCamera()
        self.iren.Initialize()
    
    def searchNode(self):
        self.iren.ReInitialize()
        self.source = fromFileToNetwork(dim=3, word=["brain"])
