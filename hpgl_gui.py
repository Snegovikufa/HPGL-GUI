#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from geo_bsd import *
from geo_bsd.cvariogram import *
import re


class algorithm_thread(QtCore.QThread):
    def __init__(self, prop, grid_object, ellipsoid_ranges, int_points, variogram, mean_value, undef_value, ind_value):
        QtCore.QThread.__init__(self)
        
        self.prop = prop
        self.grid_object = grid_object
        self.ellipsoid_ranges = ellipsoid_ranges
        self.int_points = int_points
        self.variogram = variogram
        self.mean_value = mean_value
        self.und_value = undef_value
        self.ind_value = ind_value
        
    def run(self):
        set_output_handler(self.output_log, None)
        set_progress_handler(self.progress_show, None)
        self.result = simple_kriging( self.prop, self.grid_object, self.ellipsoid_ranges, 
                                           self.int_points, self.variogram, self.mean_value )
        self.emit(QtCore.SIGNAL("result(PyQt_PyObject)"), self.result)
        
    def output_log(self, str, _):
        self.str_for_log = str
        self.emit(QtCore.SIGNAL("msg(QString)"), QtCore.QString(self.str_for_log))
        return 0
        
    def progress_show(self, stage, percent, _):
        self.percent = percent
        self.stage = stage
        if self.percent == 0:
            print self.stage,
        elif self.percent == -1:
                print ""
        else:
            self.out_str = int(self.percent)
            self.out_str = str(self.out_str)
            self.emit(QtCore.SIGNAL("progress(QString)"), QtCore.QString(self.out_str))
        return 0

    def __del__(self):
        self.exiting = True
        self.wait()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setObjectName("MainWindow")
        self.setFixedWidth(700)
        self.setFixedHeight(520)
        self.centralwidget = QtGui.QWidget()
        self.gridLayout_10 = QtGui.QGridLayout(self.centralwidget)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        
        self.cube_was_chosen = 0
        self.algorithm_count = 6
        self.int_validator = QtGui.QIntValidator(self)
        self.double_validator = QtGui.QDoubleValidator(self)
        self.cubes = []
        
        # TAB 1
        self.tab1 = QtGui.QWidget()
        self.gridLayout_5 = QtGui.QGridLayout(self.tab1)
        self.grid_size_groupbox = QtGui.QGroupBox(self.tab1)
        self.gridLayout = QtGui.QGridLayout(self.grid_size_groupbox)
        
        self.grid_size_x_label = QtGui.QLabel(self.grid_size_groupbox)
        self.gridLayout.addWidget(self.grid_size_x_label, 0, 1, 1, 1)
        self.grid_size_x = QtGui.QLineEdit(self.grid_size_groupbox)
        self.grid_size_x.setValidator(self.int_validator)
        self.gridLayout.addWidget(self.grid_size_x, 0, 2, 1, 1)
        
        self.grid_size_y_label = QtGui.QLabel(self.grid_size_groupbox)
        self.gridLayout.addWidget(self.grid_size_y_label, 1, 1, 1, 1)
        self.grid_size_y = QtGui.QLineEdit(self.grid_size_groupbox)
        self.grid_size_y.setValidator(self.int_validator)
        self.gridLayout.addWidget(self.grid_size_y, 1, 2, 1, 1)
        
        self.grid_size_z_label = QtGui.QLabel(self.grid_size_groupbox)
        self.gridLayout.addWidget(self.grid_size_z_label, 2, 1, 1, 1)
        self.grid_size_z = QtGui.QLineEdit(self.grid_size_groupbox)
        self.grid_size_z.setValidator(self.int_validator)
        self.gridLayout.addWidget(self.grid_size_z, 2, 2, 1, 1)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.gridLayout_5.addWidget(self.grid_size_groupbox, 0, 0, 1, 1)
        
        self.manage_cubes_groupbox = QtGui.QGroupBox(self.tab1)
        self.gridLayout_2 = QtGui.QGridLayout(self.manage_cubes_groupbox)
        
        self.loaded_cubes_tab1 = QtGui.QComboBox(self.manage_cubes_groupbox)
        self.gridLayout_2.addWidget(self.loaded_cubes_tab1, 0, 1, 1, 1)
        
        self.cube_delete_btn = QtGui.QPushButton(self.manage_cubes_groupbox)
        self.cube_delete_btn.setDisabled(1)
        self.gridLayout_2.addWidget(self.cube_delete_btn, 0, 2, 1, 1)
        
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 3, 1, 1)
        self.gridLayout_5.addWidget(self.manage_cubes_groupbox, 0, 1, 1, 1)
        
        self.ind_values_groupbox = QtGui.QGroupBox(self.tab1)
        self.gridLayout_3 = QtGui.QGridLayout(self.ind_values_groupbox)
        
        self.ind_values = QtGui.QSpinBox(self.ind_values_groupbox)
        self.ind_values.setEnabled(False)
        self.ind_values.setMinimum(2)
        self.ind_values.setMaximum(256)
        self.gridLayout_3.addWidget(self.ind_values, 1, 2, 1, 1)
        
        self.ind_values_checkbox = QtGui.QCheckBox(self.ind_values_groupbox)
        self.ind_values_checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gridLayout_3.addWidget(self.ind_values_checkbox, 1, 1, 1, 1)
        
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 1, 3, 1, 1)
        self.gridLayout_5.addWidget(self.ind_values_groupbox, 1, 0, 1, 1)
        
        self.undef_value_groupbox = QtGui.QGroupBox(self.tab1)
        self.horizontalLayout = QtGui.QHBoxLayout(self.undef_value_groupbox)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        
        self.undef_value_label = QtGui.QLabel(self.undef_value_groupbox)
        self.horizontalLayout.addWidget(self.undef_value_label)
        
        self.undef_value = QtGui.QLineEdit(self.undef_value_groupbox)
        self.undef_value.setValidator(self.int_validator)
        self.horizontalLayout.addWidget(self.undef_value)
        
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.gridLayout_5.addWidget(self.undef_value_groupbox, 1, 1, 1, 1)
        self.load_cube_groupbox = QtGui.QGroupBox(self.tab1)
        self.load_cube_groupbox.setTitle("")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.load_cube_groupbox)
        spacerItem8 = QtGui.QSpacerItem(241, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        
        self.load_cube_btn = QtGui.QPushButton(self.load_cube_groupbox)
        self.load_cube_btn.setDisabled(1)
        self.horizontalLayout_2.addWidget(self.load_cube_btn)
        
        spacerItem9 = QtGui.QSpacerItem(241, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.gridLayout_5.addWidget(self.load_cube_groupbox, 3, 0, 1, 2)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem10, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")
        
        # TAB 2
        self.tab2 = QtGui.QWidget()
        self.gridLayout_11 = QtGui.QGridLayout(self.tab2)
        self.variogram_type_groupbox = QtGui.QGroupBox(self.tab2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.variogram_type_groupbox)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        
        self.variogram_type_label = QtGui.QLabel(self.variogram_type_groupbox)
        self.horizontalLayout_3.addWidget(self.variogram_type_label)
        
        self.variogram_type = QtGui.QComboBox(self.variogram_type_groupbox)
        self.variogram_type.addItem("")
        self.variogram_type.addItem("")
        self.variogram_type.addItem("")
        self.horizontalLayout_3.addWidget(self.variogram_type)
        self.variogram_type.setValidator(self.int_validator)
        
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.gridLayout_11.addWidget(self.variogram_type_groupbox, 0, 0, 1, 1)
        self.ellipsoid_ranges_groupbox = QtGui.QGroupBox(self.tab2)
        self.gridLayout_6 = QtGui.QGridLayout(self.ellipsoid_ranges_groupbox)
        
        self.ellipsoid_ranges_0_label = QtGui.QLabel(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_0_label, 0, 1, 2, 1)
        
        self.ellipsoid_ranges_0 = QtGui.QLineEdit(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_0, 0, 2, 1, 1)
        self.ellipsoid_ranges_0.setValidator(self.int_validator)
        
        self.ellipsoid_ranges_90_label = QtGui.QLabel(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_90_label, 2, 1, 1, 1)
        
        self.ellipsoid_ranges_90 = QtGui.QLineEdit(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_90, 1, 2, 2, 1)
        self.ellipsoid_ranges_90.setValidator(self.int_validator)
        
        self.ellipsoid_ranges_v_label = QtGui.QLabel(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_v_label, 3, 1, 1, 1)
        
        self.ellipsoid_ranges_v = QtGui.QLineEdit(self.ellipsoid_ranges_groupbox)
        self.gridLayout_6.addWidget(self.ellipsoid_ranges_v, 3, 2, 1, 1)
        self.ellipsoid_ranges_v.setValidator(self.int_validator)
        
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem13, 1, 3, 1, 1)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem14, 1, 0, 1, 1)

        self.gridLayout_11.addWidget(self.ellipsoid_ranges_groupbox, 0, 1, 1, 1)
        self.ellipsoid_angles = QtGui.QGroupBox(self.tab2)
        self.gridLayout_7 = QtGui.QGridLayout(self.ellipsoid_angles)
        
        self.ellipsoid_angles_x_label = QtGui.QLabel(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_x_label, 0, 1, 1, 1)
        
        self.ellipsoid_angles_x = QtGui.QLineEdit(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_x, 0, 2, 1, 1)
        self.ellipsoid_angles_x.setValidator(self.int_validator)
        
        self.ellipsoid_angles_y = QtGui.QLineEdit(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_y, 1, 2, 2, 1)
        self.ellipsoid_angles_y.setValidator(self.int_validator)
        
        self.ellipsoid_angles_z_label = QtGui.QLabel(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_z_label, 2, 1, 2, 1)
        
        self.ellipsoid_angles_z = QtGui.QLineEdit(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_z, 3, 2, 1, 1)
        self.ellipsoid_angles_z.setValidator(self.int_validator)
        
        self.ellipsoid_angles_y_label = QtGui.QLabel(self.ellipsoid_angles)
        self.gridLayout_7.addWidget(self.ellipsoid_angles_y_label, 1, 1, 1, 1)
        
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem15, 1, 0, 1, 1)
        spacerItem16 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem16, 1, 3, 1, 1)

        self.gridLayout_11.addWidget(self.ellipsoid_angles, 1, 0, 1, 1)
        self.nugget_effect_groupbox = QtGui.QGroupBox(self.tab2)
        self.gridLayout_8 = QtGui.QGridLayout(self.nugget_effect_groupbox)
        
        self.sill_value_label = QtGui.QLabel(self.nugget_effect_groupbox)
        self.gridLayout_8.addWidget(self.sill_value_label, 0, 1, 1, 1)
        
        self.sill_value = QtGui.QLineEdit(self.nugget_effect_groupbox)
        self.gridLayout_8.addWidget(self.sill_value, 0, 2, 1, 1)
        self.sill_value.setValidator(self.int_validator)
        
        self.nugget_value_label = QtGui.QLabel(self.nugget_effect_groupbox)
        self.gridLayout_8.addWidget(self.nugget_value_label, 1, 1, 1, 1)
        
        self.nugget_value = QtGui.QLineEdit(self.nugget_effect_groupbox)
        self.gridLayout_8.addWidget(self.nugget_value, 1, 2, 1, 1)
        self.nugget_value.setValidator(self.int_validator)
        
        spacerItem17 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem17, 0, 0, 1, 1)
        spacerItem18 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem18, 1, 3, 1, 1)

        self.gridLayout_11.addWidget(self.nugget_effect_groupbox, 1, 1, 1, 1)
        spacerItem19 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem19, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab2, "")
        
        # TAB 3
        self.tab3 = QtGui.QWidget()
        self.gridLayout_12 = QtGui.QGridLayout(self.tab3)
        self.loaded_cubs_groupbox = QtGui.QGroupBox(self.tab3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.loaded_cubs_groupbox)
        spacerItem20 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem20)
        
        self.loaded_cubes_label = QtGui.QLabel(self.loaded_cubs_groupbox)
        self.horizontalLayout_5.addWidget(self.loaded_cubes_label)
        
        self.loaded_cubes = QtGui.QComboBox(self.loaded_cubs_groupbox)
        self.horizontalLayout_5.addWidget(self.loaded_cubes)
        
        spacerItem21 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem21)
        self.gridLayout_12.addWidget(self.loaded_cubs_groupbox, 0, 1, 1, 1)
        self.search_ranges_groupbox = QtGui.QGroupBox(self.tab3)
        self.gridLayout_4 = QtGui.QGridLayout(self.search_ranges_groupbox)
        
        self.search_ranges_0_label = QtGui.QLabel(self.search_ranges_groupbox)
        self.gridLayout_4.addWidget(self.search_ranges_0_label, 0, 1, 1, 1)
        
        self.search_ranges_0 = QtGui.QLineEdit(self.search_ranges_groupbox)
        self.gridLayout_4.addWidget(self.search_ranges_0, 0, 2, 1, 1)
        self.search_ranges_0.setValidator(self.int_validator)
        
        self.search_ranges_90_label = QtGui.QLabel(self.search_ranges_groupbox)
        self.gridLayout_4.addWidget(self.search_ranges_90_label, 1, 1, 1, 1)
        
        self.search_ranges_90 = QtGui.QLineEdit(self.search_ranges_groupbox)
        self.search_ranges_90.setValidator(self.int_validator)
        self.gridLayout_4.addWidget(self.search_ranges_90, 1, 2, 1, 1)
        
        self.search_ranges_v_label = QtGui.QLabel(self.search_ranges_groupbox)
        self.gridLayout_4.addWidget(self.search_ranges_v_label, 2, 1, 1, 1)
        
        self.search_ranges_v = QtGui.QLineEdit(self.search_ranges_groupbox)
        self.gridLayout_4.addWidget(self.search_ranges_v, 2, 2, 1, 1)
        self.search_ranges_v.setValidator(self.int_validator)
        
        spacerItem22 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem22, 1, 0, 1, 1)
        spacerItem23 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem23, 1, 3, 1, 1)

        self.gridLayout_12.addWidget(self.search_ranges_groupbox, 1, 0, 1, 1)
        self.interpolation_groupbox = QtGui.QGroupBox(self.tab3)
        self.gridLayout_9 = QtGui.QGridLayout(self.interpolation_groupbox)
        
        self.interpolation_points_label = QtGui.QLabel(self.interpolation_groupbox)
        self.gridLayout_9.addWidget(self.interpolation_points_label, 0, 1, 1, 1)
        
        self.interpolation_points = QtGui.QLineEdit(self.interpolation_groupbox)
        self.gridLayout_9.addWidget(self.interpolation_points, 0, 2, 1, 1)
        self.interpolation_points.setValidator(self.int_validator)
        
        self.mean_value_label = QtGui.QLabel(self.interpolation_groupbox)
        self.gridLayout_9.addWidget(self.mean_value_label, 1, 1, 1, 1)
        
        self.mean_value = QtGui.QLineEdit(self.interpolation_groupbox)
        self.gridLayout_9.addWidget(self.mean_value, 1, 2, 1, 1)
        self.mean_value.setValidator(self.double_validator)
        
        spacerItem24 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem24, 0, 0, 1, 1)
        spacerItem25 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem25, 0, 3, 1, 1)

        self.gridLayout_12.addWidget(self.interpolation_groupbox, 1, 1, 1, 1)
        self.run_groupbox = QtGui.QGroupBox(self.tab3)
        self.gridLayout_13 = QtGui.QGridLayout(self.run_groupbox)
        
        self.run_button = QtGui.QPushButton(self.run_groupbox)
        self.run_button.setDisabled(1)
        self.gridLayout_13.addWidget(self.run_button, 0, 1, 1, 1)
        
        self.save_button = QtGui.QPushButton(self.run_groupbox)
        self.save_button.setDisabled(1)
        self.gridLayout_13.addWidget(self.save_button, 0, 2, 1, 1)
        
        spacerItem26 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem26, 0, 0, 1, 1)
        spacerItem27 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem27, 0, 3, 1, 1)
        spacerItem28 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_13.addItem(spacerItem28, 1, 1, 1, 1)

        self.gridLayout_12.addWidget(self.run_groupbox, 2, 0, 1, 2)
        self.algorithm_type_groupbox = QtGui.QGroupBox(self.tab3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.algorithm_type_groupbox)
        spacerItem29 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem29)
        spacerItem30 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem30)
        
        self.algorithm_type_label = QtGui.QLabel(self.algorithm_type_groupbox)
        self.horizontalLayout_4.addWidget(self.algorithm_type_label)
        
        self.algorithm_type = QtGui.QComboBox(self.algorithm_type_groupbox)
        for i in xrange(0, self.algorithm_count):
            self.algorithm_type.addItem("")
        self.horizontalLayout_4.addWidget(self.algorithm_type)
        
        spacerItem31 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem31)
        self.gridLayout_12.addWidget(self.algorithm_type_groupbox, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab3, "")
        
        # Other Mainwindow layouths, bars, etc.
        self.gridLayout_10.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.gridLayout_10.addWidget(self.progressBar, 1, 0, 1, 1)
        
        self.log_textbox = QtGui.QTextEdit(self.centralwidget)
        self.log_textbox.setReadOnly(True)
        self.gridLayout_10.addWidget(self.log_textbox, 2, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 698, 24))
        self.menu = QtGui.QMenu(self.menubar)
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        
        self.statusbar = QtGui.QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.actionExit = QtGui.QAction(self)
        self.actionAbout = QtGui.QAction(self)
        self.actionPreferences = QtGui.QAction(self)
        self.menu.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        
        # Signals and slots
        QtCore.QObject.connect(self.ind_values_checkbox, QtCore.SIGNAL("toggled(bool)"), self.ind_values.setEnabled)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.load_cube_btn, QtCore.SIGNAL("clicked()"), self.cube_load)
        QtCore.QObject.connect(self.run_button, QtCore.SIGNAL("clicked()"), self.algorithm_run)
        QtCore.QObject.connect(self.grid_size_x, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.grid_size_y, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.grid_size_z, QtCore.SIGNAL("textChanged(QString)"), self.cube_load_access)
        QtCore.QObject.connect(self.cube_delete_btn, QtCore.SIGNAL("clicked()"), self.delete_cube)
        QtCore.QObject.connect(self.save_button, QtCore.SIGNAL("clicked()"), self.sk_result_save)
        QtCore.QMetaObject.connectSlotsByName(self)

    def delete_cube(self):
        self.current_index = self.loaded_cubes_tab1.currentIndex()
        del (self.cubes[self.current_index])
        self.loaded_cubes_tab1.removeItem(self.current_index)
        self.loaded_cubes.removeItem(self.current_index)
        self.log_textbox.insertPlainText('Cube deleted\n')
        if self.loaded_cubes_tab1.count() == 0:
            self.run_button.setDisabled(1)
            self.cube_delete_btn.setDisabled(1)

    def update_ui(self, string):
        self.log_textbox.insertPlainText("%s"%unicode(string))
        
    def update_progress(self, value):
        self.progressBar.setValue(int(value))
        
    def cube_load_access(self):
        if int(self.grid_size_x.text()) > 0 and int(self.grid_size_y.text()) > 0 and int(self.grid_size_z.text()) > 0:
            self.load_cube_btn.setEnabled(1)
            
    def sk_result(self, result):
        self.result = result
        if self.result != None:
            self.save_button.setEnabled(1)
            self.result_values = [self.cubes[self.curr_cube][1], self.cubes[self.curr_cube][2]]
        
    def sk_result_save(self):
        if self.result != None:
            self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as ... ')
            if self.fname and self.indicator_value > 1:
                write_property( self.result, str(self.fname), "SK_RESULT", self.result_values[1], self.result_values[0] )
            elif self.fname and self.indicator_value == 0:
                write_property( self.result, str(self.fname), "SK_RESULT", self.result_values[0] )
            self.result_was_saved = 1
    
    def cube_load(self):
        self.log_textbox.clear()
        if self.grid_size_x.text() == "":
            self.log_textbox.insertPlainText('"Grid size x" is empty\n')
        elif self.grid_size_y.text() == "":
            self.log_textbox.insertPlainText('"Grid size y" is empty\n')
        elif self.grid_size_z.text() == "":
            self.log_textbox.insertPlainText('"Grid size z" is empty\n')
        elif self.undef_value.text() == "":
            self.log_textbox.insertPlainText('"Undefined value" is empty\n')
        else :
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
            if filename:
                self.loaded_cube_fname = re.search('(.*\/)([\w.]*)',filename)
                self.loaded_cube_fname = self.loaded_cube_fname.group(self.loaded_cube_fname.lastindex)
                self.cube_was_chosen = 1
                self.log_textbox.insertPlainText("Selected cube: " + self.loaded_cube_fname +'\n')
                
                self.grid_object = SugarboxGrid( int(self.grid_size_x.text()), int(self.grid_size_y.text()), int(self.grid_size_z.text()) )
                self.grid_size = ( int(self.grid_size_x.text()), int(self.grid_size_y.text()), int(self.grid_size_z.text()) )
                self.undefined_value = int(self.undef_value.text())
                if self.ind_values_checkbox.isChecked():
                    self.indicator_value = int(self.ind_values.text())
                else:
                        self.indicator_value = 0
            
                if self.ind_values_checkbox.isChecked():
                    self.log_textbox.insertPlainText('Loaded cube with indicator values\n')
                    self.cube_was_chosen = 0
                
                    # Starting load indicator cube with HPGL
                    self.prop = load_ind_property(str(filename), self.undefined_value, self.indicator_value, self.grid_size)
                    
                elif self.ind_values_checkbox.isChecked() == 0:
                    self.log_textbox.insertPlainText('Loaded cube\n')
                    self.cube_was_chosen = 0
                
                    # Starting load cube with HPGL
                    self.prop = load_cont_property( str(filename), self.undefined_value, self.grid_size )
                    if self.prop != None:
                        self.run_button.setEnabled(1)
                        self.loaded_cubes_tab1.addItem(self.loaded_cube_fname)
                        self.loaded_cubes.addItem(self.loaded_cube_fname)
                        self.cubes.append([self.prop, self.undefined_value, self.indicator_value])
                        del(self.prop)
                        self.cube_delete_btn.setEnabled(1)
            else:
                self.log_textbox.insertPlainText("Cube not chosen\n")

    
    def algorithm_run(self):
        if self.ellipsoid_ranges_0.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid ranges 0" is empty\n')
        elif self.ellipsoid_ranges_90.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid ranges 90" is empty\n')
        elif self.ellipsoid_ranges_v.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid ranges vertical" is empty\n')
        elif self.ellipsoid_angles_x.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid angles x" is empty\n')
        elif self.ellipsoid_angles_y.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid angles y" is empty\n')
        elif self.ellipsoid_angles_z.text() == "":
            self.log_textbox.insertPlainText('"Ellipsoid angles z" is empty\n')
        elif self.sill_value.text() == "":
            self.log_textbox.insertPlainText('"Sill value" is empty\n')
        elif self.nugget_value.text() == "":
            self.log_textbox.insertPlainText('"Nugget effect value" is empty\n')
        else :
            if self.algorithm_type.currentIndex() == 0:
                if self.search_ranges_0.text() == "":
                    self.log_textbox.insertPlainText('"Search ranges 0" is empty\n')
                elif self.search_ranges_90.text() == "":
                    self.log_textbox.insertPlainText('"Search ranges 90" is empty\n')
                elif self.search_ranges_v.text() == "":
                    self.log_textbox.insertPlainText('"Search ranges vertical" is empty\n')
                elif self.interpolation_points.text() == "":
                    self.log_textbox.insertPlainText('"Interpolation points" is empty\n')
                elif self.mean_value.text() == "":
                    self.log_textbox.insertPlainText('"Mean value" is empty\n')
                elif self.loaded_cubes.count() == 0:
                    self.log_textbox.insertPlainText('No cubes loaded!\n')
                else :
                    self.log_textbox.insertPlainText("Starting Simple Kriging Algorithm\n")
                    self.progressBar.show()
                    
                    # Variogram
                    self.variogram_ranges = ( int(self.ellipsoid_ranges_0.text()), int(self.ellipsoid_ranges_90.text()), int(self.ellipsoid_ranges_v.text()) )
                    self.variogram_angles = ( int(self.ellipsoid_angles_x.text()), int(self.ellipsoid_angles_y.text()), int(self.ellipsoid_angles_z.text()) )
                    self.variogram = geo.CovarianceModel( int(self.variogram_type.currentIndex()), self.variogram_ranges, 
                                                      self.variogram_angles, int(self.sill_value.text()), int(self.nugget_value.text()) )
                    
                    # Simple Kriging
                    
                    self.ellipsoid_ranges = ( int(self.ellipsoid_ranges_0.text()), int(self.ellipsoid_ranges_90.text()), int(self.ellipsoid_ranges_v.text()) )
                    self.curr_cube = self.loaded_cubes.currentIndex()
                    self.new_thread = algorithm_thread( self.cubes[self.curr_cube][0], self.grid_object, self.ellipsoid_ranges, int(self.interpolation_points.text()),
                                                        self.variogram, float(self.mean_value.text()), self.cubes[self.curr_cube][1], self.cubes[self.curr_cube][2] )
                    
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("msg(QString)"), self.update_ui)
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("progress(QString)"), self.update_progress)
                    QtCore.QObject.connect(self.new_thread, QtCore.SIGNAL("result(PyQt_PyObject)"), self.sk_result)
                    self.new_thread.start()
                    
            elif self.algorithm_type.currentIndex() == 2:
                self.log_textbox.insertPlainText("Starting Ordinary Kriging Algorithm\n")

    def save_result(self, result):
        self.result = result
        self.output_filename = QtGui.QFileDialog.getSaveFileName(self, caption = QtCore.QString("Save file as") )
        if self.output_filename and self.ind_values_checkbox.isChecked():
            write_property( self.result, self.output_filename, "SK_RESULT", int(self.undef_value.text()), int(self.ind_values.text()) )
        elif self.output_filename and self.ind_values_checkbox.isChecked() == 0:
            write_property( self.result, self.output_filename, "SK_RESULT", int(self.undef_value.text()) )
        
    def retranslateUi(self, MainWindow):
        #self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "HPGL GUI", None, QtGui.QApplication.UnicodeUTF8))
        
        # Tab 1
        self.grid_size_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Grid Size", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_x_label.setText(QtGui.QApplication.translate("MainWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_x.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_y_label.setText(QtGui.QApplication.translate("MainWindow", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_y.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_z_label.setText(QtGui.QApplication.translate("MainWindow", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_size_z.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.manage_cubes_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Manage cubes", None, QtGui.QApplication.UnicodeUTF8))
        self.cube_delete_btn.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.ind_values_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Indicator value", None, QtGui.QApplication.UnicodeUTF8))
        self.ind_values_checkbox.setText(QtGui.QApplication.translate("MainWindow", "Indicator values", None, QtGui.QApplication.UnicodeUTF8))
        self.undef_value_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Undefined value", None, QtGui.QApplication.UnicodeUTF8))
        self.undef_value_label.setText(QtGui.QApplication.translate("MainWindow", "Undefined value", None, QtGui.QApplication.UnicodeUTF8))
        self.undef_value.setText(QtGui.QApplication.translate("MainWindow", "-99", None, QtGui.QApplication.UnicodeUTF8))
        self.load_cube_btn.setText(QtGui.QApplication.translate("MainWindow", "Load cube", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("MainWindow", "Load cube", None, QtGui.QApplication.UnicodeUTF8))
        
        # Tab 2
        self.variogram_type_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Variogram type", None, QtGui.QApplication.UnicodeUTF8))
        self.variogram_type_label.setText(QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.variogram_types = ['Spherical', 'Exponential', 'Gaussian']
        for i in xrange(len(self.variogram_types)):
            self.variogram_type.setItemText(i, QtGui.QApplication.translate("MainWindow", self.variogram_types[i], None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Ellipsoid ranges", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_0_label.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_0.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_90_label.setText(QtGui.QApplication.translate("MainWindow", "90", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_90.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_v_label.setText(QtGui.QApplication.translate("MainWindow", "Vertical", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_ranges_v.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles.setTitle(QtGui.QApplication.translate("MainWindow", "Ellipsoid angles", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_x_label.setText(QtGui.QApplication.translate("MainWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_x.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_y.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_z_label.setText(QtGui.QApplication.translate("MainWindow", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_z.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ellipsoid_angles_y_label.setText(QtGui.QApplication.translate("MainWindow", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.nugget_effect_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Sill value and nugget-effect", None, QtGui.QApplication.UnicodeUTF8))
        self.sill_value_label.setText(QtGui.QApplication.translate("MainWindow", "Sill value", None, QtGui.QApplication.UnicodeUTF8))
        self.sill_value.setText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.nugget_value_label.setText(QtGui.QApplication.translate("MainWindow", "\"Nugget\" effect value", None, QtGui.QApplication.UnicodeUTF8))
        self.nugget_value.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QtGui.QApplication.translate("MainWindow", "Variogram", None, QtGui.QApplication.UnicodeUTF8))
        
        # Tab 3
        self.loaded_cubs_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Cubes", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_cubes_label.setText(QtGui.QApplication.translate("MainWindow", "Select cube:", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Search ellipsoid ranges", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_0_label.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_0.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_90_label.setText(QtGui.QApplication.translate("MainWindow", "90", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_90.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_v_label.setText(QtGui.QApplication.translate("MainWindow", "Vertical", None, QtGui.QApplication.UnicodeUTF8))
        self.search_ranges_v.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolation_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Interpolation", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolation_points_label.setText(QtGui.QApplication.translate("MainWindow", "Maximum interpolation points", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolation_points.setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.mean_value_label.setText(QtGui.QApplication.translate("MainWindow", "Mean value", None, QtGui.QApplication.UnicodeUTF8))
        self.mean_value.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.run_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Solve algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.run_button.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.save_button.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.algorithm_type_groupbox.setTitle(QtGui.QApplication.translate("MainWindow", "Algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.algorithm_type_label.setText(QtGui.QApplication.translate("MainWindow", "Algorithm type", None, QtGui.QApplication.UnicodeUTF8))
        self.algorithm_types = ['Simple Kriging', 'Ordinary Kriging', 'Indicator Kriging', 'LVM Kriging', 
                                'Sequantial Indicator Simulation', 'Sequantial Gaussian Simulation']
        for i in xrange(len(self.algorithm_types)):
            self.algorithm_type.setItemText(i, QtGui.QApplication.translate("MainWindow", self.algorithm_types[i], None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), QtGui.QApplication.translate("MainWindow", "Algorithms", None, QtGui.QApplication.UnicodeUTF8))
        
        # Menus
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
