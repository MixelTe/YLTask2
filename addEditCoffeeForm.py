from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import sqlite3


class EditDialog(QDialog):
    def __init__(self, parent, id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.id = id
        if (self.id is not None):
            self.display()
        self.btn_save.clicked.connect(self.save)

    def display(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("""select grade, roast, ground_or_beans, description, price, volume
                             from coffee where id = ?""", (self.id,)).fetchone()
        grade, roast, ground_or_beans, description, price, volume = res
        self.inp_grade.setText(grade)
        self.inp_roast.setText(roast)
        self.inp_ground_or_beans.setText(ground_or_beans)
        self.inp_description.setText(description)
        self.inp_price.setText(price)
        self.inp_volume.setText(volume)

    def save(self):
        if (self.id is None):
            self.save_insert()
        else:
            self.save_update()
        self.close()

    def save_update(self):
        grade = self.inp_grade.text()
        roast = self.inp_roast.text()
        ground_or_beans = self.inp_ground_or_beans.text()
        description = self.inp_description.text()
        price = self.inp_price.text()
        volume = self.inp_volume.text()

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute("""update coffee set
                       grade = ?,
                       roast = ?,
                       ground_or_beans = ?,
                       description = ?,
                       price = ?,
                       volume = ?
                       where id = ?""", (grade, roast, ground_or_beans, description, price, volume, self.id))
        con.commit()
        self.close()

    def save_insert(self):
        grade = self.inp_grade.text()
        roast = self.inp_roast.text()
        ground_or_beans = self.inp_ground_or_beans.text()
        description = self.inp_description.text()
        price = self.inp_price.text()
        volume = self.inp_volume.text()

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute("""insert into coffee(grade, roast, ground_or_beans, description, price, volume)
                       values (?, ?, ?, ?, ?, ?)
                       """, (grade, roast, ground_or_beans, description, price, volume))
        con.commit()
        self.close()
