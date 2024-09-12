import json
from PyQt5 import QtWidgets, QtGui, QtCore

class EditBookDialog(QtWidgets.QDialog):
    def __init__(self, parent, title, author, description):
        super().__init__(parent)
        self.setWindowTitle("Edit Book")
        self.setModal(True)
        self.setFixedSize(300, 200)

        self.layout = QtWidgets.QVBoxLayout()

        self.title_edit = QtWidgets.QLineEdit(title)
        self.author_edit = QtWidgets.QLineEdit(author)
        self.description_edit = QtWidgets.QTextEdit(description)

        self.layout.addWidget(QtWidgets.QLabel("Title:"))
        self.layout.addWidget(self.title_edit)
        self.layout.addWidget(QtWidgets.QLabel("Author:"))
        self.layout.addWidget(self.author_edit)
        self.layout.addWidget(QtWidgets.QLabel("Description:"))
        self.layout.addWidget(self.description_edit)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        return self.title_edit.text(), self.author_edit.text(), self.description_edit.toPlainText()


class BookManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.books = {}
        self.load_books()  # Load saved books on startup
        self.setup_ui()

    def setup_ui(self):
        # Book Entry and Management Tab
        self.main_window.pushButton.clicked.connect(self.add_book)
        self.main_window.pushButton_2.clicked.connect(self.show_edit_dialog)
        self.main_window.pushButton_5.clicked.connect(self.delete_book)

        self.main_window.tableWidget.setHorizontalHeaderLabels(["Title", "Author", "Description"])
        self.load_books_into_table()  # Load books into the table when the UI is set up

        # Make the table uneditable
        self.main_window.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_window.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def add_book(self):
        title = self.main_window.textEdit.toPlainText()
        author = self.main_window.textEdit_2.toPlainText()
        description = self.main_window.textEdit_3.toPlainText()

        # Add book to dictionary
        self.books[title] = {
            "author": author,
            "description": description
        }

        # Add book to table
        row_position = self.main_window.tableWidget.rowCount()
        self.main_window.tableWidget.insertRow(row_position)
        self.main_window.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(title))
        self.main_window.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(author))
        self.main_window.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))

        # Save the updated books dictionary to a file
        self.save_books()

        # Clear the textboxes
        self.main_window.textEdit.clear()
        self.main_window.textEdit_2.clear()
        self.main_window.textEdit_3.clear()

    def show_edit_dialog(self):
        selected_row = self.main_window.tableWidget.currentRow()
        if selected_row >= 0:
            title = self.main_window.tableWidget.item(selected_row, 0).text()
            author = self.main_window.tableWidget.item(selected_row, 1).text()
            description = self.main_window.tableWidget.item(selected_row, 2).text()

            dialog = EditBookDialog(self.main_window, title, author, description)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_title, new_author, new_description = dialog.get_data()
                
                # Update the dictionary
                self.books[new_title] = {
                    "author": new_author,
                    "description": new_description
                }

                # Remove the old entry if the title changed
                if title != new_title:
                    del self.books[title]

                # Update the table
                self.main_window.tableWidget.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(new_title))
                self.main_window.tableWidget.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(new_author))
                self.main_window.tableWidget.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(new_description))

                # Save the updated books dictionary to a file
                self.save_books()

    def delete_book(self):
        selected_row = self.main_window.tableWidget.currentRow()
        if selected_row >= 0:
            title = self.main_window.tableWidget.item(selected_row, 0).text()

            # Remove the book from the dictionary
            if title in self.books:
                del self.books[title]

            # Remove the book from the table
            self.main_window.tableWidget.removeRow(selected_row)

            # Save the updated books dictionary to a file
            self.save_books()

    def save_books(self):
        # Save books dictionary to a JSON file
        with open('books.json', 'w') as file:
            json.dump(self.books, file, indent=4)  # Added indent for better readability

    def load_books(self):
        # Load books from the JSON file if it exists
        try:
            with open('books.json', 'r') as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = {}

    def load_books_into_table(self):
        # Load books into the table from the dictionary
        for title, data in self.books.items():
            row_position = self.main_window.tableWidget.rowCount()
            self.main_window.tableWidget.insertRow(row_position)
            self.main_window.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(title))
            self.main_window.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data["author"]))
            self.main_window.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data["description"]))
