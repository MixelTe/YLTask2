import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
import sqlite3
from addEditCoffeeForm import EditDialog
from UI.main import Ui_MainWindow

class MainForm(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.action_add.triggered.connect(self.add)
        self.action_edit.triggered.connect(self.edit)
        self.display()

    def display(self):
        self.tableWidget: QTableWidget = self.tableWidget

        self.tableWidget.clearContents()
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("select id, grade, roast, ground_or_beans, description, price, volume from coffee").fetchall()
        self.tableWidget.setRowCount(0)
        for y, row in enumerate(res):
            self.tableWidget.setRowCount(y + 1)
            for x, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.tableWidget.setItem(y, x, item)

        self.tableWidget.resizeColumnsToContents()

    def add(self):
        dialog = EditDialog(self)
        dialog.exec()
        self.display()

    def edit(self):
        selected, r = self.getSelected(self.tableWidget)
        if (not r):
            return
        dialog = EditDialog(self, int(self.tableWidget.item(selected, 0).text()))
        dialog.exec()
        self.display()

    def getSelected(self, table: QTableWidget):
        selected = table.selectedIndexes()
        selectedI = -1
        for el in selected:
            row = el.row()
            if (selectedI == -1):
                selectedI = row
            elif (selectedI != row):
                QMessageBox.information(self, "", "Выделите элемент в таблице")
                return (-1, False)
        if (selectedI == -1):
            QMessageBox.information(self, "", "Выделите элемент в таблице")
            return (-1, False)
        return (selectedI, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.exit(app.exec_())