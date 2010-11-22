from PyQt4 import QtGui, QtCore
from skwidget import *

class lvmwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.BaseWidgetsInit()
        self.OwnWidgetsInit()
        self.AddSpacer()
        
        self.Retranslate()
        self.RetranslateOwn()
        
    def OwnWidgetsInit(self):
        self.MeanValueLabel.hide()
        self.MeanValue.hide()
              
        self.MeanLabel = QtGui.QLabel(self.InterpolationGB)
        self.MeanCombobox = QtGui.QComboBox(self.InterpolationGB)
        self.MeanCombobox.setDisabled(1)
        #
        self.MeanCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                                        QtGui.QSizePolicy.Fixed)
        self.InterpolationPoints.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                                               QtGui.QSizePolicy.Fixed)
        self.InterpolationSpacerL.changeSize(40, 20, 
                                             QtGui.QSizePolicy.Maximum, 
                                             QtGui.QSizePolicy.Maximum)
        self.InterpolationSpacerR.changeSize(40, 20, 
                                             QtGui.QSizePolicy.Maximum, 
                                             QtGui.QSizePolicy.Minimum)
        #
        self.MeanWidgets = [self.MeanLabel, self.MeanCombobox]
        self.MeanWidgetsPlaces = [[1, 1, 1, 1], [1, 2, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.InterpolationLayout, 
                                  self.MeanWidgets, 
                                  self.MeanWidgetsPlaces)

    def GetMean(self, Cubes, CubesCont):
        if self.MeanCombobox.count() != 0:
            self.CurrIndex = self.MeanCombobox.currentIndex()
            self.Mean = Cubes[self.CurrIndex][0][0]
            return self.Mean

    def ValuesCheck(self):
        Err = ''
        if self.SearchRanges0.text() == "":
            Err += '"Search ranges 0" is empty\n'
        if self.SearchRanges90.text() == "":
            Err += '"Search ranges 90" is empty\n'
        if self.SearchRangesV.text() == "":
            Err += '"Search ranges vertical" is empty\n'
        if self.InterpolationPoints.text() == "":
            Err += '"Interpolation points" is empty\n'
        # Also check for cont properties in MeanCombobox
        if self.MeanCombobox.count() == 0:
            Err += 'No cont property loaded yet'
        if Err == '':
            return 1, None
        else:
            return 0, Err
    
    def RetranslateOwn(self):
        self.MeanLabel.setText(self.__tr("Mean (cube):"))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)