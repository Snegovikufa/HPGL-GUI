from PySide import QtCore
from geo_bsd import load_cont_property, load_ind_property
import numpy

class LoadCubeThread(QtCore.QThread):
    cubeSignal = QtCore.Signal(object)

    def __init__(self, filepath, undefValue, gridSize, indValues):
        QtCore.QThread.__init__(self)

        self.filepath = str(filepath)
        self.undefValue = numpy.float32(undefValue)
        self.gridSize = gridSize
        self.indValues = indValues

    def run(self):
        if self.indValues:
            prop = load_ind_property(str(self.filepath), self.undefValue,
                                     self.indValues, self.gridSize)
        else:
            prop = load_cont_property(str(self.filepath),
                                      self.undefValue, self.gridSize)
        if prop:
            #self.emit(QtCore.SIGNAL('Property(PyQt_PyObject)'), prop)
            self.cubeSignal.emit(prop)
