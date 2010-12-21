from numpy import arange
from enthought.tvtk.api import tvtk
from numpy.core.numeric import ravel
from PyQt4 import QtCore
from enthought.mayavi import mlab

class Visualisator(QtCore.QThread):
    def __init__(self, ValuesArray, UndefValue, CubeName):
        QtCore.QThread.__init__(self)
        self.ValuesArray = ValuesArray

    def CreateGrid(self):
        xRange = len(self.ValuesArray)
        yRange = len(self.ValuesArray[0])
        zRange = len(self.ValuesArray[0][0])
        
        self.scalars = ravel(self.ValuesArray, order='F')
        for i in xrange(len(self.scalars)):
            if self.scalars[i] > 2:
                self.scalars[i] = 2
        
        Grid = tvtk.RectilinearGrid()
        Grid.point_data.scalars = self.scalars
        Grid.point_data.scalars.name = 'scalars'
        Grid.dimensions = self.ValuesArray.shape
        Grid.x_coordinates = arange(xRange)
        Grid.y_coordinates = arange(yRange)
        Grid.z_coordinates = arange(zRange)
        
        return Grid
    
    @mlab.show
    def run(self):
        Grid = self.CreateGrid()
        fig = mlab.figure(bgcolor=(0, 0, 0), fgcolor=(0, 0, 0), 
                          figure=Grid.class_name[3:])
        surf = mlab.pipeline.surface(Grid, opacity=0.8)
        edges = mlab.pipeline.extract_edges(surf)
#        edges.point_data.scalars = self.scalars
#        edges.point_data.scalars.name = 'scalars'
        mlab.pipeline.surface(edges)