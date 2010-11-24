from PyQt4 import QtGui, QtCore
import gui_widgets.ikwidget as GWIk
import gui_widgets.siswidget as GWSis
import hpgl_run.ik_thread as IKT
import hpgl_run.sis_thread as SIST
import gui_widgets.varwidget as VW
from geo_bsd.routines import CalcMarginalProbsIndicator
from geo_bsd import write_property

class IndAlgWidget(QtGui.QWidget):
    def __init__(self, iterator = 0):
        QtGui.QWidget.__init__(self)
        self.iterator = iterator
        
        # Const
        self.MaxVariograms = 256
        self.WasVariograms = 0
        
        self.IntValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)
        
        self.resize(650, 450)
        
        self.AlgorithmTypes = ['Indicator Kriging', 'Sequential Gaussian Simulation']
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
        self.IKWidget = GWIk.ikwidget()
        self.SISWidget = GWSis.siswidget()
        self.AlgorithmWidgets = [self.IKWidget, self.SISWidget]
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
        
        # Tab 4
        self.Tab4 = QtGui.QWidget()
        self.Tab4Layout = QtGui.QGridLayout(self.Tab4)
        
        self.Tab4TabWidget = QtGui.QTabWidget(self.Tab4)
        self.Tab4Tabs = range(self.MaxVariograms)
        self.Tab4TabsNames = range(self.MaxVariograms)
        for i in xrange(self.MaxVariograms):
            self.Tab4TabsNames[i] = str(i)
            
        self.Tab4Layout.addWidget(self.Tab4TabWidget, 0, 0, 1, 1)
        self.TabWidget.addTab(self.Tab4, "Variogram")
        
        # Other Mainwindow layouths, bars, etc.
        
        self.RunGB = QtGui.QGroupBox(self)
        self.RunLayout = QtGui.QGridLayout(self.RunGB)
        
        self.RunButton = QtGui.QPushButton(self.RunGB)
        self.SaveButton = QtGui.QPushButton(self.RunGB)
        self.SaveButton.setDisabled(1)
        self.SaveButton.setToolTip(self.__tr("There is no algorithm result yet"))
        RunSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                       QtGui.QSizePolicy.Minimum)
        RunSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                       QtGui.QSizePolicy.Minimum)
        
        self.RunWidgets = [self.RunButton, self.SaveButton,
                           RunSpacerL, RunSpacerR]
        self.RunWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
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
        
        self.IndCombo = [self.SISWidget.MaskCombobox]
        
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
                
    def Push(self, Cubes, Curr_index):
        self.CurrIndex = Curr_index
        self.Cubes = Cubes
        
        self.MargProbs = self.GetMargProbs()
        self.IndCount = len(self.Cubes[self.CurrIndex][2])
        for j in xrange(len(self.IndCombo)):
            for i in xrange(len(self.Cubes)):
                self.IndCombo[j].addItem(self.Cubes[i][4])
        
        for i in xrange(self.WasVariograms):
            self.Tab4TabWidget.removeTab(0)
            del(self.Tab4Tabs[0])
        for i in xrange(self.IndCount):
            self.Tab4Tabs[i] = VW.varwidget()
            self.Tab4TabWidget.addTab(self.Tab4Tabs[i], self.Tab4TabsNames[i])
            self.Tab4Tabs[i].MargProbs.setValue(float(self.MargProbs[i]))
            self.WasVariograms = i
        
        self.show()
        
    def GetMargProbs(self):
        '''Puts marginal probs to indicator cubes\' widgets'''
        return CalcMarginalProbsIndicator(self.Cubes[self.CurrIndex][0][0],
                                          self.Cubes[self.CurrIndex][0][1],
                                          self.Cubes[self.CurrIndex][2])
    
    def CatchResult(self, Result):
        '''Catchs result of algorithm'''
        self.Result = Result
        self.RunButton.setEnabled(1)
        self.RunButton.setToolTip('')
        if self.Result != None:
            self.SaveButton.setEnabled(1)
            self.SaveButton.setToolTip('')
            self.Result_values = [self.Cubes[self.CurrIndex][1], 
                                  self.Cubes[self.CurrIndex][2]]
            self.ResultCube = [self.Result, 
                               self.Cubes[self.CurrIndex][1],
                               self.Cubes[self.CurrIndex][2],
                               self.Cubes[self.CurrIndex][3],
                               self.Cubes[self.CurrIndex][4]+'_'+str(self.iterator)]
            self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.ResultCube)
            
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
        
    def AlgorithmRun(self):
        if self.AlgorithmType.currentIndex() == 0:
            k = 0
            self.MaxIndicators = len(self.Cubes[self.CurrIndex][2])
            for i in xrange(self.MaxIndicators):
                j, errors = self.Tab4Tabs[i].VariogramCheck()
                if j == 0:
                    self.Err += 'In tab #' + str(i) +':\n' + errors
                k += j
            if k != self.MaxIndicators:
                self.ShowError(self.Err)
            else:
                self.Log += "Starting Indicator Kriging Algorithm\n"
                self.ProgressBar.show()
                    
                self.Variograms = range(self.MaxIndicators)
                self.MargProbs = range(self.MaxIndicators)
                self.VarData = range(self.MaxIndicators)
                
                self.EllipsoidRanges = self.IKWidget.GetSearchRanges()
                self.IntPoints = self.IKWidget.GetIntPoints()

                for i in xrange(self.MaxIndicators):
                    self.Variograms[i] = self.Tab4Tabs[i].GetVariogram()
                    self.MargProbs[i] = self.Tab4Tabs[i].GetMargProbs()
                    self.VarData[i] = { "cov_model" : self.Variograms[i],
                                        "max_neighbours" : self.IntPoints,
                                        "radiuses" : self.EllipsoidRanges 
                                      }

                self.NewThread = IKT.IKThread(self.Cubes[self.CurrIndex][0], 
                                                self.Cubes[self.CurrIndex][3], 
                                                self.VarData,
                                                self.MargProbs)
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
            k = 0
            self.MaxIndicators = len(self.Cubes[self.CurrIndex][2])
            for i in xrange(self.MaxIndicators):
                j, errors = self.Tab4Tabs[i].VariogramCheck()
                if j == 0:
                    self.Err += 'In variogram tab #' + str(i) +':\n' + errors
                k += j
            if k != self.MaxIndicators:
                self.ShowError(self.Err)
            else:
                self.Log += "Starting Sequantial Indicator Algorithm\n"
                self.ProgressBar.show()
                    
                self.Variograms = range(self.MaxIndicators)
                self.MargProbs = range(self.MaxIndicators)
                self.VarData = range(self.MaxIndicators)
                
                self.EllipsoidRanges = self.SISWidget.GetSearchRanges()
                self.IntPoints = self.SISWidget.GetIntPoints()
                self.Seed = self.SISWidget.GetSeed()
                self.UseCorr = self.SISWidget.GetUseCorr()
                self.Mask = self.SISWidget.GetMask(self.Cubes) # is right?

                for i in xrange(self.MaxIndicators):
                    self.Variograms[i] = self.Tab4Tabs[i].GetVariogram()
                    self.MargProbs[i] = self.Tab4Tabs[i].GetMargProbs()
                    self.VarData[i] = { "cov_model" : self.Variograms[i],
                                        "max_neighbours" : self.IntPoints,
                                        "radiuses" : self.EllipsoidRanges 
                                      }

                self.NewThread = IKT.IKThread(self.Cubes[self.CurrIndex][0], 
                                              self.Cubes[self.CurrIndex][3], 
                                              self.VarData,
                                              self.MargProbs)
                SIST.SISThread(self.Cubes[self.CurrIndex][0], 
                                   self.Cubes[self.CurrIndex][3], 
                                   self.VarData, self.MargProbs, 
                                   self.Seed, self.UseCorr, self.Mask)
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
        
    def RetranslateUI(self, MainWindow):
        # Tab 2
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))
        self.SaveButton.setText(self.__tr("Save"))
        
        self.AlgorithmTypeGB.setTitle(self.__tr("Algorithm"))
        self.AlgorithmTypeLabel.setText(self.__tr("Algorithm type"))
        
        for i in xrange(len(self.AlgorithmTypes)):
            self.AlgorithmType.setItemText(i, (self.__tr(self.AlgorithmTypes[i])))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab2), 
                                  (self.__tr("Algorithms")))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
    