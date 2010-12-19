from numpy import arange
from enthought.tvtk.api import tvtk
from enthought.mayavi.scripts import mayavi2
from numpy.core.numeric import ascontiguousarray, asfortranarray
from PyQt4 import QtCore

class Visualisator(QtCore.QThread):
    def __init__(self, ValuesArray, UndefValue, CubeName):
        QtCore.QThread.__init__(self)
        self.ValuesArray = asfortranarray(ValuesArray)

    def CreateGrid(self):
        self.xRange = len(self.ValuesArray)
        self.yRange = len(self.ValuesArray[0])
        self.zRange = len(self.ValuesArray[0][0])
        
        scalars = self.ValuesArray.ravel()
        for i in xrange(len(scalars)):
            if scalars[i] > 2:
                scalars[i] = 2
        
        self.Grid = tvtk.RectilinearGrid()
        self.Grid.point_data.scalars = self.ValuesArray.ravel()
        self.Grid.point_data.scalars.name = 'scalars'
        self.Grid.dimensions = self.ValuesArray.shape
        self.Grid.x_coordinates = arange(self.xRange)
        self.Grid.y_coordinates = arange(self.yRange)
        self.Grid.z_coordinates = arange(self.zRange)
    
    @mayavi2.standalone
    def run(self):
        from enthought.mayavi.sources.vtk_data_source import VTKDataSource
        from enthought.mayavi.modules.outline import Outline
        from enthought.mayavi.modules.surface import Surface

        self.CreateGrid()

        mayavi.new_scene()
        # The single type one
        src = VTKDataSource(data = self.Grid)
        mayavi.add_source(src) 
        mayavi.add_module(Outline())
        mayavi.add_module(Surface())
