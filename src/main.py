import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Data():

    def __init__(self):
        self.read_schedule()

    def read_schedule(self):
        f = open('./txt/scd.txt','r',encoding='UTF-8')
        lines = f.readlines()
        self.scd = [line.rstrip('\n').split('/') for line in lines]
        f.close()


class Action():

    def __init__(self):
        pass

    def getExitAction(obj):
        exitAction = QAction(QIcon('./img/exit.png'), 'Exit', obj)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        return exitAction

class MyApp(QMainWindow):

    def __init__(self, data:Data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.set_UI()
        self.show()

    # UI
    def set_UI(self):
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.set_statusBar()
        self.set_menuBar()
        self.set_toolBar()
        self.set_daily_scd()
        self.setWindowTitle('Statusbar')
        self.center()
        self.resize(800,600)
    # set window center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # toolbar
    def set_toolBar(self):
        exitAction = Action.getExitAction(self)

        self.tool_exit = self.addToolBar('Exit')
        self.tool_exit.addAction(exitAction)

    # Status Bar
    def set_statusBar(self):
        self.statusBar().showMessage('Ready')

    # Menu Bar
    def set_menuBar(self):
        exitAction = Action.getExitAction(self)
        
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

    # daily schedule
    def set_daily_scd(self):
        self.tableWidget = self.daily_scd_table()

        hbox = QHBoxLayout()
        hbox.addWidget(self.tableWidget)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.wid.setLayout(vbox)

        
    # daily schedule table
    def daily_scd_table(self)->QTableWidget:
        scd = self.data.scd
        row = len(scd)
        col = len(scd[0])
        header = ['시작','종료','내용']

        tableWidget = QTableWidget(self)
        tableWidget.resize(400,300)
        tableWidget.setRowCount(row)
        tableWidget.setColumnCount(col)
        tableWidget.setHorizontalHeaderLabels(header)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        for i,row in enumerate(scd):
            for j,col in enumerate(row):
                item = QTableWidgetItem(scd[i][j])
                tableWidget.setItem(i,j,item)

        return tableWidget

if __name__ == '__main__':
    data = Data()
    app = QApplication(sys.argv)
    ex = MyApp(data)
    sys.exit(app.exec_())