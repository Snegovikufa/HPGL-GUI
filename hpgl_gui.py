#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(600, 400)
        self.setWindowTitle('HPGL GUI')
        
        centralwidget = QWidget()
        
        self.setCentralWidget(centralwidget)
        
        exit = QAction('Exit', self)
#exit = setShortcut('Ctrl+Q')
#        exit = setStatusTip('Exit Application')
        self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)
        
        tabWidget = QTabWidget(centralwidget)
        tab1 = QWidget(tabWidget)
        tabWidget.addTab(tab1, "Load cube")
        tab2 = QWidget(tabWidget)
        tabWidget.addTab(tab2, "Variogramm")
        tab3 = QWidget(tabWidget)
        tabWidget.addTab(tab3, "Simple Kriging")

        # TAB1 "Load cube"
        tab1_vbox = QVBoxLayout(tab1)
        
        grid_size_label = QLabel("Grid Size:")
        grid_size_x_label = QLabel("x:")
        grid_size_y_label = QLabel("y:")
        grid_size_z_label = QLabel("z:")
        grid_size_x = QLineEdit("0")
        grid_size_y = QLineEdit("0")
        grid_size_z = QLineEdit("0")
        
        grid_size_hbox = QHBoxLayout()
        grid_size_hbox.addWidget(grid_size_x_label)
        grid_size_hbox.addWidget(grid_size_x)
        grid_size_hbox.addWidget(grid_size_y_label)
        grid_size_hbox.addWidget(grid_size_y)
        grid_size_hbox.addWidget(grid_size_z_label)
        grid_size_hbox.addWidget(grid_size_z)
        
        tab1_vbox.addWidget(grid_size_label)
        tab1_vbox.addLayout(grid_size_hbox)
        
        cube_choose_btn = QPushButton("Choose cube:")
        cube_choose_label = QLabel()
        
        cube_choose_hbox = QHBoxLayout()
        cube_choose_hbox.addWidget(cube_choose_btn)
        cube_choose_hbox.addWidget(cube_choose_label)
        tab1_vbox.addLayout(cube_choose_hbox)
        
        indicator_checkbox = QCheckBox("Indicator values")
        indicator_spinbox = QSpinBox()
        
        indicator_hbox = QHBoxLayout()
        indicator_hbox.addWidget(indicator_checkbox)
        indicator_hbox.addWidget(indicator_spinbox)
        tab1_vbox.addLayout(indicator_hbox)

        undef_value_label = QLabel("Undefined value:")
        undef_value = QLineEdit()
        undef_value.setText("-99")
        
        undef_value_hbox = QHBoxLayout()
        undef_value_hbox.addWidget(undef_value_label)
        undef_value_hbox.addWidget(undef_value)
        
        load_cube_btn = QPushButton("Process cube")
        tab1_vbox.addWidget(load_cube_btn)

        # TAB 2 "Variogramm type"
        tab2_vbox = QVBoxLayout(tab2)
        
        variogramm_type_label = QLabel("Variogramm type:")
        variogramm_type = QComboBox()
        variogramm_type_hbox = QHBoxLayout()
        variogramm_type_hbox.addWidget(variogramm_type_label)
        variogramm_type_hbox.addWidget(variogramm_type)
        
        tab2_vbox.addLayout(variogramm_type_hbox)
        
        ellipsoid_ranges_label = QLabel("Ellipsoid ranges")
        ellipsoid_ranges_0_label = QLabel("0")
        ellipsoid_ranges_0 = QLineEdit("0")
        ellipsoid_ranges_90_label = QLabel("90")
        ellipsoid_ranges_90 = QLineEdit("0")
        ellipsoid_ranges_v_label = QLabel("Vertical")
        ellipsoid_ranges_v = QLineEdit("0")
        ellipsoid_ranges_hbox = QHBoxLayout()
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_0_label)
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_0)
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_90_label)
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_90)
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_v_label)
        ellipsoid_ranges_hbox.addWidget(ellipsoid_ranges_v)

        tab2_vbox.addWidget(ellipsoid_ranges_label)
        tab2_vbox.addLayout(ellipsoid_ranges_hbox)
        
        ellipsoid_angles_label = QLabel("Ellipsoide Angles")
        ellipsoid_angles_x_label = QLabel("x:")
        ellipsoid_angles_x = QLineEdit("0")
        ellipsoid_angles_y_label = QLabel("y:")
        ellipsoid_angles_y = QLineEdit("0")
        ellipsoid_angles_z_label = QLabel("z:")
        ellipsoid_angles_z = QLineEdit("0")
        
        ellipsoid_angles_hbox = QHBoxLayout()
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_x_label)
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_x)
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_y_label)
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_y)
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_z_label)
        ellipsoid_angles_hbox.addWidget(ellipsoid_angles_z)
        
        tab2_vbox.addWidget(ellipsoid_angles_label)
        tab2_vbox.addLayout(ellipsoid_angles_hbox)
        
        sill_value_label = QLabel("Sill value:")
        sill_value = QLineEdit("1.0")
        sill_value_hbox = QHBoxLayout()
        sill_value_hbox.addWidget(sill_value_label)
        sill_value_hbox.addWidget(sill_value)
        
        nugget_effect_label = QLabel("Nugget-effect value:")
        nugget_effect = QLineEdit("0.0")
        nugget_effect_hbox = QHBoxLayout()
        nugget_effect_hbox.addWidget(nugget_effect_label)
        nugget_effect_hbox.addWidget(nugget_effect)
        
        tab2_vbox.addLayout(sill_value_hbox)
        tab2_vbox.addLayout(nugget_effect_hbox)
        
        # TAB3 "Simple kriging
        tab3_vbox = QVBoxLayout(tab3)
        
        search_ellipsoid_label = QLabel("Search ellipsoid radiuses")
        search_ellipsoid_x_label = QLabel("x:")
        search_ellipsoid_x = QLineEdit("0")
        search_ellipsoid_y_label = QLabel("y:")
        search_ellipsoid_y = QLineEdit("0")
        search_ellipsoid_z_label = QLabel("z:")
        search_ellipsoid_z = QLineEdit("0")
        search_ellipsoid_hbox = QHBoxLayout()
        search_ellipsoid_hbox.addWidget(search_ellipsoid_x_label)
        search_ellipsoid_hbox.addWidget(search_ellipsoid_x)
        search_ellipsoid_hbox.addWidget(search_ellipsoid_y_label)
        search_ellipsoid_hbox.addWidget(search_ellipsoid_y)
        search_ellipsoid_hbox.addWidget(search_ellipsoid_z_label)
        search_ellipsoid_hbox.addWidget(search_ellipsoid_z)
        
        tab3_vbox.addWidget(search_ellipsoid_label)
        tab3_vbox.addLayout(search_ellipsoid_hbox)
        
        inter_points_label = QLabel("Maximum interpolation points")
        inter_points = QLineEdit("0")
        inter_point_hbox = QHBoxLayout()
        inter_point_hbox.addWidget(inter_points_label)
        inter_point_hbox.addWidget(inter_points)
        
        tab3_vbox.addLayout(inter_point_hbox)
        
        mean_value_label = QLabel("Mean value:")
        mean_value = QLineEdit("0")
        mean_value_hbox = QHBoxLayout()
        mean_value_hbox.addWidget(mean_value_label)
        mean_value_hbox.addWidget(mean_value)
        
        tab3_vbox.addLayout(mean_value_hbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()