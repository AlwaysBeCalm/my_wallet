import datetime
import os
import sys
import re
from details import Details
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from sqlalchemy import *

path_folder = os.path.join(os.path.dirname(__file__), '../.venv/lib/python3.7/site-packages')
if not os.path.exists(path_folder):
    sys.path.append(path_folder)
    app = QApplication(sys.argv)
    done = QMessageBox()
    done.setIcon(QMessageBox.Critical)
    done.setText('Error must run the script run.sh first')
    done.setWindowTitle('Error')
    done.exec_()
    sys.exit(0)
else:
    design, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/main_page.ui'))


    class Main(QMainWindow, design):
        def __init__(self):
            super(Main, self).__init__()
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.connect_to_db()
            self.init_ui()
            self.check()
            self.handle_buttons()

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

        def init_ui(self):
            # changes at the load of the app
            self.setWindowTitle('my_wallet')
            self.date.setDisplayFormat('dd/MM/yyyy')
            self.date.setCalendarPopup(True)
            self.date.setDate(datetime.date.today())
            self.date.setMaximumDate(datetime.date.today())  # set maximum date in the calendar is today's date
            self.amount.textChanged.connect(self.check)
            self.amount.setFocus(True)

        def handle_buttons(self):
            self.get.clicked.connect(self.add_got)
            self.spend.clicked.connect(self.add_spent)
            self.details.clicked.connect(self.go_to_details)

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
            conn = self.engine.connect()
            conn.execute(self.ins)
            self.show_msg()
            self.amount.setText('')
            self.reason.setText('')

        # go to details page
        def go_to_details(self):
            self.window().hide()
            self.dt = Details()
            self.dt.show()

        # a dialog box after inserting some data
        def show_msg(self):
            done = QMessageBox()
            done.setIcon(QMessageBox.Information)
            done.setText('Data inserted successfully')
            done.setWindowTitle('Info')
            # add another button to go to details page
            done.exec_()

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
            meta.create_all(self.engine)


    def main():
        app = QApplication(sys.argv)
        window = Main()
        window.show()
        app.exec_()


    if __name__ == '__main__':
        main()
