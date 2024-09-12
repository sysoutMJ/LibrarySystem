from PyQt5 import QtWidgets, QtCore
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

class SearchBooks:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()
        self.stop_words = set(stopwords.words('english'))

    def setup_ui(self):
        self.main_window.pushButton_6.clicked.connect(self.search_books)
        self.main_window.tableWidget_3.setHorizontalHeaderLabels(["Title", "Author", "Description"])

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalnum()]  # Remove punctuation
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return set(filtered_tokens)

    def search_books(self):
        search_text = self.main_window.textEdit_7.toPlainText().lower()
        search_keywords = self.preprocess_text(search_text)
        
        # Clear the previous search results
        self.main_window.tableWidget_3.setRowCount(0)
        
        # Iterate over the books in the main table (tableWidget)
        for row in range(self.main_window.tableWidget.rowCount()):
            title_item = self.main_window.tableWidget.item(row, 0)
            author_item = self.main_window.tableWidget.item(row, 1)
            description_item = self.main_window.tableWidget.item(row, 2)

            if title_item and author_item and description_item:
                # Extract keywords from the title, author, and description
                title_keywords = self.preprocess_text(title_item.text())
                author_keywords = self.preprocess_text(author_item.text())
                description_keywords = self.preprocess_text(description_item.text())
                
                # Check if search keywords match any of the keywords from title, author, or description
                if (search_keywords & title_keywords) or (search_keywords & author_keywords) or (search_keywords & description_keywords):
                    # Insert a new row in the search result table
                    self.main_window.tableWidget_3.insertRow(self.main_window.tableWidget_3.rowCount())
                    
                    # Copy data from the main table (tableWidget) to the search result table (tableWidget_3)
                    for col in range(3):
                        item = self.main_window.tableWidget.item(row, col)
                        if item:
                            new_item = QtWidgets.QTableWidgetItem(item.text())
                            new_item.setFlags(new_item.flags() & ~QtCore.Qt.ItemIsEditable)
                            self.main_window.tableWidget_3.setItem(self.main_window.tableWidget_3.rowCount() - 1, col, new_item)
