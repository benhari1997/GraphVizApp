import vtk

def draw3Dgraph(source):
    """ draws the 3D graph from 
        the given data.
    """ 
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
    glyph.SetInputArrayToProcess(0,0,0,0,'degree')		# colors
    glyph.SetInputArrayToProcess(1,0,0,0,'vect')		

    # update glyph data
    glyph.Update()

    # Create tube filter
    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputData(source)
    tubeFilter.SetRadius(0.0015)
    tubeFilter.SetNumberOfSides(50)
    tubeFilter.Update()

    # Create data mappers
    ## glyph data mapper
    glyphMapper = vtk.vtkPolyDataMapper()
    glyphMapper.SetInputConnection(glyph.GetOutputPort())
    glyphMapper.SetScalarModeToUsePointFieldData()
    glyphMapper.SetColorModeToMapScalars()
    glyphMapper.ScalarVisibilityOn()
    glyphMapper.SetScalarRange(glyph.GetOutputDataObject(0).GetPointData().GetArray('degree').GetRange())
    glyphMapper.SelectColorArray('degree')

    ## tube data mapper
    tubeMapper = vtk.vtkPolyDataMapper()
    tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
    

    # Create actors
    ## glyph actor
    glyphActor = vtk.vtkActor()
    glyphActor.SetMapper(glyphMapper)

    ## tube actor
    tubeActor = vtk.vtkActor()
    tubeActor.SetMapper(tubeMapper)
    
    return glyphActor, tubeActor



def draw2Dgraph(source):
    """ draws the 2D graph from 
        the given data.
    """
    # Do layout manually before handing graph to the view.
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

    # Set the position
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

    # Add edge weights & vertex labels
    graphLayoutView.SetVertexLabelVisibility(1)
    graphLayoutView.SetEdgeLabelVisibility(1)

    graphLayoutView.SetVertexLabelArrayName("VertexLabels")
    graphLayoutView.SetEdgeLabelArrayName("EdgeWeights") 

    return graphLayoutView

def drawPlot(figure, canvas, data):
    """ draws and displays the given data 
        in the plot canvas.
    """
    # create an axis
    ax = figure.add_subplot(111)

    # discards the old graph
    ax.clear()

    # plot data
    ax.hist(data, color='grey')
    ax.set_title("degrees distribution")

    # refresh canvas
    canvas.draw()