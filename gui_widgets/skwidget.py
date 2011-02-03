from PyQt4 import QtGui

class skwidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)

        self.initBaseWidgets()
        self.retranslate()
        self.addSpacer()
        self.addTooltips()

    def initBaseWidgets(self):
        self.intValidator = QtGui.QIntValidator(self)
        self.intValidator.setBottom(0)
        doubleValidator = QtGui.QDoubleValidator(self)
        doubleValidator.setBottom(0)

        self.searchRangesGB = QtGui.QGroupBox(self)
        self.searchRangesLayout = QtGui.QGridLayout(self.searchRangesGB)

        self.searchRanges0Label = QtGui.QLabel(self.searchRangesGB)
        self.searchRanges0 = QtGui.QLineEdit(self.searchRangesGB)
        self.searchRanges0.setValidator(self.intValidator)
        self.searchRanges90Label = QtGui.QLabel(self.searchRangesGB)
        self.searchRanges90 = QtGui.QLineEdit(self.searchRangesGB)
        self.searchRanges90.setValidator(self.intValidator)
        self.searchRangesVLabel = QtGui.QLabel(self.searchRangesGB)
        self.searchRangesV = QtGui.QLineEdit(self.searchRangesGB)
        self.searchRangesV.setValidator(self.intValidator)
        self.searchRangesSpacerL = QtGui.QSpacerItem(40, 20,
                                                     QtGui.QSizePolicy.Expanding,
                                                     QtGui.QSizePolicy.Minimum)
        self.searchRangesSpacerR = QtGui.QSpacerItem(40, 20,
                                                     QtGui.QSizePolicy.Expanding,
                                                     QtGui.QSizePolicy.Minimum)

        self.searchRangesWidgets = [self.searchRanges0Label, self.searchRanges0,
                                    self.searchRanges90Label, self.searchRanges90,
                                    self.searchRangesVLabel, self.searchRangesV,
                                    self.searchRangesSpacerL, self.searchRangesSpacerR]
        self.searchRangesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                            [1, 1, 1, 1], [1, 2, 1, 1],
                                            [2, 1, 1, 1], [2, 2, 1, 1],
                                            [1, 0, 1, 1], [1, 3, 1, 1]]

        self.interpolationGB = QtGui.QGroupBox(self)
        self.interpolationLayout = QtGui.QGridLayout(self.interpolationGB)

        self.interpolationPointsLabel = QtGui.QLabel(self.interpolationGB)
        self.interpolationPoints = QtGui.QLineEdit(self.interpolationGB)
        self.interpolationPoints.setValidator(self.intValidator)
        self.meanValueLabel = QtGui.QLabel(self.interpolationGB)
        self.meanValue = QtGui.QLineEdit(self.interpolationGB)
        self.meanValue.setValidator(doubleValidator)
        self.interpolationSpacerL = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)
        self.interpolationSpacerR = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)

        self.interpolationWidgets = [self.interpolationPointsLabel,
                                     self.interpolationPoints,
                                     self.meanValueLabel,
                                     self.meanValue,
                                     self.interpolationSpacerL,
                                     self.interpolationSpacerR]
        self.interpolationWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                           [1, 1, 1, 1], [1, 2, 1, 1],
                                           [0, 0, 1, 1], [0, 3, 1, 1]]


        self.widgetItems = [self.searchRangesGB, self.interpolationGB]
        self.widgetItemsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1]]

        self.placeWidgetsAtPlaces(self.interpolationLayout,
                                  self.interpolationWidgets,
                                  self.interpolationWidgetsPlaces)
        self.placeWidgetsAtPlaces(self.searchRangesLayout,
                                  self.searchRangesWidgets,
                                  self.searchRangesWidgetsPlaces)
        self.placeWidgetsAtPlaces(self.mainLayout,
                                  self.widgetItems,
                                  self.widgetItemsPlaces)

    def addSpacer(self):
        self.Spacer = QtGui.QSpacerItem(20, 40,
                                        QtGui.QSizePolicy.Minimum,
                                        QtGui.QSizePolicy.Expanding)
        self.mainLayout.addItem(self.Spacer, 2, 0, 1, 1)

    def placeWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.searchRangesSpacerL):
                layout.addItem(widgets[i], places[i][0], places[i][1],
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])

    def isValuesValid(self):
        self.Err = ''
        if self.searchRanges0.text() == "":
            self.Err += '"Search ranges 0" is empty\n'
        if self.searchRanges90.text() == "":
            self.Err += '"Search ranges 90" is empty\n'
        if self.searchRangesV.text() == "":
            self.Err += '"Search ranges vertical" is empty\n'
        if self.interpolationPoints.text() == "":
            self.Err += '"Interpolation points" is empty\n'
        if self.meanValue.text() == "":
            self.Err += '"Mean value" is empty\n'
        if self.Err == '':
            return 1, None
        else:
            return 0, self.Err

    def retranslate(self):
        self.searchRangesGB.setTitle(self.__tr("Search ellipsoid ranges"))
        self.searchRanges0Label.setText(self.__tr("0"))
        self.searchRanges0.setText(self.__tr("20"))
        self.searchRanges90Label.setText(self.__tr("90"))
        self.searchRanges90.setText(self.__tr("20"))
        self.searchRangesVLabel.setText(self.__tr("Vertical"))
        self.searchRangesV.setText(self.__tr("20"))
        self.interpolationGB.setTitle(self.__tr("Interpolation"))
        self.interpolationPointsLabel.setText(self.__tr("Maximum interpolation points"))
        self.interpolationPoints.setText(self.__tr("20"))
        self.meanValueLabel.setText(self.__tr("Mean value"))
        self.meanValue.setText(self.__tr("0"))

        self.searchRangesGB.setTitle(self.__tr("Search ellipsoid ranges"))
        self.searchRanges0Label.setText(self.__tr("0"))
        self.searchRanges0.setText(self.__tr("20"))
        self.searchRanges90Label.setText(self.__tr("90"))
        self.searchRanges90.setText(self.__tr("20"))
        self.searchRangesVLabel.setText(self.__tr("Vertical"))
        self.searchRangesV.setText(self.__tr("20"))
        self.interpolationGB.setTitle(self.__tr("Interpolation"))
        self.interpolationPointsLabel.setText(self.__tr("Maximum interpolation points"))
        self.interpolationPoints.setText(self.__tr("20"))

    def addTooltips(self):
        self.searchRanges0.setToolTip(self.__tr("Must be >= Vario ranges"))
        self.searchRanges90.setToolTip(self.__tr("Must be >= Vario ranges"))
        self.searchRangesV.setToolTip(self.__tr("Must be >= Vario ranges"))

    def getIntPoints(self):
        return int(self.interpolationPoints.text())

    def getSearchRanges(self):
        return (int(self.searchRanges0.text()),
                 int(self.searchRanges90.text()),
                 int(self.searchRangesV.text()))

    def getMean(self):
        return float(self.meanValue.text())

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)

