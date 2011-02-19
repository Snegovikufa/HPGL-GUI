from geo_bsd import set_output_handler
from geo_bsd import set_progress_handler
from geo_bsd.geo import lvm_kriging
from PySide import QtCore

class LVMThread(QtCore.QThread):
    propSignal = QtCore.Signal(object)
    logMessage = QtCore.Signal(str)
    progressMessage = QtCore.Signal(int)

    def __init__(self, Prop, GridObject, Mean, EllipsoidRanges,
                  IntPoints, Variogram):
        QtCore.QThread.__init__(self)
        self.Prop = Prop
        self.GridObject = GridObject
        self.Mean = Mean
        self.EllipsoidRanges = EllipsoidRanges
        self.IntPoints = IntPoints
        self.Variogram = Variogram

    def run(self):
        '''Runs thread'''
        set_output_handler(self.OutputLog, None)
        set_progress_handler(self.ProgressShow, None)

        self.Result = lvm_kriging( self.Prop, self.GridObject,
                                      self.Mean,
                                      self.EllipsoidRanges,
                                      self.IntPoints,
                                      self.Variogram )
        #self.emit(QtCore.SIGNAL("Result(PyQt_PyObject)"), self.Result)
        self.propSignal.emit(self.Result)

    def OutputLog(self, string, _):
        '''Emits HPGL logs to main thread'''
        #self.emit(QtCore.SIGNAL("msg(QString)"), QtCore.QString(self.StrForLog))
        self.logMessage.emit(string)
        return 0

    def ProgressShow(self, stage, Percent, _):
        '''Emits HPGL progress to main thread'''
        self.Percent = Percent
        self.stage = stage
        if self.Percent == 0:
            print self.stage,
        elif self.Percent == -1:
            print ""
        else:
            self.OutStr = int(self.Percent)
            #self.emit(QtCore.SIGNAL("progress(QString)"),
            #         QtCore.QString(self.OutStr))
            self.progressMessage.emit(self.OutStr)
        return 0

