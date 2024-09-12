from PyQt5 import QtWidgets, QtCore
import nltk
from nltk.metrics.distance import edit_distance
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import os

# Download necessary NLTK data
nltk.download('words', quiet=True)
nltk.download('vader_lexicon', quiet=True)

class BorrowersManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()
        self.borrower_names = set()  # Store unique borrower names
        self.json_file = 'borrowers_data.json'
        self.load_data()

    def setup_ui(self):
        self.main_window.pushButton_8.clicked.connect(self.add_borrower)
        self.main_window.tableWidget_4.setHorizontalHeaderLabels(["Borrower Name", "Book Name"])

        # Add a new label for name suggestions
        self.main_window.label_name_suggestion = QtWidgets.QLabel(self.main_window.centralwidget)
        self.main_window.label_name_suggestion.setGeometry(QtCore.QRect(20, 300, 300, 30))
        self.main_window.label_name_suggestion.setText("Name Suggestion: ")

        # Connect textChanged signal of borrower name field
        self.main_window.textEdit_9.textChanged.connect(self.suggest_similar_name)

        # Add a save button
        self.main_window.pushButton_save = QtWidgets.QPushButton(self.main_window.centralwidget)
        self.main_window.pushButton_save.setGeometry(QtCore.QRect(20, 340, 100, 30))
        self.main_window.pushButton_save.setText("Save Data")
        self.main_window.pushButton_save.clicked.connect(self.save_data)

    def add_borrower(self):
        borrower_name = self.main_window.textEdit_9.toPlainText()
        book_name = self.main_window.textEdit_10.toPlainText()
        row_position = self.main_window.tableWidget_4.rowCount()
        self.main_window.tableWidget_4.insertRow(row_position)
        self.main_window.tableWidget_4.setItem(row_position, 0, QtWidgets.QTableWidgetItem(borrower_name))
        self.main_window.tableWidget_4.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book_name))

        # Add the new borrower name to our set
        self.borrower_names.add(borrower_name)
        self.save_data()

    def suggest_similar_name(self):
        current_name = self.main_window.textEdit_9.toPlainText()
        if len(current_name) < 3:
            self.main_window.label_name_suggestion.setText("Name Suggestion: ")
            return

        similar_names = self.find_similar_names(current_name)
        if similar_names:
            suggestion = f"Did you mean: {', '.join(similar_names)}?"
            self.main_window.label_name_suggestion.setText(f"Name Suggestion: {suggestion}")
        else:
            self.main_window.label_name_suggestion.setText("Name Suggestion: No similar names found")

    def find_similar_names(self, name, max_distance=2):
        similar = []
        for existing_name in self.borrower_names:
            distance = edit_distance(name.lower(), existing_name.lower())
            if 0 < distance <= max_distance:
                similar.append(existing_name)
        return similar[:3]  # Return top 3 similar names

    def save_data(self):
        data = []
        for row in range(self.main_window.tableWidget_4.rowCount()):
            borrower_name = self.main_window.tableWidget_4.item(row, 0).text()
            book_name = self.main_window.tableWidget_4.item(row, 1).text()
            data.append({"borrower_name": borrower_name, "book_name": book_name})

        with open(self.json_file, 'w') as f:
            json.dump(data, f)

        QtWidgets.QMessageBox.information(self.main_window, "Save", "Data saved successfully!")

    def load_data(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                data = json.load(f)

            for item in data:
                borrower_name = item["borrower_name"]
                book_name = item["book_name"]
                row_position = self.main_window.tableWidget_4.rowCount()
                self.main_window.tableWidget_4.insertRow(row_position)
                self.main_window.tableWidget_4.setItem(row_position, 0, QtWidgets.QTableWidgetItem(borrower_name))
                self.main_window.tableWidget_4.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book_name))
                self.borrower_names.add(borrower_name)

class Circulation:
    def __init__(self, main_window, borrowers_management):
        self.main_window = main_window
        self.borrowers_management = borrowers_management
        self.setup_ui()

    def setup_ui(self):
        self.main_window.pushButton_9.clicked.connect(self.return_book)
        self.main_window.tableWidget_5.setHorizontalHeaderLabels(["Borrower Name", "Book Name"])
        
        # Add a new text edit for book review
        self.main_window.textEdit_review = QtWidgets.QTextEdit(self.main_window.centralwidget)
        self.main_window.textEdit_review.setGeometry(QtCore.QRect(20, 400, 300, 100))
        self.main_window.textEdit_review.setPlaceholderText("Enter book review here")
        
        # Add a label to display sentiment
        self.main_window.label_sentiment = QtWidgets.QLabel(self.main_window.centralwidget)
        self.main_window.label_sentiment.setGeometry(QtCore.QRect(20, 510, 300, 30))
        self.main_window.label_sentiment.setText("Sentiment: ")

        # Add a label to display return status
        self.main_window.label_return_status = QtWidgets.QLabel(self.main_window.centralwidget)
        self.main_window.label_return_status.setGeometry(QtCore.QRect(20, 550, 300, 30))
        self.main_window.label_return_status.setText("Return Status: ")

    def return_book(self):
        borrower_name = self.main_window.textEdit_11.toPlainText()
        row_count = self.borrowers_management.main_window.tableWidget_4.rowCount()
        book_returned = False
        
        for row in range(row_count):
            item = self.borrowers_management.main_window.tableWidget_4.item(row, 0)
            if item and item.text() == borrower_name:
                book_name = self.borrowers_management.main_window.tableWidget_4.item(row, 1).text()
                self.borrowers_management.main_window.tableWidget_4.removeRow(row)
                book_returned = True
                
                # Get the review and analyze sentiment
                review = self.main_window.textEdit_review.toPlainText()
                sentiment = self.analyze_sentiment(review)
                self.main_window.label_sentiment.setText(f"Sentiment: {sentiment}")
                
                # Update book inventory (assuming you have a method for this)
                self.update_book_inventory(book_name)
                
                # Display return status
                self.main_window.label_return_status.setText(f"Return Status: Book '{book_name}' returned successfully")
                
                # Remove the borrower from the set of borrower names
                self.borrowers_management.borrower_names.remove(borrower_name)
                
                # Save the updated data
                self.borrowers_management.save_data()
                
                # Here you could save the review and sentiment to a database
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
        # This method should update your book inventory
        # For example, increment the available count of the book
        # You'll need to implement this based on how you're storing book inventory
        pass

# Main application setup
class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.borrowers_management = BorrowersManagement(self)
        self.circulation = Circulation(self, self.borrowers_management)

    def setupUi(self):
        # Set up your main window UI here
        # This is where you'd create all the widgets (buttons, text edits, tables, etc.)
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApplication()
    main_window.show()
    sys.exit(app.exec_())