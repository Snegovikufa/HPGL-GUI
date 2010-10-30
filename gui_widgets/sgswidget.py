from PyQt4 import QtGui, QtCore
from skwidget import *
from geo_bsd.geo import load_cont_property

class sgswidget(skwidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.BaseWidgetsInit()
        self.OwnWidgetsInit()
        self.AddSpacer()
        
        self.Retranslate()
        self.RetranslateOwn()
        
        self.connect(self.MaskCheckbox, QtCore.SIGNAL("toggled(bool)"), self.MaskCombobox, 
                     QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.MeanCheckbox, QtCore.SIGNAL("toggled(bool)"), 
                     self.MeanCombobox, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.MeanCheckbox, QtCore.SIGNAL("toggled(bool)"),
                     self.MeanValue,    QtCore.SLOT("setDisabled(bool)"))
        
    
    def OwnWidgetsInit(self):
        self.SeedGB = QtGui.QGroupBox(self)
        self.SeedLayout = QtGui.QGridLayout(self.SeedGB)
        
        self.SeedNum = QtGui.QLineEdit(self.SeedGB)
        self.SeedNum.setValidator(self.IntValidator)
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
        self.PlaceWidgetsAtPlaces(self.SeedLayout, self.SeedWidgets, self.SeedWidgetsPlaces)
        
        self.MaskGB = QtGui.QGroupBox(self)
        self.MaskLayout = QtGui.QGridLayout(self.MaskGB)
        
        self.MaskCheckbox = QtGui.QCheckBox(self.MaskGB)
        self.MaskCombobox = QtGui.QComboBox(self.MaskGB)
        self.MaskCombobox.setDisabled(1)
        self.MeanNewLabel = QtGui.QLabel(self.MaskGB)
        self.MeanCheckbox = QtGui.QCheckBox(self.MaskGB)
        self.MeanCombobox = QtGui.QComboBox(self.MaskGB)
        self.MeanCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.MaskCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.MeanCombobox.setDisabled(1)
        MaskSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        MaskSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        
        self.MaskWidgets = [self.MaskCheckbox, self.MaskCombobox,
                            self.MeanCheckbox, self.MeanCombobox,
                            MaskSpacerL, MaskSpacerR]
        self.MaskWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                  [1, 1, 1, 1], [1, 2, 1, 1],
                                  [0, 0, 1, 1], [0, 4, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.MaskLayout, self.MaskWidgets, self.MaskWidgetsPlaces)
        
        self.WidgetItems = [self.SeedGB, self.MaskGB]
        self.WidgetItemsPlaces = [[1, 0, 1, 1], [1, 1, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.WidgetItems, self.WidgetItemsPlaces)
        
    def AddSpacer(self):
        self.Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.Layout.addItem(self.Spacer, 2, 0, 1, 1)
        
    def GetSeed(self):
        return int(self.SeedNum.text())
    
    def GetUseHd(self):
        return 1 # It's unusable?
    
    def GetKrType(self):
        if int(self.KrigingType.currentIndex()) == 0:
            return "sk"
        else:
            return "ok"
    
    def GetMean(self, Cubes, CubesCont):
        if self.MeanCheckbox.isChecked() == 1:
            self.CurrIndex = CubesCont[self.MeanCombobox.currentIndex()]
            self.Mean = Cubes[self.CurrIndex][0][0]
        else:
            self.Mean = float(self.MeanValue.text())
        return self.Mean
    
    def GetMask(self, Cubes, CubesInd):
        if self.MaskCheckbox.isChecked() == 1:
            self.CurrIndex = CubesInd[self.MaskCombobox.currentIndex()]
            self.Mask = Cubes[self.CurrIndex][0]
    
    def ValuesCheck(self, LogTextbox):
        if self.SearchRanges0.text() == "":
            LogTextbox.insertPlainText('"Search ranges 0" is empty\n')
        elif self.SearchRanges90.text() == "":
            LogTextbox.insertPlainText('"Search ranges 90" is empty\n')
        elif self.SearchRangesV.text() == "":
            LogTextbox.insertPlainText('"Search ranges vertical" is empty\n')
        elif self.InterpolationPoints.text() == "":
            LogTextbox.insertPlainText('"Interpolation points" is empty\n')
        elif self.MeanValue.text() == "":
            LogTextbox.insertPlainText('"Mean value" is empty\n')
        elif self.SeedNum.text() == "":
            LogTextbox.insertPlainText('"Seed value" is empty')
        else:
            return 1
        return 0
        
    def RetranslateOwn(self):
        self.SeedLabel.setText(self.__tr("Seed value:"))
        self.SeedNum.setText(self.__tr("0"))
        self.SeedGB.setTitle(self.__tr("Seed"))
        self.KrigingTypeLabel.setText(self.__tr("Kriging type:"))
        self.KrigingType.setItemText(0, "Simple Kriging")
        self.KrigingType.setItemText(1, "Ordinary Kriging")
        
        self.MaskGB.setTitle(self.__tr("Mask"))
        self.MaskCheckbox.setText(self.__tr("Mask"))
        self.MeanCheckbox.setText(self.__tr("Mean (cube)"))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
