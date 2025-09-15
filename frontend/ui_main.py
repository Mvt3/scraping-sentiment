# imports
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFrame,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal



from backend.sentiment import analyze_sentiment
from backend.scraper import get_comments
from backend.functions_aux import simple_appreciation_score


class ScraperThread(QThread):
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    finished_with_score = pyqtSignal(float)

    def __init__(self, search_text):
        super().__init__()
        self.search_text = search_text

    #### ALL THE MAGIC HAPPENS HERE ####
    def run(self):
        try:
            self.progress.emit("Starting scraping...")

            comments = get_comments(
                "all", self.search_text, post_limit=4, comment_limit=55
            )

            results_df = analyze_sentiment(comments)

            summary = simple_appreciation_score(results_df)

            self.finished_with_score.emit(summary)

        except Exception as e:
            self.error.emit(str(e))


            # Optional: Export to CSV
            # export_to_csv(results_df, f"{self.search_text}_sentiment.csv")
            # self.progress.emit("Analysis complete and CSV saved!")

            # testing the function
            # print(f"Comentarios encontrados: {len(comments)}")
            # for c in comments[:10]:
            #     print("-", c[:200])  # print first 200 characters of each comment

        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentiment Analysis Scraper")
        self.setGeometry(1300, 600, 1500, 900)

        self.scraping_thread = None

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(60, 60, 60, 60)
        self.layout.setSpacing(30)

        # Top spacing
        self.layout.addStretch(1)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter your search term...")
        self.search_input.setMinimumHeight(80)
        self.search_input.setMaximumWidth(900)
        self.layout.addWidget(self.search_input, alignment=Qt.AlignCenter)

        # Analyze button
        self.analyze_button = QPushButton("Start Analysis")
        self.analyze_button.setMinimumHeight(65)
        self.analyze_button.setMaximumWidth(300)
        self.layout.addWidget(self.analyze_button, alignment=Qt.AlignCenter)

        self.analyze_button.clicked.connect(
            lambda: print(f"Analyzing: {self.search_input.text()}")
        )

        # Result container
        self.result_container = QFrame()
        self.result_container.setMaximumWidth(850)
        self.result_container.setMinimumHeight(350)
        self.layout.addWidget(self.result_container, alignment=Qt.AlignCenter)

        # Internal layout for container
        container_layout = QVBoxLayout(self.result_container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)

        # Container title
        title_label = QLabel("ANALYSIS RESULTS")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        container_layout.addWidget(title_label)

        # Percentage display
        self.sentiment_label = QLabel("Sentiment Percentage: Awaiting Analysis...")
        self.sentiment_label.setAlignment(Qt.AlignCenter)
        self.sentiment_label.setWordWrap(True)
        self.sentiment_label.setObjectName("result")
        container_layout.addWidget(self.sentiment_label)

        self.comments_display = QTextEdit()
        self.comments_display.setMaximumHeight(180)
        self.comments_display.setPlaceholderText("Results will be displayed here...")
        self.comments_display.setReadOnly(True)
        container_layout.addWidget(self.comments_display)

        # Bottom spacing to center everything
        self.layout.addStretch(1)

        # Apply styles
        self.apply_clean_styles()

        # Connect button to function
        self.analyze_button.clicked.connect(self.start_analysis)

    # Function to start analysis
    def start_analysis(self):
        search_text = self.search_input.text().strip()

        # Validation
        if not search_text:
            self.sentiment_label.setText("Please enter a valid search term.")
            return

        # Prevent multiple clicks
        if self.scraping_thread and self.scraping_thread.isRunning():
            self.sentiment_label.setText("Scraping is already in progress.")
            return

        # Update UI
        self.analyze_button.setText("Analyzing...")
        self.analyze_button.setEnabled(False)
        self.sentiment_label.setText("Starting analysis...")
        self.comments_display.clear()

        # Start scraping in a separate thread
        self.scraping_thread = ScraperThread(search_text)
        self.scraping_thread.start()

        # Update button when finished
        self.scraping_thread.finished.connect(self.restore_button)
        self.scraping_thread.finished_with_score.connect(self.update_score_display)

    def closeEvent(self, event):
        if self.scraping_thread and self.scraping_thread.isRunning():
            self.scraping_thread.terminate()
            self.scraping_thread.wait()
        event.accept()

    def update_score_display(self, score):
        self.comments_display.setHtml(
            f"""
            <div style="text-align:center; font-size:52px; font-weight:bold; color:#00ffff;">
                {score:.1f}%
            </div>
        """
        )

    def restore_button(self):
        self.analyze_button.setText("Start Analysis")
        self.analyze_button.setEnabled(True)
        self.sentiment_label.setText("Analysis complete!")

    # App styles
    def apply_clean_styles(self):
        stylesheet = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a1e, stop:0.5 #1a1a2e, stop:1 #2a2a3e);
                color: #ffffff;
            }
            
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12), 
                    stop:1 rgba(255, 255, 255, 0.06));
                border: 2px solid rgba(64, 224, 255, 0.5);
                border-radius: 18px;
                padding: 22px 35px;
                font-size: 24px;
                font-weight: 500;
                color: #ffffff;
                selection-background-color: #40e0ff;
            }
            
            QLineEdit:focus {
                border: 2px solid #40e0ff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(64, 224, 255, 0.18), 
                    stop:1 rgba(64, 224, 255, 0.08));
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:0.5 #8b5cf6, stop:1 #a855f7);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 20px 40px;
                font-size: 19px;
                font-weight: bold;
                color: #ffffff;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:0.5 #a855f7, stop:1 #c084fc);
                border: 2px solid #40e0ff;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5b21b6, stop:0.5 #7c2d12, stop:1 #9333ea);
            }
            
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #374151, stop:0.5 #4b5563, stop:1 #6b7280);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.06),
                    stop:0.5 rgba(255, 255, 255, 0.04),
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 2px solid rgba(64, 224, 255, 0.3);
                border-radius: 22px;
            }
            
            QFrame:hover {
                border: 2px solid rgba(64, 224, 255, 0.5);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:0.5 rgba(255, 255, 255, 0.06),
                    stop:1 rgba(255, 255, 255, 0.04));
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
                font-size: 20px;
                font-weight: 400;
            }
            
            QLabel[objectName="title"] {
                font-size: 28px;
                font-weight: bold;
                color: #40e0ff;
                margin-bottom: 10px;
            }
            
            QLabel[objectName="result"] {
                font-size: 22px;
                font-weight: 600;
                color: #ffffff;
                padding: 18px;
                background: rgba(64, 224, 255, 0.12);
                border-radius: 12px;
                border: 1px solid rgba(64, 224, 255, 0.3);
            }
            
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 0, 0, 0.3),
                    stop:1 rgba(0, 0, 0, 0.1));
                border: 2px solid rgba(64, 224, 255, 0.2);
                border-radius: 14px;
                padding: 15px;
                font-size: 16px;
                color: #ffffff;
                selection-background-color: #40e0ff;
            }
            
            QTextEdit:focus {
                border: 2px solid rgba(64, 224, 255, 0.4);
            }
        """

        self.setStyleSheet(stylesheet)
