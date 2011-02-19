from PySide import QtCore, QtGui
import numpy
from gui_widgets.cube_list import CubeItem
from geo_bsd import SugarboxGrid, ContProperty, IndProperty

class CreateCube(QtGui.QDialog):
    cubeSignal = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(CreateCube, self).__init__(parent)
        self.resize(500, 160)

        self.initWidgets()
        self.initSignals()

        self.retranslateUI(self)

    def initWidgets(self):
        self.mainLayout = QtGui.QVBoxLayout(self)
        #self.mainLayout.setContentsMargins(3, 3, 3, 3)
        self.mainLayout.setSpacing(0)

        intValidator = QtGui.QIntValidator(self)
        intValidator.setBottom(1)
        doubleValidator = QtGui.QDoubleValidator(self)

        self.GridSizeGB = QtGui.QGroupBox(self)
        self.GridLayout = QtGui.QGridLayout(self.GridSizeGB)
        self.GridSizeXLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeX = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeX.setValidator(intValidator)
        self.GridSizeYLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeY = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeY.setValidator(intValidator)
        self.GridSizeZLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeZ = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeZ.setValidator(intValidator)
        self.GridSizeSpacerL = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)
        self.GridSizeSpacerR = QtGui.QSpacerItem(40, 20,
                                                 QtGui.QSizePolicy.Expanding,
                                                 QtGui.QSizePolicy.Minimum)
        self.GridSizeWidgets = [self.GridSizeXLabel, self.GridSizeX,
                                self.GridSizeYLabel, self.GridSizeY,
                                self.GridSizeZLabel, self.GridSizeZ,
                                self.GridSizeSpacerL, self.GridSizeSpacerR]
        self.GridSizeWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                      [1, 1, 1, 1], [1, 2, 1, 1],
                                      [2, 1, 1, 1], [2, 2, 1, 1],
                                      [0, 0, 1, 1], [0, 3, 1, 1]]

        self.IndValuesGB = QtGui.QGroupBox(self)
        self.IndValuesLayout = QtGui.QGridLayout(self.IndValuesGB)
#        self.IndValuesLayout.setSpacing(0)
#        self.IndValuesLayout.setContentsMargins(0, 0, 0, 0)
        
        self.IndValues = QtGui.QSpinBox(self.IndValuesGB)
        self.IndValues.setEnabled(False)
        self.IndValues.setMinimum(2)
        self.IndValues.setMaximum(256)
        self.IndValuesCheckbox = QtGui.QCheckBox(self.IndValuesGB)
        #self.IndValuesCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.UndefValueLabel = QtGui.QLabel(self.IndValuesGB)
        self.undefValue = QtGui.QLineEdit(self.IndValuesGB)
        self.undefValue.setValidator(doubleValidator)
        
        self.constantCB = QtGui.QCheckBox(self.IndValuesGB)
        #self.constantCB.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.constant = QtGui.QLineEdit(self.IndValuesGB)
        self.constant.setValidator(doubleValidator)
        self.constant.setDisabled(True)
        
        self.cubeName = QtGui.QLineEdit(self.IndValuesGB)
        self.cubeNameLabel = QtGui.QLabel(self.IndValuesGB)

        IndValuesSpacerL = QtGui.QSpacerItem(40, 20,
                                             QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Minimum)
        IndValuesSpacerR = QtGui.QSpacerItem(40, 20,
                                             QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Minimum)
        self.IndValuesWidgets = [self.IndValues, self.IndValuesCheckbox,
                                 self.constantCB, self.constant,
                                 self.UndefValueLabel, self.undefValue,
                                 self.cubeNameLabel, self.cubeName,
                                 IndValuesSpacerL, IndValuesSpacerR]
        self.IndValuesWidgetsPlaces = [[1, 2, 1, 1], [1, 1, 1, 1],
                                       [2, 1, 1, 1], [2, 2, 1, 1],
                                       [3, 1, 1, 1], [3, 2, 1, 1],
                                       [4, 1, 1, 1], [4, 2, 1, 1],
                                       [1, 3, 1, 1], [1, 0, 1, 1]]

        self.createCubeGB = QtGui.QGroupBox(self)
        self.createCubeLayout = QtGui.QGridLayout(self.createCubeGB)
#        self.createCubeLayout.setSpacing(0)
#        self.createCubeLayout.setContentsMargins(0, 0, 0, 0)
        
        self.createCubeButton = QtGui.QPushButton(self.createCubeGB)
        self.createCubeButton.setDisabled(1)
        self.createCubeButton.setToolTip(self.__tr("Enter grid sizes first"))
        createCubeSpacerL = QtGui.QSpacerItem(241, 20,
                                            QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Minimum)
        createCubeSpacerR = QtGui.QSpacerItem(241, 20,
                                            QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Minimum)
        self.createCubeWidgets = [self.createCubeButton, createCubeSpacerL,
                                createCubeSpacerR]
        self.createCubeWidgetsPlaces = [[0, 1, 1, 1], [0, 0, 1, 1],
                                      [0, 2, 1, 1]]

        self.PlaceWidgetsAtPlaces(self.GridLayout, self.GridSizeWidgets, self.GridSizeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.IndValuesLayout, self.IndValuesWidgets, self.IndValuesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.createCubeLayout, self.createCubeWidgets, self.createCubeWidgetsPlaces)

        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(0)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.GridSizeGB)
        vbox.addWidget(QtGui.QWidget())
        vbox.setSpacing(0)

        hbox.addLayout(vbox)
        hbox.addWidget(self.IndValuesGB)

        self.mainLayout.addLayout(hbox)
        self.mainLayout.addWidget(self.createCubeGB)

    def initSignals(self):
        # Signals/slots
        self.connect(self.createCubeButton, QtCore.SIGNAL("clicked()"), self.cubeCreate)
        self.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"), self.IndValues.setEnabled)
        self.connect(self.GridSizeX, QtCore.SIGNAL("textChanged(QString)"), self.cubeCreateAccess)
        self.connect(self.GridSizeY, QtCore.SIGNAL("textChanged(QString)"), self.cubeCreateAccess)
        self.connect(self.GridSizeZ, QtCore.SIGNAL("textChanged(QString)"), self.cubeCreateAccess)
        self.connect(self.cubeName, QtCore.SIGNAL("textChanged(QString)"), self.cubeCreateAccess)
        self.connect(self.constantCB, QtCore.SIGNAL("toggled(bool)"), self.constant.setEnabled)
        self.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"), self.updateChecks)
        
    def updateChecks(self, checked):
        if checked:
            self.constantCB.setChecked(False)
    
    def checkValues(self):
        err = ''
        
        if self.constant.text() == '' or self.constant.text() == '-':
            err += self.__tr('Constant field is empty or invalid')
        if self.undefValue.text() == '' or self.undefValue.text() == '-':
            err += self.__tr('Undefined value field is empty or invalid')
        
        if err != '':
            self.showErr(err)
            return False
        
        return True

    def showErr(self, err):
        message = QtGui.QMessageBox()
        message.warning(self, 'EMPTY FIELDS', err)
    
    def cubeCreate(self):
        if not self.checkValues():
            return
        
        gridSize = (int(self.GridSizeX.text()),
                    int(self.GridSizeY.text()),
                    int(self.GridSizeZ.text()))
        gridObject = SugarboxGrid(*gridSize)
        undefValue = float(self.undefValue.text())
        name = self.cubeName.text()

        self.item = CubeItem()
        
        if self.constantCB.isChecked():
            data = numpy.zeros(gridSize, dtype='uint8', order='F') + float(self.constant.text())
            mask = numpy.ones(gridSize, dtype='uint8', order='F')
        else:
            data = numpy.zeros(gridSize, dtype='uint8', order='F') + undefValue
            mask = numpy.zeros(gridSize, dtype='uint8', order='F')

        if self.IndValuesCheckbox.isChecked():
            indCount = int(self.IndValues.text())
            indValues = range(indCount)
            prop = IndProperty(data, mask, indCount)
        else:
            indValues = None
            prop = ContProperty(data, mask)

        self.item.append(prop, undefValue, indValues,
                         gridObject, name, gridSize)
        #self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.item)
        self.cubeSignal.emit(self.item)
        self.hide()

    def cubeCreateAccess(self):
        if self.GridSizeX.text() == '' or \
            self.GridSizeY.text() == '' or \
            self.GridSizeZ.text() == '' or \
            self.cubeName.text() == '' or \
            int(self.GridSizeX.text()) == 0 or \
            int(self.GridSizeY.text()) == 0 or \
            int(self.GridSizeZ.text()) == 0:
            self.createCubeButton.setDisabled(1)
            self.createCubeButton.setToolTip(self.__tr("Enter grid sizes and name first"))
            return
        if int(self.GridSizeX.text()) > 0 and \
            int(self.GridSizeY.text()) > 0 and \
            int(self.GridSizeZ.text()) > 0:
            self.createCubeButton.setEnabled(1)
            self.createCubeButton.setToolTip('')

    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(QtGui.QSpacerItem(0, 0)):
                layout.addItem(widgets[i], places[i][0], places[i][1],
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])

    def retranslateUI(self, MainWindow):
        '''Adds text to widgets'''
        self.setWindowTitle(self.__tr("HPGL GUI ") + self.tr("Create cube"))

        # Tab 1
        self.GridSizeGB.setTitle(self.__tr("Grid Size"))
        self.GridSizeXLabel.setText(self.__tr("x"))
        self.GridSizeX.setText('0')
        self.GridSizeYLabel.setText(self.__tr("y"))
        self.GridSizeY.setText('0')
        self.GridSizeZLabel.setText(self.__tr("z"))
        self.GridSizeZ.setText('0')

        self.IndValuesGB.setTitle(self.__tr("Undefined values and indicators"))
        self.IndValuesCheckbox.setText(self.__tr("Indicator values"))
        self.UndefValueLabel.setText(self.__tr("Undefined value"))
        self.undefValue.setText(self.__tr("-99"))
        self.constantCB.setText(self.__tr("Fill with constant"))
        self.constant.setText('0')
        self.cubeNameLabel.setText(self.__tr("Name"))

        self.createCubeButton.setText(self.__tr("Create cube"))

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
