import sqlite3
import sys

from UI_main import Ui_MainWindow
from UI_addEditCoffeeForm import Ui_Form
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QApplication


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.PB_update.clicked.connect(self.select_data)
        self.PB_add.clicked.connect(self.add_data)
        self.PB_edit.clicked.connect(self.edit_data)

    def select_data(self):
        query = "SELECT * FROM coffee"
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def add_data(self):
        self.widget = Widget('Добавить', self.connection, None)
        self.widget.show()

    def edit_data(self):
        row = self.tableWidget.currentRow()
        # print(row)
        if row == -1:
            self.mbox = QMessageBox(self)
            self.mbox.setWindowTitle('Ошибка!')
            self.mbox.setText("Укажите строку, которую хотите изменить!")
            self.mbox.setIcon(QMessageBox.Warning)
            self.mbox.exec()
        else:
            information = [self.tableWidget.item(row, i).text() for i in range(1, 7)]
            # print(information)
            self.widget = Widget('Изменить', self.connection, row, information)
            self.widget.show()

    def closeEvent(self, event):
        self.connection.commit()


class Widget(QWidget, Ui_Form):
    def __init__(self, fx, connection, *args):
        super().__init__()
        # uic.loadUi('addEditCoffeeForm.ui', self)
        self.setupUi(self)
        self.connection = connection
        if fx == 'Добавить':
            self.PB_Ready.clicked.connect(self.add_data)
        if fx == 'Изменить':
            self.PB_Ready.clicked.connect(self.edit_data)
            self.row = args[0] + 1
            self.information = args[1]
            self.LE_Variety.setText(self.information[0])
            self.LE_Roast.setText(self.information[1])
            self.LE_Type.setText(self.information[2])
            self.LE_Taste.setText(self.information[3])
            self.LE_Price.setText(self.information[4])
            self.LE_Volume.setText(self.information[5])
        self.PB_Cancel.clicked.connect(self.close)
        self.setWindowTitle(fx)

    def add_data(self):
        query = f'''insert into coffee(Variety, Roast_Degree, Type, Taste, Price, Volume)
        values ('{self.LE_Variety.text()}','{self.LE_Roast.text()}','{self.LE_Type.text()}',
        '{self.LE_Taste.text()}','{self.LE_Price.text()}','{self.LE_Volume.text()}')'''
        self.connection.cursor().execute(query)
        self.close()

    def edit_data(self):
        query = f'''update coffee set (Variety, Roast_Degree, Type, Taste, Price, Volume) = 
        ('{self.LE_Variety.text()}','{self.LE_Roast.text()}','{self.LE_Type.text()}',
        '{self.LE_Taste.text()}','{self.LE_Price.text()}','{self.LE_Volume.text()}') 
        where id = {self.row}'''
        self.connection.cursor().execute(query)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
