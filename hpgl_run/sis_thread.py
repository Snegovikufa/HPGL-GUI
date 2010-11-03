from geo_bsd import set_output_handler
from geo_bsd import set_progress_handler
from geo_bsd import sis_simulation
from geo_bsd import calc_cdf
from PyQt4 import QtCore, QtGui

class SISThread(QtCore.QThread):
    def __init__(self, Prop, GridObject, Data, MargProbs, Seed, UseCorr, Mask):
        QtCore.QThread.__init__(self)
        self.Prop = Prop
        self.GridObject = GridObject
        self.Data = Data
        self.Seed = Seed
        self.Mask = Mask
        self.MargProbs = MargProbs
        self.UseCorr = UseCorr
        
    def run(self):
        '''Runs thread'''
        set_output_handler(self.OutputLog, None)
        set_progress_handler(self.ProgressShow, None)
        
        self.Result = sis_simulation(self.Prop, self.GridObject, self.Data, self.Seed, 
                                     self.MargProbs, self.UseCorr, self.Mask)
        self.emit(QtCore.SIGNAL("Result(PyQt_PyObject)"), self.Result)
        
    def OutputLog(self, string, _):
        '''Emits HPGL logs to main thread'''
        self.StrForLog = string
        self.emit(QtCore.SIGNAL("msg(QString)"), QtCore.QString(self.StrForLog))
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
            self.OutStr = str(self.OutStr)
            self.emit(QtCore.SIGNAL("progress(QString)"), QtCore.QString(self.OutStr))
        return 0