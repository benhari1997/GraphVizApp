import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tools.graphPrep import fromFileToNetwork
from Lib.drawData import draw3Dgraph, draw2Dgraph, drawPlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VTKGraph(QWidget):
    
    def __init__(self, parent, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        # initial parameters
        self.parent = parent
        self.vl = QGridLayout()
        
        #==============================

        # vtk visualisation :
        ## create frames
        self.frame2D = QFrame()
        self.frame3D = QFrame()
        
        ## create vtk widgets
        self.vtkWidget2D = QVTKRenderWindowInteractor(self.frame2D)
        self.vtkWidget3D = QVTKRenderWindowInteractor(self.frame3D)

        ## create vtk sub-tabs
        self.graphTabs = QTabWidget()
        self.gTab2D = self.vtkWidget2D
        self.gTab3D = self.vtkWidget3D

        ## Add tabs
        self.graphTabs.addTab(self.gTab3D,"3D Visualisation")
        self.graphTabs.addTab(self.gTab2D,"2D Oriented Visualisation")

        ## Create renderer and interactor 3D
        self.ren3D = vtk.vtkRenderer()
        self.vtkWidget3D.GetRenderWindow().AddRenderer(self.ren3D)
        self.iren3D = self.vtkWidget3D.GetRenderWindow().GetInteractor()
        
        ## Initialize interactor 3D
        self.ren3D.ResetCamera()
        self.iren3D.Initialize()

        ## Create renderer and interactor 2D
        self.ren2D = vtk.vtkGraphLayoutView()
        self.vtkWidget2D.GetRenderWindow().AddRenderer(self.ren2D.GetRenderer())
        self.iren2D = self.vtkWidget2D.GetRenderWindow().GetInteractor()

        # Initialize interactor 2D
        self.ren2D.ResetCamera()
        self.iren2D.Initialize()

        #==============================

        # Statistics group visualisation
        ## create the group
        self.stats = QGroupBox("Statistics :")
        statsBoxLayout = QVBoxLayout()

        ## add first sub-group
        self.statplot = QGroupBox("Degrees distribution :")

        ### Prepare figure & canvas for the plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        ### create sub-group layout 
        plotBoxLayout = QVBoxLayout()
        plotBoxLayout.addWidget(self.canvas)
        self.statplot.setLayout(plotBoxLayout)

        ## add second sub-group
        self.infos = QGroupBox("Statistical Infos :")
        infoBoxLayout = QVBoxLayout()

        ### add labels
        self.nbrWords = QLabel("<b>Number of distinct words :</b>  <i>12</i>")
        infoBoxLayout.addWidget(self.nbrWords)

        self.nbrEdges = QLabel("<b>Number of edges found :</b>  <i>6</i>")
        infoBoxLayout.addWidget(self.nbrEdges)

        ### add layout
        self.infos.setLayout(infoBoxLayout)

        # add widgets & layouts to the main group
        statsBoxLayout.addWidget(self.infos)
        statsBoxLayout.addWidget(self.statplot)
        self.stats.setLayout(statsBoxLayout)

        #==============================

        # Filters group visualisation
        ## create the group
        self.filters = QGroupBox("Filters :")
        filterLayout = QVBoxLayout()
        
        ### create search sub-group
        self.searchGroup = QGroupBox("Search by word :")
        searchBoxLayout = QVBoxLayout()

        self.searchBar = QLineEdit()
        searchBoxLayout.addWidget(self.searchBar)

        searchButton = QPushButton("Display results :")
        searchBoxLayout.addWidget(searchButton)
        searchButton.clicked.connect(self.updateOverallGraphs)

        ### add layout
        self.searchGroup.setLayout(searchBoxLayout)

        ### create the display method sub-group
        self.dispMGroup = QGroupBox("Select Display Method :")
        dispMBoxLayout = QHBoxLayout()

        self.dispMbutton1 = QRadioButton("Spring")
        dispMBoxLayout.addWidget(self.dispMbutton1)
        self.dispMbutton1.toggled.connect(self.updateOverallGraphs)
        self.dispMbutton1.setChecked(True)

        self.dispMbutton2 = QRadioButton("Planar")
        dispMBoxLayout.addWidget(self.dispMbutton2)
        self.dispMbutton2.toggled.connect(self.updateTo3D)

        self.dispMbutton3 = QRadioButton("Atlas")
        dispMBoxLayout.addWidget(self.dispMbutton3)
        self.dispMbutton3.toggled.connect(self.updateTo3D)

        self.dispMbutton4 = QRadioButton("Kamada-ka")
        dispMBoxLayout.addWidget(self.dispMbutton4)
        self.dispMbutton4.toggled.connect(self.updateTo3D)

        ### add layout
        self.dispMGroup.setLayout(dispMBoxLayout)

        ### create the number of steps choice sub-group
        self.dispTGroup = QGroupBox("Number of steps to display :")
        dispTBoxLayout = QHBoxLayout()

        self.dispTLabel = QLabel("Select number of steps to display :")
        dispTBoxLayout.addWidget(self.dispTLabel)

        self.dispTSpin = QSpinBox()
        self.dispTSpin.setRange(0,4)
        self.dispTSpin.setValue(0)
        dispTBoxLayout.addWidget(self.dispTSpin)
        self.dispTSpin.valueChanged.connect(self.updateOverallGraphs)

        ### add layout
        self.dispTGroup.setLayout(dispTBoxLayout)

        ## add the widgets to the group
        filterLayout.addWidget(self.searchGroup)
        filterLayout.addWidget(self.dispMGroup)
        filterLayout.addWidget(self.dispTGroup)

        ## add layout 
        self.filters.setLayout(filterLayout)

        #==============================

        # Add all layouts and groups to the main Layout
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.filters)
        vLayout.addWidget(self.stats)

        self.vl.addLayout(vLayout, 0, 0, 2, 2)
        self.vl.addWidget(self.graphTabs, 0, 3, 1, 1)

    #
    # vtk Tab trigger functions :
    #
        
    def getMethod(self):
        """ Returns the chosen method.
        """
        if self.dispMbutton1.isChecked():
            return self.dispMbutton1.text()
        elif self.dispMbutton2.isChecked():
            return self.dispMbutton2.text()
        elif self.dispMbutton3.isChecked():
            return self.dispMbutton3.text()
        else:
            return self.dispMbutton4.text()

    def updateInsights(self, nbEdges, nbNodes):
        """ Updates graph infos.
        """
        self.nbrWords.setText(
            f"<b>Number of distinct words :</b>  <i>{nbNodes}</i>")
        self.nbrEdges.setText(
            f"<b>Number of edges found :</b>  <i>{nbEdges}</i>")
        
    def updateTo3D(self):
        """ Updates the 3D graph based
            on the user inputs.
        """
        # Displayed words
        words = self.searchBar.text().split(',')

        # Reset actors
        for actor in  self.ren3D.GetActors():
            self.ren3D.RemoveActor(actor)
        
        # New data
        if len(words[0])!=0:
            self.source, self.graphData = fromFileToNetwork(path=self.parent.tabParent.path,
                                                             method=self.getMethod(),
                                                             words=words,
                                                             maxStep=self.dispTSpin.value())

        else:
            self.source, self.graphData = fromFileToNetwork(path=self.parent.tabParent.path,
                                                             method=self.getMethod())
        self.actors = draw3Dgraph(self.source)

        # update stats & plots
        drawPlot(self.figure, self.canvas, self.graphData[0])

        # update graph infos:
        self.updateInsights(self.graphData[1], self.graphData[2])
        
        # Add Actors to renderer
        for actor in self.actors:
            self.ren3D.AddActor(actor)
        
        # reinitialise view
        self.iren3D.ReInitialize()
        self.ren3D.ResetCamera()
        
        # get the current network to the parent tab
        self.parent.tabParent.networkData = self.source

    def updateTo2D(self):
        """ Updates the 2D graph based
            on the user inputs.
        """
        # Displayed words
        words = self.searchBar.text().split(',')
        
        # New data
        if len(words[0])!=0:
            self.source, self.graphData = fromFileToNetwork(dim=2,
                                                             path=self.parent.tabParent.path,
                                                             words=words,
                                                             maxStep=self.dispTSpin.value())

        else:
            self.source, self.graphData = fromFileToNetwork(dim=2,
                                                             path=self.parent.tabParent.path)

        # remove existing renderers
        for renderer in self.vtkWidget2D.GetRenderWindow().GetRenderers():
            self.vtkWidget2D.GetRenderWindow().RemoveRenderer(renderer)

        # update renderer
        self.ren2D = draw2Dgraph(self.source)
        self.vtkWidget2D.GetRenderWindow().AddRenderer(self.ren2D.GetRenderer())
        
        # reinitialise view
        self.ren2D.ResetCamera()
        self.iren2D = self.ren2D.GetInteractor()

    def updateOverallGraphs(self):
        """ An overall graph update.
        """
        # update graphs visualisation
        self.updateTo3D()
        self.updateTo2D()
