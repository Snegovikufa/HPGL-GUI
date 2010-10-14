#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from geo_bsd import write_property
from geo_bsd import SugarboxGrid
from geo_bsd import load_cont_property
from geo_bsd import load_ind_property
from geo_bsd import CovarianceModel
import re
import hpgl_run.ok_thread as OKT
import hpgl_run.sk_thread as SKT
import hpgl_run.lvm_thread as LVMT
import hpgl_run.sgs_thread as SGST
import gui_widgets.skwidget as GWSk
import gui_widgets.okwidget as GWOk
import gui_widgets.sgswidget as GWSgs
import gui_widgets.lvmwidget as GWLvm

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setObjectName("MainWindow")
        #self.setFixedWidth(700)
        #self.setFixedHeight(520)
        self.resize(700, 520)
        self.CentralWidget = QtGui.QWidget()
        self.CentralLayout = QtGui.QGridLayout(self.CentralWidget)
        self.TabWidget = QtGui.QTabWidget(self.CentralWidget)
        
        # Constants and variables
        
        self.IntValidator = QtGui.QIntValidator(self)
        self.DoubleValidator = QtGui.QDoubleValidator(self)
        self.Cubes = []
        self.CubesInd = []
        self.CubesCont = []
        self.AlgorithmTypes = ['Simple Kriging', 'Ordinary Kriging', 
                                'Indicator Kriging', 'LVM Kriging', 
                                'Sequantial Indicator Simulation', 
                                'Sequantial Gaussian Simulation']
        
        # TAB 1
        self.Tab1 = QtGui.QWidget()
        self.Tab1Layout = QtGui.QGridLayout(self.Tab1)
        
        self.GridSizeGB = QtGui.QGroupBox(self.Tab1)
        self.GridLayout = QtGui.QGridLayout(self.GridSizeGB)
        
        self.GridSizeXLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeX = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeX.setValidator(self.IntValidator)
        self.GridSizeYLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeY = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeY.setValidator(self.IntValidator)
        self.GridSizeZLabel = QtGui.QLabel(self.GridSizeGB)
        self.GridSizeZ = QtGui.QLineEdit(self.GridSizeGB)
        self.GridSizeZ.setValidator(self.IntValidator)
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

        self.ManageCubesGB = QtGui.QGroupBox(self.Tab1)
        self.ManageCubesLayout = QtGui.QGridLayout(self.ManageCubesGB)
        
        self.LoadedCubesTab1 = QtGui.QComboBox(self.ManageCubesGB)
        self.CubeDeleteButton = QtGui.QPushButton(self.ManageCubesGB)
        self.CubeDeleteButton.setDisabled(1)
        self.CubeDeleteButton.setSizePolicy(QtGui.QSizePolicy.Maximum, 
                                            QtGui.QSizePolicy.Fixed)
        ManageCubesSpacerL = QtGui.QSpacerItem(10, 20, 
                                               QtGui.QSizePolicy.Maximum, 
                                               QtGui.QSizePolicy.Maximum)
        ManageCubesSpacerR = QtGui.QSpacerItem(10, 20, 
                                               QtGui.QSizePolicy.Maximum, 
                                               QtGui.QSizePolicy.Minimum)
        
        self.ManageCubesWidgets = [self.LoadedCubesTab1, self.CubeDeleteButton,
                                   ManageCubesSpacerL, ManageCubesSpacerR]
        self.ManageCubesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                         [0, 0, 1, 1], [0, 3, 1, 1]]
        
        
        self.IndValuesGB = QtGui.QGroupBox(self.Tab1)
        self.IndValuesLayout = QtGui.QGridLayout(self.IndValuesGB)
        
        self.IndValues = QtGui.QSpinBox(self.IndValuesGB)
        self.IndValues.setEnabled(False)
        self.IndValues.setMinimum(2)
        self.IndValues.setMaximum(256)
        self.IndValuesCheckbox = QtGui.QCheckBox(self.IndValuesGB)
        self.IndValuesCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        IndValuesSpacerL = QtGui.QSpacerItem(40, 20, 
                                             QtGui.QSizePolicy.Expanding, 
                                             QtGui.QSizePolicy.Minimum)
        IndValuesSpacerR = QtGui.QSpacerItem(40, 20, 
                                             QtGui.QSizePolicy.Expanding, 
                                             QtGui.QSizePolicy.Minimum)
        
        self.IndValuesWidgets = [self.IndValues, self.IndValuesCheckbox,
                                 IndValuesSpacerL, IndValuesSpacerR]
        self.IndValuesWidgetsPlaces = [[1, 2, 1, 1], [1, 1, 1, 1], 
                                       [1, 3, 1, 1], [1, 0, 1, 1]]
        
        
        self.UndefValueGB = QtGui.QGroupBox(self.Tab1)
        self.UndefValueLayout = QtGui.QGridLayout(self.UndefValueGB)
        self.UndefValueLabel = QtGui.QLabel(self.UndefValueGB)
        self.UndefValue = QtGui.QLineEdit(self.UndefValueGB)
        self.UndefValue.setValidator(self.IntValidator)
        UndefValueSpacerL = QtGui.QSpacerItem(40, 20, 
                                              QtGui.QSizePolicy.Expanding, 
                                              QtGui.QSizePolicy.Minimum)
        UndefValueSpacerR = QtGui.QSpacerItem(40, 20, 
                                              QtGui.QSizePolicy.Expanding, 
                                              QtGui.QSizePolicy.Minimum)
        
        self.UndefValueWidgets = [self.UndefValueLabel, self.UndefValue,
                                  UndefValueSpacerL, UndefValueSpacerR]
        self.UndefValueWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1], 
                                        [0, 0, 1, 1], [0, 3, 1, 1]]
        
        self.LoadCubeGB = QtGui.QGroupBox(self.Tab1)
        self.LoadCubeLayout = QtGui.QGridLayout(self.LoadCubeGB)
        
        self.LoadCubeButton = QtGui.QPushButton(self.LoadCubeGB)
        self.LoadCubeButton.setDisabled(1)
        LoadCubeSpacerL = QtGui.QSpacerItem(241, 20, 
                                            QtGui.QSizePolicy.Expanding, 
                                            QtGui.QSizePolicy.Minimum)
        LoadCubeSpacerR = QtGui.QSpacerItem(241, 20, 
                                            QtGui.QSizePolicy.Expanding, 
                                            QtGui.QSizePolicy.Minimum)
        
        self.LoadCubeWidgets = [self.LoadCubeButton, LoadCubeSpacerL, 
                                LoadCubeSpacerR]
        self.LoadCubeWidgetsPlaces = [[0, 1, 1, 1], [0, 0, 1, 1], 
                                      [0, 2, 1, 1]]
        
        self.Tab1Spacer = QtGui.QSpacerItem(20, 40, 
                                            QtGui.QSizePolicy.Minimum, 
                                            QtGui.QSizePolicy.Expanding)
        
        self.Tab1Widgets = [self.GridSizeGB, self.ManageCubesGB, 
                            self.IndValuesGB, self.UndefValueGB,
                            self.LoadCubeGB, self.Tab1Spacer]
        self.Tab1WidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1], 
                                  [1, 0, 1, 1], [1, 1, 1, 1],
                                  [3, 0, 1, 2], [4, 0, 1, 1]]
        
        self.PlaceWidgetsAtPlaces(self.GridLayout, self.GridSizeWidgets, 
                                  self.GridSizeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.ManageCubesLayout, 
                                  self.ManageCubesWidgets, 
                                  self.ManageCubesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.IndValuesLayout, self.IndValuesWidgets, 
                                  self.IndValuesWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.UndefValueLayout, 
                                  self.UndefValueWidgets, 
                                  self.UndefValueWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.LoadCubeLayout, self.LoadCubeWidgets, 
                                  self.LoadCubeWidgetsPlaces)
        self.PlaceWidgetsAtPlaces(self.Tab1Layout, self.Tab1Widgets, 
                                  self.Tab1WidgetsPlaces)
        
        
        self.TabWidget.addTab(self.Tab1, "")
        
        # TAB 2
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
        
        self.LoadedCubesGB = QtGui.QGroupBox(self.Tab2)
        self.LoadedCubesLayout = QtGui.QGridLayout(self.LoadedCubesGB)
        
        self.LoadedCubesLabel = QtGui.QLabel(self.LoadedCubesGB)
        self.LoadedCubes = QtGui.QComboBox(self.LoadedCubesGB)
        self.LoadedCubes.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                                       QtGui.QSizePolicy.Fixed)
        LoadedCubesSpacerL = QtGui.QSpacerItem(10, 20, 
                                               QtGui.QSizePolicy.Maximum, 
                                               QtGui.QSizePolicy.Maximum)
        LoadedCubesSpacerR = QtGui.QSpacerItem(10, 20, 
                                               QtGui.QSizePolicy.Maximum, 
                                               QtGui.QSizePolicy.Minimum)
        
        self.LoadedCubesWidgets = [self.LoadedCubesLabel, self.LoadedCubes,
                                   LoadedCubesSpacerL, LoadedCubesSpacerR]
        self.LoadedCubesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                         [0, 0, 1, 1], [0, 3, 1, 1]]
        
        self.AlgorithmWidget = QtGui.QStackedWidget()
        self.SKWidget = GWSk.skwidget()
        self.OKWidget = GWOk.okwidget()
        self.IKWidget = QtGui.QWidget()
        self.LVMWidget = GWLvm.lvmwidget()
        self.SISWidget = QtGui.QWidget()
        self.SGSWidget = GWSgs.sgswidget()
        self.AlgorithmWidgets = [self.SKWidget, self.OKWidget, 
                                 self.IKWidget, self.LVMWidget, 
                                 self.SISWidget, self.SGSWidget]
        for i in xrange(0, len(self.AlgorithmTypes)):
            self.AlgorithmWidget.addWidget(self.AlgorithmWidgets[i])
        
        
                
        self.Tab2Spacer = QtGui.QSpacerItem(20, 40, 
                                            QtGui.QSizePolicy.Minimum, 
                                            QtGui.QSizePolicy.Expanding)
        self.Tab2Widgets = [self.AlgorithmTypeGB, self.LoadedCubesGB,
                            self.AlgorithmWidget, self.Tab2Spacer]
        self.Tab2WidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1],
                                  [1, 0, 1, 2], [3, 1, 1, 1]]
        
        self.PlaceWidgetsAtPlaces(self.LoadedCubesLayout, 
                                  self.LoadedCubesWidgets, 
                                  self.LoadedCubesWidgetsPlaces)
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
        
        Tab3Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, 
                                       QtGui.QSizePolicy.Expanding)
        
        self.Tab3Widgets = [self.VariogramTypeGB, self.EllipsoidRangesGB,
                            self.EllipsoidAnglesGB, self.NuggetEffectGB,
                            Tab3Spacer]
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
        
        self.RunGB = QtGui.QGroupBox(self.CentralWidget)
        self.RunLayout = QtGui.QGridLayout(self.RunGB)
        
        self.RunButton = QtGui.QPushButton(self.RunGB)
        self.RunButton.setDisabled(1)
        self.SaveButton = QtGui.QPushButton(self.RunGB)
        self.SaveButton.setDisabled(1)
        RunSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                       QtGui.QSizePolicy.Minimum)
        RunSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                       QtGui.QSizePolicy.Minimum)
        RunSpacerD = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, 
                                       QtGui.QSizePolicy.Expanding)
        
        self.RunWidgets = [self.RunButton, self.SaveButton,
                           RunSpacerL, RunSpacerR, RunSpacerD]
        self.RunWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                 [0, 0, 1, 1], [0, 3, 1, 1], [2, 0, 1, 2]]
        self.PlaceWidgetsAtPlaces(self.RunLayout, 
                                  self.RunWidgets, 
                                  self.RunWidgetsPlaces)
        self.CentralLayout.addWidget(self.RunGB, 2, 0, 1, 2)      
        
        self.CentralLayout.addWidget(self.TabWidget, 0, 0, 1, 1)
        self.ProgressBar = QtGui.QProgressBar(self.CentralWidget)
        self.ProgressBar.setProperty("value", 24)
        self.ProgressBar.setValue(0)
        self.ProgressBar.hide()
        self.CentralLayout.addWidget(self.ProgressBar, 1, 0, 1, 1)
        
        self.Log = ''
        self.Err = ''
        #self.ShowError('Error message')
        
        self.setCentralWidget(self.CentralWidget)
        
        
        self.RetranslateUI(self)
        self.TabWidget.setCurrentIndex(0)
        
        #
        self.IndCombo = [self.SGSWidget.MaskCombobox]
        self.ContCombo = [self.LVMWidget.MeanCombobox, 
                          self.SGSWidget.MeanCombobox]
        # Signals and slots
        self.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"), 
                     self.IndValues.setEnabled)
        self.connect(self.LoadCubeButton, QtCore.SIGNAL("clicked()"), 
                     self.CubeLoad)
        self.connect(self.AlgorithmType, 
                     QtCore.SIGNAL("currentIndexChanged(int)"), 
                     self.AlgorithmTypeChanged)
        self.connect(self.RunButton, QtCore.SIGNAL("clicked()"), 
                     self.AlgorithmRun)
        self.connect(self.GridSizeX, QtCore.SIGNAL("textChanged(QString)"), 
                     self.CubeLoadAccess)
        self.connect(self.GridSizeY, QtCore.SIGNAL("textChanged(QString)"), 
                     self.CubeLoadAccess)
        self.connect(self.GridSizeZ, QtCore.SIGNAL("textChanged(QString)"), 
                     self.CubeLoadAccess)
        self.connect(self.CubeDeleteButton, QtCore.SIGNAL("clicked()"), 
                     self.DeleteCube)
        self.connect(self.SaveButton, QtCore.SIGNAL("clicked()"), 
                     self.ResultSave)
        
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.Tab1Spacer):
                layout.addItem(widgets[i], places[i][0], places[i][1], 
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1], 
                                 places[i][2], places[i][3])

    def DeleteCube(self):
        '''Deletes cube from memory and UI'''
        self.current_index = self.LoadedCubesTab1.currentIndex()
        if self.Cubes[self.current_index][2] == None:
            self.DelComboCont(self.current_index)
        else:
            self.DelComboInd(self.current_index)
        del (self.Cubes[self.current_index])
        self.LoadedCubesTab1.removeItem(self.current_index)
        self.LoadedCubes.removeItem(self.current_index)
        
        self.Log +='Cube deleted\n'
        if self.LoadedCubesTab1.count() == 0:
            self.RunButton.setDisabled(1)
            self.CubeDeleteButton.setDisabled(1)

    def UpdateUI(self, string):
        '''Outputs HPGL\'s output to log'''
        self.Log += "%s" % unicode(string)
        
    def UpdateProgress(self, value):
        '''Outputs percentage of current algorithm progress'''
        self.ProgressBar.setValue(int(value))
        
    def CubeLoadAccess(self):
        '''Controls the grid size and allow to load cube'''
        if int(self.GridSizeX.text()) > 0 and int(self.GridSizeY.text()) > 0 and int(self.GridSizeZ.text()) > 0:
            self.LoadCubeButton.setEnabled(1)
            
    def ShowError(self, string):
        self.ErrorWindow = QtGui.QMessageBox()
        self.ErrorWindow.warning(None, "Error", string)
            
    def UpdateComboCont(self, string):
        for i in xrange(len(self.ContCombo)):
            self.ContCombo[i].addItem(string)
            self.ContCombo[i].setEnabled(1)
    
    def UpdateComboInd(self, string):
        for i in xrange(len(self.IndCombo)):
            self.IndCombo[i].AddItem(string)
            
    def DelComboInd(self, num):
        self.index = self.IndCombo.index(num)
        self.IndCombo.remove(self.index)
        if self.IndCombo[0].count() == 0:
            for i in xrange(len(self.IndCombo)):
                self.IndCombo[i].SetDisabled(1)
        
    def DelComboCont(self, num):
        #print num
        self.index = self.ContCombo.index(num)
        self.ContCombo.remove(self.index)
        if self.ContCombo[0].count() == 0:
            for i in xrange(len(self.ContCombo)):
                self.ContCombo[i].SetDisabled(1)
        
    def AlgorithmTypeChanged(self, value):
        self.AlgorithmWidget.setCurrentIndex(value)
            
    def CatchResult(self, Result):
        '''Catchs result of algorithm'''
        self.Result = Result
        self.RunButton.setEnabled(1)
        if self.Result != None:
            self.SaveButton.setEnabled(1)
            self.Result_values = [self.Cubes[self.CurrCube][1], 
                                  self.Cubes[self.CurrCube][2]]
        
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
            
    def CheckCubeLoad(self):
        if self.GridSizeX.text() == "":
            self.Err += '"Grid size x" is empty\n'
        if self.GridSizeY.text() == "":
            self.Err += '"Grid size y" is empty\n'
        if self.GridSizeZ.text() == "":
            self.Err += '"Grid size z" is empty\n'
        if self.UndefValue.text() == "":
            self.Err += '"Undefined value" is empty\n'
        if self.Err == '':
            return 1
        else:
            self.ShowError(self.Err)
            self.Err = ''
            return 0
            
    def CubeLoad(self):
        '''Loads cube from file'''
        if self.CheckCubeLoad() == 1:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
            if filename:
                self.loaded_cube_fname = re.search('(.*\/)([\w.]*)', filename) 
                self.loaded_cube_fname = self.loaded_cube_fname.group(self.loaded_cube_fname.lastindex)
                self.Log += "Selected cube: " + self.loaded_cube_fname +'\n'
                
                self.GridObject = SugarboxGrid( int(self.GridSizeX.text()), 
                                                int(self.GridSizeY.text()), 
                                                int(self.GridSizeZ.text()) )
                self.GridSize = ( int(self.GridSizeX.text()), 
                                  int(self.GridSizeY.text()), 
                                  int(self.GridSizeZ.text()) )
                self.undefined_value = int(self.UndefValue.text())
                
            
                if self.IndValuesCheckbox.isChecked():
                    self.Log += 'Loaded cube with indicator values\n'
                
                    self.indicator_value = range(int(self.IndValues.text()))
                    # Starting load indicator cube with HPGL
                    self.Prop = load_ind_property(str(filename), 
                                                  self.undefined_value, 
                                                  self.indicator_value, 
                                                  self.GridSize)
                    if self.Prop != None:
                        self.RunButton.setEnabled(1)
                        self.LoadedCubesTab1.addItem(self.loaded_cube_fname)
                        self.UpdateComboInd(self.loaded_cube_fname)
                        self.LoadedCubes.addItem(self.loaded_cube_fname)
                        self.Cubes.append([self.Prop, self.undefined_value, 
                                           self.indicator_value,
                                           self.GridObject])
                        self.CubesInd.append(len(self.Cubes)-1)
                        del(self.Prop)
                        self.CubeDeleteButton.setEnabled(1)
                    
                elif self.IndValuesCheckbox.isChecked() == 0:
                    self.Log += 'Loaded cube\n'
                
                    # Starting load cube with HPGL
                    self.Prop = load_cont_property( str(filename), 
                                                    self.undefined_value, 
                                                    self.GridSize )
                    if self.Prop != None:
                        self.RunButton.setEnabled(1)
                        self.LoadedCubesTab1.addItem(self.loaded_cube_fname)
                        self.UpdateComboCont(self.loaded_cube_fname)
                        self.LoadedCubes.addItem(self.loaded_cube_fname)
                        self.Cubes.append([self.Prop, self.undefined_value, 
                                           None,
                                           self.GridObject])
                        self.CubesCont.append(len(self.Cubes)-1)
                        del(self.Prop)
                        self.CubeDeleteButton.setEnabled(1)
    
    def VariogramCheck(self):
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
        if self.Err == '':
            return 1
        else:
            self.ShowError(self.Err)
            self.Err = ''
            return 0
    
    def GetVariogram(self):
        # Variogram
        self.VariogramRanges = ( int(self.EllipsoidRanges0.text()), 
                                 int(self.EllipsoidRanges90.text()), 
                                 int(self.EllipsoidRangesV.text()) )
        self.VariogramAngles = ( int(self.EllipsoidAnglesX.text()), 
                                 int(self.EllipsoidAnglesY.text()), 
                                 int(self.EllipsoidAnglesZ.text()) )
        self.Variogram = CovarianceModel( int(self.VariogramType.currentIndex()),
                                          self.VariogramRanges, 
                                          self.VariogramAngles, 
                                          float(self.SillValue.text()), 
                                          int(self.NuggetValue.text()) )
        
    def AlgorithmRun(self):
        '''Run algorithm'''
        if self.VariogramCheck() == 1:
            if self.AlgorithmType.currentIndex() == 0:
                if self.SKWidget.ValuesCheck(self.LogTextbox) == 1:
                    self.Log += "Starting Simple Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # Simple Kriging                                  
                    self.EllipsoidRanges = self.SKWidget.GetSearchRanges()
                    self.CurrCube = self.LoadedCubes.currentIndex()
                    self.IntPoints = self.SKWidget.GetIntPoints()
                    self.Mean = self.SKWidget.GetMean()
                    self.NewThread = SKT.SKThread( self.Cubes[self.CurrCube][0], 
                                               self.Cubes[self.CurrCube][3], 
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
                    
            elif self.AlgorithmType.currentIndex() == 1:
                if self.OKWidget.ValuesCheck(self.LogTextbox) == 1:
                    self.Log += "Starting Ordinary Kriging Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # Ordinary Kriging                                  
                    self.EllipsoidRanges = self.OKWidget.GetSearchRanges()
                    self.CurrCube = self.LoadedCubes.currentIndex()
                    self.IntPoints = self.OKWidget.GetIntPoints()
                    self.NewThread = OKT.OKThread( self.Cubes[self.CurrCube][0], 
                                               self.Cubes[self.CurrCube][3], 
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
                    
            elif self.AlgorithmType.currentIndex() == 3:
                if self.LVMWidget.ValuesCheck(self.LogTextbox) == 1:
                    self.Log += "Starting Locale Varying Mean Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()
                    # LVM
                    self.EllipsoidRanges = self.LVMWidget.GetSearchRanges()
                    self.CurrCube = self.LoadedCubes.currentIndex()
                    self.IntPoints = self.LVMWidget.GetIntPoints()
                    self.Mean = self.LVMWidget.GetMean(self.Cubes, self.CubesCont)
                    
                    self.NewThread = LVMT.LVMThread( self.Cubes[self.CurrCube][0], 
                                               self.Cubes[self.CurrCube][3],
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
                    
                
            elif self.AlgorithmType.currentIndex() == 5:
                if self.SGSWidget.ValuesCheck(self.LogTextbox) == 1:
                    self.Log += "Starting Sequantial Gaussian Algorithm\n"
                    self.ProgressBar.show()
                    
                    self.GetVariogram()

                    # Sequantial Gaussian Simulation
                    self.EllipsoidRanges = self.SGSWidget.GetSearchRanges()
                    self.CurrCube = self.LoadedCubes.currentIndex()
                    self.IntPoints = self.SGSWidget.GetIntPoints()
                    self.Seed = self.SGSWidget.GetSeed()
                    self.UseHd = self.SGSWidget.GetUseHd()
                    self.KrType = self.SGSWidget.GetKrType()
                    self.Mean = self.SGSWidget.GetMean(self.Cubes, self.CubesCont)
                    self.Mask = self.SGSWidget.GetMask(self.Cubes, self.CubesInd)
                    
                    self.NewThread = SGST.SGSThread( self.Cubes[self.CurrCube][0], 
                                                self.Cubes[self.CurrCube][3],
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
        
    def RetranslateUI(self, MainWindow):
        '''Adds text to widgets'''
        self.setWindowTitle(self.__tr("HPGL GUI"))
        
        # Tab 1
        self.GridSizeGB.setTitle(self.__tr("Grid Size"))
        self.GridSizeXLabel.setText(self.__tr("x"))
        self.GridSizeX.setText(self.__tr("0"))
        self.GridSizeYLabel.setText(self.__tr("y"))
        self.GridSizeY.setText(self.__tr("0"))
        self.GridSizeZLabel.setText(self.__tr("z"))
        self.GridSizeZ.setText(self.__tr("0"))
        
        self.ManageCubesGB.setTitle(self.__tr("Manage Cubes"))
        self.CubeDeleteButton.setText(self.__tr("Delete"))
        
        self.IndValuesGB.setTitle(self.__tr("Indicator value"))
        self.IndValuesCheckbox.setText(self.__tr("Indicator values"))
        self.UndefValueGB.setTitle(self.__tr("Undefined value"))
        self.UndefValueLabel.setText(self.__tr("Undefined value"))
        self.UndefValue.setText(self.__tr("-99"))
        
        self.LoadCubeButton.setText(self.__tr("Load cube"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab1), 
                                  (self.__tr("Load cube")))
        
        # Tab 2
        self.LoadedCubesGB.setTitle(self.__tr("Cubes"))
        self.LoadedCubesLabel.setText(self.__tr("Select cube:"))
        
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))
        self.SaveButton.setText(self.__tr("Save"))
        
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
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab3), 
                                  (self.__tr("Variogram")))
        
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())

