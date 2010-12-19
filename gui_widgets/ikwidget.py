from PyQt4 import QtGui, QtCore
from skwidget import *

class ikwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.InitBaseWidgets()
        self.OwnWidgetsInit()
        self.AddSpacer()
        
        self.Retranslate()
        
    def OwnWidgetsInit(self):
        self.MeanValueLabel.hide()
        self.MeanValue.hide()
        