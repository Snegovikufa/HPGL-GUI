# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from geo_bsd.geo import write_property
from geo_bsd.routines import write_gslib_property
from gui_widgets.cube_list import CubeItem
import sys
import icons_rc

try:
    from gui_widgets.visualisator import MayaviQWidget
    MAYAVI_INSTALLED = True
except:
    MAYAVI_INSTALLED = False

try:
    import enthought.chaco
    CHACO_INSTALLED = True
except:
    CHACO_INSTALLED = False

    _ = QtGui.QApplication(sys.argv)


import gui_widgets.cont_alg_widget as CAW
import gui_widgets.ind_alg_widget as IAW
import gui_widgets.load_cube_widget as LCW
import gui_widgets.progressindicator as Progress
import gui_widgets.statistics_window as SW
import gui_widgets.undef_widget as UW
import gui_widgets.create_cube_widget as CCW
import gui_widgets.logwindow as LW
from gui_widgets.treemodel import TreeModel
import numpy


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(4, 4, 0, 3)
        self.resize(950, 500)

        self.contCubes = CubeItem()
        self.indCubes = CubeItem()

        self.iterator = 0 # iterator for cubes' names
        self.log = ''

        self.initWidgets()
        self.initSignals()
        self.retranslateUI(self)
    
    def addNewCube(self):
        self.createCubeWidget.show()

        row = self.getRow()
        if row == 0:
            self.createCubeWidget.IndValuesCheckbox.setChecked(False)
        else:
            self.createCubeWidget.IndValuesCheckbox.setChecked(True)
            
    def animateBusy(self, started=False):
        if started:
            self.busyIcon.startAnimation()
        else:
            self.busyIcon.stopAnimation()

    def applyAlgorithm(self):
        index = self.getIndex()
        
        self.progressBar.setValue(0)

        if self.isIndexCont(index):
            self.contAlgWidget.push(self.contCubes, index.row(), self.indCubes)
        else:
            self.indAlgWidget.push(self.indCubes, index.row())

        self.iterator += 1
        
    def catchCube(self, cube):
        child = cube.name()
        childSize = str(cube.size())
        undef = str(cube.undefValue())

        if cube.isIndicator():
            childIndicators = str(cube.indicatorsCount(0))
        else:
            childIndicators = str('-')
        list = [child, childSize, childIndicators, undef]

        if not cube.isIndicator():
            self.insertChild(list, self.contCubes.count(), self.contBranchIndex)
            self.contCubes.appendItem(cube)
        else:
            self.insertChild(list, self.indCubes.count(), self.indBranchIndex)
            self.indCubes.appendItem(cube)

        self.resizeColumn()
        self.animateBusy()
        self.progressBar.setValue(0)

    def catchLog(self, text):
        self.log += text

    def changeUV(self):
        index = self.getIndex()
        row = self.getRow()
        if self.isIndexCont(index):
            self.changeUndefWidget = UW.UndefChangeWidget(self.contCubes, row)
        else:
            self.changeUndefWidget = UW.UndefChangeWidget(self.contCubes, row)
        self.changeUndefWidget.show()
        
    def clearStatusBar(self):
        self.algorithmText.clear()
        self.algorithmText.setDisabled(1)
        self.progressBar.setDisabled(1)
        self.busyIcon.stopAnimation()


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, self.__tr('Quit?'),
                                           self.__tr("Are you sure to quit?"), 
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                self.view.needQuit()
            except AttributeError:
                pass
            event.accept()
        else:
            event.ignore()
            
    def contextMenu(self, point):
        index = self.tree.indexAt(point)
        if self.isIndexCont(index) or self.isIndexInd(index):
            self.itemMenu.exec_(self.tree.mapToGlobal(point))
        else:
            self.branchMenu.exec_(self.tree.mapToGlobal(point))
            
    def createModel(self, parent=None):
        header = ['Cube', 'Size', 'Indicators', 'Undef. value']
        model = TreeModel(header, self.contCubes, self.indCubes, parent)
        
        return model
    

    def deleteCube(self):   
        index = self.getIndex()
        
        
        if self.isIndexCont(index):
            self.contCubes.deleteItem(index.row())
        else:
            self.indCubes.deleteItem(index.row())
            
        self.model.removeRow( index.row(), index.parent() )

    def getIndex(self):
        return self.tree.currentIndex()

    def getRow(self):
        return self.tree.currentIndex().row()

    def hasDefined(self, cubeType, row):
        if cubeType is 'cont':
            if not self.contCubes.hasDefined(row):
                message = QtGui.QMessageBox()
                message.warning(self, 'Warning',
                                'This cube doesn\'t have defined values, please select another')
                return False
            
            return True
        else:
            if not self.indCubes.hasDefined(row):
                message = QtGui.QMessageBox()
                message.warning(self, 'Warning',
                                'This cube doesn\'t have defined values, please select another')
                return False
                
            return True

    def initSignals(self):
        # Signals and slots
        self.tree.customContextMenuRequested.connect(self.contextMenu)
        self.tree.collapsed.connect(self.resizeColumn)
        self.tree.expanded.connect(self.resizeColumn)
        self.logButton.clicked.connect(self.showLog)
        self.loadAction.triggered.connect(self.loadCube)
        self.deleteAction.triggered.connect(self.deleteCube)
        self.algorithmAction.triggered.connect(self.applyAlgorithm)
        self.statisticsAction.triggered.connect(self.showStatistics)
        self.saveAction.triggered.connect(self.saveCube)
        self.renderAction.triggered.connect(self.renderCube)
        self.newCubeAction.triggered.connect(self.addNewCube)

        self.loadCubesWidget.cubeSignal.connect(self.catchCube)
        self.loadCubesWidget.loadingSignal.connect(self.animateBusy)
        self.loadCubesWidget.logMessage.connect(self.catchLog)
        
        self.createCubeWidget.cubeSignal.connect(self.catchCube)
        
        self.contAlgWidget.progressMessage.connect(self.updateProgress)
        self.contAlgWidget.algoInfo.connect(self.updateStatusBar)
        self.contAlgWidget.cubeSignal.connect(self.catchCube)
        self.contAlgWidget.finishedSignal.connect(self.clearStatusBar)
        self.contAlgWidget.logMessage.connect(self.catchLog)

        self.indAlgWidget.progressMessage.connect(self.updateProgress)
        self.indAlgWidget.algoInfo.connect(self.updateStatusBar)
        self.indAlgWidget.finishedSignal.connect(self.clearStatusBar)
        self.indAlgWidget.cubeSignal.connect(self.catchCube)
        self.indAlgWidget.logMessage.connect(self.catchLog)

    def initWidgets(self):
        # Buttons
        self.logButton = QtGui.QPushButton( QtGui.QIcon(":/icons/log.png"), self.__tr('Log') )

        # Tree
        self.tree = QtGui.QTreeView()
        self.model = self.createModel(self)
        self.tree.setModel(self.model)
        
        self.insertRow(['Indicator cubes', '', '', ''])
        self.insertRow(['Continuous cubes', '', '', ''])
        
        self.contBranchIndex = self.model.index(0, 0)
        self.indBranchIndex = self.model.index(1, 0)
        
        self.model.setData(self.contBranchIndex, QtGui.QIcon(':/icons/render.png'), QtCore.Qt.DecorationRole)
        self.model.setData(self.indBranchIndex, QtGui.QIcon(':/icons/render.png'), QtCore.Qt.DecorationRole)
        
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.resizeColumn()

        # 3D View
        if MAYAVI_INSTALLED:
            self.view = MayaviQWidget()
        else:
            self.view = QtGui.QWidget()
        

        # Progress info
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setDisabled(1)
        self.algorithmText = QtGui.QLineEdit()
        self.busyWidget = QtGui.QWidget()
        self.busyIcon = Progress.QProgressIndicator(self.busyWidget)
        
        # Actions:
        # ----Tree item actions
        self.deleteAction = QtGui.QAction(self.__tr("Delete"), self)
        self.statisticsAction = QtGui.QAction(self.__tr("Statistics"), self)
        self.algorithmAction = QtGui.QAction(self.__tr("Apply algorithm"), self)
        self.saveAction = QtGui.QAction(self.__tr("Save"), self)
        self.renderAction = QtGui.QAction(self.__tr("Render"), self)

        # ----Tree branch actions
        self.newCubeAction = QtGui.QAction(self.__tr("New cube"), self)
        self.loadAction = QtGui.QAction(self.__tr("Load cube"), self)
        
        # Icons:
        self.deleteAction.setIcon(QtGui.QIcon(':/icons/del.png'))
        self.statisticsAction.setIcon(QtGui.QIcon(':/icons/statistics.png'))
        self.renderAction.setIcon(QtGui.QIcon(':/icons/render.png'))
        self.saveAction.setIcon(QtGui.QIcon(':/icons/save.png'))
        self.newCubeAction.setIcon(QtGui.QIcon(':/icons/new.png'))
        self.loadAction.setIcon(QtGui.QIcon(':/icons/open.png'))
        self.algorithmAction.setIcon(QtGui.QIcon(':/icons/algorithm.png'))
        self.logButton.setIcon(QtGui.QIcon(':/icons/log.png'))
        self.setWindowIcon(QtGui.QIcon(':/icons/hpgl-gui.png'))

        # Toolbar
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addActions([self.newCubeAction, self.loadAction])

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
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.tree)
        vbox.setSpacing(2)

        rightWidget = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.setSpacing(0)
        rightWidget.setLayout(vbox)

        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)
        splitter.setContentsMargins(0, 0, 0, 0)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.busyIcon)
        hbox.addWidget(self.algorithmText)
        hbox.addWidget(self.progressBar)
        hbox.addWidget(self.logButton)
        hbox.setSpacing(2)
        hbox.setContentsMargins(4, 0, 4, 0)

        self.mainLayout.addWidget(splitter)
        self.mainLayout.addLayout(hbox)

        # Other widgets
        self.loadCubesWidget = LCW.LoadCube(self)
        self.contAlgWidget = CAW.ContAlgWidget(self.iterator, self)
        self.indAlgWidget = IAW.IndAlgWidget(self.iterator, self)
        self.createCubeWidget = CCW.CreateCube(self)
    
    
    def insertChild(self, data, position, index = None):

        model = self.tree.model()
        
        if not model.insertRow(position, index):
            return
        
        for column in range(model.columnCount(index)):
            child = model.index(position, column, index)
            model.setData(child, data[column], QtCore.Qt.EditRole)
    
    def insertRow(self, data, index = None):
        if index == None:
            index = self.tree.selectionModel().currentIndex()
        model = self.tree.model()
        
        if not model.insertRow(index.row()+1, index.parent()):
            return
        
        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, data[column], QtCore.Qt.EditRole)

    def isIndexCont(self, index):
        if index.parent().row() != 0:
            return False

        return True

    def isIndexInd(self, index):
        if index.parent().row() != 1:
            return False

        return True
    
    def loadCube(self):
        index = self.getIndex()
        self.loadCubesWidget.show()

        if index.row() == 0:
            self.loadCubesWidget.IndValuesCheckbox.setChecked(False)
        else:
            self.loadCubesWidget.IndValuesCheckbox.setChecked(True)
            
    def placeWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])
            
    def renderCube(self):
        index = self.tree.currentIndex()
        row = index.row()
        
        if not MAYAVI_INSTALLED:
            message = QtGui.QMessageBox()
            message.warning(self, 'Warning',
                            'You don\'t have Mayavi installed')
            return
        
        if self.isIndexCont(index) and self.hasDefined('cont', row):
            self.view.pushArgs(self.contCubes.allValues(row),
                               self.contCubes.undefValue(row))
                               
        if self.isIndexInd(index) and self.hasDefined('ind', row):
            self.view.pushArgs(self.indCubes.allValues(row),
                               self.indCubes.undefValue(row))

    def resizeColumn(self):
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
        
    def retranslateUI(self, MainWindow):
        self.setWindowTitle(self.__tr('HPGL GUI'))
        
    def saveCube(self):
        index = self.getIndex()
        row = self.getRow()
        
        eclipseFilter = "Eclipse (*.inc)"
        gslibFilter = "GSLIB (*.gslib)"
        numpyFilter = "Numpy (*.npy)"
        
        fileDialog = QtGui.QFileDialog()
        fileDialog.setNameFilters((
                                   eclipseFilter, 
                                   gslibFilter,
                                   numpyFilter
                                 ))
        fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        fileDialog.setFileMode(QtGui.QFileDialog.AnyFile)
        
        if fileDialog.exec_():
            filter = fileDialog.selectedNameFilter()
            fname = fileDialog.selectedFiles()[0]
        else:
            return
        #fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as ...')[0]
        
        if fname and self.isIndexCont(index):
            if filter == eclipseFilter:
                fname += '.inc'
                
                try:
                    write_property(self.contCubes.property(row), fname,
                                   self.contCubes.name(row), numpy.float32(self.contCubes.undefValue(row)),
                                   self.contCubes.indicators(row))
                    self.algorithmText.setText(self.__tr('Cube was saved'))
    
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))

            if filter == gslibFilter:
                fname += '.gslib'
                try:
                    write_gslib_property(self.contCubes.property(row), fname, 
                                         self.contCubes.name(row), numpy.float32(self.contCubes.undefValue(row))
                                        )
                    self.algorithmText.setText(self.__tr('Cube was saved'))
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))
            
            if filter == numpyFilter:
                try:
                    numpy.save(fname, self.contCubes.property(row))
                    self.algorithmText.setText(self.__tr('Cube was saved'))
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))

        elif fname and self.isIndexInd(index):
            if filter == eclipseFilter:
                fname += '.inc'
                
                try:
                    write_property(self.indCubes.property(row), fname,
                                   self.indCubes.name(row), numpy.float32(self.indCubes.undefValue(row)),
                                   list(self.indCubes.indicators(row)))
                    self.algorithmText.setText(self.__tr('Cube was saved'))
    
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))
            if filter == gslibFilter:
                fname += '.gslib'
                try:
                    write_gslib_property(self.indCubes.property(row), fname, 
                                         self.indCubes.name(row), numpy.float32(self.indCubes.undefValue(row)),
                                         list(self.indCubes.indicators(row))
                                        )
                    self.algorithmText.setText(self.__tr('Cube was saved'))
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))
            
            if filter == numpyFilter:
                try:
                    numpy.save(fname, self.indCubes.property(row))
                    self.algorithmText.setText(self.__tr('Cube was saved'))
                except:
                    self.algorithmText.setText(self.__tr('Error saving cube'))
                    

    def showLog(self):
        self.logWindow = LW.LogWindow(self)
        self.logWindow.showMessage('HPGL GUI LOG', self.log)
        #print self.log
            
    def showStatistics(self):

        index = self.getIndex()
        row = self.getRow()
        
        if not CHACO_INSTALLED:
            message = QtGui.QMessageBox()
            message.warning(self, 'Warning',
                            'You don\'t have Chaco installed')
            return

        if self.isIndexCont(index) and self.hasDefined('cont', row):
            self.statWindow = SW.Statistics(self.contCubes, row, self)
            self.statWindow.show()
            
        if self.isIndexInd(index) and self.hasDefined('ind', row):
            self.statWindow = SW.Statistics(self.indCubes, row, self)
            self.statWindow.show()
            
    def updateProgress(self, percent):
        self.progressBar.setEnabled(1)
        self.progressBar.setValue(int(percent))

    def updateStatusBar(self, info):    
        self.algorithmText.setEnabled(1)
        self.busyIcon.startAnimation()

        algType = info
        self.algorithmText.setText(algType)
        
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)


if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
