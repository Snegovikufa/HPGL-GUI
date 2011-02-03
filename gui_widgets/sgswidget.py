from PyQt4 import QtCore
from skwidget import *

class sgswidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)
        
        self.initBaseWidgets()
        self.initOwnWidgets()
        self.addSpacer()
        
        self.retranslate()
        self.retranslateOwn()
        
        self.initSignals()

    def initSignals(self):
        self.connect(self.maskCheckbox, QtCore.SIGNAL("toggled(bool)"), 
                     self.MaskCombobox, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.meanCheckbox, QtCore.SIGNAL("toggled(bool)"), 
                     self.meanCombobox, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.meanCheckbox, QtCore.SIGNAL("toggled(bool)"), 
                     self.meanValue, QtCore.SLOT("setDisabled(bool)"))
    
    def initOwnWidgets(self):
        IntValidator = QtGui.QIntValidator()
        
        self.SeedGB = QtGui.QGroupBox(self)
        self.SeedGB.hide()
        self.SeedLayout = QtGui.QGridLayout(self.SeedGB)
        
        self.SeedNum = QtGui.QLineEdit(self.SeedGB)
        self.SeedNum.setValidator(IntValidator)
        self.SeedLabel = QtGui.QLabel(self.SeedGB)
        self.KrigingType = QtGui.QComboBox(self.SeedGB)
        self.KrigingType.addItem("")
        self.KrigingType.addItem("")
        self.KrigingTypeLabel = QtGui.QLabel(self.SeedGB)
        SeedSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        SeedSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.SeedWidgets = [self.SeedLabel, self.SeedNum,
                            self.KrigingTypeLabel, self.KrigingType,
                            SeedSpacerL, SeedSpacerR]
        self.SeedWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                  [1, 1, 1, 1], [1, 2, 1, 1],
                                  [0, 0, 1, 1], [0, 3, 1, 1]]
        self.placeWidgetsAtPlaces(self.SeedLayout, self.SeedWidgets, self.SeedWidgetsPlaces)
        
        self.MaskGB = QtGui.QGroupBox(self)
        self.MaskGB.hide()
        self.MaskLayout = QtGui.QGridLayout(self.MaskGB)
        
        self.maskCheckbox = QtGui.QCheckBox(self.MaskGB)
        self.MaskCombobox = QtGui.QComboBox(self.MaskGB)
        self.MaskCombobox.setDisabled(1)
        self.MeanNewLabel = QtGui.QLabel(self.MaskGB)
        self.meanCheckbox = QtGui.QCheckBox(self.MaskGB)
        self.meanCombobox = QtGui.QComboBox(self.MaskGB)
        self.meanCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.MaskCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.meanCombobox.setDisabled(1)
        MaskSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        MaskSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        
        self.MaskWidgets = [self.maskCheckbox, self.MaskCombobox,
                            self.meanCheckbox, self.meanCombobox,
                            MaskSpacerL, MaskSpacerR]
        self.MaskWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                  [1, 1, 1, 1], [1, 2, 1, 1],
                                  [0, 0, 1, 1], [0, 4, 1, 1]]
        self.placeWidgetsAtPlaces(self.MaskLayout, self.MaskWidgets, self.MaskWidgetsPlaces)
        
        self.widgetItems = [self.SeedGB, self.MaskGB]
        self.widgetItemsPlaces = [[1, 0, 1, 1], [1, 1, 1, 1]]
        self.placeWidgetsAtPlaces(self.mainLayout, self.widgetItems, self.widgetItemsPlaces)
        
    def addSpacer(self):
        Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.mainLayout.addItem(Spacer, 2, 0, 1, 1)
        
    def GetSeed(self):
        return int(self.SeedNum.text())
    
    def GetUseHd(self):
        return 1 # It's unused?
    
    def GetKrType(self):
        if int(self.KrigingType.currentIndex()) == 0:
            return "sk"
        else:
            return "ok"
    
    def getMean(self, cubes):
        if self.meanCheckbox.isChecked() and self.meanCombobox.count() > 1:
            currIndex = self.meanCombobox.currentIndex()
            return cubes.allValues(currIndex)
        else:
            return float(self.meanValue.text())
    
    def GetMask(self, cubes):
        if self.maskCheckbox.isChecked() == 1:
            currIndex = self.MaskCombobox.currentIndex()
            return cubes.property(currIndex)
        else:
            return None
    
    def isValuesValid(self, Err):
        Err = ''
        if self.searchRanges0.text() == "":
            Err += '"Search ranges 0" is empty\n'
        if self.searchRanges90.text() == "":
            Err += '"Search ranges 90" is empty\n'
        if self.searchRangesV.text() == "":
            Err += '"Search ranges vertical" is empty\n'
        if self.interpolationPoints.text() == "":
            Err += '"Interpolation points" is empty\n'
        if self.meanValue.text() == "":
            Err += '"Mean value" is empty\n'
        if self.SeedNum.text() == "":
            Err += '"Seed value" is empty'
        if Err == '':
            return 1, None
        else:
            return 0, Err
        
    def retranslateOwn(self):
        self.SeedLabel.setText(self.__tr("Seed value"))
        self.SeedNum.setText(self.__tr("0"))
        self.SeedGB.setTitle(self.__tr("Seed"))
        self.KrigingTypeLabel.setText(self.__tr("Kriging type"))
        self.KrigingType.setItemText(0, "Simple Kriging")
        self.KrigingType.setItemText(1, "Ordinary Kriging")
        
        self.MaskGB.setTitle(self.__tr("Mask"))
        self.maskCheckbox.setText(self.__tr("Mask"))
        self.meanCheckbox.setText(self.__tr("Mean (cube)"))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
