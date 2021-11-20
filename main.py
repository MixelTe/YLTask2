import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sqlite3

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.display()

    def display(self):
        self.tableWidget: QTableWidget = self.tableWidget

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("select id, grade, roast, ground_or_beans, description, price, volume from coffee").fetchall()
        self.tableWidget.setRowCount(0)
        for y, row in enumerate(res):
            self.tableWidget.setRowCount(y + 1)
            for x, cell in enumerate(row):
                self.tableWidget.setItem(y, x, QTableWidgetItem(str(cell)))

        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())