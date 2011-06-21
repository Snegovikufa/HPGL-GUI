from PySide import QtGui, QtCore
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.patches as patches
#import matplotlib.path as path

from enthought.enable.api import Component, ComponentEditor
from enthought.chaco.api import ArrayDataSource, BarPlot, DataRange1D, \
                                LinearMapper, OverlayPlotContainer, PlotAxis, \
                                LabelAxis
from enthought.traits.ui.api import Item, Group, View
from enthought.chaco.example_support import COLOR_PALETTE
from enthought.traits.api import HasTraits, Instance
import numpy

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, header, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.arrayData = datain
        self.header = header

    def rowCount(self, parent):
        return len(self.arrayData[0])

    def columnCount(self, parent):
        return len(self.arrayData)

    def data(self, index, role):
        if not index.isValid():
            #return QtCore.QVariant()
            return None
        elif role != QtCore.Qt.DisplayRole:
            #return QtCore.QVariant()
            return None

        return self.arrayData[index.column()][index.row()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        #return QtCore.QVariant()
        return None

class Statistics(QtGui.QDialog):
    def __init__(self, cubes, index, parent=None):
        #QtGui.QWidget.__init__(self, parent)
        super(Statistics, self).__init__(parent)
        
        self.resize(800, 500)

        self.valuesArray = cubes.allValues(index)
        self.clearValues = cubes.definedValues(index)
        self.undefValue = cubes.undefValue(index)

        name = cubes.name(index)
        self.setWindowTitle(self.__tr("HPGL GUI: Statistics for: ") + name)

        self.initWidgets()
        self.initSignals()
        self.retranslateUI(self)

        self.updateValues()
    
    def asProbability(self):
        return self.probabilityChange.isChecked()
    
    def initWidgets(self):
        # Layouts, groupboxes
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setContentsMargins(6, 0, 6, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        # Values GroupBox
        self.valuesGB = QtGui.QGroupBox()
        self.valuesGBLayout = QtGui.QVBoxLayout(self.valuesGB)
        self.valuesGBLayout.setSpacing(0)

        self.valuesTable = QtGui.QTableView()
        self.valuesGBLayout.addWidget(self.valuesTable)

        # Histogram configuring widgets
        self.viewConfigGB = QtGui.QGroupBox()
        self.viewConfigGBLayout = QtGui.QGridLayout(self.viewConfigGB)
        self.viewConfigGBLayout.setSpacing(0)

        self.rowCountLabel = QtGui.QLabel(self.viewConfigGB)
        self.rowCount = QtGui.QSpinBox(self.viewConfigGB)
        self.rowCount.setValue(10)
        self.rowCount.setSingleStep(20)
        self.rowCount.setRange(10, 150)

        self.probabilityChange = QtGui.QCheckBox()
        #self.probabilityChange.setLayoutDirection(QtCore.Qt.RightToLeft)

        doubleValidator = QtGui.QDoubleValidator(self)
        self.xMin = QtGui.QLineEdit(self.viewConfigGB)
        self.xMin.setValidator(doubleValidator)
        self.xMinLabel = QtGui.QLabel(self.viewConfigGB)
        self.xMax = QtGui.QLineEdit(self.viewConfigGB)
        self.xMax.setValidator(doubleValidator)
        self.xMaxLabel = QtGui.QLabel(self.viewConfigGB)

        self.viewConfigWidgets = [self.rowCountLabel, self.rowCount,
                                  self.probabilityChange,
                                  self.xMinLabel, self.xMin,
                                  self.xMaxLabel, self.xMax, ]
        self.viewConfigWidgetsPlaces = [[0, 0, 1, 1],
                                        [0, 1, 1, 1],
                                        [1, 0, 1, 1],
                                        [2, 0, 1, 1], [2, 1, 1, 1],
                                        [3, 0, 1, 1], [3, 1, 1, 1],
                                        ]
        self.placeWidgetsAtPlaces(self.viewConfigGBLayout,
                                  self.viewConfigWidgets,
                                  self.viewConfigWidgetsPlaces)

        # Graphics
        self.graphWidget = QtGui.QWidget()
        self.graphWidget.setContentsMargins(0, 0, 0, 0)
        self.graphLayout = QtGui.QVBoxLayout(self.graphWidget)
        
        self.histWidget = HistQWidget(None, 5, True, range(0, 20))

        self.closeButtonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.closeButton = self.closeButtonBox.addButton(self.__tr("Close"),
                                                         QtGui.QDialogButtonBox.RejectRole)

        # Let's draw graph and calculate cube's values
        self.makeDefault()

        # Catching Histogram window
        self.graphLayout.addWidget(self.histWidget)
        self.graphLayout.addWidget(self.closeButtonBox)

        # Layouts
        leftVBox = QtGui.QVBoxLayout()
        leftVBox.addWidget(self.viewConfigGB)
        leftVBox.addWidget(self.valuesGB)
        leftVBox.addWidget(QtGui.QWidget())

        rightVBox = QtGui.QVBoxLayout()
        rightVBox.addWidget(self.graphWidget)

        self.mainLayout.addLayout(leftVBox)
        self.mainLayout.addLayout(rightVBox)
        self.mainLayout.setStretch(1, 1)

    def initSignals(self):
        self.connect(self.rowCount, QtCore.SIGNAL('valueChanged(int)'),
                     self.updateHistogram)
        self.connect(self.probabilityChange, QtCore.SIGNAL('stateChanged(int)'),
                     self.updateHistogram)
        self.xMax.editingFinished.connect(self.updateValues)
        self.xMin.editingFinished.connect(self.updateValues)
        self.connect(self.closeButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('close()'))

    def initRanges(self):
        self.cutValues = self.clearValues
        self.globalMin = float(self.min)
        self.globalMax = float(self.max)

        self.xMin.setText(self.min)
        self.xMax.setText(self.max)

    def keyPressEvent(self, event):
        '''Reimplement of key press Enter'''
        if (event.type() == QtCore.QEvent.KeyPress
                and (event.key() == QtCore.Qt.Key_Enter
                    or event.key() == QtCore.Qt.Key_Return)):
            self.updateHistogram()
            
    def makeCuts(self):
        self.localMin = float(self.xMin.text())
        self.localMax = float(self.xMax.text())

        self.cutValues = self.clearValues[numpy.nonzero(self.clearValues >= self.localMin)]
        self.cutValues = self.cutValues[numpy.nonzero(self.cutValues <= self.localMax)]
        self.cutClearValues = self.cutValues[numpy.nonzero(self.cutValues != self.undefValue)]

        self.max = '%.2f' % numpy.max(self.cutClearValues)
        self.mean = '%.2f' % numpy.mean(self.cutClearValues)
        self.min = '%.2f' % numpy.min(self.cutClearValues)
        self.median = '%.2f' % numpy.median(self.cutClearValues)
        self.variance = '%.2f' % numpy.var(self.cutClearValues)
        self.defPoints = numpy.size(self.cutClearValues)
        
    def makeDefault(self):
        self.globalMin = float('%.2f' % numpy.min(self.clearValues))
        self.globalMax = float('%.2f' % numpy.max(self.clearValues))
        self.localMin = self.globalMin
        self.localMax = self.globalMax

        self.cutValues = numpy.copy(self.valuesArray)
        self.cutClearValues = self.clearValues

        self.defPoints = numpy.size(self.clearValues)
        self.allPoints = numpy.size(self.valuesArray)
        self.max = '%.2f' % numpy.max(self.clearValues)
        self.mean = '%.2f' % numpy.mean(self.clearValues)
        self.min = '%.2f' % numpy.min(self.clearValues)
        self.median = '%.2f' % numpy.median(self.clearValues)
        self.variance = '%.2f' % numpy.var(self.clearValues)

        self.xMin.setText(str(self.localMin))
        self.xMax.setText(str(self.localMax))
        
    def retranslateUI(self, MainWindow):
        self.valuesGB.setTitle(self.__tr("Values"))
        self.viewConfigGB.setTitle(self.__tr("Histogram config"))

        self.rowCountLabel.setText(self.__tr('Row count'))
        self.probabilityChange.setText(self.__tr('Show as probability'))
        self.xMaxLabel.setText(self.__tr("X max"))
        self.xMinLabel.setText(self.__tr("X min"))

        # Blah-blah-blah like =)
        self.xMin.setText('1')
        self.xMax.setText('0')
           
    def placeWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1],
                             places[i][2], places[i][3])
            
    def updateValues(self):
        if self.validateRanges():
            self.makeCuts()
        else:
            self.makeDefault()

        self.updateTable()
        self.updateHistogram()
        
    def updateTable(self):
        '''Calculate statistic values and place them in table'''
        values = [['Max', 'Min', 'Mean', 'Median',
                  'Variance', 'Defined points', 'Total points'],
                  [self.max, self.min, self.mean, self.median,
                   self.variance, self.defPoints, self.allPoints]]
        header = ['Property', 'Value']

        self.tableModel = TableModel(values, header, self)
        self.valuesTable.setModel(self.tableModel)
        self.valuesTable.resizeColumnToContents(0)

        # Adding stretch to last header item
        header = self.valuesTable.horizontalHeader()
        header.setStretchLastSection(1)

    def updateHistogram(self):
#        if self.histWidget.push(self.cutClearValues, self.rowCount.value(), self.localMin, self.localMax):
#            self.histWidget.updatePlot()
        self.histWidget.updatePlot(self.rowCount.value(), True, self.cutClearValues)
        
    def validateRanges(self):
        xMin = float(self.xMin.text())
        xMax = float(self.xMax.text())

        if xMin < self.globalMin \
            or xMin > self.globalMax \
                or xMax < self.globalMin \
                    or  xMax > self.globalMax \
                        or xMin > xMax:
            return False

        return True

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)


class HistQWidget(QtGui.QWidget):    
    def __init__(self, parent, barsNum, normed, valuesArray):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        
        self.chacoHist = ChacoHistogram()
        self.chacoHist.setHistParams(barsNum, normed, valuesArray)
        
        # The edit_traits call will generate the widget to embed.
        self.ui = self.chacoHist.edit_traits(parent=self, 
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)
        
        self.currentMin = None
        self.currentMax = None
        
    def updatePlot(self, barsNum, normed, valuesArray):
        self.chacoHist.setHistParams(barsNum, normed, valuesArray)
        self.chacoHist.updatePlot()
        
    def updateCuts(self, min, max):
        if self.currentMax != max or self.currentMin != min: 
            
            self.currentMax = max
            self.currentMin = min
            
            self.chacoHist.updateCuts(min, max)
        
class ChacoHistogram(HasTraits):
    plot = Instance(Component)
    view = View(
                Group(
                      Item('plot', 
                           editor=ComponentEditor(size=(500, 500)), 
                           show_label=False),
                    orientation='vertical'),
                resizable=True,
                title='Statistics')
    
    def updateCuts(self, min, max):
        self.currentMin = min
        self.currentMax = max
        
    def setHistParams(self, binsNum, normed, valuesArray):
        self.normed = normed
        self.valuesArray = valuesArray
        self.binsNum = binsNum
        
        try:
            min = self.currentMin
            max = self.currentMax
            
            minCutValues = self.valuesArray[ numpy.nonzero(self.valuesArray >= self.currentMin)[0] ]
            minMaxCutValues = minCutValues[ numpy.nonzero(minCutValues <= self.currentMax)[0] ]
            
            self.valuesArray = minMaxCutValues
            
        except:
            pass
        
        pts = numpy.histogram(self.valuesArray, bins = binsNum, normed = self.normed)
        centerBinsCoords = [ (pts[1][num] + pts[1][num+1])/2.0 for num in range(len(pts[1])-1) ]
        
        self.value_points = pts[0]
        self.index_points = centerBinsCoords
        
        
    def _plot_default(self):
        
        container = OverlayPlotContainer(bgcolor = "white")
        
        
        self.idx = ArrayDataSource( range(1, self.binsNum+1) )
        self.vals = ArrayDataSource(self.value_points, sort_order="none")
        
        index_range = DataRange1D(self.idx, low=0, high=self.binsNum+2 )
        index_mapper = LinearMapper(range=index_range)
    
        value_range = DataRange1D(low=0, high=self.value_points.max())
        value_mapper = LinearMapper(range=value_range)
    
        # Create the plot
        self.histPlot = BarPlot(index=self.idx, value=self.vals,
                        value_mapper=value_mapper,
                        index_mapper=index_mapper,
                        line_color='black',
                        fill_color=tuple(COLOR_PALETTE[1]),
                        bar_width=0.8, antialias=False)
        
        plots = [self.histPlot]
        
        for plot in plots:
            plot.padding = 50
            plot.padding_left = 80
            plot.padding_top = 30
            container.add(plot)
    
        left_axis = PlotAxis(plot, orientation='left',
                               title='Number / Probability',
                               positions = [num for num in self.value_points],
                               labels = ["%.2f" % num for num in self.value_points],
                               #small_haxis_style=True
                               )

        bottom_axis = LabelAxis(plot, orientation='bottom',
                               title='Values',
                               positions = range(1, self.binsNum+1),
                               labels = ["%.2f" % num for num in self.index_points],
                               )
    
        plot.underlays.append(left_axis)
        plot.underlays.append(bottom_axis)
           
        return container
    
    def updatePlot(self):
        left_axis = PlotAxis(self.histPlot, orientation='left',
                               title='Number / Probability',
                               positions = [num for num in self.value_points],
                               labels = ["%.2f" % num for num in self.value_points])


        bottom_axis = LabelAxis(self.histPlot, orientation='bottom',
                               title='Values',
                               positions = range(1, self.binsNum+1),
                               labels = ["%.2f" % num for num in self.index_points])

        
        self.histPlot.underlays = [left_axis, bottom_axis]
#        
        self.idx = ArrayDataSource( range(1, self.binsNum+1) )
        self.vals = ArrayDataSource(self.value_points, sort_order="none")

        index_range = DataRange1D(self.idx, low=0, high=self.binsNum+2 )
        value_range = DataRange1D(low=0, high=self.value_points.max())

        self.histPlot.index.set_data( range(1, self.binsNum+1) )
        self.histPlot.value.set_data( self.value_points, sort_order="none" )

        self.histPlot.index_mapper.range = index_range
        self.histPlot.value_mapper.range = value_range

        self.histPlot.request_redraw()
