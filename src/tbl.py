from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random


class Splash(QWidget):
    def __init__(self):
        super().__init__()
        # self.min_date.setEnabled(False)
        # self.max_date.setEnabled(False)
        # self.all.setEnabled(False)
        # self.spent.setEnabled(False)
        # self.got.setEnabled(False)
        # self.data_table.setEnabled(False)
        # self.details.setEnabled(False)
        # CREATE THE TABLE
        self.table = QTableView(self)  # SELECTING THE VIEW
        self.table.setGeometry(0, 0, 575, 575)
        self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.table.setModel(self.model)  # SETTING THE MODEL
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.populate()

        self.table.clicked.connect(self.on_click)

    def on_click(self, tbl):
        # this function is giving you the ability to get the currents row's data
        # and every cell data
        row = tbl.row()  # RETRIEVES ROW OF CELL THAT WAS DOUBLE CLICKED
        column = tbl.column()  # RETRIEVES COLUMN OF CELL THAT WAS DOUBLE CLICKED
        cell_dict = self.model.itemData(tbl)  # RETURNS DICT VALUE OF SIGNAL
        cell_value = cell_dict.get(0)  # RETRIEVE VALUE FROM DICT

        index = tbl.sibling(row, 0)
        index_dict = self.model.itemData(index)
        index_value = index_dict.get(0)
        print(
            'Row {}, Column {} clicked - value: {}\nColumn 1 contents: {}'.format(row, column, cell_value, index_value)
        )

    def populate(self):
        # GENERATE A 4x10 GRID OF RANDOM NUMBERS.
        # VALUES WILL CONTAIN A LIST OF INT.
        # MODEL ONLY ACCEPTS STRINGS - MUST CONVERT.
        values = []
        for i in range(10):
            sub_values = []
            for i in range(4):
                value = random.randrange(1, 100)
                sub_values.append(value)
            values.append(sub_values)

        for value in values:
            row = []
            for item in value:
                cell = QStandardItem(str(item))
                row.append(cell)
            self.model.appendRow(row)

        # self.table.hideColumn(0)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = Splash()
    sys.exit(app.exec_())
# import sys
# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot
#
#
# class App(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 table - pythonspot.com'
#         self.left = 1750
#         self.top = 500
#         self.width = 300
#         self.height = 200
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.createTable()
#
#         # Add box layout, add table to box layout and add box layout to widget
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.tableWidget)
#         self.setLayout(self.layout)
#
#         # Show widget
#         self.show()
#
#     def createTable(self):
#         # Create table
#         self.tableWidget = QTableWidget()
#         self.tableWidget.setRowCount(4)
#         self.tableWidget.setColumnCount(2)
#         self.tableWidget.hideColumn(1)
#         self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
#         self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
#         self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
#         self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
#         self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
#         self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
#         self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
#         self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
#         self.tableWidget.move(0, 0)
#
#         # table selection change
#         self.tableWidget.doubleClicked.connect(self.on_click)
#
#     @pyqtSlot()
#     def on_click(self):
#         print("\n")
#         for currentQTableWidgetItem in self.tableWidget.selectedItems():
#             row = currentQTableWidgetItem.row()
#             self.tableWidget.selectRow(row)
#             print(row)
#             print(str(self.tableWidget.selectedItems().__str__()))
#             print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())
