from PyQt4 import QtGui, QtCore

class skwidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.BaseWidgetsInit()
        self.Retranslate()
        self.AddSpacer()

    def BaseWidgetsInit(self):
        self.IntValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)
        
        self.SearchRangesGB = QtGui.QGroupBox(self)
        self.SearchRangesLayout = QtGui.QGridLayout(self.SearchRangesGB)
        
        self.SearchRanges0Label = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRanges0 = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRanges0.setValidator(self.IntValidator)
        self.SearchRanges90Label = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRanges90 = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRanges90.setValidator(self.IntValidator)
        self.SearchRangesVLabel = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRangesV = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRangesV.setValidator(self.IntValidator)
        self.SearchRangesSpacerL = QtGui.QSpacerItem(40, 20, 
                                                     QtGui.QSizePolicy.Expanding, 
                                                     QtGui.QSizePolicy.Minimum)
        self.SearchRangesSpacerR = QtGui.QSpacerItem(40, 20, 
                                                     QtGui.QSizePolicy.Expanding, 
                                                     QtGui.QSizePolicy.Minimum)
        
        self.SearchRangesWidgets = [self.SearchRanges0Label, self.SearchRanges0,
                                    self.SearchRanges90Label, self.SearchRanges90,
                                    self.SearchRangesVLabel, self.SearchRangesV,
                                    self.SearchRangesSpacerL, self.SearchRangesSpacerR]
        self.SearchRangesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                            [1, 1, 1, 1], [1, 2, 1, 1],
                                            [2, 1, 1, 1], [2, 2, 1, 1],
                                            [1, 0, 1, 1], [1, 3, 1, 1]]
        
        self.InterpolationGB = QtGui.QGroupBox(self)
        self.InterpolationLayout = QtGui.QGridLayout(self.InterpolationGB)
        
        self.InterpolationPointsLabel = QtGui.QLabel(self.InterpolationGB)
        self.InterpolationPoints = QtGui.QLineEdit(self.InterpolationGB)
        self.InterpolationPoints.setValidator(self.IntValidator)
        self.MeanValueLabel = QtGui.QLabel(self.InterpolationGB)
        self.MeanValue = QtGui.QLineEdit(self.InterpolationGB)
        self.MeanValue.setValidator(self.DoubleValidator)
        self.InterpolationSpacerL = QtGui.QSpacerItem(40, 20, 
                                                 QtGui.QSizePolicy.Expanding, 
                                                 QtGui.QSizePolicy.Minimum)
        self.InterpolationSpacerR = QtGui.QSpacerItem(40, 20, 
                                                 QtGui.QSizePolicy.Expanding, 
                                                 QtGui.QSizePolicy.Minimum)
        
        self.InterpolationWidgets = [self.InterpolationPointsLabel, 
                                     self.InterpolationPoints,
                                     self.MeanValueLabel, 
                                     self.MeanValue,
                                     self.InterpolationSpacerL, 
                                     self.InterpolationSpacerR]
        self.InterpolationWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                           [1, 1, 1, 1], [1, 2, 1, 1],
                                           [0, 0, 1, 1], [0, 3, 1, 1]]
        
                                       
        self.WidgetItems = [self.SearchRangesGB, self.InterpolationGB]
        self.WidgetItemsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1]]
        
        self.PlaceWidgetsAtPlaces(self.InterpolationLayout, 
                                  self.InterpolationWidgets, 
                                  self.InterpolationWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.SearchRangesLayout, 
                                  self.SearchRangesWidgets, 
                                  self.SearchRangesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.Layout, 
                                  self.WidgetItems, 
                                  self.WidgetItemsPlaces)
        
    def AddSpacer(self):
        self.Spacer = QtGui.QSpacerItem(20, 40, 
                                        QtGui.QSizePolicy.Minimum, 
                                        QtGui.QSizePolicy.Expanding)
        self.Layout.addItem(self.Spacer, 2, 0, 1, 1)
        
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.SearchRangesSpacerL):
                layout.addItem(widgets[i], places[i][0], places[i][1], 
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1], 
                                 places[i][2], places[i][3])
                
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
        else:
            return 1
        return 0
    
    def Retranslate(self):
        self.SearchRangesGB.setTitle(self.__tr("Search ellipsoid ranges"))
        self.SearchRanges0Label.setText(self.__tr("0"))
        self.SearchRanges0.setText(self.__tr("20"))
        self.SearchRanges90Label.setText(self.__tr("90"))
        self.SearchRanges90.setText(self.__tr("20"))
        self.SearchRangesVLabel.setText(self.__tr("Vertical"))
        self.SearchRangesV.setText(self.__tr("20"))
        self.InterpolationGB.setTitle(self.__tr("Interpolation"))
        self.InterpolationPointsLabel.setText(self.__tr("Maximum interpolation points"))
        self.InterpolationPoints.setText(self.__tr("20"))
        self.MeanValueLabel.setText(self.__tr("Mean value"))
        self.MeanValue.setText(self.__tr("0"))
        
        self.SearchRangesGB.setTitle(self.__tr("Search ellipsoid ranges"))
        self.SearchRanges0Label.setText(self.__tr("0"))
        self.SearchRanges0.setText(self.__tr("20"))
        self.SearchRanges90Label.setText(self.__tr("90"))
        self.SearchRanges90.setText(self.__tr("20"))
        self.SearchRangesVLabel.setText(self.__tr("Vertical"))
        self.SearchRangesV.setText(self.__tr("20"))
        self.InterpolationGB.setTitle(self.__tr("Interpolation"))
        self.InterpolationPointsLabel.setText(self.__tr("Maximum interpolation points"))
        self.InterpolationPoints.setText(self.__tr("20"))
                  
    def GetIntPoints(self):
        return int(self.InterpolationPoints.text())
        
    def GetSearchRanges(self):
        return (int(self.SearchRanges0.text()),
                 int(self.SearchRanges90.text()),
                 int(self.SearchRangesV.text()))
    def GetMean(self):
        return float(self.MeanValue.text())
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)

