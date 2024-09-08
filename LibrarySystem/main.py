import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from book_management import BookManagement
from search_books import SearchBooks
from sentiment_analysis import SentimentAnalysis
from borrowers_management import BorrowersManagement
from circulation import Circulation

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LibrarySystem.ui", self)
        self.setWindowTitle("Library System")
        
        # Initialize and set up each tab
        self.book_management = BookManagement(self)
        self.search_books = SearchBooks(self)
        self.sentiment_analysis = SentimentAnalysis(self)
        self.borrowers_management = BorrowersManagement(self)
        self.circulation = Circulation(self)
        
        self.tabWidget.setTabText(0, "Book Entry and Management")
        self.tabWidget.setTabText(1, "Search Books")
        self.tabWidget.setTabText(2, "Sentiment Analysis for User Reviews")
        self.tabWidget.setTabText(3, "Borrowers Management")
        self.tabWidget.setTabText(4, "Circulation (Borrowing and Returning)")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
