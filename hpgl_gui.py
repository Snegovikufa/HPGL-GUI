#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from geo_bsd import *
from geo_bsd.cvariogram import *
import re
from types import ClassType


class algorithm_thread(QtCore.QThread):
    def __init__(self, Prop, GridObject, EllipsoidRanges, IntPoints, Variogram, MeanValue, UndefValue):
        QtCore.QThread.__init__(self)
        
        self.Prop = Prop
        self.GridObject = GridObject
        self.EllipsoidRanges = EllipsoidRanges
        self.IntPoints = IntPoints
        self.Variogram = Variogram
        self.MeanValue = MeanValue
        self.und_value = UndefValue
        
    def run(self):
        set_output_handler(self.output_log, None)
        set_progress_handler(self.progress_show, None)
        self.Result = simple_kriging( self.Prop, self.GridObject, self.EllipsoidRanges, 
                                      self.IntPoints, self.Variogram, self.MeanValue )
        self.emit(QtCore.SIGNAL("Result(PyQt_PyObject)"), self.Result)
        
    def output_log(self, string, _):
        self.StrForLog = string
        self.emit(QtCore.SIGNAL("msg(QString)"), QtCore.QString(self.StrForLog))
        return 0
        
    def progress_show(self, stage, Percent, _):
        self.Percent = Percent
        self.stage = stage
        if self.Percent == 0:
            print self.stage,
        elif self.Percent == -1:
            print ""
        else:
            self.OutStr = int(self.Percent)
            self.OutStr = str(self.OutStr)
            self.emit(QtCore.SIGNAL("progress(QString)"), QtCore.QString(self.OutStr))
        return 0


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setObjectName("MainWindow")
        self.setFixedWidth(700)
        self.setFixedHeight(520)
        self.CentralWidget = QtGui.QWidget()
        self.CentralLayout = QtGui.QGridLayout(self.CentralWidget)
        self.TabWidget = QtGui.QTabWidget(self.CentralWidget)
        
        self.CubeWasChosen = 0
        self.AlgorithmCount = 6
        self.IntValidator = QtGui.QIntValidator(self)
        self.double_validator = QtGui.QDoubleValidator(self)
        self.Cubes = []
        
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
        self.GridSizeSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.GridSizeSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.GridSizeWidgets = [self.GridSizeXLabel, self.GridSizeX, 
                                self.GridSizeYLabel, self.GridSizeY, 
                                self.GridSizeZLabel, self.GridSizeZ,
                                self.GridSizeSpacerL, self.GridSizeSpacerR]
        self.GridSizeWidgetsPlaces = [[0,1,1,1], [0,2,1,1], 
                                      [1,1,1,1], [1,2,1,1], 
                                      [2,1,1,1], [2,2,1,1],
                                      [0,0,1,1], [0,3,1,1]]      

        self.ManageCubesGB = QtGui.QGroupBox(self.Tab1)
        self.ManageCubesLayout = QtGui.QGridLayout(self.ManageCubesGB)
        
        self.LoadedCubesTab1 = QtGui.QComboBox(self.ManageCubesGB)
        self.CubeDeleteButton = QtGui.QPushButton(self.ManageCubesGB)
        self.CubeDeleteButton.setDisabled(1)
        ManageCubesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        ManageCubesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.ManageCubesWidgets = [self.LoadedCubesTab1, self.CubeDeleteButton,
                                   ManageCubesSpacerL, ManageCubesSpacerR]
        self.ManageCubesWidgetsPlaces = [[0,1,1,1], [0,2,1,1], [0,0,1,1], [0,3,1,1]]
        
        
        self.IndValuesGB = QtGui.QGroupBox(self.Tab1)
        self.IndValuesLayout = QtGui.QGridLayout(self.IndValuesGB)
        
        self.IndValues = QtGui.QSpinBox(self.IndValuesGB)
        self.IndValues.setEnabled(False)
        self.IndValues.setMinimum(2)
        self.IndValues.setMaximum(256)
        self.IndValuesCheckbox = QtGui.QCheckBox(self.IndValuesGB)
        self.IndValuesCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        IndValuesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        IndValuesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.IndValuesWidgets = [self.IndValues, self.IndValuesCheckbox,
                                 IndValuesSpacerL, IndValuesSpacerR]
        self.IndValuesWidgetsPlaces = [[1,2,1,1], [1,1,1,1], [1,3,1,1], [1,0,1,1]]
        
        
        self.UndefValueGB = QtGui.QGroupBox(self.Tab1)
        self.UndefValueLayout = QtGui.QGridLayout(self.UndefValueGB)
        self.UndefValueLabel = QtGui.QLabel(self.UndefValueGB)
        self.UndefValue = QtGui.QLineEdit(self.UndefValueGB)
        self.UndefValue.setValidator(self.IntValidator)
        UndefValueSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        UndefValueSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.UndefValueWidgets = [self.UndefValueLabel, self.UndefValue,
                                  UndefValueSpacerL, UndefValueSpacerR]
        self.UndefValueWidgetsPlaces = [[0,1,1,1], [0,2,1,1], [0,0,1,1], [0,3,1,1]]
        
        self.LoadCubeGB = QtGui.QGroupBox(self.Tab1)
        self.LoadCubeLayout = QtGui.QGridLayout(self.LoadCubeGB)
        
        self.LoadCubeButton = QtGui.QPushButton(self.LoadCubeGB)
        self.LoadCubeButton.setDisabled(1)
        LoadCubeSpacerL = QtGui.QSpacerItem(241, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        LoadCubeSpacerR = QtGui.QSpacerItem(241, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.LoadCubeWidgets = [self.LoadCubeButton, LoadCubeSpacerL, LoadCubeSpacerR]
        self.LoadCubeWidgetsPlaces = [[0,1,1,1], [0,0,1,1],[0,2,1,1]]
        
        Tab1Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        self.Tab1Widgets = [self.GridSizeGB, self.ManageCubesGB, 
                            self.IndValuesGB, self.UndefValueGB,
                            self.LoadCubeGB, Tab1Spacer]
        self.Tab1WidgetsPlaces = [[0,0,1,1], [0,1,1,1], 
                                  [1,0,1,1], [1,1,1,1],
                                  [3,0,1,2], [4,0,1,1]]
        
        self.place_widgets_at_places(self.GridLayout, self.GridSizeWidgets, self.GridSizeWidgetsPlaces)
        self.place_widgets_at_places(self.ManageCubesLayout, self.ManageCubesWidgets, self.ManageCubesWidgetsPlaces)
        self.place_widgets_at_places(self.IndValuesLayout, self.IndValuesWidgets, self.IndValuesWidgetsPlaces)
        self.place_widgets_at_places(self.UndefValueLayout, self.UndefValueWidgets, self.UndefValueWidgetsPlaces)
        self.place_widgets_at_places(self.LoadCubeLayout, self.LoadCubeWidgets, self.LoadCubeWidgetsPlaces)
        self.place_widgets_at_places(self.Tab1Layout, self.Tab1Widgets, self.Tab1WidgetsPlaces)
        
        
        self.TabWidget.addTab(self.Tab1, "")
        
        # TAB 2
        self.Tab2 = QtGui.QWidget()
        self.Tab2Layout = QtGui.QGridLayout(self.Tab2)
        
        self.VariogramTypeGB = QtGui.QGroupBox(self.Tab2)
        self.VariogramTypeLayout = QtGui.QGridLayout(self.VariogramTypeGB)
               
        self.VariogramType_label = QtGui.QLabel(self.VariogramTypeGB)
        self.VariogramType = QtGui.QComboBox(self.VariogramTypeGB)
        self.VariogramType.addItem("")
        self.VariogramType.addItem("")
        self.VariogramType.addItem("")
        self.VariogramType.setValidator(self.IntValidator)
        VariogramTypeSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum) 
        VariogramTypeSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
              
        self.VariogramTypeWidgets = [self.VariogramType_label, self.VariogramType,
                                     VariogramTypeSpacerL, VariogramTypeSpacerR]
        self.VariogramTypeWidgetsPlaces = [[0,1,1,1], [0,2,1,1],[0,0,1,1],[0,3,1,1]]
        
        self.EllipsoidRangesGB = QtGui.QGroupBox(self.Tab2)
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
        EllipsoidRangesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        EllipsoidRangesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.EllipsoidRangesWidgets = [self.EllipsoidRanges0Label, self.EllipsoidRanges0,
                                       self.EllipsoidRanges90Label, self.EllipsoidRanges90,
                                       self.EllipsoidRangesVLabel, self.EllipsoidRangesV,
                                       EllipsoidRangesSpacerL, EllipsoidRangesSpacerR]
        self.EllipsoidRangesWidgetsPlaces = [[0,1,1,1], [0,2,1,1], 
                                             [1,1,1,1], [1,2,1,1],
                                             [2,1,1,1], [2,2,1,1],
                                             [1,0,1,1], [1,3,1,1]]
               
        self.EllipsoidAnglesGB = QtGui.QGroupBox(self.Tab2)
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
        
        EllipsoidAnglesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        EllipsoidAnglesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)      
        
        self.EllipsoidAnglesWidgets = [self.EllipsoidAnglesXLabel, self.EllipsoidAnglesX,
                                       self.EllipsoidAnglesYLabel, self.EllipsoidAnglesY,
                                       self.EllipsoidAnglesZLabel, self.EllipsoidAnglesZ,
                                       EllipsoidAnglesSpacerL, EllipsoidAnglesSpacerR]
        self.EllipsoidAnglesWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                             [1,1,1,1], [1,2,1,1],
                                             [2,1,2,1], [2,2,1,1],
                                             [1,0,1,1], [1,3,1,1]]
                
        self.NuggetEffectGB = QtGui.QGroupBox(self.Tab2)
        self.NuggetEffectLayout = QtGui.QGridLayout(self.NuggetEffectGB)
        
        self.SillValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.SillValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.SillValue.setValidator(self.IntValidator)
        self.NuggetValueLabel = QtGui.QLabel(self.NuggetEffectGB)
        self.NuggetValue = QtGui.QLineEdit(self.NuggetEffectGB)
        self.NuggetValue.setValidator(self.IntValidator)
        NuggetEffectSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        NuggetEffectSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.NuggetEffectWidgets = [self.SillValueLabel, self.SillValue,
                                    self.NuggetValueLabel, self.NuggetValue,
                                    NuggetEffectSpacerL, NuggetEffectSpacerR]
        self.NuggetEffectWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                          [1,1,1,1], [1,2,1,1],
                                          [0,0,1,1], [0,3,1,1]]
        
        Tab2Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        self.Tab2Widgets = [self.VariogramTypeGB, self.EllipsoidRangesGB,
                            self.EllipsoidAnglesGB, self.NuggetEffectGB,
                            Tab2Spacer]
        self.Tab2WidgetsPlaces = [[0,0,1,1], [0,1,1,1],
                                  [1,0,1,1], [1,1,1,1],
                                  [2,1,1,1]]
        
        self.place_widgets_at_places(self.VariogramTypeLayout, self.VariogramTypeWidgets, self.VariogramTypeWidgetsPlaces)
        self.place_widgets_at_places(self.EllipsoidRangesLayout, self.EllipsoidRangesWidgets, self.EllipsoidRangesWidgetsPlaces)
        self.place_widgets_at_places(self.EllipsoidAnglesLayout, self.EllipsoidAnglesWidgets, self.EllipsoidAnglesWidgetsPlaces)
        self.place_widgets_at_places(self.NuggetEffectLayout, self.NuggetEffectWidgets, self.NuggetEffectWidgetsPlaces)
        self.place_widgets_at_places(self.Tab2Layout, self.Tab2Widgets, self.Tab2WidgetsPlaces)
        
        self.TabWidget.addTab(self.Tab2, "")
        
        # TAB 3
        self.Tab3 = QtGui.QWidget()
        self.Tab3Layout = QtGui.QGridLayout(self.Tab3)
        
        self.LoadedCubesGB = QtGui.QGroupBox(self.Tab3)
        self.LoadedCubesLayout = QtGui.QGridLayout(self.LoadedCubesGB)
        
        self.LoadedCubesLabel = QtGui.QLabel(self.LoadedCubesGB)
        self.LoadedCubes = QtGui.QComboBox(self.LoadedCubesGB)
        LoadedCubesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        LoadedCubesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.LoadedCubesWidgets = [self.LoadedCubesLabel, self.LoadedCubes,
                                   LoadedCubesSpacerL, LoadedCubesSpacerR]
        self.LoadedCubesWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                         [0,0,1,1], [0,3,1,1]]       
        
        self.SearchRangesGB = QtGui.QGroupBox(self.Tab3)
        self.SearchRangesLayout = QtGui.QGridLayout(self.SearchRangesGB)
        
        self.SearchRanges0Label = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRanges0 = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRanges0.setValidator(self.IntValidator)
        
        self.SearchRanges90Label = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRanges90 = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRanges90.setValidator(self.IntValidator)
        self.SearchRangesVLabel = QtGui.QLabel(self.SearchRangesGB)
        self.SearchRangesV = QtGui.QLineEdit(self.SearchRangesGB)
        self.SearchRangesV.setValidator(self.IntValidator)
        SearchRangesSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        SearchRangesSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.SearchRangesWidgets = [self.SearchRanges0Label, self.SearchRanges0,
                                    self.SearchRanges90Label, self.SearchRanges90,
                                    self.SearchRangesVLabel, self.SearchRangesV,
                                    SearchRangesSpacerL, SearchRangesSpacerR]
        self.SearchRangesWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                          [1,1,1,1], [1,2,1,1],
                                          [2,1,2,1], [2,2,1,1],
                                          [1,0,1,1], [1,3,1,1]]
        
        self.InterpolationGB = QtGui.QGroupBox(self.Tab3)
        self.InterpolationLayout = QtGui.QGridLayout(self.InterpolationGB)
        
        self.InterpolationPointsLabel = QtGui.QLabel(self.InterpolationGB)
        self.InterpolationPoints = QtGui.QLineEdit(self.InterpolationGB)
        self.InterpolationPoints.setValidator(self.IntValidator)
        self.MeanValueLabel = QtGui.QLabel(self.InterpolationGB)
        self.MeanValue = QtGui.QLineEdit(self.InterpolationGB)
        self.MeanValue.setValidator(self.double_validator)
        InterpolationSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        InterpolationSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.InterpolationWidgets = [self.InterpolationPointsLabel, self.InterpolationPoints,
                                     self.MeanValueLabel, self.MeanValue,
                                     InterpolationSpacerL, InterpolationSpacerR]
        self.InterpolationWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                           [1,1,1,1], [1,2,1,1],
                                           [0,0,1,1], [0,3,1,1]]
        
        self.RunGB = QtGui.QGroupBox(self.Tab3)
        self.RunLayout = QtGui.QGridLayout(self.RunGB)
        
        self.RunButton = QtGui.QPushButton(self.RunGB)
        self.RunButton.setDisabled(1)
        self.SaveButton = QtGui.QPushButton(self.RunGB)
        self.SaveButton.setDisabled(1)
        RunSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        RunSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        RunSpacerD = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        self.RunWidgets = [self.RunButton, self.SaveButton,
                           RunSpacerL, RunSpacerR, RunSpacerD]
        self.RunWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                 [0,0,1,1], [0,3,1,1], [2,0,1,2]]       
        
        self.AlgorithmTypeGB = QtGui.QGroupBox(self.Tab3)
        self.AlgorithmTypeLayout = QtGui.QGridLayout(self.AlgorithmTypeGB)
        
        self.AlgorithmTypeLabel = QtGui.QLabel(self.AlgorithmTypeGB)        
        self.AlgorithmType = QtGui.QComboBox(self.AlgorithmTypeGB)
        for i in xrange(0, self.AlgorithmCount):
            self.AlgorithmType.addItem("")        
        AlgorithmTypeSpacerL = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        AlgorithmTypeSpacerR = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        self.AlgorithmTypeWidgets = [self.AlgorithmTypeLabel, self.AlgorithmType,
                                     AlgorithmTypeSpacerL, AlgorithmTypeSpacerR]
        self.AlgorithmTypeWidgetsPlaces = [[0,1,1,1], [0,2,1,1],
                                           [0,0,1,1], [0,3,1,1]]
        
        
        Tab3Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        self.Tab3Widgets = [self.AlgorithmTypeGB, self.LoadedCubesGB,
                            self.SearchRangesGB, self.InterpolationGB,
                            self.RunGB, Tab3Spacer]
        self.Tab3WidgetsPlaces = [[0,0,1,1],[0,1,1,1],
                                  [1,0,1,1],[1,1,1,1],
                                  [2,0,1,2],[3,1,1,1]]
        
        self.place_widgets_at_places(self.LoadedCubesLayout, self.LoadedCubesWidgets, self.LoadedCubesWidgetsPlaces)
        self.place_widgets_at_places(self.InterpolationLayout, self.InterpolationWidgets, self.InterpolationWidgetsPlaces)
        self.place_widgets_at_places(self.SearchRangesLayout, self.SearchRangesWidgets, self.SearchRangesWidgetsPlaces)
        self.place_widgets_at_places(self.AlgorithmTypeLayout, self.AlgorithmTypeWidgets, self.AlgorithmTypeWidgetsPlaces)
        self.place_widgets_at_places(self.RunLayout, self.RunWidgets, self.RunWidgetsPlaces) 
        self.place_widgets_at_places(self.Tab3Layout, self.Tab3Widgets, self.Tab3WidgetsPlaces)
    
        self.TabWidget.addTab(self.Tab3, "")
        
        # Other Mainwindow layouths, bars, etc.
        self.CentralLayout.addWidget(self.TabWidget, 0, 0, 1, 1)
        self.ProgressBar = QtGui.QProgressBar(self.CentralWidget)
        self.ProgressBar.setProperty("value", 24)
        self.ProgressBar.setValue(0)
        self.ProgressBar.hide()
        self.CentralLayout.addWidget(self.ProgressBar, 1, 0, 1, 1)
        
        self.LogTextbox = QtGui.QTextEdit(self.CentralWidget)
        self.LogTextbox.setReadOnly(True)
        self.CentralLayout.addWidget(self.LogTextbox, 2, 0, 1, 1)
        self.setCentralWidget(self.CentralWidget)
        
        self.Menubar = QtGui.QMenuBar()
        self.Menubar.setGeometry(QtCore.QRect(0, 0, 700, 24))
        self.Menu = QtGui.QMenu(self.Menubar)
        self.MenuEdit = QtGui.QMenu(self.Menubar)
        self.MenuHelp = QtGui.QMenu(self.Menubar)
        self.setMenuBar(self.Menubar)
        
        self.Statusbar = QtGui.QStatusBar()
        self.setStatusBar(self.Statusbar)
        
        self.ActionExit = QtGui.QAction(self)
        self.ActionAbout = QtGui.QAction(self)
        self.ActionPreferences = QtGui.QAction(self)
        self.Menu.addAction(self.ActionExit)
        self.MenuEdit.addAction(self.ActionPreferences)
        self.MenuHelp.addAction(self.ActionAbout)
        self.Menubar.addAction(self.Menu.menuAction())
        self.Menubar.addAction(self.MenuEdit.menuAction())
        self.Menubar.addAction(self.MenuHelp.menuAction())
        
        self.RetranslateUI(self)
        self.TabWidget.setCurrentIndex(0)
        
        # Signals and slots
        QtCore.QObject.connect(self.IndValuesCheckbox, QtCore.SIGNAL("toggled(bool)"), self.IndValues.setEnabled)
        QtCore.QObject.connect(self.ActionExit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.LoadCubeButton, QtCore.SIGNAL("clicked()"), self.cube_load)
        QtCore.QObject.connect(self.RunButton, QtCore.SIGNAL("clicked()"), self.algorithm_run)
        QtCore.QObject.connect(self.GridSizeX, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.GridSizeY, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.GridSizeZ, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.CubeDeleteButton, QtCore.SIGNAL("clicked()"), self.delete_cube)
        QtCore.QObject.connect(self.SaveButton, QtCore.SIGNAL("clicked()"), self.sk_result_save)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def place_widgets_at_places(self, layout, widgets, places):
        self.layout = layout
        self.widgets = widgets
        self.places = places
        for i in xrange(len(self.widgets)):
            if type(self.widgets[i]) == type(self.GridSizeSpacerL):
                self.layout.addItem(widgets[i], places[i][0], places[i][1], places[i][2], places[i][3])
            else:
                self.layout.addWidget(widgets[i], places[i][0], places[i][1], places[i][2], places[i][3])

    def delete_cube(self):
        self.current_index = self.LoadedCubesTab1.currentIndex()
        del (self.Cubes[self.current_index])
        self.LoadedCubesTab1.removeItem(self.current_index)
        self.LoadedCubes.removeItem(self.current_index)
        self.LogTextbox.insertPlainText('Cube deleted\n')
        if self.LoadedCubesTab1.count() == 0:
            self.RunButton.setDisabled(1)
            self.CubeDeleteButton.setDisabled(1)

    def update_ui(self, string):
        self.LogTextbox.insertPlainText("%s"%unicode(string))
        
    def update_progress(self, value):
        self.ProgressBar.setValue(int(value))
        
    def cube_load_access(self):
        if int(self.GridSizeX.text()) > 0 and int(self.GridSizeY.text()) > 0 and int(self.GridSizeZ.text()) > 0:
            self.LoadCubeButton.setEnabled(1)
            
    def sk_result(self, Result):
        self.Result = Result
        self.RunButton.setEnabled(1)
        if self.Result != None:
            self.SaveButton.setEnabled(1)
            self.Result_values = [self.Cubes[self.curr_cube][1], self.Cubes[self.curr_cube][2]]
        
    def sk_result_save(self):
        if self.Result != None:
            self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as ... ')
            if self.fname and self.Result_values[1] != None:
                write_property( self.Result, str(self.fname), "SK_RESULT", self.Result_values[1], self.Result_values[0] )
            elif self.fname and self.Result_values[1] == None:
                write_property( self.Result, str(self.fname), "SK_RESULT", self.Result_values[0] )
            self.Result_was_saved = 1
    
    def cube_load(self):
        self.LogTextbox.clear()
        if self.GridSizeX.text() == "":
            self.LogTextbox.insertPlainText('"Grid size x" is empty\n')
        elif self.GridSizeY.text() == "":
            self.LogTextbox.insertPlainText('"Grid size y" is empty\n')
        elif self.GridSizeZ.text() == "":
            self.LogTextbox.insertPlainText('"Grid size z" is empty\n')
        elif self.UndefValue.text() == "":
            self.LogTextbox.insertPlainText('"Undefined value" is empty\n')
        else :
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
            if filename:
                self.loaded_cube_fname = re.search('(.*\/)([\w.]*)', filename) 
                self.loaded_cube_fname = self.loaded_cube_fname.group(self.loaded_cube_fname.lastindex)
                self.CubeWasChosen = 1
                self.LogTextbox.insertPlainText("Selected cube: " + self.loaded_cube_fname +'\n')
                
                self.GridObject = SugarboxGrid( int(self.GridSizeX.text()), int(self.GridSizeY.text()), int(self.GridSizeZ.text()) )
                self.GridSize = ( int(self.GridSizeX.text()), int(self.GridSizeY.text()), int(self.GridSizeZ.text()) )
                self.undefined_value = int(self.UndefValue.text())
                if self.IndValuesCheckbox.isChecked():
                    self.indicator_value = range(int(self.IndValues.text()))
                else:
                    self.indicator_value = None
            
                if self.IndValuesCheckbox.isChecked():
                    self.LogTextbox.insertPlainText('Loaded cube with indicator values\n')
                    self.CubeWasChosen = 0
                
                    # Starting load indicator cube with HPGL
                    self.Prop = load_ind_property(str(filename), self.undefined_value, self.indicator_value, self.GridSize)
                    
                elif self.IndValuesCheckbox.isChecked() == 0:
                    self.LogTextbox.insertPlainText('Loaded cube\n')
                    self.CubeWasChosen = 0
                
                    # Starting load cube with HPGL
                    self.Prop = load_cont_property( str(filename), self.undefined_value, self.GridSize )
                    if self.Prop != None:
                        self.RunButton.setEnabled(1)
                        self.LoadedCubesTab1.addItem(self.loaded_cube_fname)
                        self.LoadedCubes.addItem(self.loaded_cube_fname)
                        self.Cubes.append([self.Prop, self.undefined_value, self.indicator_value])
                        del(self.Prop)
                        self.CubeDeleteButton.setEnabled(1)
            else:
                self.LogTextbox.insertPlainText("Cube not chosen\n")

    
    def algorithm_run(self):
        if self.EllipsoidRanges0.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid ranges 0" is empty\n')
        elif self.EllipsoidRanges90.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid ranges 90" is empty\n')
        elif self.EllipsoidRangesV.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid ranges vertical" is empty\n')
        elif self.EllipsoidAnglesX.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid angles x" is empty\n')
        elif self.EllipsoidAnglesY.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid angles y" is empty\n')
        elif self.EllipsoidAnglesZ.text() == "":
            self.LogTextbox.insertPlainText('"Ellipsoid angles z" is empty\n')
        elif self.SillValue.text() == "":
            self.LogTextbox.insertPlainText('"Sill value" is empty\n')
        elif self.NuggetValue.text() == "":
            self.LogTextbox.insertPlainText('"Nugget effect value" is empty\n')
        else :
            if self.AlgorithmType.currentIndex() == 0:
                if self.SearchRanges0.text() == "":
                    self.LogTextbox.insertPlainText('"Search ranges 0" is empty\n')
                elif self.SearchRanges90.text() == "":
                    self.LogTextbox.insertPlainText('"Search ranges 90" is empty\n')
                elif self.SearchRangesV.text() == "":
                    self.LogTextbox.insertPlainText('"Search ranges vertical" is empty\n')
                elif self.InterpolationPoints.text() == "":
                    self.LogTextbox.insertPlainText('"Interpolation points" is empty\n')
                elif self.MeanValue.text() == "":
                    self.LogTextbox.insertPlainText('"Mean value" is empty\n')
                elif self.LoadedCubes.count() == 0:
                    self.LogTextbox.insertPlainText('No Cubes loaded!\n')
                else :
                    self.LogTextbox.insertPlainText("Starting Simple Kriging Algorithm\n")
                    self.ProgressBar.show()
                    
                    # Variogram
                    self.Variogram_ranges = ( int(self.EllipsoidRanges0.text()), int(self.EllipsoidRanges90.text()), int(self.EllipsoidRangesV.text()) )
                    self.Variogram_angles = ( int(self.EllipsoidAnglesX.text()), int(self.EllipsoidAnglesY.text()), int(self.EllipsoidAnglesZ.text()) )
                    self.Variogram = geo.CovarianceModel( int(self.VariogramType.currentIndex()), self.Variogram_ranges, 
                                                      self.Variogram_angles, int(self.SillValue.text()), int(self.NuggetValue.text()) )
                    
                    # Simple Kriging
                    
                    self.EllipsoidRanges = ( int(self.EllipsoidRanges0.text()), int(self.EllipsoidRanges90.text()), int(self.EllipsoidRangesV.text()) )
                    self.curr_cube = self.LoadedCubes.currentIndex()
                    self.new_thread = algorithm_thread( self.Cubes[self.curr_cube][0], self.GridObject, self.EllipsoidRanges, int(self.InterpolationPoints.text()),
                                                        self.Variogram, float(self.MeanValue.text()), self.Cubes[self.curr_cube][1] )
                    
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("msg(QString)"), self.update_ui)
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("progress(QString)"), self.update_progress)
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("Result(PyQt_PyObject)"), self.sk_result)
                    self.new_thread.start()
                    self.RunButton.setDisabled(1)
                    
            elif self.AlgorithmType.currentIndex() == 2:
                self.LogTextbox.insertPlainText("Starting Ordinary Kriging Algorithm\n")
        
    def RetranslateUI(self, MainWindow):
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
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab1), (self.__tr("Load cube")))
        
        # Tab 2
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
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab2), (self.__tr("Variogram")))
        
        # Tab 3
        self.LoadedCubesGB.setTitle(self.__tr("Cubes"))
        self.LoadedCubesLabel.setText(self.__tr("Select cube:"))
        self.SearchRangesGB.setTitle(self.__tr("Search ellipsoid ranges"))
        self.SearchRanges0Label.setText(self.__tr("0"))
        self.SearchRanges0.setText(self.__tr("20"))
        self.SearchRanges90Label.setText(self.__tr("90"))
        self.SearchRanges90.setText(self.__tr("20"))
        self.SearchRangesVLabel.setText(self.__tr("Vertical"))
        self.SearchRangesV.setText(self.__tr("20"))
        self.InterpolationGB.setTitle(self.__tr("Interpolation"))
        self.InterpolationPointsLabel.setText(self.__tr("Maximum interpolation points"))
        self.InterpolationPoints.setText(self.__tr("20"))
        self.MeanValueLabel.setText(self.__tr("Mean value"))
        self.MeanValue.setText(self.__tr("0"))
        self.RunGB.setTitle(self.__tr("Solve algorithm"))
        self.RunButton.setText(self.__tr("Run"))
        self.SaveButton.setText(self.__tr("Save"))
        self.AlgorithmTypeGB.setTitle(self.__tr("Algorithm"))
        self.AlgorithmTypeLabel.setText(self.__tr("Algorithm type"))
        self.AlgorithmTypes = ['Simple Kriging', 'Ordinary Kriging', 
                                'Indicator Kriging', 'LVM Kriging', 
                                'Sequantial Indicator Simulation', 
                                'Sequantial Gaussian Simulation']
        for i in xrange(len(self.AlgorithmTypes)):
            self.AlgorithmType.setItemText(i, (self.__tr(self.AlgorithmTypes[i])))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Tab3), (self.__tr("Algorithms")))
        
        # Menus
        self.Menu.setTitle(self.__tr("File"))
        self.MenuEdit.setTitle(self.__tr("Edit"))
        self.MenuHelp.setTitle(self.__tr("Help"))
        self.ActionExit.setText(self.__tr("Exit"))
        self.ActionExit.setShortcut(self.__tr("Ctrl+Q"))
        self.ActionAbout.setText(self.__tr("About"))
        self.ActionPreferences.setText(self.__tr("Preferences"))
        self.ActionPreferences.setShortcut(self.__tr("Ctrl+P"))
        
    def __tr(self, s, c=None):
        return QtGui.qApp.translate("MainWindow", s, c, QtGui.QApplication.UnicodeUTF8)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
