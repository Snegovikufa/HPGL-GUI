from skwidget import *

class lvmwidget(skwidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)

        self.initBaseWidgets()
        self.initOwnWidgets()
        self.addSpacer()

        self.retranslate()
        self.retranslateOwn()

    def initOwnWidgets(self):
        self.meanValueLabel.hide()
        self.meanValue.hide()

        self.meanLabel = QtGui.QLabel(self.interpolationGB)
        self.meanCombobox = QtGui.QComboBox(self.interpolationGB)
        #
        self.meanCombobox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Fixed)
        self.interpolationPoints.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                               QtGui.QSizePolicy.Fixed)
        self.interpolationSpacerL.changeSize(40, 20,
                                             QtGui.QSizePolicy.Maximum,
                                             QtGui.QSizePolicy.Maximum)
        self.interpolationSpacerR.changeSize(40, 20,
                                             QtGui.QSizePolicy.Maximum,
                                             QtGui.QSizePolicy.Minimum)
        #
        self.meanWidgets = [self.meanLabel, self.meanCombobox]
        self.meanWidgetsPlaces = [[1, 1, 1, 1], [1, 2, 1, 1]]
        self.placeWidgetsAtPlaces(self.interpolationLayout,
                                  self.meanWidgets,
                                  self.meanWidgetsPlaces)

    def getMean(self, cubes):
        currIndex = self.meanCombobox.currentIndex()
        return cubes.allValues(currIndex)

    def isValuesValid(self):
        Err = ''
        if self.searchRanges0.text() == "":
            Err += '"Search ranges 0" is empty\n'
        if self.searchRanges90.text() == "":
            Err += '"Search ranges 90" is empty\n'
        if self.searchRangesV.text() == "":
            Err += '"Search ranges vertical" is empty\n'
        if self.interpolationPoints.text() == "":
            Err += '"Interpolation points" is empty\n'
        # Also check for cont properties in meanCombobox
        if self.meanCombobox.count() < 2:
            Err += 'Not enough properties loaded'
        if Err == '':
            return 1, None
        else:
            return 0, Err

    def retranslateOwn(self):
        self.meanLabel.setText(self.__tr("Mean (cube)"))

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)

class LVMError(Exception): pass
