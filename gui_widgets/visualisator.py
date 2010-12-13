from numpy import array, arange, random
import numpy
from enthought.tvtk.api import tvtk
from enthought.mayavi.scripts import mayavi2
from numpy.lib.index_tricks import mgrid
from PyQt4 import QtCore

class Visualisator(QtCore.QThread):
    def __init__(self, ValuesArray, UndefValue, CubeName):
        QtCore.QThread.__init__(self)
        self.ValuesArray = ValuesArray
        self.UndefValues = UndefValue
        self.CubeName = CubeName
        
        self.xRange = len(self.ValuesArray)
        self.yRange = len(self.ValuesArray[0])
        self.zRange = len(self.ValuesArray[0][0])
        
    def CreateCubeGrid(self):
        # Creating cubes' points
        Points = mgrid[0:self.xRange*self.yRange*self.zRange*8, 0:3][0]
        
        Points[0:8] = array([ [0,0,0], [1,0,0], [1,1,0], [0,1,0],
                              [0,0,1], [1,0,1], [1,1,1], [0,1,1] ])

        now = 8
        next = now+8
        for i in xrange(self.xRange):
            for j in xrange(self.yRange):
                for k in xrange(self.zRange):
                    if (i,j,k)!=(0,0,0):
                        Points[now:next] = Points[0:8]+array([[i, j, k]])
                        now += 8
                        next += 8
        # Creating cubes' cells
        Cells = mgrid[0:self.xRange*self.yRange*self.zRange, 0:9][0]
        Cells[0] = array([0, 1, 2, 3, 4, 5, 6, 7, 0])
        
        for i in xrange(1, self.xRange*self.yRange*self.zRange):
            Cells[i] = Cells[i-1]+8

        CellsType = tvtk.Hexahedron().cell_type
        Grid = tvtk.UnstructuredGrid(points=Points)
        Grid.set_cells(CellsType, Cells)

        temperature = arange(0, self.xRange*self.yRange*self.zRange*8, 1, 'd')
        Grid.point_data.scalars = temperature
        Grid.point_data.scalars.name = 'temperature'
        
        return Grid
    
    @mayavi2.standalone
    def run(self):
        Grid = self.CreateCubeGrid()
        
        from enthought.mayavi.sources.vtk_data_source import VTKDataSource
        from enthought.mayavi.modules.outline import Outline
        from enthought.mayavi.modules.surface import Surface

        mayavi.new_scene()
        # The single type one
        src = VTKDataSource(data = Grid)
        mayavi.add_source(src) 
        mayavi.add_module(Outline())
        mayavi.add_module(Surface())
        