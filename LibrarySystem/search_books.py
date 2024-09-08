from PyQt5 import QtWidgets

class SearchBooks:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.main_window.pushButton_6.clicked.connect(self.search_books)
        self.main_window.tableWidget_3.setHorizontalHeaderLabels(["Title", "Author", "Description"])

    def search_books(self):
        search_text = self.main_window.textEdit_7.toPlainText().lower()
        for row in range(self.main_window.tableWidget.rowCount()):
            title_item = self.main_window.tableWidget.item(row, 0)
            if title_item and search_text in title_item.text().lower():
                self.main_window.tableWidget_3.insertRow(self.main_window.tableWidget_3.rowCount())
                for col in range(3):
                    item = self.main_window.tableWidget.item(row, col)
                    if item:
                        self.main_window.tableWidget_3.setItem(self.main_window.tableWidget_3.rowCount() - 1, col, QtWidgets.QTableWidgetItem(item.text()))
