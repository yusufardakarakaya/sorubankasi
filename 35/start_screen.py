from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Soru Bankası")
        self.title_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.add_btn = QPushButton("Yeni Soru Ekle")
        self.select_btn = QPushButton("Soru Seç")

        layout.addWidget(self.title_label)
        layout.addSpacing(30)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.select_btn)

        self.setLayout(layout)