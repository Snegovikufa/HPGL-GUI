from skwidget import *

class okwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)
        
        self.initBaseWidgets()
        self.initOwnWidgets()
        self.addSpacer()
        
        self.retranslate()
        
    def initOwnWidgets(self):
        self.meanValueLabel.hide()
        self.meanValue.hide()
