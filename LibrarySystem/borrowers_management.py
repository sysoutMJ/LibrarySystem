from PyQt5 import QtWidgets

class BorrowersManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.main_window.pushButton_8.clicked.connect(self.add_borrower)
        self.main_window.tableWidget_4.setHorizontalHeaderLabels(["Borrower Name", "Book Name"])

    def add_borrower(self):
        borrower_name = self.main_window.textEdit_9.toPlainText()
        book_name = self.main_window.textEdit_10.toPlainText()
        row_position = self.main_window.tableWidget_4.rowCount()
        self.main_window.tableWidget_4.insertRow(row_position)
        self.main_window.tableWidget_4.setItem(row_position, 0, QtWidgets.QTableWidgetItem(borrower_name))
        self.main_window.tableWidget_4.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book_name))
