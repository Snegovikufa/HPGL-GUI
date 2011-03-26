from PySide import QtCore, QtGui
from geo_bsd import SugarboxGrid
from geo_bsd.routines import LoadGslibFile
from gui_widgets.cube_list import CubeItem
from hpgl_run.load_cube_thread import LoadCubeThread

class LoadCube(QtGui.QDialog):
    cubeSignal = QtCore.Signal(object)
    loadingSignal = QtCore.Signal(bool)
    logMessage = QtCore.Signal(str)
    
    iterator = 0
    numpy_name = 'numpy_array_'

    def __init__(self, parent=None):
        super(LoadCube, self).__init__(parent)
        self.resize(500, 160)

        self.initWidgets()
        self.initSignals()

        self.RetranslateUI(self)

        # Mistakes
        self.Err = ''
        self.log = ''

    def initSignals(self):
        # Signals/slots
        self.connect(self.loadCubeButton, QtCore.SIGNAL("clicked()"), self.CubeLoad)
        self.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"), self.IndValues.setEnabled)
        self.connect(self.GridSizeX, QtCore.SIGNAL("textChanged(QString)"), self.CubeLoadAccess)
        self.connect(self.GridSizeY, QtCore.SIGNAL("textChanged(QString)"), self.CubeLoadAccess)
        self.connect(self.GridSizeZ, QtCore.SIGNAL("textChanged(QString)"), self.CubeLoadAccess)
        self.connect(self.fileFormat, QtCore.SIGNAL("currentIndexChanged(int)"), self.enableDisableGridSizes)

    def initWidgets(self):
        self.mainLayout = QtGui.QGridLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(6, 0, 6, 0)
        
        intValidator = QtGui.QIntValidator(self)
        intValidator.setBottom(1)
        doubleValidator = QtGui.QDoubleValidator(self)

        self.GridSizeGB = QtGui.QGroupBox(self)
        self.GridLayout = QtGui.QGridLayout(self.GridSizeGB)
#        self.GridLayout.setContentsMargins(0, 0, 6, 0)
#        self.GridLayout.setSpacing(0)
        
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
        self.IndValuesLayout.setSpacing(0)
        self.IndValuesLayout.setContentsMargins(0, 0, 6, 0)
        
        self.IndValues = QtGui.QSpinBox(self.IndValuesGB)
        self.IndValues.setEnabled(False)
        self.IndValues.setMinimum(2)
        self.IndValues.setMaximum(256)
        self.IndValuesCheckbox = QtGui.QCheckBox(self.IndValuesGB)
        #self.IndValuesCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
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
                                 IndValuesSpacerL, IndValuesSpacerR,
                                 ]
        self.IndValuesWidgetsPlaces = [[1, 2, 1, 1], [1, 1, 1, 1],
                                       [2, 1, 1, 1], [2, 2, 1, 1],
                                       [1, 3, 1, 1], [1, 0, 1, 1],
                                       ]

        self.LoadCubeGB = QtGui.QGroupBox(self)
        self.LoadCubeLayout = QtGui.QGridLayout(self.LoadCubeGB)
#        self.LoadCubeLayout.setSpacing(0)
#        self.LoadCubeLayout.setContentsMargins(0, 0, 0, 0)
        
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
        
        fileFormatGB = QtGui.QGroupBox(self)
        fileFormatLayout = QtGui.QHBoxLayout(fileFormatGB)
        
        self.fileFormatLabel = QtGui.QLabel()
        self.fileFormat = QtGui.QComboBox()
        
        items = [ self.__tr('Eclipse Property'),
                  self.__tr('GSLIB'),
                  self.__tr('Numpy array') ]
        self.fileFormat.addItems(items)
        
        fileFormatLayout.addWidget(self.fileFormatLabel)
        fileFormatLayout.addWidget(self.fileFormat)

        self.Widgets = [fileFormatGB,
                        self.GridSizeGB, self.IndValuesGB,
                        self.LoadCubeGB]
        self.WidgetsPlaces = [[0, 0, 1, 2],
                              [1, 0, 1, 1], [1, 1, 1, 1],
                              [3, 0, 1, 2]]

        self.PlaceWidgetsAtPlaces(self.GridLayout, self.GridSizeWidgets, self.GridSizeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.IndValuesLayout, self.IndValuesWidgets, self.IndValuesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.LoadCubeLayout, self.LoadCubeWidgets, self.LoadCubeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.mainLayout, self.Widgets, self.WidgetsPlaces)


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
#            return
        
        if int(self.GridSizeX.text()) > 0 and \
                int(self.GridSizeY.text()) > 0 and \
                    int(self.GridSizeZ.text()) > 0:
            self.loadCubeButton.setEnabled(1)
            self.loadCubeButton.setToolTip('')
            
        if self.fileFormat.currentIndex() == 2:
            
            self.loadCubeButton.setEnabled(1)
            self.loadCubeButton.setToolTip('')

    def enableDisableGridSizes(self):
        type = self.fileFormat.currentIndex()
        
        if type == 0 or type == 1:
            self.GridSizeX.setDisabled(0)
            self.GridSizeY.setDisabled(0)
            self.GridSizeZ.setDisabled(0)
        elif type == 2:
            self.GridSizeX.setDisabled(1)
            self.GridSizeY.setDisabled(1)
            self.GridSizeZ.setDisabled(1)
            
            self.loadCubeButton.setEnabled(1)
            self.loadCubeButton.setToolTip('')

    def loadEclipse(self, filepath):
        
        self.loadingSignal.emit(True)
        
        item = self.getItem(filepath)
        
        
        self.newThread = LoadCubeThread(filepath, item.undefValue(),
                                        item.gridSize(), item.indicators())
        self.newThread.cubeSignal.connect(self.catchProp)
        self.newThread.start()


    def loadGSLIB(self, filepath):
        
        gridSize = (int(self.GridSizeX.text()), 
                        int(self.GridSizeY.text()), 
                            int(self.GridSizeZ.text()))
        
        cubesDict = LoadGslibFile(filepath, gridSize)
        
        for i in xrange(len(cubesDict)):
            item = self.getItem()
            item.setName( cubesDict.keys()[i] )
            
            self.cubeSignal.emit(item)

    def loadNumpy(self, filepath):
        # FIXME: move up
        from numpy import load, shape
        
        self.item = CubeItem()
        
        prop = load(filepath)
        print type(prop)
        gridSize = shape(prop)
        gridObject = SugarboxGrid(*gridSize)
        undefValue = float(self.undefValue.text())
        name = self.numpy_name+str(self.iterator)
        self.iterator += 1
        
        if self.IndValuesCheckbox.isChecked():
            indValues = range(int(self.IndValues.text()))
        else:
            indValues = None
        
        self.item.append(prop, undefValue, indValues, gridObject, 
                         name, gridSize)
        
        self.cubeSignal.emit(self.item)
    
    def getItem(self, filepath = None):
        
        gridSize = int(self.GridSizeX.text()), int(self.GridSizeY.text()), int(self.GridSizeZ.text())
        gridObject = SugarboxGrid(*gridSize)
        undefValue = float(self.undefValue.text())
        
        if self.IndValuesCheckbox.isChecked():
            indValues = range(int(self.IndValues.text()))
        else:
            indValues = None
            
        if filepath:
            cubeName = self.getCubeName(filepath)
        else:
            cubeName = None
        
        item = CubeItem()
        item.append(None, undefValue, indValues, gridObject, cubeName, gridSize)
        
        return item
        
    def CubeLoad(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Select file')[0]

        if filepath:
            
            if self.fileFormat.currentIndex() == 0:
                self.loadEclipse(filepath)
            
            elif self.fileFormat.currentIndex() == 1:
                self.loadGSLIB(filepath)
            
            elif self.fileFormat.currentIndex() == 2:
                self.loadNumpy(filepath)
                
            self.hide()
        

    def catchProp(self, prop):
        self.item.setProperty(prop)

#        self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.item)
        self.cubeSignal.emit(self.item)
#        self.emit(QtCore.SIGNAL("Loading(PyQt_PyObject)"), False)
        self.loadingSignal.emit(False)

    def getCubeName(self, filepath):
        '''Return cubes' name that described inside of Eclipse property file'''
        try:
            f = open(filepath, 'r')

            line = 'blah-blah-blah' # Only for first cycle step =)
            while line != '':
                line = f.readline()
                clearline = line.lstrip()

                if clearline.startswith('--') : continue
                if clearline == '' : continue

                break

            f.close()
            return line.rstrip()

        except IOError, err:
            print 'Error while loading:\n', err

    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(QtGui.QSpacerItem(0,0)):
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
        self.fileFormatLabel.setText(self.__tr('File format'))
        
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

    def emitLog(self, text):
        #self.emit(QtCore.SIGNAL('LogMessage(QString &)'), text)
        self.logMessage.emit(text)

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        #return QtGui.qApp.translate("MainWindow", string, dis,
        #                             QtGui.QApplication.UnicodeUTF8)
        return str(string)
