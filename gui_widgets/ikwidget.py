from skwidget import *

class ikwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)
        
        self.initBaseWidgets()
        self.ownWidgetsInit()
        self.addSpacer()
        
        self.retranslate()
        
    def ownWidgetsInit(self):
        self.meanValueLabel.hide()
        self.meanValue.hide()
        