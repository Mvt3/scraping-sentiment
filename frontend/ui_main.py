#imports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


font = QFont("Arial", 14)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentiment Analysis Scraper")
        self.setGeometry(1300,950, 1200, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
   

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setFont(font)
        self.search_input.setMaximumWidth(400)  
        self.layout.addWidget(self.search_input, alignment=Qt.AlignCenter) 

        # Analyze button 
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setFont(font)
        self.analyze_button.setMaximumWidth(200)  
        self.layout.addWidget(self.analyze_button, alignment=Qt.AlignCenter)  

        # Percentage display 
        self.sentiment_label = QLabel("Sentiment Percentage: N/A")
        self.sentiment_label.setAlignment(Qt.AlignCenter)
        self.sentiment_label.setFont(font)
        self.sentiment_label.setMaximumWidth(400) 
        self.layout.addWidget(self.sentiment_label, alignment=Qt.AlignCenter)  

      
    


        
