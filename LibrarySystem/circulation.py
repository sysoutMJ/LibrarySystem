from PyQt5 import QtWidgets, QtCore
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import os

# Download necessary NLTK data
nltk.download('vader_lexicon', quiet=True)

class Circulation:
    def __init__(self, main_window, borrowers_management):
        self.main_window = main_window
        self.borrowers_management = borrowers_management
        self.json_file = self.borrowers_management.json_file
        self.setup_ui()
        self.load_borrowers_data()

    def setup_ui(self):
        self.main_window.pushButton_9.clicked.connect(self.return_book)
        self.main_window.tableWidget_5.setHorizontalHeaderLabels(["Borrower Name", "Book Name"])
        
        self.main_window.textEdit_review = QtWidgets.QTextEdit(self.main_window.centralwidget)
        self.main_window.textEdit_review.setGeometry(QtCore.QRect(20, 400, 300, 100))
        self.main_window.textEdit_review.setPlaceholderText("Enter book review here")
        
        self.main_window.label_sentiment = QtWidgets.QLabel(self.main_window.centralwidget)
        self.main_window.label_sentiment.setGeometry(QtCore.QRect(20, 510, 300, 30))
        self.main_window.label_sentiment.setText("Sentiment: ")

        self.main_window.label_return_status = QtWidgets.QLabel(self.main_window.centralwidget)
        self.main_window.label_return_status.setGeometry(QtCore.QRect(20, 550, 300, 30))
        self.main_window.label_return_status.setText("Return Status: ")

    def load_borrowers_data(self):
        self.main_window.tableWidget_5.setRowCount(0)
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            for row, item in enumerate(data):
                self.main_window.tableWidget_5.insertRow(row)
                self.main_window.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(item['borrower_name']))
                self.main_window.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(item['book_name']))
        else:
            QtWidgets.QMessageBox.warning(self.main_window, "Warning", "Borrowers data file not found!")

    def return_book(self):
        borrower_name = self.main_window.textEdit_11.toPlainText()
        row_count = self.main_window.tableWidget_5.rowCount()
        book_returned = False
        
        for row in range(row_count):
            item = self.main_window.tableWidget_5.item(row, 0)
            if item and item.text() == borrower_name:
                book_name = self.main_window.tableWidget_5.item(row, 1).text()
                self.main_window.tableWidget_5.removeRow(row)
                book_returned = True
                
                review = self.main_window.textEdit_review.toPlainText()
                sentiment = self.analyze_sentiment(review)
                self.main_window.label_sentiment.setText(f"Sentiment: {sentiment}")
                
                self.update_book_inventory(book_name)
                self.main_window.label_return_status.setText(f"Return Status: Book '{book_name}' returned successfully")
                self.update_borrowers_management(borrower_name)
                self.save_borrowers_data()
                break
        
        if not book_returned:
            self.main_window.label_return_status.setText("Return Status: No book found for this borrower")

    def analyze_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        
        if compound_score >= 0.05:
            return "Positive"
        elif compound_score <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def update_book_inventory(self, book_name):
        # Update book inventory logic goes here
        pass

    def update_borrowers_management(self, borrower_name):
        self.borrowers_management.load_borrowers_data()  # Reload data from JSON
        row_count = self.borrowers_management.main_window.tableWidget_4.rowCount()
        for row in range(row_count):
            item = self.borrowers_management.main_window.tableWidget_4.item(row, 0)
            if item and item.text() == borrower_name:
                self.borrowers_management.main_window.tableWidget_4.removeRow(row)
                break

    def save_borrowers_data(self):
        data = []
        for row in range(self.main_window.tableWidget_5.rowCount()):
            borrower_name = self.main_window.tableWidget_5.item(row, 0).text()
            book_name = self.main_window.tableWidget_5.item(row, 1).text()
            data.append({"borrower_name": borrower_name, "book_name": book_name})

        with open(self.json_file, 'w') as f:
            json.dump(data, f)

        QtWidgets.QMessageBox.information(self.main_window, "Save", "Borrowers data updated successfully!")
        self.borrowers_management.load_borrowers_data()  # Reload data in BorrowersManagement