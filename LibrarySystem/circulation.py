from PyQt5 import QtWidgets

class Circulation:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.main_window.pushButton_9.clicked.connect(self.return_book)
        self.main_window.tableWidget_5.setHorizontalHeaderLabels(["Borrower Name", "Book Name"])

    def return_book(self):
        borrower_name = self.main_window.textEdit_11.toPlainText()
        row_count = self.main_window.tableWidget_5.rowCount()
        for row in range(row_count):
            item = self.main_window.tableWidget_5.item(row, 0)
            if item and item.text() == borrower_name:
                self.main_window.tableWidget_5.removeRow(row)
                break
