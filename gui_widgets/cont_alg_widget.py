from PyQt4 import QtCore, QtGui
from geo_bsd import CovarianceModel, set_thread_num
import gui_widgets.lvmwidget as GWLvm
import gui_widgets.okwidget as GWOk
import gui_widgets.sgswidget as GWSgs
import gui_widgets.skwidget as GWSk
#from gui_widgets.cube_list import CubeItem
import hpgl_run.lvm_thread as LVMT
import hpgl_run.ok_thread as OKT
import hpgl_run.sgs_thread as SGST
import hpgl_run.sk_thread as SKT

class ContAlgWidget(QtGui.QDialog):
    def __init__(self, iterator=0, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(650, 450)

        self.iterator = iterator
        self.algorithmTypes = [self.__tr('Simple Kriging'),
                               self.__tr('Ordinary Kriging'),
                               self.__tr('LVM Kriging'),
                               self.__tr('Sequential Gaussian Simulation')]
        self.log = ''

        self.initWidgets()
        self.initSignals()
        self.retranslateUI(self)

        # Comboboxes
        self.indCombo = [self.SGSWidget.MaskCombobox]
        self.contCombo = [self.LVMWidget.meanCombobox,
                          self.SGSWidget.meanCombobox]

    def initSignals(self):
        self.connect(self.AlgorithmType,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.AlgorithmTypeChanged)
        self.connect(self.RunButton, QtCore.SIGNAL("clicked()"),
                     self.AlgorithmRun)


    def initWidgets(self):
        self.intValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)

        self.CentralWidget = QtGui.QWidget()
        self.CentralLayout = QtGui.QGridLayout(self.CentralWidget)
        self.setLayout(self.CentralLayout)

        self.TabWidget = QtGui.QTabWidget(self.CentralWidget)

        self.Tab2 = QtGui.QWidget()
        self.Tab2Layout = QtGui.QGridLayout(self.Tab2)
        self.AlgorithmTypeGB = QtGui.QGroupBox(self.Tab2)
        self.AlgorithmTypeLayout = QtGui.QGridLayout(self.AlgorithmTypeGB)
        self.AlgorithmTypeLabel = QtGui.QLabel(self.AlgorithmTypeGB)
        self.AlgorithmType = QtGui.QComboBox(self.AlgorithmTypeGB)
        self.AlgorithmType.addItems(self.algorithmTypes)

        self.threadsNumLabel = QtGui.QLabel(self.AlgorithmTypeGB)
        self.threadsNum = QtGui.QSpinBox(self.AlgorithmTypeGB)
        self.threadsNum.setRange(1, 4)
        spacer = QtGui.QSpacerItem(20, 40,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Minimum)

        self.AlgorithmTypeWidgets = [self.AlgorithmTypeLabel,
                                     self.AlgorithmType,
                                     spacer,
                                     self.threadsNumLabel,
                                     self.threadsNum]
        self.AlgorithmTypeWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                           [0, 3, 1, 1],
                                           [0, 4, 1, 1], [0, 5, 1, 1]]

        self.AlgorithmWidget = QtGui.QStackedWidget()
        self.SKWidget = GWSk.skwidget()
        self.OKWidget = GWOk.okwidget()
        self.LVMWidget = GWLvm.lvmwidget()
        self.SGSWidget = GWSgs.sgswidget()
        self.AlgorithmWidgets = [self.SKWidget, self.OKWidget,
                                 self.LVMWidget, self.SGSWidget]
        for i in xrange(len(self.AlgorithmWidgets)):
            self.AlgorithmWidget.addWidget(self.AlgorithmWidgets[i])

        self.Tab2Spacer = QtGui.QSpacerItem(20, 40,
                                            QtGui.QSizePolicy.Minimum,
                                            QtGui.QSizePolicy.Expanding)
        self.Tab2Widgets = [self.AlgorithmTypeGB,
                            self.AlgorithmWidget, self.Tab2Spacer]
        self.Tab2WidgetsPlaces = [[0, 0, 1, 1],
                                  [1, 0, 1, 2], [3, 1, 1, 1]]

        self.PlaceWidgetsAtPlaces(self.AlgorithmTypeLayout,
                                  self.AlgorithmTypeWidgets,
                                  self.AlgorithmTypeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.Tab2Layout, self.Tab2Widgets, self.Tab2WidgetsPlaces)
        self.TabWidget.addTab(self.Tab2, "")

        # TAB 3
        self.Tab3 = QtGui.QWidget()
        self.Tab3Layout = QtGui.QGridLayout(self.Tab3)
        self.Tab3Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)

        # Variogram
        self.VariogramTypeGB = QtGui.QGroupBox(self.Tab3)
        self.VariogramTypeGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
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

        # Ranges
        self.EllipsoidRangesGB = QtGui.QGroupBox(self.Tab3)
        self.EllipsoidRangesGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
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

        # Angles
        self.EllipsoidAnglesGB = QtGui.QGroupBox(self.Tab3)
        self.EllipsoidAnglesGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
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

        # Nugget Effect, Sill Value
        self.NuggetEffectGB = QtGui.QGroupBox(self.Tab3)
        self.NuggetEffectGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        self.NuggetEffectLayout = QtGui.QGridLayout(self.NuggetEffectGB)
        self.SillValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.SillValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.SillValue.setValidator(self.DoubleValidator)
        self.NuggetValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.NuggetValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.NuggetValue.setValidator(self.DoubleValidator)
        NuggetEffectSpacerL = QtGui.QSpacerItem(40, 20,
                                                QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Minimum)
        NuggetEffectSpacerR = QtGui.QSpacerItem(40, 20,
                                                QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Minimum)
        self.NuggetEffectWidgets = [self.SillValueLabel, self.SillValue,
                                    self.NuggetValueLabel, self.NuggetValue,
                                    NuggetEffectSpacerL, NuggetEffectSpacerR]
        self.NuggetEffectWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                          [1, 1, 1, 1], [1, 2, 1, 1],
                                          [0, 0, 1, 1], [0, 3, 1, 1]]

        # TabWidget
        self.Tab3Widgets = [self.VariogramTypeGB, self.EllipsoidRangesGB,
                            self.EllipsoidAnglesGB, self.NuggetEffectGB,
                            self.Tab3Spacer]
        self.Tab3WidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1],
                                  [1, 0, 1, 1], [1, 1, 1, 1],
                                  [2, 1, 1, 1]]

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
        self.PlaceWidgetsAtPlaces(self.Tab3Layout,
                                  self.Tab3Widgets,
                                  self.Tab3WidgetsPlaces)
        self.TabWidget.addTab(self.Tab3, "")

        # Other Mainwindow layouts, bars, etc.
        #     Run Button
        self.RunGB = QtGui.QGroupBox(self)
        self.RunLayout = QtGui.QGridLayout(self.RunGB)
        self.RunButton = QtGui.QPushButton(self.RunGB)
        RunSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        RunSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.RunWidgets = [self.RunButton,
                           RunSpacerL, RunSpacerR]
        self.RunWidgetsPlaces = [[0, 1, 1, 1],
                                 [0, 0, 1, 1], [0, 3, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.RunLayout, self.RunWidgets, self.RunWidgetsPlaces)

        #    Central widget
        self.CentralLayout.addWidget(self.RunGB, 2, 0, 1, 2)
        self.CentralLayout.addWidget(self.TabWidget, 0, 0, 1, 1)

    def UpdateUI(self, string):
        '''Outputs HPGL\'s output to log'''
        self.emit(QtCore.SIGNAL("msg(QString)"), QtCore.QString(string))

    def UpdateProgress(self, value):
        '''Emits percentage of current algorithm progress'''
        self.emit(QtCore.SIGNAL('progress(PyQt_PyObject)'), value)

    def AlgorithmTypeChanged(self, value):
        '''Locks and unlocks widgets for cont and ind cubes'''
        self.AlgorithmWidget.setCurrentIndex(value)
        if value == 3:
            self.SGSWidget.SeedGB.show()
            self.SGSWidget.MaskGB.show()
        else:
            self.SGSWidget.SeedGB.hide()
            self.SGSWidget.MaskGB.hide()

    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.Tab2Spacer):
                layout.addItem(widgets[i], places[i][0], places[i][1],
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])

    def isVariogramValid(self):
        '''Checks variogram values before running algorithm'''
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
        # Additional check
        self.SR = self.AlgorithmWidgets[self.AlgorithmType.currentIndex()].getSearchRanges()
        self.VR = self.GetVariogramRanges()
        if self.SR < self.VR:
            self.Err += '"Search Ranges" are smaller than "Variogram Ranges"\n'

        if self.Err == '':
            return 1
        else:
            self.ShowError(self.Err)
            self.Err = ''
            return 0

    def ShowError(self, string):
        '''Error output widget'''
        self.ErrorWindow = QtGui.QMessageBox()
        self.ErrorWindow.warning(None, self.__tr("Error"), self.__tr(string))

    def GetVariogramRanges(self):
        '''Returns variogram ranges'''
        return (int(self.EllipsoidRanges0.text()),
                int(self.EllipsoidRanges90.text()),
                int(self.EllipsoidRangesV.text()))

    def GetVariogramAngles(self):
        '''Returns variogram angles'''
        return (int(self.EllipsoidAnglesX.text()),
                int(self.EllipsoidAnglesY.text()),
                int(self.EllipsoidAnglesZ.text()))

    def GetVariogram(self):
        '''Returns variogram from entered variogram values'''
        VarRanges = self.GetVariogramRanges()
        VarAngles = self.GetVariogramAngles()
        VarType = int(self.VariogramType.currentIndex())
        sillValue = float(self.SillValue.text())
        nuggetValue = float(self.NuggetValue.text())

#self.emitLog(
#            '# CREATING VARIOGRAM\n'+
#            'varRanges = %s\n' % (VarRanges,) +
#            'varAngles = %s\n' % (VarAngles,) +
#            'varType = %i\n' % (VarType) +
#            'sillValue = %f\n' % (sillValue) +
#           'nuggetValue = %f\n' % (nuggetValue) +
#           'variogram = CovarianceModel(varType, varRanges, '+
#                                       'varAngles, sillValue, nuggetValue)'
#       )

        return CovarianceModel(VarType, VarRanges, VarAngles, sillValue, nuggetValue)

    def UpdateMean(self):
        '''Puts calculated mean value to cont cubes\' widgets'''
        Mean = self.cubes.meanOf(self.currIndex)
        self.SKWidget.meanValue.setText(str('%.2f' % Mean))
        self.SGSWidget.meanValue.setText(str('%.2f' % Mean))

    def push(self, cubes, Curr_index, indCubes):
        from copy import copy
        self.currIndex = Curr_index
        self.cubes = cubes
        self.indCubes = indCubes
        self.parentItem = copy(self.cubes.item(self.currIndex))

        names = self.cubes.allNames()
        for j in self.contCombo:
            j.clear()
            j.addItems(names)
            
        names = self.indCubes.allNames()
        for j in self.indCombo:
            j.clear()
            j.addItems(names)

        self.UpdateMean()
        self.show()

    def CatchResult(self, Result):
        '''Catchs result of algorithm'''
        self.RunButton.setEnabled(1)
        self.RunButton.setToolTip('')

        if Result != None:
            self.parentItem.setProperty(Result)
            name = self.parentItem.name()+self.algName+'_'+str(self.iterator)
            self.parentItem.setName(name)

            self.emit(QtCore.SIGNAL("finished(PyQt_PyObject)"), True)
            self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.parentItem)
            self.close()

    def AlgorithmRun(self):
        # Setting threads
        set_thread_num(int(self.threadsNum.value()))

        if self.isVariogramValid() == 1:
            if self.AlgorithmType.currentIndex() == 0:
                check, self.Err = self.SKWidget.isValuesValid()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.hide()

                    self.log += "Starting Simple Kriging Algorithm\n"
                    self.algName = '_SK'

                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.SKWidget.getSearchRanges()
                    IntPoints = self.SKWidget.getIntPoints()
                    Mean = self.cubes.meanOf(self.currIndex)
                    self.NewThread = SKT.SKThread(self.cubes.property(self.currIndex),
                                                  self.cubes.gridObject(self.currIndex),
                                                  EllipsoidRanges, IntPoints,
                                                  Variogram, Mean
                                                 )
#                    self.emitLog(
#                       '# RUNNING SIMPLE KRIGING\n' +
#                       'ellipsRanges = %s\n' % (EllipsoidRanges,) +
#                       'intPoints = %i\n' % (IntPoints,) +
#                       'mean = %f\n' % (Mean,) +
#                       'result = simple_kriging(prop, gridObject, '+
#                       'ellipsRanges, intPoints, variogram, mean)'
#                   )

                    info = ['Simple Kriging', self.NewThread]
                    self.emit(QtCore.SIGNAL('algorithm(PyQt_PyObject)'), info)

                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("msg(QString)"),
                                           self.UpdateUI)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("progress(QString)"),
                                           self.UpdateProgress)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("Result(PyQt_PyObject)"),
                                           self.CatchResult)

                    self.NewThread.start()
                    self.RunButton.setDisabled(1)
                    self.RunButton.setToolTip(self.__tr("Wait while algorithm is processing"))

            elif self.AlgorithmType.currentIndex() == 1:
                check, self.Err = self.OKWidget.isValuesValid()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.hide()

                    self.algName = '_OK'

                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.OKWidget.getSearchRanges()
                    IntPoints = self.OKWidget.getIntPoints()
                    self.NewThread = OKT.OKThread(self.cubes.property(self.currIndex),
                                               self.cubes.gridObject(self.currIndex),
                                               EllipsoidRanges, IntPoints,
                                               Variogram)
#                   self.emitLog(
#                       '# RUNNING ORDINARY KRIGING\n' +
#                       'ellipsRanges = %s\n' % (EllipsoidRanges,) +
#                        'intPoints = %i\n' % (IntPoints,) +
#                       'result = ordinary_kriging(prop, gridObject, '+
#                       'ellipsRanges, intPoints, variogram)'
#                   )

                    info = ['Ordinary Kriging', self]
                    self.emit(QtCore.SIGNAL('algorithm(PyQt_PyObject)'), info)

                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("msg(QString)"),
                                           self.UpdateUI)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("progress(QString)"),
                                           self.UpdateProgress)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("Result(PyQt_PyObject)"),
                                           self.CatchResult)

                    self.NewThread.start()
                    self.RunButton.setDisabled(1)
                    self.RunButton.setToolTip(self.__tr("Wait while algorithm is processing"))

            elif self.AlgorithmType.currentIndex() == 2:
                check, self.Err = self.LVMWidget.isValuesValid()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.hide()

                    self.log += "Starting Local Varying Mean Algorithm\n"
                    self.algName = '_LVM'

                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.LVMWidget.getSearchRanges()
                    IntPoints = self.LVMWidget.getIntPoints()
                    Mean = self.LVMWidget.getMean(self.cubes)
                    self.NewThread = LVMT.LVMThread(self.cubes.property(self.currIndex),
                                               self.cubes.gridObject(self.currIndex),
                                               Mean, EllipsoidRanges,
                                               IntPoints, Variogram)
#self.emitLog(
#                       '# RUNNING LVM KRIGING\n' +
#                       'ellipsRanges = %s\n' % (EllipsoidRanges,) +
#                       'intPoints = %i\n' % (IntPoints,) +
#                       'mean = %s\n' % (Mean,) +
#                       'result = lvm_kriging(prop, gridObject, '+
#                       'mean, ellipsRanges, intPoints, variogram)'
#                   )

                    info = ['LVM Kriging', self]
                    self.emit(QtCore.SIGNAL('algorithm(PyQt_PyObject)'), info)

                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("msg(QString)"),
                                           self.UpdateUI)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("progress(QString)"),
                                           self.UpdateProgress)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("Result(PyQt_PyObject)"),
                                           self.CatchResult)

                    self.NewThread.start()

                    self.RunButton.setDisabled(1)
                    self.RunButton.setToolTip(self.__tr("Wait while algorithm is processing"))

            elif self.AlgorithmType.currentIndex() == 3:
                check, self.Err = self.SGSWidget.isValuesValid(self.Err)
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.hide()

                    self.log += "Starting Sequantial Gaussian Algorithm\n"
                    self.algName = '_SGS'

                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.SGSWidget.getSearchRanges()
                    IntPoints = self.SGSWidget.getIntPoints()
                    Seed = self.SGSWidget.GetSeed()
                    UseHd = self.SGSWidget.GetUseHd()
                    KrType = self.SGSWidget.GetKrType()
                    Mean = self.SGSWidget.getMean(self.cubes)
                    Mask = self.SGSWidget.GetMask(self.cubes)
                    self.NewThread = SGST.SGSThread(self.cubes.property(self.currIndex),
                                                self.cubes.gridObject(self.currIndex),
                                                EllipsoidRanges, IntPoints,
                                                Variogram, Seed, KrType, Mean,
                                                UseHd, Mask)

                    info = ['SGS', self]
                    self.emit(QtCore.SIGNAL('algorithm(PyQt_PyObject)'), info)

                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("msg(QString)"),
                                           self.UpdateUI)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("progress(QString)"),
                                           self.UpdateProgress)
                    QtCore.QObject.connect(self.NewThread,
                                           QtCore.SIGNAL("Result(PyQt_PyObject)"),
                                           self.CatchResult)

                    self.NewThread.start()
                    self.RunButton.setDisabled(1)
                    self.RunButton.setToolTip(self.__tr("Wait while algorithm is processing"))

    def emitLog(self, text):
        self.emit(QtCore.SIGNAL('LogMessage(QString&)'), text)

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)

    def retranslateUI(self, MainWindow):
        '''Adds text to widgets'''
        self.setWindowTitle(self.__tr('HPGL GUI: ')+
                            self.__tr('Continuous Algorithms'))
        # Tab 2
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))

        self.AlgorithmTypeGB.setTitle(self.__tr("Algorithm"))
        self.AlgorithmTypeLabel.setText(self.__tr("Algorithm type"))
        self.threadsNumLabel.setText(self.__tr('Number of threads'))

        for i in xrange(len(self.algorithmTypes)):
            self.AlgorithmType.setItemText(i, (self.__tr(self.algorithmTypes[i])))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab2),
                                  (self.__tr("Algorithms")))

        # Tab 3
        self.VariogramTypeGB.setTitle(self.__tr("Variogram type"))
        self.VariogramType_label.setText(self.__tr("Type"))
        self.VariogramTypes = ['Spherical', 'Exponential', 'Gaussian']
        for i in xrange(len(self.VariogramTypes)):
            self.VariogramType.setItemText(i, (self.__tr(self.VariogramTypes[i])))

        self.EllipsoidRangesGB.setTitle(self.__tr("Variogram ranges"))
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
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab3),
                                  (self.__tr("Variogram")))
