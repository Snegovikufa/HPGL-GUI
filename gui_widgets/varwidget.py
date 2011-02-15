from PyQt4 import QtGui
from geo_bsd import CovarianceModel

class varwidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.mainLayout = QtGui.QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.intValidator = QtGui.QIntValidator(self)
        self.intValidator.setBottom(0)
        self.DoubleValidator = QtGui.QDoubleValidator(self)

        self.InitOwnWidgets()
        self.Retranslate()

    def InitOwnWidgets(self):
        self.VariogramTypeGB = QtGui.QGroupBox(self)
        self.VariogramTypeLayout = QtGui.QGridLayout(self.VariogramTypeGB)

        self.VariogramType_label = QtGui.QLabel(self.VariogramTypeGB)
        self.VariogramType = QtGui.QComboBox(self.VariogramTypeGB)
        self.VariogramType.addItem("")
        self.VariogramType.addItem("")
        self.VariogramType.addItem("")
        self.VariogramType.setValidator(self.intValidator)
        VariogramTypeSpacerL = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)
        VariogramTypeSpacerR = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)

        self.VariogramTypeWidgets = [self.VariogramType_label,
                                     self.VariogramType,
                                     VariogramTypeSpacerL,
                                     VariogramTypeSpacerR]
        self.VariogramTypeWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                           [0, 0, 1, 1], [0, 3, 1, 1]]

        self.EllipsoidRangesGB = QtGui.QGroupBox(self)
        self.EllipsoidRangesLayout = QtGui.QGridLayout(self.EllipsoidRangesGB)

        self.EllipsoidRanges0Label = QtGui.QLabel(self.EllipsoidRangesGB)
        self.EllipsoidRanges0 = QtGui.QLineEdit(self.EllipsoidRangesGB)
        self.EllipsoidRanges0.setValidator(self.intValidator)
        self.EllipsoidRanges90Label = QtGui.QLabel(self.EllipsoidRangesGB)
        self.EllipsoidRanges90 = QtGui.QLineEdit(self.EllipsoidRangesGB)
        self.EllipsoidRanges90.setValidator(self.intValidator)
        self.EllipsoidRangesVLabel = QtGui.QLabel(self.EllipsoidRangesGB)
        self.EllipsoidRangesV = QtGui.QLineEdit(self.EllipsoidRangesGB)
        self.EllipsoidRangesV.setValidator(self.intValidator)
        EllipsoidRangesSpacerL = QtGui.QSpacerItem(40, 20,
                                                   QtGui.QSizePolicy.Expanding,
                                                   QtGui.QSizePolicy.Minimum)
        EllipsoidRangesSpacerR = QtGui.QSpacerItem(40, 20,
                                                   QtGui.QSizePolicy.Expanding,
                                                   QtGui.QSizePolicy.Minimum)

        self.EllipsoidRangesWidgets = [self.EllipsoidRanges0Label,
                                       self.EllipsoidRanges0,
                                       self.EllipsoidRanges90Label,
                                       self.EllipsoidRanges90,
                                       self.EllipsoidRangesVLabel,
                                       self.EllipsoidRangesV,
                                       EllipsoidRangesSpacerL,
                                       EllipsoidRangesSpacerR]
        self.EllipsoidRangesWidgetsPlaces = [[0, 1, 1, 1],
                                             [0, 2, 1, 1],
                                             [1, 1, 1, 1],
                                             [1, 2, 1, 1],
                                             [2, 1, 1, 1],
                                             [2, 2, 1, 1],
                                             [1, 0, 1, 1],
                                             [1, 3, 1, 1]]

        self.EllipsoidAnglesGB = QtGui.QGroupBox(self)
        self.EllipsoidAnglesLayout = QtGui.QGridLayout(self.EllipsoidAnglesGB)

        self.EllipsoidAnglesXLabel = QtGui.QLabel(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesX = QtGui.QLineEdit(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesX.setValidator(self.intValidator)
        self.EllipsoidAnglesYLabel = QtGui.QLabel(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesY = QtGui.QLineEdit(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesY.setValidator(self.intValidator)
        self.EllipsoidAnglesZLabel = QtGui.QLabel(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesZ = QtGui.QLineEdit(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesZ.setValidator(self.intValidator)

        EllipsoidAnglesSpacerL = QtGui.QSpacerItem(40, 20,
                                                   QtGui.QSizePolicy.Expanding,
                                                   QtGui.QSizePolicy.Minimum)
        EllipsoidAnglesSpacerR = QtGui.QSpacerItem(40, 20,
                                                   QtGui.QSizePolicy.Expanding,
                                                   QtGui.QSizePolicy.Minimum)

        self.EllipsoidAnglesWidgets = [self.EllipsoidAnglesXLabel,
                                       self.EllipsoidAnglesX,
                                       self.EllipsoidAnglesYLabel,
                                       self.EllipsoidAnglesY,
                                       self.EllipsoidAnglesZLabel,
                                       self.EllipsoidAnglesZ,
                                       EllipsoidAnglesSpacerL,
                                       EllipsoidAnglesSpacerR]
        self.EllipsoidAnglesWidgetsPlaces = [[0, 1, 1, 1],
                                             [0, 2, 1, 1],
                                             [1, 1, 1, 1],
                                             [1, 2, 1, 1],
                                             [2, 1, 2, 1],
                                             [2, 2, 1, 1],
                                             [1, 0, 1, 1],
                                             [1, 3, 1, 1]]

        self.NuggetEffectGB = QtGui.QGroupBox(self)
        self.NuggetEffectLayout = QtGui.QGridLayout(self.NuggetEffectGB)

        self.SillValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.SillValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.SillValue.setValidator(self.DoubleValidator)
        self.NuggetValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.NuggetValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.NuggetValue.setValidator(self.DoubleValidator)
        self.MargProbsLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.MargProbs = QtGui.QDoubleSpinBox(self.NuggetEffectGB)
        self.MargProbs.setMaximum(0.99)
        self.MargProbs.setMinimum(0)
        self.MargProbs.setSingleStep(0.01)
        NuggetEffectSpacerL = QtGui.QSpacerItem(40, 20,
                                                QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Minimum)
        NuggetEffectSpacerR = QtGui.QSpacerItem(40, 20,
                                                QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Minimum)

        self.NuggetEffectWidgets = [self.SillValueLabel, self.SillValue,
                                    self.NuggetValueLabel, self.NuggetValue,
                                    self.MargProbsLabel, self.MargProbs,
                                    NuggetEffectSpacerL, NuggetEffectSpacerR]
        self.NuggetEffectWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                          [1, 1, 1, 1], [1, 2, 1, 1],
                                          [2, 1, 1, 1], [2, 2, 1, 1],
                                          [0, 0, 1, 1], [0, 3, 1, 1]]


        self.Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Expanding)

        self.VarWidgets = [self.VariogramTypeGB, self.EllipsoidRangesGB,
                            self.EllipsoidAnglesGB, self.NuggetEffectGB,
                          ]
        self.VarWidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1],
                                  [1, 0, 1, 1], [1, 1, 1, 1],
                                 ]

        self.PlaceWidgetsAtPlaces(self.VariogramTypeLayout,
                                  self.VariogramTypeWidgets,
                                  self.VariogramTypeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.EllipsoidRangesLayout,
                                  self.EllipsoidRangesWidgets,
                                  self.EllipsoidRangesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.EllipsoidAnglesLayout,
                                  self.EllipsoidAnglesWidgets,
                                  self.EllipsoidAnglesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.NuggetEffectLayout,
                                  self.NuggetEffectWidgets,
                                  self.NuggetEffectWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.mainLayout,
                                  self.VarWidgets,
                                  self.VarWidgetsPlaces)

    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.Spacer):
                layout.addItem(widgets[i], places[i][0], places[i][1],
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])

    def Retranslate(self):
        self.VariogramTypeGB.setTitle(self.__tr("Variogram type"))
        self.VariogramType_label.setText(self.__tr("Type"))
        self.VariogramTypes = ['Spherical', 'Exponential', 'Gaussian']
        for i in xrange(len(self.VariogramTypes)):
            self.VariogramType.setItemText(i, (self.__tr(self.VariogramTypes[i])))

        self.EllipsoidRangesGB.setTitle(self.__tr("Ellipsoid ranges"))
        self.EllipsoidRanges0Label.setText(self.__tr("0"))
        self.EllipsoidRanges0.setText(self.__tr("20"))
        self.EllipsoidRanges90Label.setText(self.__tr("90"))
        self.EllipsoidRanges90.setText(self.__tr("20"))
        self.EllipsoidRangesVLabel.setText(self.__tr("Vertical"))
        self.EllipsoidRangesV.setText(self.__tr("20"))

        self.EllipsoidAnglesGB.setTitle(self.__tr("Ellipsoid angles"))
        self.EllipsoidAnglesXLabel.setText(self.__tr("x"))
        self.EllipsoidAnglesX.setText(self.__tr("0"))
        self.EllipsoidAnglesY.setText(self.__tr("0"))
        self.EllipsoidAnglesZLabel.setText(self.__tr("z"))
        self.EllipsoidAnglesZ.setText(self.__tr("0"))
        self.EllipsoidAnglesYLabel.setText(self.__tr("y"))

        self.NuggetEffectGB.setTitle(self.__tr("Sill value and nugget-effect"))
        self.SillValueLabel.setText(self.__tr("Sill value"))
        self.SillValue.setText(self.__tr("1"))
        self.NuggetValueLabel.setText(self.__tr("\"Nugget\" effect value"))
        self.NuggetValue.setText(self.__tr("0"))
        self.MargProbsLabel.setText(self.__tr("Marginal probability:"))

    def isVariogramValid(self):
        self.Err = ''
        if self.EllipsoidRanges0.text() == "":
            self.Err += '"Ellipsoid ranges 0" is empty\n'
        if self.EllipsoidRanges90.text() == "":
            self.Err += '"Ellipsoid ranges 90" is empty\n'
        if self.EllipsoidRangesV.text() == "":
            self.Err += '"Ellipsoid ranges vertical" is empty\n'
        if self.EllipsoidAnglesX.text() == "":
            self.Err += '"Ellipsoid angles x" is empty\n'
        if self.EllipsoidAnglesY.text() == "":
            self.Err += '"Ellipsoid angles y" is empty\n'
        if self.EllipsoidAnglesZ.text() == "":
            self.Err += '"Ellipsoid angles z" is empty\n'
        if self.SillValue.text() == "":
            self.Err += '"Sill value" is empty\n'
        if self.NuggetValue.text() == "":
            self.Err += '"Nugget effect value" is empty\n'
        if self.Err == '':
            return 1, None
        else:
            return 0, self.Err

    def GetVariogram(self):
        # Variogram
        self.VariogramRanges = (int(self.EllipsoidRanges0.text()),
                                 int(self.EllipsoidRanges90.text()),
                                 int(self.EllipsoidRangesV.text()))
        self.VariogramAngles = (int(self.EllipsoidAnglesX.text()),
                                 int(self.EllipsoidAnglesY.text()),
                                 int(self.EllipsoidAnglesZ.text()))
        self.Variogram = CovarianceModel(int(self.VariogramType.currentIndex()),
                                          self.VariogramRanges,
                                          self.VariogramAngles,
                                          float(self.SillValue.text()),
                                          float(self.NuggetValue.text()))
        return self.Variogram

    def GetMargProbs(self):
        return float(self.MargProbs.value())

    def ShowError(self, string):
        self.ErrorWindow = QtGui.QMessageBox()
        self.ErrorWindow.warning(None, "Error", string)

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)

class VARError(Exception) : pass
