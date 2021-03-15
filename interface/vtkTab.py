import vtk
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from tools.txtToVtk import fromFileToNetwork
from tools.drawGraph import draw3Dgraph, draw2Dgraph, drawPlot
from tools.interactor import InteractorStyle
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

        ###
        # Create vtk widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        
        # Create renderer and interactor
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        
        # Initialize interactor
        self.ren.ResetCamera()
        self.iren.Initialize()

        ###
        self.stats = QGroupBox("Statistics :")
        statsBoxLayout = QVBoxLayout()
        
        # Prepare figure canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        statsBoxLayout.addWidget(self.canvas)
        self.stats.setLayout(statsBoxLayout)

        ###
        self.filters = QGroupBox("Filters :")
        filterLayout = QVBoxLayout()
        ##
        self.searchGroup = QGroupBox("Search by word :")
        searchBoxLayout = QVBoxLayout()

        self.searchBar = QLineEdit()
        searchBoxLayout.addWidget(self.searchBar)

        searchButton = QPushButton("Display results :")
        searchBoxLayout.addWidget(searchButton)
        searchButton.clicked.connect(self.updateDisplay)

        self.searchGroup.setLayout(searchBoxLayout)

        ##
        self.dispMGroup = QGroupBox("Select Display Method :")
        dispMBoxLayout = QHBoxLayout()

        self.dispMbutton1 = QRadioButton("Spring")
        dispMBoxLayout.addWidget(self.dispMbutton1)
        self.dispMbutton1.toggled.connect(self.updateDisplay)
        self.dispMbutton1.setChecked(True)

        self.dispMbutton2 = QRadioButton("Planar")
        dispMBoxLayout.addWidget(self.dispMbutton2)
        self.dispMbutton2.toggled.connect(self.updateDisplay)

        self.dispMbutton3 = QRadioButton("Atlas")
        dispMBoxLayout.addWidget(self.dispMbutton3)
        self.dispMbutton3.toggled.connect(self.updateDisplay)

        self.dispMbutton4 = QRadioButton("Kamada-ka")
        dispMBoxLayout.addWidget(self.dispMbutton4)
        self.dispMbutton4.toggled.connect(self.updateDisplay)

        self.dispMGroup.setLayout(dispMBoxLayout)

        ## 
        self.dispTGroup = QGroupBox("Select Display type :")
        dispTBoxLayout = QHBoxLayout()

        self.dispTbutton1 = QRadioButton("Non oriented - Scaled")
        dispTBoxLayout.addWidget(self.dispTbutton1)
        self.dispTbutton1.setChecked(False)

        self.dispTbutton2 = QRadioButton("Oriented - Unscaled")
        dispTBoxLayout.addWidget(self.dispTbutton2)

        self.dispTGroup.setLayout(dispTBoxLayout)

        ###
        filterLayout.addWidget(self.searchGroup)
        filterLayout.addWidget(self.dispMGroup)
        filterLayout.addWidget(self.dispTGroup)

        self.filters.setLayout(filterLayout)
        ###
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.filters)
        vLayout.addWidget(self.stats)

        self.vl.addLayout(vLayout, 0, 0, 2, 2)
        self.vl.addWidget(self.vtkWidget, 0, 3, 1, 1)
    
    def updateMethod(self):
        if self.dispMbutton1.isChecked():
            return self.dispMbutton1.text()
        elif self.dispMbutton2.isChecked():
            return self.dispMbutton2.text()
        elif self.dispMbutton3.isChecked():
            return self.dispMbutton3.text()
        else:
            return self.dispMbutton4.text()
    
    def getDim(self):
        if self.dispMbutton1.isChecked():
            return 2
        return 2
    def updateDisplay(self):
        # Displayed words
        words = self.searchBar.text().split(',')

        # Reset actors
        for actor in  self.ren.GetActors():
            self.ren.RemoveActor(actor)
        
        # New data
        if len(words[0])!=0:
            self.source, self.degreeData = fromFileToNetwork(dim=self.getDim(),
                                                             path=self.parent.tabParent.path,
                                                             method=self.updateMethod(),
                                                             words=words)

        else:
            self.source, self.degreeData = fromFileToNetwork(dim=self.getDim(),
                                                             path=self.parent.tabParent.path,
                                                             method=self.updateMethod())
        renderer = draw2Dgraph(self.source)

        # update stats plot
        drawPlot(self.figure, self.canvas, self.degreeData)
        
        # Add Actors to renderer
        """
        for actor in self.actors:
            self.ren.AddActor(actor)
        style = InteractorStyle(self.glyph, self.ren, self.source)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)
        """
        # reinitialise view
        self.ren = renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren.GetRenderer())
        self.ren.ResetCamera()
        self.iren= self.vtkWidget.GetRenderWindow().GetInteractor()