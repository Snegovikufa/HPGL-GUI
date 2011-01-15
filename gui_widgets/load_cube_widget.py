from PyQt4 import QtCore, QtGui
from geo_bsd import load_cont_property
from geo_bsd import load_ind_property
from geo_bsd import SugarboxGrid
import os

class LoadCube(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(500, 160)
        
        self.mainLayout = QtGui.QGridLayout(self)
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
        
        self.IndValues = QtGui.QSpinBox(self.IndValuesGB)
        self.IndValues.setEnabled(False)
        self.IndValues.setMinimum(2)
        self.IndValues.setMaximum(256)
        self.IndValuesCheckbox = QtGui.QCheckBox(self.IndValuesGB)
        self.IndValuesCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.UndefValueLabel = QtGui.QLabel(self.IndValuesGB)
        self.undefValue = QtGui.QLineEdit(self.IndValuesGB)
        self.undefValue.setValidator(doubleValidator)
        IndValuesSpacerL = QtGui.QSpacerItem(40, 20,
                                             QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Minimum)
        IndValuesSpacerR = QtGui.QSpacerItem(40, 20,
                                             QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Minimum)
        
        self.IndValuesWidgets = [self.IndValues, self.IndValuesCheckbox,
                                 self.UndefValueLabel, self.undefValue,
                                 IndValuesSpacerL, IndValuesSpacerR]
        self.IndValuesWidgetsPlaces = [[1, 2, 1, 1], [1, 1, 1, 1],
                                       [2, 1, 1, 1], [2, 2, 1, 1],
                                       [1, 3, 1, 1], [1, 0, 1, 1]]
        
        self.LoadCubeGB = QtGui.QGroupBox(self)
        self.LoadCubeLayout = QtGui.QGridLayout(self.LoadCubeGB)
        
        self.loadCubeButton = QtGui.QPushButton(self.LoadCubeGB)
        self.loadCubeButton.setDisabled(1)
        self.loadCubeButton.setToolTip(self.__tr("Enter grid sizes first"))
        LoadCubeSpacerL = QtGui.QSpacerItem(241, 20,
                                            QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Minimum)
        LoadCubeSpacerR = QtGui.QSpacerItem(241, 20,
                                            QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Minimum)
        
        self.LoadCubeWidgets = [self.loadCubeButton, LoadCubeSpacerL,
                                LoadCubeSpacerR]
        self.LoadCubeWidgetsPlaces = [[0, 1, 1, 1], [0, 0, 1, 1],
                                      [0, 2, 1, 1]]
        
        self.Widgets = [self.GridSizeGB, self.IndValuesGB,
                            self.LoadCubeGB]
        self.WidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1],
                                  [2, 0, 1, 2]]
        
        self.PlaceWidgetsAtPlaces(self.GridLayout, self.GridSizeWidgets,
                                  self.GridSizeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.IndValuesLayout, self.IndValuesWidgets,
                                  self.IndValuesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.LoadCubeLayout, self.LoadCubeWidgets,
                                  self.LoadCubeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.mainLayout, self.Widgets,
                                  self.WidgetsPlaces)
        # Retranslate
        self.RetranslateUI(self)
        
        # Mistakes
        self.Err = ''
        self.Log = ''
        
        # Signals/slots
        self.connect(self.loadCubeButton, QtCore.SIGNAL("clicked()"),
                     self.CubeLoad)
        self.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"),
                     self.IndValues.setEnabled)
        self.connect(self.GridSizeX, QtCore.SIGNAL("textChanged(QString)"),
                     self.CubeLoadAccess)
        self.connect(self.GridSizeY, QtCore.SIGNAL("textChanged(QString)"),
                     self.CubeLoadAccess)
        self.connect(self.GridSizeZ, QtCore.SIGNAL("textChanged(QString)"),
                     self.CubeLoadAccess)
        
    def CubeLoadAccess(self):
        '''Controls the grid size and allow to load cube'''
        if self.GridSizeX.text() == '' or \
            self.GridSizeY.text() == '' or \
            self.GridSizeZ.text() == '' or \
            int(self.GridSizeX.text()) == 0 or \
            int(self.GridSizeY.text()) == 0 or \
            int(self.GridSizeZ.text()) == 0:
            self.loadCubeButton.setDisabled(1)
            self.loadCubeButton.setToolTip(self.__tr("Enter grid sizes first"))
            return
        if int(self.GridSizeX.text()) > 0 and \
            int(self.GridSizeY.text()) > 0 and \
            int(self.GridSizeZ.text()) > 0:
            self.loadCubeButton.setEnabled(1)
            self.loadCubeButton.setToolTip('')
        
    def CubeLoad(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if filename:
            self.emit(QtCore.SIGNAL("Loading(PyQt_PyObject)"), True)
            # First, we must get cube's filename
            CubeName = os.path.basename(str(filename))
            self.Log += "Selected cube: " + CubeName + '\n'
                
            GridObject = SugarboxGrid(int(self.GridSizeX.text()),
                                       int(self.GridSizeY.text()),
                                       int(self.GridSizeZ.text()))
            GridSize = (int(self.GridSizeX.text()),
                        int(self.GridSizeY.text()),
                        int(self.GridSizeZ.text()))
            UndefValue = int(self.undefValue.text())

            if self.IndValuesCheckbox.isChecked():
                self.Log += 'Loading indicator cube\n'
                
                IndValue = range(int(self.IndValues.text()))
                Prop = load_ind_property(unicode(filename),
                                             UndefValue, IndValue, GridSize)
                if Prop != None:
                    Cube = [Prop, UndefValue, IndValue,
                            GridObject, CubeName, GridSize]
                    del(Prop)
                    self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), Cube)
            else:
                self.Log += 'Loaded continuous cube\n'

                Prop = load_cont_property(unicode(filename),
                                                UndefValue,
                                                GridSize)
                if Prop != None:
                    Cube = [Prop, UndefValue, None,
                            GridObject, CubeName, GridSize]
                    del(Prop)
                    self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), Cube)
            
            self.emit(QtCore.SIGNAL("Loading(PyQt_PyObject)"), False)
            self.hide()

    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.GridSizeSpacerL):
                layout.addItem(widgets[i], places[i][0], places[i][1],
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])
            
    def ShowError(self, string):
        '''Error output widget'''
        self.ErrorWindow = QtGui.QMessageBox()
        self.ErrorWindow.warning(None, "Error", str(string))
        
    def RetranslateUI(self, MainWindow):
        '''Adds text to widgets'''
        self.setWindowTitle(self.__tr("HPGL GUI ") + self.tr("Load cube"))
        
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
        
        self.loadCubeButton.setText(self.__tr("Load cube"))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
