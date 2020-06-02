import datetime
import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import *
from sqlalchemy import *

design, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/details_page.ui'))


class Details(QMainWindow, design):
    def __init__(self):
        super(Details, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect_to_db()
        self.init_ui()
        self.handle_radio_buttons()
        self.handle_buttons()

    def init_ui(self):
        self.setWindowTitle('details')
        self.all.setChecked(True)
        self.show_all()
        self.edit.setVisible(False)
        self.back.setVisible(False)

    def handle_radio_buttons(self):
        self.all.toggled.connect(self.show_all)
        self.got.toggled.connect(self.show_got)
        self.spent.toggled.connect(self.show_spent)

    def handle_buttons(self):
        self.back.clicked.connect(self.back_to_main)
        self.edit.clicked.connect(self.edit_row_data)

    def back_to_main(self):
        pass

    def edit_row_data(self):
        pass

    def show_got(self):
        self.data_table.clearContents()
        if self.got.isChecked():
            get = select([self.GOT.c.GOT, self.GOT.c.DATE, self.GOT.c.DETAILS])
            res = self.conn.execute(get).fetchall()
            for row, row_data in enumerate(res):
                for col, col_data in enumerate(row_data):
                    row_pos = self.data_table.rowCount()
                    self.data_table.insertRow(row_pos)
                    self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
            self.data_table.setRowCount(len(res))

    def show_spent(self):
        self.data_table.clearContents()
        if self.spent.isChecked():
            spent = select([self.SPENT.c.SPENT, self.SPENT.c.DATE, self.SPENT.c.DETAILS])
            res = self.conn.execute(spent).fetchall()
            for row, row_data in enumerate(res):
                for col, col_data in enumerate(row_data):
                    row_pos = self.data_table.rowCount()
                    self.data_table.insertRow(row_pos)
                    self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
            self.data_table.setRowCount(len(res))

    def show_all(self):
        self.data_table.clearContents()
        if self.all.isChecked():
            all = union_all(select([-self.SPENT.c.SPENT, self.SPENT.c.DATE, self.SPENT.c.DETAILS]),
                            select([self.GOT.c.GOT, self.GOT.c.DATE, self.GOT.c.DETAILS]))
            res = self.conn.execute(all).fetchall()
            for row, row_data in enumerate(res):
                for col, col_data in enumerate(row_data):
                    row_pos = self.data_table.rowCount()
                    self.data_table.insertRow(row_pos)
                    self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
            self.data_table.setRowCount(len(res))

    def connect_to_db(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        database_dir = current_dir + '/../database'
        if not os.path.exists(database_dir):
            os.mkdir(database_dir)
            self.engine = create_engine('sqlite:///' + database_dir + '/finance.db')
        else:
            self.engine = create_engine('sqlite:///' + database_dir + '/finance.db', echo=True)
        self.conn = self.engine.connect()
        meta = MetaData()
        self.SPENT = Table(
            'SPENT', meta,
            Column('ID', Integer, primary_key=True,
                   nullable=False),
            Column('SPENT', Float, nullable=False),
            # default here is to set default value for date column
            Column('DATE', Date, nullable=False, default=datetime.date.today()),
            Column('DETAILS', String(255))
            # sqlite_autoincrement=True,  # to set autoincrement on the pk
        )
        self.GOT = Table(
            'GOT', meta,
            Column('ID', Integer, primary_key=True,
                   nullable=False, autoincrement="auto"),
            Column('GOT', Float, nullable=False),
            Column('DATE', Date, nullable=False, default=datetime.date.today()),
            Column('DETAILS', String(255)),
            # sqlite_autoincrement=True,
        )
        meta.create_all(self.engine)


def main():
    app = QApplication(sys.argv)
    window = Details()
    window.show()
    app.exec_()
