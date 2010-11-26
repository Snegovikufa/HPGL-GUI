from PyQt4 import QtGui, QtCore

class Statistics(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.ValuesGB = QtGui.QGroupBox()
        self.ValuesGBLayout = QtGui.QGridLayout(self.ValuesGB)
        
        self.MeanLabel = QtGui.QLabel(self.ValuesGB)
        self.VarianceLabel = QtGui.QLabel(self.ValuesGB)
        self.MaxLabel = QtGui.QLabel(self.ValuesGB)
        self.MinLabel = QtGui.QLabel(self.ValuesGB)
        self.MedianLabel = QtGui.QLabel(self.ValuesGB)
        self.PointsLabel = QtGui.QLabel(self.ValuesGB)
        
        self.MeanField = QtGui.QLineEdit(self.ValuesGB)
        self.MeanField.setReadOnly(1)
        self.VarianceField = QtGui.QLineEdit(self.ValuesGB)
        self.VarianceField.setReadOnly(1)
        self.MaxField = QtGui.QLineEdit(self.ValuesGB)
        self.MaxField.setReadOnly(1)
        self.MinField = QtGui.QLineEdit(self.ValuesGB)
        self.MinField.setReadOnly(1)
        self.MedianField = QtGui.QLineEdit(self.ValuesGB)
        self.MedianField.setReadOnly(1)
        self.PointsField = QtGui.QLineEdit(self.ValuesGB)
        self.PointsField.setReadOnly(1)
        
        self.ValuesSpacer = QtGui.QSpacerItem(40, 20, 
                                              QtGui.QSizePolicy.Expanding, 
                                              QtGui.QSizePolicy.Minimum)
        
        self.ValuesWidgets = [self.MeanLabel, self.MeanField,
                              self.VarianceLabel, self.VarianceField,
                              self.MaxLabel, self.MaxField,
                              self.MinLabel, self.MinField,
                              self.MedianLabel, self.MedianField,
                              self.PointsLabel, self.PointsField,
                              self.ValuesSpacer
                              ]
        self.ValuesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                    [1, 1, 1, 1], [1, 2, 1, 1],
                                    [2, 1, 1, 1], [2, 2, 1, 1],
                                    [3, 1, 1, 1], [3, 2, 1, 1],
                                    [4, 1, 1, 1], [4, 2, 1, 1],
                                    [5, 1, 1, 1], [5, 2, 1, 1],
                                    [0, 0, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.ValuesGBLayout, self.ValuesWidgets, 
                                  self.ValuesWidgetsPlaces)
        
        self.ViewConfigGB = QtGui.QGroupBox()
        self.ViewConfigGBLayout = QtGui.QGridLayout(self.ViewConfigGB)
        
        self.RowCountLabel = QtGui.QLabel(self.ViewConfigGB)
        self.RowCount = QtGui.QSpinBox(self.ViewConfigGB)
        self.ViewConfigWidgets = [self.RowCountLabel,
                                  self.RowCount]
        self.ViewConfigWidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.ViewConfigGBLayout, 
                                  self.ViewConfigWidgets,
                                  self.ViewConfigWidgetsPlaces)
        
        self.GraphView = QtGui.QGraphicsView()
        
        self.WindowWidgets = [self.ViewConfigGB,
                              self.GraphView,
                              self.ValuesGB]
        self.WindowWidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1],
                                    [1, 1, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.WindowWidgets, 
                                  self.WindowWidgetsPlaces)
        
        self.RetranslateUI(self)
                
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.ValuesSpacer):
                layout.addItem(widgets[i], places[i][0], places[i][1], 
                               places[i][2], places[i][3])
            else:
                layout.addWidget(widgets[i], places[i][0], places[i][1], 
                                 places[i][2], places[i][3])
                
    def RetranslateUI(self, MainWindow):
        self.MeanLabel.setText(self.__tr('Mean:'))
        self.VarianceLabel.setText(self.__tr('Variance:'))
        self.MaxLabel.setText(self.__tr('Max:'))
        self.MinLabel.setText(self.__tr('Min:'))
        self.MedianLabel.setText(self.__tr('Median:'))
        self.PointsLabel.setText(self.__tr('Number of points:'))
        self.RowCountLabel.setText(self.__tr('Row count:'))
        
        self.ValuesGB.setTitle(self.__tr('Values:'))
        self.ViewConfigGB.setTitle(self.__tr('Rows:'))
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
                