from PyQt5 import QtWidgets
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

class SentimentAnalysis:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

        # Download the VADER lexicon if not already available
        nltk.download('vader_lexicon')

        # Initialize the sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def setup_ui(self):
        self.main_window.pushButton_7.clicked.connect(self.analyze_sentiment)

    def analyze_sentiment(self):
        review = self.main_window.textEdit_8.toPlainText()

        # Analyze sentiment
        sentiment = self.analyzer.polarity_scores(review)

        # Determine sentiment label
        if sentiment['compound'] >= 0.05:
            sentiment_label = "Positive"
        elif sentiment['compound'] <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        # Show result in a message box
        QtWidgets.QMessageBox.information(self.main_window, "Sentiment Analysis", f"The sentiment of the review is: {sentiment_label}")
