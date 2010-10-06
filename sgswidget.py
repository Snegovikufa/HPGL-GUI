from PyQt4 import QtGui, QtCore
from skwidget import *

class sgswidget(skwidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.BaseWidgetsInit()
        #self.OwnWidgetsInit()
        
        self.Retranslate()
    
    def OwnWidgetsInit(self):
        self.SeedGB = QtGui.QGroupBox(self.Widget)
        self.SeedLayout = QtGui.QGridLayout(self.SeedGB)
        
        self.SeedNum = QtGui.QLineEdit(self.SeedGB)
        self.SeedNum.setValidator(self.IntValidator)
        self.SeedLabel = QtGui.QLabel(self.SeedGB)
        self.KrigingType = QtGui.QComboBox(self.SeedGB)
        self.KrigingType.addItem("")
        self.KrigingType.addItem("")
        self.KrigingTypeLabel = QtGui.QLabel(self.SeedGB)
        SeedSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        SeedSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SeedWidgets = [self.SeedLabel, self.SeedNum,
                            self.KrigingTypeLabel, self.KrigingType,
                            SeedSpacerL, SeedSpacerR]
        self.SeedWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                     [1, 1, 1, 1], [1, 2, 1, 1],
                                     [0, 0, 1, 1], [0, 3, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.SeedLayout, self.SeedWidgets, self.SeedWidgetsPlaces)
        
        self.WidgetItems = [self.SeedGB]
        self.WidgetItemsPlaces = [[0, 0, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.WidgetItems, self.WidgetItemsPlaces)
        
        
        #self.SeedLabel.setText(self.__tr("Seed value:"))
        #self.SeedNum.setText(self.__tr("0"))
        #self.SGSSeedGB.setTitle(self.__tr("Seed"))
        #self.SGSKrigingTypeLabel.setText(self.__tr("Kriging type:"))
        #self.SGSKrigingType.setItemText(0, "Simple Kriging")
        #self.SGSKrigingType.setItemText(1, "Ordinary Kriging")
