import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from start_screen import StartScreen
from question_entry_screen import QuestionEntryScreen
from question_selection_screen import QuestionSelectionScreen

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soru Bankası")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.start_screen = StartScreen()
        self.question_entry_screen = QuestionEntryScreen()
        self.question_selection_screen = QuestionSelectionScreen()

        self.stack.addWidget(self.start_screen)              # index 0
        self.stack.addWidget(self.question_entry_screen)     # index 1
        self.stack.addWidget(self.question_selection_screen) # index 2

        self.start_screen.add_btn.clicked.connect(self.goto_entry)
        self.start_screen.select_btn.clicked.connect(self.goto_select)

    def goto_entry(self):
        self.stack.setCurrentIndex(1)

    def goto_select(self):
        self.stack.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())