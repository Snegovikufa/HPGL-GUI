import os
os.environ['ETS_TOOLKIT'] = 'qt4'

from PyQt4 import QtCore, QtGui
from enthought.mayavi import mlab
from enthought.tvtk.api import tvtk
from numpy import arange, nonzero, float32, min, max, median, copy
from numpy.core.numeric import ravel

from enthought.traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict
from enthought.traits.ui.api import View, Item
from enthought.mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor

class Visualisator(HasTraits):
    scene = Instance(MlabSceneModel, ())
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True
                )

    def push(self, grid):
        self.grid = grid

    @on_trait_change('scene.activated')
    def updatePlot(self, grid):
        self.scene.mlab.clf()

        surf = self.scene.mlab.pipeline.surface(self.grid, opacity=1)
        surf.actor.property.interpolation = 'flat'

        self.scene.mlab.orientation_axes()
        self.scene.background = (0, 0, 0)
        self.scene.mlab.colorbar(orientation='vertical')
#        fig = mlab.figure(bgcolor=(0, 0, 0), fgcolor=(0, 0, 0),
#                          figure=self.grid.class_name[3:])
#        edges = mlab.pipeline.extract_edges(surf)
#        edgesSurf = mlab.pipeline.surface(edges)
#        edgesSurf.actor.property.interpolation = 'flat'
#        mlab.title(str(self.cubeName), color = (1, 1, 1) , height = 8)
#        mlab.colorbar(title = 'Scalars')

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, valuesArray, undefValue, name, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.valuesArray = valuesArray
        self.undefValue = undefValue

        layout = QtGui.QVBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)

        self.grid = self.createGrid()
        self.values()
        self.cutScalars(self.min, 1.5*self.median)

        self.visualization = Visualisator()
        self.visualization.push(self.grid)

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

        self.show()

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

    def values(self):
        self.clearValues = self.valuesArray[nonzero(self.valuesArray != self.undefValue)]
        self.median = median(self.clearValues)
        self.max = max(self.clearValues)
        self.min = min(self.clearValues)

    def cutScalars(self, min, max):
        for i in self.grid.point_data.scalars:
            if i > max:
                i = max
            if i < min:
                i = min
