from PyQt5 import QtWidgets

class BookManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        # Book Entry and Management Tab
        self.main_window.pushButton.clicked.connect(self.add_book)
        self.main_window.pushButton_2.clicked.connect(self.edit_book)
        self.main_window.pushButton_5.clicked.connect(self.delete_book)

        self.main_window.tableWidget.setHorizontalHeaderLabels(["Title", "Author", "Description"])

    def add_book(self):
        title = self.main_window.textEdit.toPlainText()
        author = self.main_window.textEdit_2.toPlainText()
        description = self.main_window.textEdit_3.toPlainText()
        row_position = self.main_window.tableWidget.rowCount()
        self.main_window.tableWidget.insertRow(row_position)
        self.main_window.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(title))
        self.main_window.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(author))
        self.main_window.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))

    def edit_book(self):
        selected_row = self.main_window.tableWidget.currentRow()
        if selected_row >= 0:
            self.main_window.tableWidget.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(self.main_window.textEdit.toPlainText()))
            self.main_window.tableWidget.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(self.main_window.textEdit_2.toPlainText()))
            self.main_window.tableWidget.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(self.main_window.textEdit_3.toPlainText()))

    def delete_book(self):
        selected_row = self.main_window.tableWidget.currentRow()
        if selected_row >= 0:
            self.main_window.tableWidget.removeRow(selected_row)
