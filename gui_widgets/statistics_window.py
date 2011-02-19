from PySide import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.path as path
import numpy

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, header, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.arrayData = datain
        self.headerData = header

    def rowCount(self, parent):
        return len(self.arrayData[0])

    def columnCount(self, parent):
        return len(self.arrayData)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(self.arrayData[index.column()][index.row()])

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerData[col])
        return QtCore.QVariant()

class Statistics(QtGui.QDialog):
    def __init__(self, cubes, index, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(840, 500)

        self.valuesArray = cubes.allValues(index)
        self.clearValues = cubes.definedValues(index)
        self.undefValue = cubes.undefValue(index)

        name = cubes.name(index)
        self.setWindowTitle(self.__tr("HPGL GUI: Statistics for: " + name))

        self.initWidgets()
        self.initSignals()
        self.retranslateUI(self)

        self.update()

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

        self.closeButtonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.closeButton = self.closeButtonBox.addButton(self.__tr("Close"),
                                                         QtGui.QDialogButtonBox.RejectRole)

        # Let's draw graph and calculate cube's values
        self.makeDefault()
        self.createHistogramFrame()

        # Catching Histogram window
        self.graphLayout.addWidget(self.canvas)
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
        self.connect(self.xMax, QtCore.SIGNAL('editingFinished()'),
                     self.update)
        self.connect(self.xMin, QtCore.SIGNAL('editingFinished()'),
                     self.update)
        self.connect(self.closeButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('close()'))

    def placeWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1],
                             places[i][2], places[i][3])

    def keyPressEvent(self, event):
        '''Reimplement of key press Enter'''
        if (event.type() == QtCore.QEvent.KeyPress
                and (event.key() == QtCore.Qt.Key_Enter
                    or event.key() == QtCore.Qt.Key_Return)):
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

    def createHistogramFrame(self):
        # First, set font size
        import matplotlib as mpl
        mpl.rcParams['font.size'] = 9

        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi,)
        self.canvas = FigureCanvas(self.fig)

        self.axes = self.fig.add_subplot(111)

    def initRanges(self):
        self.cutValues = self.clearValues
        self.globalMin = float(self.min)
        self.globalMax = float(self.max)

        self.xMin.setText(self.min)
        self.xMax.setText(self.max)

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
        #self.allPoints = numpy.size(self.cutValues)

    def asProbability(self):
        return self.probabilityChange.isChecked()

    def update(self):
        if self.validateRanges():
            self.makeCuts()
        else:
            self.makeDefault()

        self.updateTable()
        self.updateHistogram()

    def updateHistogram(self):
        self.axes.clear()
        n, bins = numpy.histogram(self.cutClearValues, self.rowCount.value())

        left = numpy.array(bins[:-1])
        right = numpy.array(bins[1:])
        bottom = numpy.zeros(len(left))

        if self.asProbability():
            top = (bottom + n) / int(self.defPoints)
            self.axes.set_ylabel(self.__tr("Probability"))
        else:
            top = bottom + n
            self.axes.set_ylabel(self.__tr("Number of cells"))

        XY = numpy.array([[left, left, right, right], [bottom, top, top, bottom]]).T
        barPath = path.Path.make_compound_path_from_polys(XY)
        patch = patches.PathPatch(barPath, facecolor='blue',
                                  edgecolor='gray', alpha=0.8)

        self.axes.add_patch(patch)

        # Limits
        self.axes.set_xlim(self.localMin, self.localMax)
        self.axes.set_ylim(bottom.min(), top.max())
        self.axes.grid(1)
        self.axes.set_xlabel(self.__tr('Value'))

        self.canvas.draw()

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

    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)

