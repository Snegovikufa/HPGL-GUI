from PyQt4 import QtGui, QtCore
from skwidget import *

class okwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.InitBaseWidgets()
        self.InitOwnWidgets()
        self.AddSpacer()
        
        self.Retranslate()
        
    def InitOwnWidgets(self):
        self.MeanValueLabel.hide()
        self.MeanValue.hide()
