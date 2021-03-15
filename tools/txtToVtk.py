import vtk
import networkx as nx 
import forceatlas2
from tools.txtPrep import create_graph_from_text
from tools.forceatlas import forceatlas2_layout


def fromFileToNetwork(method = "spring", path = None, dim = 3, words=[]):
    """
    Creates a words network from a chosen file and specific layout.
    """
    # Create a networkx graph element from file :
    H = create_graph_from_text(path)

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

    if words :
        nodes = [word for word in words 
                                if word in H.nodes()]
        edges = [edge for edge in H.edges() 
                                if (edge[0] in nodes) ]
        neighborNodes = list(dict.fromkeys([edge[1] for edge in edges]+nodes))
        nodesIndex = [list(H.nodes()).index(node) for node in neighborNodes]
        nXYZ = [XYZ[index] for index in nodesIndex]
        ndegreeValues = [degreeValues[i] for i in nodesIndex]
        # Creates the vtk network data
        network = changeToVTKNetwork(nXYZ,
                                    nodeLabels=neighborNodes,
                                    edges=edges,
                                    scalar=ndegreeValues,
                                    name='degree', dim=dim)
        return network, ndegreeValues

    # Creates the vtk network data
    network = changeToVTKNetwork(XYZ,
                                nodeLabels=H.nodes(),
                                edges=H.edges(),
                                scalar=degreeValues,
                                name='degree', dim=dim)
    return network, degreeValues

def changeToVTKNetwork(nodeCoords,
                nodeLabels = [],
                edges = [],
                scalar = [],
                name = '',
                dim = 3):
    """
    Store points and/or graphs as vtkPolyData or vtkUnstructuredGrid.
    """
    # Build all the network elements as vtk elements :
    
## nodes
    points = vtk.vtkPoints() if (dim==3) else vtk.vtkPoints2D()
    for node in nodeCoords:
        points.InsertNextPoint(node)
    # for a 3D Graph :
    if dim == 3:
        
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
        attribute.SetNumberOfTuples(len(scalar))
        for i, j in enumerate(scalar):   # i becomes 0,1,2,..., and j runs through scalars
            attribute.SetValue(i,j)

        # Creates the Polydata Object :
        graphData = vtk.vtkPolyData()
        # Set params
        graphData.SetPoints(points)
        graphData.SetLines(line)
        graphData.GetPointData().AddArray(attribute)

        return graphData

    # For a 2D Graph 
    graphData = vtk.vtkMutableDirectedGraph()
    vx = []
    for i in range(len(nodeLabels)):
        vx.append(graphData.AddVertex())

    for edge in edges:
        graphData.AddEdge(vx[list(nodeLabels).index(edge[0])], vx[list(nodeLabels).index(edge[1])])
        
    return graphData

def saveNetwork(networkData, name="network"):
    """
    Saves the network as a ".vtp" for further analysis (on Paraview).
    """
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('data/networks'+name+'.vtp')
    writer.SetInputData(networkData)
    writer.Write()