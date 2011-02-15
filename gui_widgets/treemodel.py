#from PyQt4 import QtGui, QtCore
#from cube_list import CubeItem, RootItem
#
#class TreeModel(QtGui.QStandardItemModel):
#    def __init__(self, rows, columns, contCubes, indCubes, parent = None):
#        super(TreeModel, self).__init__(rows, columns, parent)
#        self.contCubes = contCubes
#        self.indCubes = indCubes
#        
##        self.rootItem = CubeItem()
#        
#    def flags(self, index):       
#        if index.parent() == QtCore.QModelIndex():
#            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
#        
#        if index.column() == 1 or index.column() == 2:
#            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
#        
#        
#        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
#    
#    def setData(self, index, value, role=QtCore.Qt.EditRole):
#        if role != QtCore.Qt.EditRole:
#            return False
#        variant = value
#        if index.column() == 0:
#            value = str(value.toString())
#
#            if index.row() == 0:
#                self.contCubes.setName(value, index.row())
#            if index.row() == 1: #index.parent.row()==1
#                self.indCubes.setName(value, index.row())
#
#            result = True
#
#        if index.column() == 3:
#            value = int(value)
#            
#            if index.row() == 0:
#                self.contCubes.changeUndefValue(value, index.row())
#            if index.row() == 1:
#                self.indCubes.changeUndefValue(value, index.row())
#
#            result = True
#            
#        if result:
#            self.dataChanged.emit(index, index)
#        return result



from PyQt4 import QtCore, QtGui

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.insert(position, None)

        for child in self.childItems:
            child.insertColumns(position, columns)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.pop(position)

        for child in self.childItems:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, headers, contCubes, indCubes, parent=None):
        super(TreeModel, self).__init__(parent)
        
        self.contCubes = contCubes
        self.indCubes = indCubes

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
#        self.setupModelData(data.split("\n"), self.rootItem)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DecorationRole:
            if self.getItem(index).parent() == self.rootItem:
                if index.column() == 0:
                    if index.row() == 0:
                        pixmap = QtGui.QPixmap()
                        pixmap.load('icons/cont.png')
                        
                        pixmap = pixmap.scaled(22, 22, aspectRatioMode=QtCore.Qt.KeepAspectRatio, 
                                               transformMode=QtCore.Qt.SmoothTransformation)
                        return pixmap
                    if index.row() == 1:
                        pixmap = QtGui.QPixmap()
                        pixmap.load('icons/ind.png')
                        
                        pixmap = pixmap.scaled(22, 22, aspectRatioMode=QtCore.Qt.KeepAspectRatio, 
                                               transformMode=QtCore.Qt.SmoothTransformation)
                        return pixmap
        
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            return item.data(index.column())
        return None

    def flags(self, index):
        parentItem = self.getItem(index).parent()
        
        if parentItem == self.rootItem:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        if index.column() == 1 or index.column() == 2:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        
        print index.row(), index.column()
        
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        try:
            result = item.setData(index.column(), value)
            
            if index.column() == 0:
                value = str(value.toString())
                
                if index.parent().row() == 0:
                    self.contCubes.setName(value, index.row())
                if index.parent().row() == 1:
                    self.indCubes.setName(value, index.row())
                
                result = True

            if index.column() == 3:
                value = int(value)
                print 'Yeap, i am here, value=', value
                
                if index.parent().row() == 0:
                    self.contCubes.changeUndefValue(value, index.row())
                if index.parent().row() == 1:
                    self.indCubes.changeUndefValue(value, index.row())
                    
                result = True
        except:
            result = False

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

#class MainWindow(QtGui.QWidget):
#    def __init__(self, parent = None):
#        QtGui.QWidget.__init__(self, parent)
#        
#        header = ['1', '2', '3']
#        model = TreeModel(header)
#        
#        self.tree = QtGui.QTreeView()
#        self.tree.setModel(model)
#        
#        vbox = QtGui.QVBoxLayout()
#        self.setLayout(vbox)
#        vbox.addWidget(self.tree)
#        
#        self.insertRow(['1', '2', '3'])
#        self.insertRow(['4', '5', '6'])
#        
#        index = model.index(0, 0)
#        print model.data(index, QtCore.Qt.DisplayRole)
#        self.insertChild(['5', '15', '25'], index)
#        
#    def insertChild(self, data, index = None):
#        if index == None:
#            index = self.tree.selectionModel().currentIndex()
#        model = self.tree.model()
#        
#        if not model.insertRow(0, index):
#            return
#        
#        for column in range(model.columnCount(index)):
#            child = model.index(0, column, index)
#            model.setData(child, data[column], QtCore.Qt.EditRole)
#    
#    def insertRow(self, data, index = None):
#        if index == None:
#            index = self.tree.selectionModel().currentIndex()
#        model = self.tree.model()
#        
#        if not model.insertRow(index.row()+1, index.parent()):
#            return
#        
#        for column in range(model.columnCount(index.parent())):
#            child = model.index(index.row()+1, column, index.parent())
#            model.setData(child, data[column], QtCore.Qt.EditRole)
#        
#if __name__ == "__main__":
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    gui = MainWindow()
#    gui.show()
#    sys.exit(app.exec_())
