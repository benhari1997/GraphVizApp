import vtk
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

def draw3Dgraph(source):
    
    # Generate the cone for the glyphs
    sph = vtk.vtkSphereSource()
    sph.SetRadius(1)

    # Set up the glyph filter
    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(source)
    glyph.SetSourceConnection(sph.GetOutputPort())
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()

    # Tell the filter to "clamp" the scalar range
    glyph.ClampingOn()  
    glyph.GeneratePointIdsOn()
    # Set the overall (multiplicative) scaling factor
    glyph.SetScaleFactor(1)

    # Set the Range to "clamp" the data to on
    glyph.SetRange(0, 150)

    # Tell glyph which attribute arrays to use for what
    glyph.SetInputArrayToProcess(0,0,0,0,'degree')		# colors using scalar values
    glyph.SetInputArrayToProcess(1,0,0,0,'vect')		# colors using scalar values

    # Calling update because I'm going to use the scalar range to set the color map range
    glyph.Update()

    # Create tube filter
    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputData(source)
    tubeFilter.SetRadius(0.0015)
    tubeFilter.SetNumberOfSides(50)
    tubeFilter.Update()

    # Create data mapper
    glyphMapper = vtk.vtkPolyDataMapper()
    glyphMapper.SetInputConnection(glyph.GetOutputPort())
    glyphMapper.SetScalarModeToUsePointFieldData()
    glyphMapper.SetColorModeToMapScalars()
    glyphMapper.ScalarVisibilityOn()
    glyphMapper.SetScalarRange(glyph.GetOutputDataObject(0).GetPointData().GetArray('degree').GetRange())
    glyphMapper.SelectColorArray('degree')

    tubeMapper = vtk.vtkPolyDataMapper()
    tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
    ###
    # Create actors
    glyphActor = vtk.vtkActor()
    glyphActor.SetMapper(glyphMapper)

    tubeActor = vtk.vtkActor()
    tubeActor.SetMapper(tubeMapper)
    
    return glyphActor, tubeActor



def draw2Dgraph(source):
    # Do layout manually before handing graph to the view.
    # This allows us to know the positions of edge arrows.
    graphLayoutView = vtk.vtkGraphLayoutView()

    layout = vtk.vtkGraphLayout()
    strategy = vtk.vtkSimple2DLayoutStrategy()
    layout.SetInputData(source)
    layout.SetLayoutStrategy(strategy)

    # Tell the view to use the vertex layout we provide
    graphLayoutView.SetLayoutStrategyToPassThrough()
    # The arrows will be positioned on a straight line between two
    # vertices so tell the view not to draw arcs for parallel edges
    graphLayoutView.SetEdgeLayoutStrategyToPassThrough()

    # Add the graph to the view. This will render vertices and edges,
    # but not edge arrows.
    graphLayoutView.AddRepresentationFromInputConnection(layout.GetOutputPort())

    # Manually create an actor containing the glyphed arrows.
    graphToPoly = vtk.vtkGraphToPolyData()
    graphToPoly.SetInputConnection(layout.GetOutputPort())
    graphToPoly.EdgeGlyphOutputOn()

    # Set the position (0: edge start, 1: edge end) where
    # the edge arrows should go.
    graphToPoly.SetEdgeGlyphPosition(0.98)

    # Make a simple edge arrow for glyphing.
    arrowSource = vtk.vtkGlyphSource2D()
    arrowSource.SetGlyphTypeToEdgeArrow()
    arrowSource.SetScale(1)
    arrowSource.Update()

    # Use Glyph3D to repeat the glyph on all edges.
    arrowGlyph = vtk.vtkGlyph3D()
    arrowGlyph.SetInputConnection(0, graphToPoly.GetOutputPort(1))
    arrowGlyph.SetInputConnection(1, arrowSource.GetOutputPort())

    # Add the edge arrow actor to the view.
    arrowMapper = vtk.vtkPolyDataMapper()
    arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())
    arrowActor = vtk.vtkActor()
    arrowActor.SetMapper(arrowMapper)
    graphLayoutView.GetRenderer().AddActor(arrowActor)

    return graphLayoutView

def drawPlot(figure, canvas, data):
    # create an axis
    ax = figure.add_subplot(111)

    # discards the old graph
    ax.clear()

    # plot data
    ax.hist(data)

    # refresh canvas
    canvas.draw()