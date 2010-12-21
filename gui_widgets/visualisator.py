from numpy import arange, nonzero
import numpy
from enthought.tvtk.api import tvtk
from numpy.core.numeric import ravel
from PyQt4 import QtCore
from enthought.mayavi import mlab

class Visualisator(QtCore.QThread):
    def __init__(self, ValuesArray, UndefValue, CubeName):
        QtCore.QThread.__init__(self)
        self.ValuesArray = ValuesArray
        
        self.ClearValues = self.ValuesArray[nonzero(self.ValuesArray != UndefValue)]
        self.Median = numpy.median(self.ClearValues)
        self.Max = numpy.max(self.ClearValues)
        self.Min = numpy.min(self.ClearValues)

    def CutScalars(self, Min, Max):
        scalars = ravel(self.ValuesArray, order='F')
        for i in xrange(len(scalars)):
            if scalars[i] > Max:
                scalars[i] = Max
            if scalars[i] < Min:
                scalars[i] = Min
        return scalars

    def CreateGrid(self):
        xRange = len(self.ValuesArray)
        yRange = len(self.ValuesArray[0])
        zRange = len(self.ValuesArray[0][0])
        
        Grid = tvtk.RectilinearGrid()
        scalars = self.CutScalars(self.Min, self.Median*1.5)
        Grid.point_data.scalars = scalars
        Grid.point_data.scalars.name = 'scalars'
        Grid.dimensions = self.ValuesArray.shape
        Grid.x_coordinates = arange(xRange)
        Grid.y_coordinates = arange(yRange)
        Grid.z_coordinates = arange(zRange)
        
        return Grid
    
    @mlab.show
    def run(self):
        self.Grid = self.CreateGrid()

        Fig = mlab.figure(bgcolor=(0, 0, 0), fgcolor=(0, 0, 0), 
                          figure=self.Grid.class_name[3:])
        
        Surf = mlab.pipeline.surface(self.Grid, opacity=0.8)
        Surf.actor.property.interpolation = 'flat'
        
        edges = mlab.pipeline.extract_edges(Surf)
        edgesSurf = mlab.pipeline.surface(edges)
        edgesSurf.actor.property.interpolation = 'flat'
        