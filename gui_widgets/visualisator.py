from PyQt4 import QtCore
from enthought.mayavi import mlab
from enthought.tvtk.api import tvtk
from numpy import arange, nonzero, float32, min, max, median, copy
from numpy.core.numeric import ravel

class Visualisator(QtCore.QThread):
    def __init__(self, valuesArray, undefValue, name):
        QtCore.QThread.__init__(self)
        self.valuesArray = valuesArray
        self.cubeName = name
        
        self.clearValues = self.valuesArray[nonzero(self.valuesArray != undefValue)]
        self.median = median(self.clearValues)
        self.max = max(self.clearValues)
        self.min = min(self.clearValues)

    def cutScalars(self, min, max):
        for i in self.Grid.point_data.scalars:
            if i > max:
                i = max
            if i < min:
                i = min

    def createGrid(self):
        xRange = len(self.valuesArray)
        yRange = len(self.valuesArray[0])
        zRange = len(self.valuesArray[0][0])
        
        grid = tvtk.RectilinearGrid()
        scalars = float32(ravel(self.valuesArray, order='F'))
        grid.point_data.scalars = scalars
        grid.point_data.scalars.name = 'scalars'
        grid.dimensions = float32(self.valuesArray.shape)
        grid.x_coordinates = float32(arange(xRange))
        grid.y_coordinates = float32(arange(yRange))
        grid.z_coordinates = float32(arange(zRange))
        
        return grid
    
    @mlab.show
    def run(self):
        self.grid = self.createGrid()
        self.cutScalars(self.min, 1.5*self.median)

        Fig = mlab.figure(bgcolor=(0, 0, 0), fgcolor=(0, 0, 0),
                          figure=self.grid.class_name[3:])
        
        surf = mlab.pipeline.surface(self.grid, opacity=1)
        surf.actor.property.interpolation = 'flat'
                
#        edges = mlab.pipeline.extract_edges(surf)
#        edgesSurf = mlab.pipeline.surface(edges)
#        edgesSurf.actor.property.interpolation = 'flat'

        mlab.title(str(self.cubeName), color = (1, 1, 1) , height = 8)
        mlab.colorbar(title = 'Scalars')