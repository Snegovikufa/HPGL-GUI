from PyQt4 import QtCore, QtGui
from geo_bsd import CovarianceModel
from geo_bsd.routines import CalcMean
from geo_bsd import write_property
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
        self.Iterator = iterator
        self.resize(650, 450)
        
        self.AlgorithmTypes = ['Simple Kriging', 'Ordinary Kriging',
                               'LVM Kriging', 'Sequential Gaussian Simulation']
        self.IntValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)
        self.Log = ''
        
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
        
        self.PlaceWidgetsAtPlaces(self.Tab2Layout, 
                                  self.Tab2Widgets, 
                                  self.Tab2WidgetsPlaces)
    
        self.TabWidget.addTab(self.Tab2, "")
        
        # TAB 3
        self.Tab3 = QtGui.QWidget()
        self.Tab3Layout = QtGui.QGridLayout(self.Tab3)
        
        self.VariogramTypeGB = QtGui.QGroupBox(self.Tab3)
        self.VariogramTypeGB.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                           QtGui.QSizePolicy.Preferred)
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
        
        self.EllipsoidRangesGB = QtGui.QGroupBox(self.Tab3)
        self.EllipsoidRangesGB.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                           QtGui.QSizePolicy.Preferred)
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
               
        self.EllipsoidAnglesGB = QtGui.QGroupBox(self.Tab3)
        self.EllipsoidAnglesGB.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                           QtGui.QSizePolicy.Preferred)
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
                
        self.NuggetEffectGB = QtGui.QGroupBox(self.Tab3)
        self.NuggetEffectGB.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                           QtGui.QSizePolicy.Preferred)
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
        
        self.Tab3Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, 
                                       QtGui.QSizePolicy.Expanding)
        
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
        
        
        
        # Other Mainwindow layouths, bars, etc.
        
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
        self.PlaceWidgetsAtPlaces(self.RunLayout, 
                                  self.RunWidgets, 
                                  self.RunWidgetsPlaces)
        self.CentralLayout.addWidget(self.RunGB, 2, 0, 1, 2)      
        
        self.CentralLayout.addWidget(self.TabWidget, 0, 0, 1, 1)
        self.ProgressBar = QtGui.QProgressBar(self)
        self.ProgressBar.setProperty("value", 24)
        self.ProgressBar.setValue(0)
        self.ProgressBar.hide()
        self.CentralLayout.addWidget(self.ProgressBar, 1, 0, 1, 1)
        
        self.RetranslateUI(self)
        
        # Comboboxes
        self.IndCombo = [self.SGSWidget.MaskCombobox]
        self.ContCombo = [self.LVMWidget.MeanCombobox, 
                          self.SGSWidget.MeanCombobox]
        
        self.connect(self.AlgorithmType, 
                     QtCore.SIGNAL("currentIndexChanged(int)"), 
                     self.AlgorithmTypeChanged)
        self.connect(self.RunButton, QtCore.SIGNAL("clicked()"), 
                     self.AlgorithmRun)
        self.connect(self.SaveButton, QtCore.SIGNAL("clicked()"), 
                     self.ResultSave)
        
        
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
                
    def AlgorithmAccess(self, value):
        '''Locks and unlocks widgets for cont and ind widgets'''
        if value < 0 or self.Cubes[value][2] == None:
            self.IKWidget.setDisabled(1)
            self.SISWidget.setDisabled(1)
            self.SKWidget.setEnabled(1)
            self.OKWidget.setEnabled(1)
            self.LVMWidget.setEnabled(1)
            self.SGSWidget.setEnabled(1)
        else:
            self.IKWidget.setDisabled(0)
            self.SISWidget.setDisabled(0)
            self.SKWidget.setEnabled(0)
            self.OKWidget.setEnabled(0)
            self.LVMWidget.setEnabled(0)
            self.SGSWidget.setEnabled(0)
        self.AlgorithmTypeChanged(self.AlgorithmType.currentIndex())
    
    def ResultSave(self):
        '''Saves the result of algorithm'''
        if self.Result != None:
            self.fname = QtGui.QFileDialog.getSaveFileName(self,'Save as ... ')
            if self.fname and self.Result_values[1] != None:
                write_property( self.Result, str(self.fname), 
                                "SK_RESULT", self.Result_values[0], 
                                self.Result_values[1] )
            elif self.fname and self.Result_values[1] == None:
                write_property( self.Result, str(self.fname), 
                                "SK_RESULT", self.Result_values[0] )
        
    def VariogramCheck(self):
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
        self.ErrorWindow.warning(None, "Error", str(string))
        
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
        # Variogram
        self.VariogramRanges = self.GetVariogramRanges()
        self.VariogramAngles = self.GetVariogramAngles()
        self.Variogram = CovarianceModel( int(self.VariogramType.currentIndex()),
                                          self.VariogramRanges, 
                                          self.VariogramAngles, 
                                          float(self.SillValue.text()), 
                                          int(self.NuggetValue.text()) )
        
    def UpdateMean(self):
        '''Puts calculated mean value to cont cubes\' widgets'''
        if self.Cubes[self.CurrIndex][2] == None:
            self.Mean = CalcMean(self.Cubes[self.CurrIndex][0][0],
                                 self.Cubes[self.CurrIndex][0][1])
            self.SKWidget.MeanValue.setText(str('%5.2f' % self.Mean))
            self.SGSWidget.MeanValue.setText(str('%5.2f' % self.Mean))
            
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
            self.Result_values = [self.Cubes[self.CurrIndex][1], 
                                  self.Cubes[self.CurrIndex][2]]
            self.ResultCube = [self.Result, 
                               self.Cubes[self.CurrIndex][1],
                               self.Cubes[self.CurrIndex][2],
                               self.Cubes[self.CurrIndex][3],
                               self.Cubes[self.CurrIndex][4]+'_'+str(self.Iterator),
                               self.Cubes[self.CurrIndex][5]]
            self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.ResultCube)
            self.close()
        
    def AlgorithmRun(self):
        if self.VariogramCheck() == 1:
            if self.AlgorithmType.currentIndex() == 0:
                check, self.Err = self.SKWidget.ValuesCheck()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.Log += "Starting Simple Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # Simple Kriging                                  
                    self.EllipsoidRanges = self.SKWidget.GetSearchRanges()
                    self.IntPoints = self.SKWidget.GetIntPoints()
                    self.Mean = self.SKWidget.GetMean()
                    self.NewThread = SKT.SKThread( self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3], 
                                               self.EllipsoidRanges, 
                                               self.IntPoints, self.Variogram,
                                               self.Mean )
                    
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
                check, self.Err = self.OKWidget.ValuesCheck()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.Log += "Starting Ordinary Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # Ordinary Kriging                                  
                    self.EllipsoidRanges = self.OKWidget.GetSearchRanges()
                    self.IntPoints = self.OKWidget.GetIntPoints()
                    self.NewThread = OKT.OKThread( self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3], 
                                               self.EllipsoidRanges, 
                                               self.IntPoints, self.Variogram )
                    
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
                check, self.Err = self.LVMWidget.ValuesCheck()
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.Log += "Starting Locale Varying Mean Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # LVM
                    self.EllipsoidRanges = self.LVMWidget.GetSearchRanges()
                    self.IntPoints = self.LVMWidget.GetIntPoints()
                    self.Mean = self.LVMWidget.GetMean(self.Cubes, self.CubesCont)
                    
                    self.NewThread = LVMT.LVMThread( self.Cubes[self.CurrIndex][0], 
                                               self.Cubes[self.CurrIndex][3],
                                               self.Mean, 
                                               self.EllipsoidRanges, 
                                               self.IntPoints, self.Variogram )
                    
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
                check, self.Err = self.SGSWidget.ValuesCheck(self.Err)
                if check == 0:
                    self.ShowError(self.Err)
                else:
                    self.Log += "Starting Sequantial Gaussian Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()

                    # Sequantial Gaussian Simulation
                    self.EllipsoidRanges = self.SGSWidget.GetSearchRanges()
                    self.IntPoints = self.SGSWidget.GetIntPoints()
                    self.Seed = self.SGSWidget.GetSeed()
                    self.UseHd = self.SGSWidget.GetUseHd()
                    self.KrType = self.SGSWidget.GetKrType()
                    self.Mean = self.SGSWidget.GetMean(self.Cubes, self.CubesCont)
                    self.Mask = self.SGSWidget.GetMask(self.Cubes, self.CubesInd)
                    
                    self.NewThread = SGST.SGSThread( self.Cubes[self.CurrIndex][0], 
                                                self.Cubes[self.CurrIndex][3],
                                                self.EllipsoidRanges, self.IntPoints, 
                                                self.Variogram, self.Seed, 
                                                self.KrType, self.Mean, 
                                                self.UseHd, self.Mask )
                    
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
