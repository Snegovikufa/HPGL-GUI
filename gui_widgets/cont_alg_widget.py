from PyQt4 import QtCore, QtGui
from geo_bsd import CovarianceModel
from geo_bsd.routines import CalcMean
import hpgl_run.ok_thread as OKT
import hpgl_run.sk_thread as SKT
import hpgl_run.lvm_thread as LVMT
import hpgl_run.sgs_thread as SGST
import gui_widgets.skwidget as GWSk
import gui_widgets.okwidget as GWOk
import gui_widgets.sgswidget as GWSgs
import gui_widgets.lvmwidget as GWLvm

class ContAlgWidget(QtGui.QDialog):
    def __init__(self, iterator = 0, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(650, 450)
        
        self.Iterator = iterator
        self.AlgorithmTypes = [self.__tr('Simple Kriging'), 
                               self.__tr('Ordinary Kriging'),
                               self.__tr('LVM Kriging'), 
                               self.__tr('Sequential Gaussian Simulation')]
        self.Log = ''
        
        self.InitWidgets()
        self.InitSignals()
        self.RetranslateUI(self)
        
        # Comboboxes
        self.IndCombo = [self.SGSWidget.MaskCombobox]
        self.ContCombo = [self.LVMWidget.MeanCombobox, 
                          self.SGSWidget.MeanCombobox]

    def InitSignals(self):
        self.connect(self.AlgorithmType, QtCore.SIGNAL("currentIndexChanged(int)"), self.AlgorithmTypeChanged)
        self.connect(self.RunButton, QtCore.SIGNAL("clicked()"), self.AlgorithmRun)


    def InitWidgets(self):
        self.IntValidator = QtGui.QIntValidator(self)
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
        self.AlgorithmType.addItems(self.AlgorithmTypes)
        
        AlgorithmTypeSpacerL = QtGui.QSpacerItem(40, 20, 
                                                QtGui.QSizePolicy.Expanding, 
                                                QtGui.QSizePolicy.Minimum)
        AlgorithmTypeSpacerR = QtGui.QSpacerItem(40, 20, 
                                                 QtGui.QSizePolicy.Expanding, 
                                                 QtGui.QSizePolicy.Minimum)
        self.AlgorithmTypeWidgets = [self.AlgorithmTypeLabel, 
                                     self.AlgorithmType, 
                                     AlgorithmTypeSpacerL, 
                                     AlgorithmTypeSpacerR]
        self.AlgorithmTypeWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1], 
                                           [0, 0, 1, 1], [0, 3, 1, 1]]
        
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
        self.VariogramType.setValidator(self.IntValidator)
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
        self.EllipsoidRanges0.setValidator(self.IntValidator)
        self.EllipsoidRanges90Label = QtGui.QLabel(self.EllipsoidRangesGB)
        self.EllipsoidRanges90 = QtGui.QLineEdit(self.EllipsoidRangesGB)
        self.EllipsoidRanges90.setValidator(self.IntValidator)
        self.EllipsoidRangesVLabel = QtGui.QLabel(self.EllipsoidRangesGB)
        self.EllipsoidRangesV = QtGui.QLineEdit(self.EllipsoidRangesGB)
        self.EllipsoidRangesV.setValidator(self.IntValidator)
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
        self.EllipsoidAnglesX.setValidator(self.IntValidator)
        self.EllipsoidAnglesYLabel = QtGui.QLabel(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesY = QtGui.QLineEdit(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesY.setValidator(self.IntValidator)
        self.EllipsoidAnglesZLabel = QtGui.QLabel(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesZ = QtGui.QLineEdit(self.EllipsoidAnglesGB)
        self.EllipsoidAnglesZ.setValidator(self.IntValidator)
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
        self.NuggetValue.setValidator(self.IntValidator)
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
        self.ProgressBar = QtGui.QProgressBar(self)
        self.ProgressBar.setProperty("value", 24)
        self.ProgressBar.setValue(0)
        self.ProgressBar.hide()
        self.CentralLayout.addWidget(self.ProgressBar, 1, 0, 1, 1)

    def UpdateUI(self, string):
        '''Outputs HPGL\'s output to log'''
        self.Log += "%s" % unicode(string)
        
    def UpdateProgress(self, value):
        '''Outputs percentage of current algorithm progress'''
        self.ProgressBar.setValue(int(value))
        
    def AlgorithmTypeChanged(self, value):
        '''Locks and unlocks widgets for cont and ind cubes'''
        self.AlgorithmWidget.setCurrentIndex(value)
        
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
            self.Err +='"Ellipsoid ranges 0" is empty\n'
        if self.EllipsoidRanges90.text() == "":
            self.Err +='"Ellipsoid ranges 90" is empty\n'
        if self.EllipsoidRangesV.text() == "":
            self.Err +='"Ellipsoid ranges vertical" is empty\n'
        if self.EllipsoidAnglesX.text() == "":
            self.Err +='"Ellipsoid angles x" is empty\n'
        if self.EllipsoidAnglesY.text() == "":
            self.Err +='"Ellipsoid angles y" is empty\n'
        if self.EllipsoidAnglesZ.text() == "":
            self.Err +='"Ellipsoid angles z" is empty\n'
        if self.SillValue.text() == "":
            self.Err +='"Sill value" is empty\n'
        if self.NuggetValue.text() == "":
            self.Err +='"Nugget effect value" is empty\n'
        # Additional check
        self.SR = self.AlgorithmWidgets[self.AlgorithmType.currentIndex()].GetSearchRanges()
        self.VR = self.GetVariogramRanges()
        if self.SR < self.VR:
            self.Err +='"Search Ranges" are smaller than "Variogram Ranges"\n'
        
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
        return ( int(self.EllipsoidRanges0.text()), 
                 int(self.EllipsoidRanges90.text()), 
                 int(self.EllipsoidRangesV.text()) )
        
    def GetVariogramAngles(self):
        '''Returns variogram angles'''
        return ( int(self.EllipsoidAnglesX.text()), 
                 int(self.EllipsoidAnglesY.text()), 
                 int(self.EllipsoidAnglesZ.text()) )
    
    def GetVariogram(self):
        '''Returns variogram from entered variogram values'''
        VariogramRanges = self.GetVariogramRanges()
        VariogramAngles = self.GetVariogramAngles()
        return CovarianceModel( int(self.VariogramType.currentIndex()),
                                VariogramRanges, VariogramAngles, 
                                float(self.SillValue.text()), 
                                int(self.NuggetValue.text()) )
        
    def UpdateMean(self):
        '''Puts calculated mean value to cont cubes\' widgets'''
        if self.Cubes[self.CurrIndex][2] == None:
            self.Mean = CalcMean(self.Cubes[self.CurrIndex][0][0],
                                 self.Cubes[self.CurrIndex][0][1])
            self.SKWidget.MeanValue.setText(str('%.2f' % self.Mean))
            self.SGSWidget.MeanValue.setText(str('%.2f' % self.Mean))
            
    def Push(self, Cubes, Curr_index):
        self.CurrIndex = Curr_index
        self.Cubes = Cubes
        
        for j in xrange(len(self.ContCombo)):
            for i in xrange(len(self.Cubes)):
                self.ContCombo[j].addItem(self.Cubes[i][4])
        
        self.UpdateMean()
        self.show()
    
    def CatchResult(self, Result):
        '''Catchs result of algorithm'''
        self.Result = Result
        self.RunButton.setEnabled(1)
        self.RunButton.setToolTip('')
        if self.Result != None:
            self.ResultCube = [self.Result, 
                               self.Cubes[self.CurrIndex][1],
                               self.Cubes[self.CurrIndex][2],
                               self.Cubes[self.CurrIndex][3],
                               self.Cubes[self.CurrIndex][4]+'_'+str(self.Iterator),
                               self.Cubes[self.CurrIndex][5]]
            self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.ResultCube)
            self.close()
        
    def AlgorithmRun(self):
        if self.isVariogramValid() == 1:
            if self.AlgorithmType.currentIndex() == 0:
                check, self.Err = self.SKWidget.isValuesValid()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.Log += "Starting Simple Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.SKWidget.GetSearchRanges()
                    IntPoints = self.SKWidget.GetIntPoints()
                    Mean = self.SKWidget.GetMean()
                    self.NewThread = SKT.SKThread( self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3], 
                                               EllipsoidRanges, IntPoints, 
                                               Variogram, Mean )
                    
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
                    self.Log += "Starting Ordinary Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    Variogram = self.GetVariogram()                        
                    EllipsoidRanges = self.OKWidget.GetSearchRanges()
                    IntPoints = self.OKWidget.GetIntPoints()
                    self.NewThread = OKT.OKThread( self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3], 
                                               EllipsoidRanges, IntPoints, 
                                               Variogram )
                    
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
                    self.Log += "Starting Locale Varying Mean Algorithm\n"
                    self.ProgressBar.show()
                    
                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.LVMWidget.GetSearchRanges()
                    IntPoints = self.LVMWidget.GetIntPoints()
                    Mean = self.LVMWidget.GetMean(self.Cubes)
                    self.NewThread = LVMT.LVMThread(self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3],
                                               Mean, EllipsoidRanges, 
                                               IntPoints, Variogram )
                    
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
                    self.Log += "Starting Sequantial Gaussian Algorithm\n"
                    self.ProgressBar.show()
                    
                    Variogram = self.GetVariogram()
                    EllipsoidRanges = self.SGSWidget.GetSearchRanges()
                    IntPoints = self.SGSWidget.GetIntPoints()
                    Seed = self.SGSWidget.GetSeed()
                    UseHd = self.SGSWidget.GetUseHd()
                    KrType = self.SGSWidget.GetKrType()
                    Mean = self.SGSWidget.GetMean(self.Cubes)
                    Mask = self.SGSWidget.GetMask(self.Cubes)
                    self.NewThread = SGST.SGSThread( self.Cubes[self.CurrIndex][0], 
                                                self.Cubes[self.CurrIndex][3],
                                                EllipsoidRanges, IntPoints, 
                                                Variogram, Seed, KrType, Mean,
                                                UseHd, Mask )
                    
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
                
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
        
        
    def RetranslateUI(self, MainWindow):
        '''Adds text to widgets'''
        self.setWindowTitle('HPGL GUI: Continuous Algorithms')
        # Tab 2
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))
        
        self.AlgorithmTypeGB.setTitle(self.__tr("Algorithm"))
        self.AlgorithmTypeLabel.setText(self.__tr("Algorithm type"))
        
        for i in xrange(len(self.AlgorithmTypes)):
            self.AlgorithmType.setItemText(i, (self.__tr(self.AlgorithmTypes[i])))
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
