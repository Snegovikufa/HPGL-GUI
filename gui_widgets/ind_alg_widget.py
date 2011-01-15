from PyQt4 import QtGui, QtCore
from geo_bsd import set_thread_num
from geo_bsd.routines import CalcMarginalProbsIndicator
import gui_widgets.ikwidget as GWIk
import gui_widgets.siswidget as GWSis
import gui_widgets.varwidget as VW
import hpgl_run.ik_thread as IKT
import hpgl_run.sis_thread as SIST

class IndAlgWidget(QtGui.QDialog):
    def __init__(self, iterator=0):
        QtGui.QWidget.__init__(self)
        self.iterator = iterator
        
        # Const
        self.MaxVariograms = 256
        self.WasVariograms = 0
        
        self.intValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)
        
        self.resize(650, 450)
        
        self.AlgorithmTypes = [self.__tr('Indicator Kriging'),
                               self.__tr('Sequential Indicator Simulation')]
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
        
        self.threadsNumLabel = QtGui.QLabel(self.AlgorithmTypeGB)
        self.threadsNum = QtGui.QSpinBox(self.AlgorithmTypeGB)
        self.threadsNum.setRange(1, 4)
        spacer = QtGui.QSpacerItem(40, 20,
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
        
        self.RetranslateUI(self)
        
        # Comboboxes
        
        self.IndCombo = [self.SISWidget.MaskCombobox]
        
        self.connect(self.AlgorithmType,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.AlgorithmTypeChanged)
        self.connect(self.RunButton, QtCore.SIGNAL("clicked()"),
                     self.AlgorithmRun)
        
        
    def UpdateUI(self, string):
        '''Outputs HPGL\'s output to log'''
        self.Log += "%s" % unicode(string)
        
    def UpdateProgress(self, value):
        '''Emits percentage of current algorithm progress'''
        self.emit(QtCore.SIGNAL('progress(PyQt_PyObject)'), value)
        
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
                
    def push(self, Cubes, Curr_index):
        self.CurrIndex = Curr_index
        self.Cubes = Cubes
        
        self.MargProbs = self.GetMargProbs()
        self.IndCount = len(self.Cubes[self.CurrIndex][2])
        
        for j in self.IndCombo:
            j.clear()
            for i in self.Cubes:
                j.addItem(i[4])
        
        del(self.Tab4Tabs)
        self.Tab4TabWidget.clear()
        self.Tab4Tabs = range(self.MaxVariograms)
        
        for i in xrange(self.IndCount):
            self.Tab4Tabs[i] = VW.varwidget()
            self.Tab4TabWidget.addTab(self.Tab4Tabs[i], self.Tab4TabsNames[i])
            self.Tab4Tabs[i].MargProbs.setValue(float('%.2f' % self.MargProbs[i]))
            self.WasVariograms = i
        
        self.show()
        
    def GetMargProbs(self):
        '''Puts marginal probs to indicator cubes\' widgets'''
        return CalcMarginalProbsIndicator(self.Cubes[self.CurrIndex][0][0],
                                          self.Cubes[self.CurrIndex][0][1],
                                          self.Cubes[self.CurrIndex][2])
    
    def CatchResult(self, Result):
        '''Catchs result of algorithm'''
        self.RunButton.setEnabled(1)
        self.RunButton.setToolTip('')
        if Result != None:
            self.ResultCube = [Result,
                               self.Cubes[self.CurrIndex][1],
                               self.Cubes[self.CurrIndex][2],
                               self.Cubes[self.CurrIndex][3],
                               self.Cubes[self.CurrIndex][4] + '_' + str(self.iterator),
                               self.Cubes[self.CurrIndex][5]]
            self.emit(QtCore.SIGNAL("finished(PyQt_PyObject)"), True)
            self.emit(QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.ResultCube)
            self.close()
        
    def AlgorithmRun(self):
        # Setting threads
        set_thread_num(int(self.threadsNum.value()))
        
        if self.AlgorithmType.currentIndex() == 0:
            k = 0
            MaxIndicators = len(self.Cubes[self.CurrIndex][2])
            for i in xrange(MaxIndicators):
                j, errors = self.Tab4Tabs[i].isVariogramValid()
                if j == 0:
                    self.Err += 'In tab #' + str(i) + ':\n' + errors
                k += j
            if k != MaxIndicators:
                self.ShowError(self.Err)
            else:
                self.hide()
                
                self.Log += "Starting Indicator Kriging Algorithm\n"
                    
                Variograms = range(MaxIndicators)
                MargProbs = range(MaxIndicators)
                VarData = range(MaxIndicators)
                
                EllipsoidRanges = self.IKWidget.getSearchRanges()
                IntPoints = self.IKWidget.getIntPoints()

                for i in xrange(MaxIndicators):
                    Variograms[i] = self.Tab4Tabs[i].GetVariogram()
                    MargProbs[i] = self.Tab4Tabs[i].GetMargProbs()
                    VarData[i] = { "cov_model" : Variograms[i],
                                    "max_neighbours" : IntPoints,
                                    "radiuses" : EllipsoidRanges 
                                 }

                self.NewThread = IKT.IKThread(self.Cubes[self.CurrIndex][0],
                                                self.Cubes[self.CurrIndex][3],
                                                VarData,
                                                MargProbs)
                info = ['Indicator Kriging', self]
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
            k = 0
            MaxIndicators = len(self.Cubes[self.CurrIndex][2])
            for i in xrange(MaxIndicators):
                j, errors = self.Tab4Tabs[i].isVariogramValid()
                if j == 0:
                    self.Err += 'In variogram tab #' + str(i) + ':\n' + errors
                k += j
            if k != MaxIndicators:
                self.ShowError(self.Err)
            else:
                self.hide()
                
                self.Log += "Starting Sequantial Indicator Algorithm\n"
                    
                Variograms = range(MaxIndicators)
                MargProbs = range(MaxIndicators)
                VarData = range(MaxIndicators)
                
                EllipsoidRanges = self.SISWidget.getSearchRanges()
                IntPoints = self.SISWidget.getIntPoints()
                Seed = self.SISWidget.GetSeed()
                UseCorr = self.SISWidget.GetUseCorr()
                Mask = self.SISWidget.GetMask(self.Cubes) # is right?

                for i in xrange(MaxIndicators):
                    Variograms[i] = self.Tab4Tabs[i].GetVariogram()
                    MargProbs[i] = self.Tab4Tabs[i].GetMargProbs()
                    VarData[i] = { "cov_model" : Variograms[i],
                                        "max_neighbours" : IntPoints,
                                        "radiuses" : EllipsoidRanges 
                                      }

                self.NewThread = IKT.IKThread(self.Cubes[self.CurrIndex][0],
                                              self.Cubes[self.CurrIndex][3],
                                              VarData,
                                              MargProbs)
                
                info = ['SIS', self]
                self.emit(QtCore.SIGNAL('algorithm(PyQt_PyObject)'), info)
                
                SIST.SISThread(self.Cubes[self.CurrIndex][0],
                                   self.Cubes[self.CurrIndex][3],
                                   VarData, MargProbs,
                                   Seed, UseCorr, Mask)
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
        self.setWindowTitle(self.__tr("HPGL GUI ") + self.__tr("Indicator Algorithms"))
        # Tab 2
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))
        
        self.AlgorithmTypeGB.setTitle(self.__tr("Algorithm"))
        self.AlgorithmTypeLabel.setText(self.__tr("Algorithm type"))
        self.threadsNumLabel.setText(self.__tr('Number of threads'))
        
        for i in xrange(len(self.AlgorithmTypes)):
            self.AlgorithmType.setItemText(i, (self.__tr(self.AlgorithmTypes[i])))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab2),
                                  (self.__tr("Algorithms")))
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
    
