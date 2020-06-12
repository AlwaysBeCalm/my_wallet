import datetime
import os
import sys
import re
import platform
import threading
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from sqlalchemy import *

if platform.system() in ['windows', 'Windows']:
    path_folder = os.path.join(os.path.dirname(__file__), '../.venv/Lib/site-packages')
else:
    path_folder = os.path.join(os.path.dirname(__file__), '../.venv/lib/python3.7/site-packages')
if not os.path.exists(path_folder):
    sys.path.append(path_folder)
    app = QApplication(sys.argv)
    done = QMessageBox()
    done.setIcon(QMessageBox.Critical)
    if platform.system() in ['windows', 'Windows']:
        done.setText('Error must run the script run.bat first')
    else:
        done.setText('Error must run the script run.sh first')
    done.setWindowTitle('Error')
    done.exec_()
    sys.exit(0)
else:
    ui, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/app.ui'))


    class Main(QMainWindow, ui):
        def __init__(self):
            super(Main, self).__init__()
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.connect_to_db()
            self.init_ui()
            self.check()
            self.handle_radio_buttons()
            self.handle_buttons()

        def init_ui(self):
            # changes at the load of the app
            self.setWindowTitle('my_wallet')
            self.tabWidget.setCurrentIndex(0)
            self.min_date.dateChanged.connect(self.byDate)
            self.max_date.dateChanged.connect(self.byDate)
            self.date.setDisplayFormat('yyyy-MM-dd')
            self.date.setCalendarPopup(True)
            self.date.setDate(datetime.date.today())
            self.date.setMaximumDate(datetime.date.today())  # set maximum date in the calendar is today's date
            self.min_date.setDisplayFormat('yyyy-MM-dd')
            self.min_date.setCalendarPopup(True)
            self.max_date.setDisplayFormat('yyyy-MM-dd')
            self.max_date.setCalendarPopup(True)
            self.amount.textChanged.connect(self.check)
            self.details.textChanged.connect(self.byDetail)
            self.amount.setFocus(True)
            self.tabWidget.tabBar().setVisible(False)
            self.statsBtn.setVisible(False)
            self.all.setChecked(True)
            self.editBtn.setVisible(False)
            self.deleteBtn.setVisible(False)
            table_header = self.data_table.horizontalHeader()
            table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            table_header.setSectionResizeMode(2, QHeaderView.Stretch)
            # this to prevent sorting table cols
            self.data_table.setSortingEnabled(False)
            # this trigger is to prevent editing table sells
            # self.data_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            all = select([text('* from "ALL" order by date desc')])
            res = self.conn.execute(all).fetchall()
            if res == []:
                self.viewBtn.setEnabled(False)
            else:
                self.viewBtn.setEnabled(True)
            threading.Thread(group=None, target=self.auto_fill(), args=(1,)).start()

        def check(self):
            if re.match('^\\d+[.\\d]*$', self.amount.text()):
                self.get.setEnabled(True)
                self.spend.setEnabled(True)
                self.reason.setPlaceholderText('reason')
            elif self.amount.text() == '':
                self.reason.setPlaceholderText('reason')
                self.get.setEnabled(False)
                self.spend.setEnabled(False)
            else:
                self.reason.setPlaceholderText('the amount field takes only numbers')
                self.get.setEnabled(False)
                self.spend.setEnabled(False)

        def handle_radio_buttons(self):
            self.all.toggled.connect(self.show_all)
            self.got.toggled.connect(self.show_got)
            self.spent.toggled.connect(self.show_spent)

        def handle_buttons(self):
            self.insertBtn.clicked.connect(self.open_insert_tab)
            self.viewBtn.clicked.connect(self.open_view_tab)
            self.statsBtn.clicked.connect(self.open_stats_tab)
            self.get.clicked.connect(self.add_got)
            self.spend.clicked.connect(self.add_spent)
            self.editBtn.clicked.connect(self.edit_row_data)

        # open insert data tab
        def open_insert_tab(self):
            self.date.setDate(datetime.date.today())
            self.tabWidget.setCurrentIndex(0)

        def auto_fill(self):
            reasons = union(select([self.SPENT.c.DETAILS]).distinct(),
                            select([self.GOT.c.DETAILS]).distinct())
            result = self.conn.execute(reasons).fetchall()
            reasons = {''}
            for val in result:
                reasons.add(list(val)[0])
            completer = QCompleter(reasons)
            self.reason.setCompleter(completer)

        # add spend
        def add_spent(self):
            self.add_to('spent')

        # add get
        def add_got(self):
            self.add_to('got')

        def add_to(self, table_name):
            amount = self.amount.text()
            reason = self.reason.text()
            date = self.date.date()
            proper_date = datetime.datetime(date.year(), date.month(), date.day())
            if table_name.lower() == 'spent':
                if reason == '':
                    self.ins = self.SPENT.insert().values(SPENT=amount, DETAILS='no details', DATE=proper_date)
                else:
                    self.ins = self.SPENT.insert().values(SPENT=amount, DETAILS=reason, DATE=proper_date)
            elif table_name.lower() == 'got':
                if reason == '':
                    self.ins = self.GOT.insert().values(GOT=amount, DETAILS='no details', DATE=proper_date)
                else:
                    self.ins = self.GOT.insert().values(GOT=amount, DETAILS=reason, DATE=proper_date)
            self.conn = self.engine.connect()
            self.conn.execute(self.ins)
            self.show_msg()
            self.amount.setText('')
            self.reason.setText('')
            self.viewBtn.setEnabled(True)
            threading.Thread(group=None, target=self.auto_fill(), args=(1,)).start()

        # a dialog box after inserting some data
        def show_msg(self):
            done = QMessageBox()
            done.setIcon(QMessageBox.Information)
            done.setText('Data inserted successfully')
            done.setWindowTitle('Info')
            # add another button to go to details page
            done.exec_()

        # open view data tab
        def open_view_tab(self):
            self.show_all()
            self.tabWidget.setCurrentIndex(1)

        def show_got(self):
            self.data_table.clearContents()
            if self.got.isChecked():
                self.data_table.horizontalHeaderItem(0).setText('got')
                try:
                    minDate = self.conn.execute(select([func.min(self.GOT.c.DATE)])).fetchone()[0]
                    self.min_date.clearMinimumDate()
                    self.min_date.setMinimumDate(minDate)
                    self.min_date.setDate(minDate)
                    # print(self.min_date.date().toPyDate())
                    maxDate = self.conn.execute(select([func.max(self.GOT.c.DATE)])).fetchone()[0]
                    self.max_date.clearMaximumDate()
                    self.max_date.setMaximumDate(maxDate)
                    self.max_date.setDate(maxDate)
                    # get = select([self.GOT.c.GOT, self.GOT.c.DATE, self.GOT.c.DETAILS]).order_by(desc(self.GOT.c.DATE))
                    get = select([self.GOT.c.GOT, self.GOT.c.DATE, self.GOT.c.DETAILS]).where(
                        and_(self.GOT.c.DETAILS.like('%' + self.details.text() + '%'),
                             between(self.GOT.c.DATE, self.min_date.date().toPyDate(),
                                     self.max_date.date().toPyDate()))).order_by(desc(self.GOT.c.DATE))
                    res = self.conn.execute(get).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            # use rowCount to get the number or rows in your current table
                            row_pos = self.data_table.rowCount()
                            # in pyqt before filling the table you must insert an empty row to the table
                            # then the table will be filled
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)

        def show_spent(self):
            self.data_table.clearContents()
            if self.spent.isChecked():
                self.data_table.horizontalHeaderItem(0).setText('spent')
                try:
                    minDate = self.conn.execute(select([func.min(self.SPENT.c.DATE)])).fetchone()[0]
                    self.min_date.clearMinimumDate()
                    self.min_date.setMinimumDate(minDate)
                    self.min_date.setDate(minDate)
                    maxDate = self.conn.execute(select([func.max(self.SPENT.c.DATE)])).fetchone()[0]
                    self.max_date.clearMaximumDate()
                    self.max_date.setMaximumDate(maxDate)
                    self.max_date.setDate(maxDate)
                    # spent = select([self.SPENT.c.SPENT, self.SPENT.c.DATE, self.SPENT.c.DETAILS]).order_by(
                    #     desc(self.SPENT.c.DATE))
                    spent = select([self.SPENT.c.SPENT, self.SPENT.c.DATE, self.SPENT.c.DETAILS]).where(
                        and_(self.SPENT.c.DETAILS.like('%' + self.details.text() + '%'),
                             between(self.SPENT.c.DATE, self.min_date.date().toPyDate(),
                                     self.max_date.date().toPyDate()))).order_by(desc(self.SPENT.c.DATE))
                    res = self.conn.execute(spent).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            row_pos = self.data_table.rowCount()
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)

        def show_all(self):
            self.data_table.clearContents()
            if self.all.isChecked():
                self.data_table.horizontalHeaderItem(0).setText('all')
                try:
                    minDate = str(list(self.conn.execute(select([text('min(date) from "all"')])).fetchone())[0]).split(
                        '-')
                    self.min_date.clearMinimumDate()
                    self.min_date.setDate(datetime.date(int(minDate[0]), int(minDate[1]), int(minDate[2])))
                    self.min_date.setMinimumDate(datetime.date(int(minDate[0]), int(minDate[1]), int(minDate[2])))
                    maxDate = str(list(self.conn.execute(select([text('max(date) from "all"')])).fetchone())[0]).split(
                        '-')
                    self.max_date.clearMaximumDate()
                    self.max_date.setDate(datetime.date(int(maxDate[0]), int(maxDate[1]), int(maxDate[2])))
                    self.max_date.setMaximumDate(datetime.date(int(maxDate[0]), int(maxDate[1]), int(maxDate[2])))
                    # all = select([text('* from "ALL" order by date desc')])
                    all = select([text(
                        "* from 'ALL' where details like '%" + self.details.text() + "%' and 'ALL'.'date' between '" + str(
                            self.min_date.date().toPyDate()) + "' and '" + str(
                            self.max_date.date().toPyDate()) + "' order by 'date' desc")])
                    res = self.conn.execute(all).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            row_pos = self.data_table.rowCount()
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)

        def errorMsg(self, e):
            errorMsg = QMessageBox()
            errorMsg.setIcon(QMessageBox.Critical)
            errorMsg.setText(e)
            errorMsg.setWindowTitle('Error')
            # add another button to go to details page
            errorMsg.exec_()

        def byDate(self):
            # this function will search in all the data between max and min date
            # select amount, date, details from "all" where date between min_date.date().toPyDate() and max_date.date().toPyDate()
            self.byDetail()
            pass

        def byDetail(self):
            self.data_table.clearContents()
            if self.got.isChecked():
                self.data_table.horizontalHeaderItem(0).setText('got')
                try:
                    get = select([self.GOT.c.GOT, self.GOT.c.DATE, self.GOT.c.DETAILS]).where(
                        and_(self.GOT.c.DETAILS.like('%' + self.details.text() + '%'),
                             between(self.GOT.c.DATE, self.min_date.date().toPyDate(),
                                     self.max_date.date().toPyDate()))).order_by(desc(self.GOT.c.DATE))
                    res = self.conn.execute(get).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            # use rowCount to get the number or rows in your current table
                            row_pos = self.data_table.rowCount()
                            # in pyqt before filling the table you must insert an empty row to the table
                            # then the table will be filled
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)
            elif self.all.isChecked():
                try:
                    all = select([text(
                        "* from 'ALL' where details like '%" + self.details.text() + "%' and 'ALL'.'date' between '" + str(
                            self.min_date.date().toPyDate()) + "' and '" + str(
                            self.max_date.date().toPyDate()) + "' order by 'date' desc")])
                    res = self.conn.execute(all).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            row_pos = self.data_table.rowCount()
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)
            elif self.spent.isChecked():
                self.data_table.horizontalHeaderItem(0).setText('spent')
                try:
                    spent = select([self.SPENT.c.SPENT, self.SPENT.c.DATE, self.SPENT.c.DETAILS]).where(
                        and_(self.SPENT.c.DETAILS.like('%' + self.details.text() + '%'),
                             between(self.SPENT.c.DATE, self.min_date.date().toPyDate(),
                                     self.max_date.date().toPyDate()))).order_by(desc(self.SPENT.c.DATE))
                    res = self.conn.execute(spent).fetchall()
                    for row, row_data in enumerate(res):
                        for col, col_data in enumerate(row_data):
                            # use rowCount to get the number or rows in your current table
                            row_pos = self.data_table.rowCount()
                            # in pyqt before filling the table you must insert an empty row to the table
                            # then the table will be filled
                            self.data_table.insertRow(row_pos)
                            self.data_table.setItem(row, col, QTableWidgetItem(str(col_data)))
                    self.data_table.setRowCount(len(res))
                except Exception as e:
                    self.errorMsg(e)

        def edit_row_data(self):
            pass

        def delete_row(self):
            pass

        # open stats tab
        def open_stats_tab(self):
            self.tabWidget.setCurrentIndex(2)

        def connect_to_db(self):
            current_dir = os.path.dirname(os.path.realpath(__file__))
            database_dir = current_dir + '/../database'
            if not os.path.exists(database_dir):
                os.mkdir(database_dir)
                self.engine = create_engine('sqlite:///' + database_dir + '/finance.db')
            else:
                self.engine = create_engine('sqlite:///' + database_dir + '/finance.db')
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
            self.engine.execute('''
            create view if not exists "ALL" (amount, date, details) as
                select * from (
                    select -spent, date, details from SPENT
                    union all
                    select got, date, details from got
                    ) order by date desc;
                      ''')
            meta.create_all(self.engine)
            self.conn = self.engine.connect()


    def main():
        app = QApplication(sys.argv)
        window = Main()
        window.show()
        app.exec_()


    if __name__ == '__main__':
        main()
