import datetime
import os
import sys
import re

from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
from PyQt5.uic import *
from sqlalchemy import *

design, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/ui.ui'))


# خانة السبب، خليها تتعبى وتظهر الاسباب اللي ادخلها الuser من قبل
# في صفحة الإحصائيات، اظهر المتوسط كل اسبوع وكل شهر، والمجموع كل اسبوع ومن بداية الشهر لليوم الحالي
class Main(QMainWindow, design):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('../ui/ui.ui')
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.check()
        self.handle_buttons()
        self.connect_to_db()

    def check(self):
        if re.match('^\d+[.\d]*$', self.amount.text()):
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
        self.amount.textChanged.connect(self.check)
        self.details.setFocus(True)

    def handle_buttons(self):
        self.get.clicked.connect(self.add_get)
        self.spend.clicked.connect(self.add_spend)
        self.details.clicked.connect(self.go_to_details)

    # add spend
    def add_spend(self):
        amount = self.amount.text()
        reason = self.reason.text()
        date = self.date.date()
        properDate = datetime.datetime(date.year(), date.month(), date.day())
        ins = self.SPEND.insert().values(SPEND=amount, DETAILS=reason, DATE=properDate)
        conn = self.engine.connect()
        conn.execute(ins)
        print('Date inserted successfully')
        self.amount.setText('')
        self.reason.setText('')

    # add get
    def add_get(self):
        amount = self.amount.text()
        reason = self.reason.text()
        date = self.date.date()
        properDate = datetime.datetime(date.year(), date.month(), date.day())
        ins = self.GET.insert().values(GET=amount, DETAILS=reason, DATE=properDate)
        conn = self.engine.connect()
        conn.execute(ins)
        print('Date inserted successfully')
        self.amount.setText('')
        self.reason.setText('')
        

    # go to details page
    def go_to_details(self):
        print('went to details page')

    def connect_to_db(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        database_dir = current_dir + '/../database'
        # if not os.path.exists(database_dir):
        #     os.mkdir(database_dir)
        #     engine = create_engine('sqlite:///' + database_dir + '/finance.db')
        # else:
        self.engine = create_engine('sqlite:///' + database_dir + '/finance.db')
        meta = MetaData()
        self.SPEND = Table(
            'SPEND', meta,
            Column('ID', Integer, primary_key=True,
                   nullable=False),
            Column('SPEND', Float, nullable=False),
            # default here is to set default value for date column
            Column('DATE', Date, nullable=False, default=datetime.date.today()),
            Column('DETAILS', String(255))
            # sqlite_autoincrement=True,  # to set autoincrement on the pk
        )
        self.GET = Table(
            'GET', meta,
            Column('ID', Integer, primary_key=True,
                   nullable=False, autoincrement="auto"),
            Column('GET', Float, nullable=False),
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
