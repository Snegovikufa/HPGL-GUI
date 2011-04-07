from PySide import QtCore
from geo_bsd.routines import LoadGslibFile

class LoadGslibThread(QtCore.QThread):
    cubeSignal = QtCore.Signal(object)
    errSignal = QtCore.Signal(str)

    def __init__(self, filepath, gridSize):
        QtCore.QThread.__init__(self)

        self.filepath = filepath
        self.gridSize = gridSize

    def run(self):
        try:
            dict = LoadGslibFile(self.filepath, self.gridSize)
            self.cubeSignal.emit(dict)
        except:
            self.errSignal.emit('Something wrong while loading GSLIB file. Try again!')