import vtk
import networkx as nx 

from tools.txtPrep import createGraphFromText
from Lib.forceatlas import forceatlas2_layout


def fromFileToNetwork(method = "spring",
                path = None, dim = 3,
                words=[], maxStep=0):
    """ Creates a words network from a chosen
        file and specific layout.
    """
    # Create a networkx graph element from file :
    H = createGraphFromText(path)

    # Return a dictionary of positions keyed by node 
    # ... depending on the chosen method :
    if method == "Spring" :
        pos = nx.spring_layout(H,dim=dim,k=1)
    elif method == "Atlas" :
        pos = forceatlas2_layout(H, iterations=100,
                                kr=0.001, dim=3)
    elif method == "Kamada-ka" :
        pos = nx.kamada_kawai_layout(H, dim=3)
    elif method == "Planar" :
        pos = nx.spectral_layout(H, dim=3)
    else :
        pos = nx.random_layout(H,dim=3)

    # Convert to list of positions (each is a list)
    XYZ = [list(pos[i]) for i in pos]

    # Gets a list of network degrees
    degreeValues = [v for k, v in H.degree()]

    # gets a graph for the specific chosen words
    if words :
        nodes = [word for word in words 
                                    if word in H.nodes()]
        edges = [edge for edge in H.edges() 
                                    if (edge[0] in nodes)]
        nodes = list(dict.fromkeys(
                [edge[1] for edge in edges]+nodes))
        
        # traveling through the graph by 'maxStep' steps
        for i in range(maxStep):
            edges = [edge for edge in H.edges() 
                                    if (edge[0] in nodes) ]

            nodes = list(dict.fromkeys(
                [edge[1] for edge in edges]+nodes))

        nodesIndex = [list(H.nodes()).index(node) for node in nodes]
        nXYZ = [XYZ[index] for index in nodesIndex]
        ndegreeValues = [degreeValues[i] for i in nodesIndex]

        # Creates the vtk network data
        network = changeToVTKNetwork(nXYZ,
                                    nodeLabels=nodes,
                                    edges=edges,
                                    degreeScale=ndegreeValues,
                                    name='degree', dim=dim)

        return network, [ndegreeValues, len(edges), len(nodes)]

    # Creates the vtk network data
    network = changeToVTKNetwork(XYZ,
                                nodeLabels=H.nodes(),
                                edges=H.edges(),
                                degreeScale=degreeValues,
                                name='degree', dim=dim)

    return network, [degreeValues, len(H.edges()), len(H.nodes())]

def changeToVTKNetwork(nodeCoords,
                nodeLabels = [],
                edges = [],
                degreeScale = [],
                name = '',
                dim = 3):
    """ Store points and/or graphs as vtkPolyData
        or vtkUnstructuredGrid.
    """
    # Build all the network elements as vtk elements :
    # ...for a 3D Graph :
    if dim == 3:
        ## nodes
        points = vtk.vtkPoints() if (dim==3) else vtk.vtkPoints2D()
        for node in nodeCoords:
            points.InsertNextPoint(node)
        ## Edges 
        line = vtk.vtkCellArray()
        line.Allocate(len(edges))
        for edge in edges:
            line.InsertNextCell(2)
            line.InsertCellPoint(list(nodeLabels).index(edge[0]))
            line.InsertCellPoint(list(nodeLabels).index(edge[1]))   # line from point edge[0] to point edge[1]
        
        ## Scaling 
        attribute = vtk.vtkFloatArray()
        attribute.SetNumberOfComponents(1)
        attribute.SetName(name)
        attribute.SetNumberOfTuples(len(degreeScale))
        for i, j in enumerate(degreeScale):   # i becomes 0,1,2,..., and j runs through degreesScale
            attribute.SetValue(i,j)

        # Creates the Polydata Object :
        graphData = vtk.vtkPolyData()

        # Set params
        graphData.SetPoints(points)
        graphData.SetLines(line)
        graphData.GetPointData().AddArray(attribute)

        return graphData

    # ...for a 2D Graph
    ## Create vertex labels
    vertexLabels = vtk.vtkStringArray()
    vertexLabels.SetNumberOfComponents(1)
    vertexLabels.SetName("VertexLabels")
    for label in nodeLabels:
        vertexLabels.InsertNextValue(label)

    ## Create edge weights
    edgeWeights = vtk.vtkDoubleArray()
    edgeWeights.SetNumberOfComponents(1)
    edgeWeights.SetName("EdgeWeights")
    for deg in degreeScale:
        edgeWeights.InsertNextValue(deg)

    ## Create the Graph Object :
    graphData = vtk.vtkMutableDirectedGraph()
    vx = []
    for i in range(len(nodeLabels)):
        vx.append(graphData.AddVertex())

    for edge in edges:
        graphData.AddEdge(vx[list(nodeLabels).index(edge[0])], vx[list(nodeLabels).index(edge[1])])
    
    ### add the labels and edge weights
    graphData.GetVertexData().AddArray(vertexLabels)
    graphData.GetEdgeData().AddArray(edgeWeights)

    return graphData

