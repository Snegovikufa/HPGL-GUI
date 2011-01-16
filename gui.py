# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from geo_bsd.geo import write_property
from gui_widgets.cube_list import CubeItem
import gui_widgets.cont_alg_widget as CAW
import gui_widgets.ind_alg_widget as IAW
import gui_widgets.load_cube_widget as LCW
import gui_widgets.progressindicator as Progress
import gui_widgets.statistics_window as SW

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.resize(800, 400)
        
        self.iterator = 0 # iterator for cubes' names
        
        self.initWidgets()
        self.initSignals()
        self.retranslateUI(self)
        
        self.cubesCont = []
        self.cubesInd = []
        self.contCubes = CubeItem()
        self.indCubes = CubeItem()

    def initSignals(self):
        # Signals and slots
        self.connect(self.tree, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.contextMenu)
        self.connect(self.tree, QtCore.SIGNAL('collapsed(const QModelIndex &)'), self.resizeColumn)
        self.connect(self.tree, QtCore.SIGNAL('expanded(const QModelIndex &)'), self.resizeColumn)
        self.connect(self.loadAction, QtCore.SIGNAL("triggered()"), self.loadCube)
        self.connect(self.deleteAction, QtCore.SIGNAL("triggered()"), self.deleteCube)
        self.connect(self.algorithmAction, QtCore.SIGNAL("triggered()"), self.applyAlgorithm)
        self.connect(self.statisticsAction, QtCore.SIGNAL("triggered()"), self.showStatistics)
        self.connect(self.saveAction, QtCore.SIGNAL("triggered()"), self.saveCube)
        self.connect(self.renderAction, QtCore.SIGNAL("triggered()"), self.renderCube)
        self.connect(self.newCubeAction, QtCore.SIGNAL("triggered()"), self.addNewCube)
        
        self.connect(self.loadCubesWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.catchCube)
        self.connect(self.loadCubesWidget, QtCore.SIGNAL("Loading(PyQt_PyObject)"), self.animateBusy)
        self.connect(self.contAlgWidget, QtCore.SIGNAL("progress(PyQt_PyObject)"), self.updateProgress)
        self.connect(self.contAlgWidget, QtCore.SIGNAL("algorithm(PyQt_PyObject)"), self.updateStatusBar)
        self.connect(self.contAlgWidget, QtCore.SIGNAL("finished(PyQt_PyObject)"), self.clearStatusBar)
        self.connect(self.indAlgWidget, QtCore.SIGNAL("progress(PyQt_PyObject)"), self.updateProgress)
        self.connect(self.indAlgWidget, QtCore.SIGNAL("algorithm(PyQt_PyObject)"), self.updateStatusBar)
        self.connect(self.indAlgWidget, QtCore.SIGNAL("finished(PyQt_PyObject)"), self.clearStatusBar)

    def initWidgets(self):
        # Buttons
        self.logButton = QtGui.QToolButton()
        self.stopAlgoButton = QtGui.QToolButton()
        self.stopAlgoButton.setDisabled(1)
        
        # Tree
        self.tree = QtGui.QTreeView()
        self.model = self.createModel(self)
        self.tree.setModel(self.model)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.resizeColumn()
        
        # 3D View
        self.view = QtGui.QGraphicsView()
        
        # Progress info
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setDisabled(1)
        self.algorithmText = QtGui.QLineEdit()
        self.busyWidget = QtGui.QWidget()
        self.busyIcon = Progress.QProgressIndicator(self.busyWidget)
        
        # Actions:
        #     Tree item actions
        self.deleteAction = QtGui.QAction(self.__tr("Delete"), self)
        self.statisticsAction = QtGui.QAction(self.__tr("Statistics"), self)
        self.algorithmAction = QtGui.QAction(self.__tr("Apply algorithm"), self)
        self.saveAction = QtGui.QAction(self.__tr("Save"), self)
        self.renderAction = QtGui.QAction(self.__tr("Render"), self)
        
        #     Tree branch actions
        self.newCubeAction = QtGui.QAction(self.__tr("New cube"), self)
        self.loadAction = QtGui.QAction(self.__tr("Load cube"), self)
        
        # Menu
        self.itemMenu = QtGui.QMenu(self)
        self.itemMenu.addAction(self.algorithmAction)
        self.itemMenu.addAction(self.statisticsAction)
        self.itemMenu.addAction(self.renderAction)
        self.itemMenu.addAction(self.saveAction)
        self.itemMenu.addAction(self.deleteAction)
        
        self.branchMenu = QtGui.QMenu(self)
        self.branchMenu.addAction(self.loadAction)
        self.branchMenu.addAction(self.newCubeAction)
        
        # Placing on form
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        
        leftWidget = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout(leftWidget)
        vbox.addWidget(self.tree)
        
        rightWidget = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout(rightWidget)
        vbox.addWidget(self.view)
        
        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.busyIcon)
        hbox.addWidget(self.algorithmText)
        hbox.addWidget(self.progressBar)
        hbox.addWidget(self.logButton)
        hbox.addWidget(self.stopAlgoButton)
        
        self.mainLayout.addWidget(splitter)
        self.mainLayout.addLayout(hbox)
        
        # Other widgets
        self.loadCubesWidget = LCW.LoadCube(self)
        self.contAlgWidget = CAW.ContAlgWidget(self.iterator)
        self.indAlgWidget = IAW.IndAlgWidget(self.iterator)

    def animateBusy(self, started=False):
        if started:
            self.busyIcon.startAnimation()
        else:
            self.busyIcon.stopAnimation()
            
    def updateProgress(self, percent):
        self.progressBar.setEnabled(1)
        self.progressBar.setValue(int(percent))
        
    def updateStatusBar(self, info):
        self.algorithmInfo = info
        
        self.algorithmText.setEnabled(1)
        self.stopAlgoButton.setEnabled(1)
        self.busyIcon.startAnimation()
        
        self.algorithmText.setText(info[0])
        self.connect(self.stopAlgoButton, QtCore.SIGNAL('clicked()'),
                     self.algorithmInfo[1].NewThread, QtCore.SLOT('quit()'))
        
    def clearStatusBar(self):
        self.algorithmText.clear()
        self.algorithmText.setDisabled(1)
        self.stopAlgoButton.setDisabled(1)
        self.progressBar.setDisabled(1)
        self.busyIcon.stopAnimation()
        
        self.disconnect(self.stopAlgoButton, QtCore.SIGNAL('clicked()'),
                        self.algorithmInfo[1].NewThread, QtCore.SLOT('terminate()'))
    
    def renderCube(self):
        from gui_widgets.visualisator import Visualisator
        index = self.tree.currentIndex()
        row = index.row()
        if index.parent().row() == 0:
            self.v = Visualisator(self.contCubes.allValues(row),
                                  self.contCubes.undefValue(row),
                                  self.contCubes.name(row))
        else:
            self.v = Visualisator(self.indCubes.allValues(row),
                                  self.indCubes.undefValue(row),
                                  self.indCubes.name(row))
        self.v.run()
        
    def placeWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])
            
    def loadCube(self):
        index = self.getIndex()
        self.loadCubesWidget.show()
        
        if index.row() == 0:
            self.loadCubesWidget.IndValuesCheckbox.setChecked(False)
        else:
            self.loadCubesWidget.IndValuesCheckbox.setChecked(True)
        
    def resizeColumn(self):
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
        
    def catchCube(self, cube):
        child = QtGui.QStandardItem(self.__tr(cube[4]))
        childSize = QtGui.QStandardItem(str(cube[5]))
        child.setEditable(0)
        childSize.setEditable(0)
        if cube[2] != None:
            childIndicators = QtGui.QStandardItem(str(len(cube[2])))
        else:
            childIndicators = QtGui.QStandardItem(str('-'))
        childIndicators.setEditable(0)
        list = [child, childSize, childIndicators]
        if cube[2] == None:
            # Remove this
            #------------------------------------------------------------------------------ 
            self.model.item(0, 0).appendRow(list)
            self.cubesCont.append(cube)
            #------------------------------------------------------------------------------ 
            self.contCubes.append(cube[0], cube[1], cube[2],
                                  cube[3], cube[4], cube[5])
        else:
            # Remove this
            #------------------------------------------------------------------------------ 
            self.model.item(1, 0).appendRow(list)
            self.cubesInd.append(cube)
            #------------------------------------------------------------------------------ 
            self.indCubes.append(cube[0], cube[1], cube[2],
                                 cube[3], cube[4], cube[5])
        self.resizeColumn()
        
    def addNewCube(self):
        child = QtGui.QStandardItem('Test')
        child_size = QtGui.QStandardItem('Test')
        child_indicators = QtGui.QStandardItem('Test')
        list = [child, child_size, child_indicators]
        self.model.item(0, 0).appendRow(list)
    
    def contextMenu(self, point):
        index = self.tree.indexAt(point)
        if self.isIndexCont(index) or self.isIndexInd(index):
            self.itemMenu.exec_(self.tree.mapToGlobal(point))
        else:
            self.branchMenu.exec_(self.tree.mapToGlobal(point))
            
    def isIndexCont(self, index):
        if index.parent().row() != 0:
            return False
        
        return True
        
    def isIndexInd(self, index):
        if index.parent().row() != 1:
            return False
        
        return True
    
    def getIndex(self):
        return self.tree.currentIndex()
    
    def getRow(self):
        return self.tree.currentIndex().row()
    
    def deleteCube(self):
        index = self.getIndex()
        row = self.getRow()
        self.model.removeRow(row, index.parent())
        
        if self.isIndexCont(index):
            del(self.cubesCont[row])
        else:
            del(self.cubesInd[row])
            
    def saveCube(self):
        index = self.getIndex()
        row = self.getRow()
        
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as ...')
        if fname and self.isIndexCont(index):
            write_property(self.cubesCont[row][0], str(fname), 'Output',
                           self.cubesCont[row][1], self.cubesCont[row][2])
        elif fname and self.isIndexInd(index):
            write_property(self.cubesInd[row][0], str(fname), 'Output',
                           self.cubesInd[row][1], self.cubesInd[row][2])
            #write_property(self.contCubes.property(row), str(fname), 'Output', undefined_value, indicator_values)
    
    def createModel(self, parent=None):
        model = QtGui.QStandardItemModel(2, 2, parent)
    
        contBranch = QtGui.QStandardItem("Continuous cubes")
        contBranch.setEditable(0)
        indBranch = QtGui.QStandardItem("Indicator cubes")
        indBranch.setEditable(0)
        model.setItem(0, 0, contBranch)
        model.setItem(1, 0, indBranch)
                    
        model.setHorizontalHeaderItem(0, QtGui.QStandardItem("Cube"))
        model.setHorizontalHeaderItem(1, QtGui.QStandardItem("Size"))
        model.setHorizontalHeaderItem(2, QtGui.QStandardItem("Indicators"))
        return model
    
    def applyAlgorithm(self):
        index = self.getIndex()
        
        if self.isIndexCont(index):
            self.contAlgWidget.push(self.cubesCont, index.row())
            self.connect(self.contAlgWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"),
                         self.catchCube)
        else:
            self.indAlgWidget.push(self.cubesInd, index.row())
            self.connect(self.indAlgWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"),
                         self.catchCube)
        self.iterator += 1

    def showStatistics(self):
        index = self.getIndex()
        row = self.getRow()
        
        if self.isIndexCont(index):
            self.statWindow = SW.Statistics(self.contCubes.definedValues(row),
                                            self.contCubes.undefValue(row),
                                            self.contCubes.name(row))
        else:
            self.statWindow = SW.Statistics(self.indCubes.definedValues(row),
                                            self.indCubes.undefValue(row),
                                            self.indCubes.name(row))
        self.statWindow.show()
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
    
    def retranslateUI(self, MainWindow):
        self.setWindowTitle(self.__tr('HPGL GUI'))
        self.logButton.setText(self.__tr("Log"))
        self.stopAlgoButton.setText(self.__tr('X'))
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv).instance()
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
