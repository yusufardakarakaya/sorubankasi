from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QRadioButton,
    QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QButtonGroup, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
import pandas as pd

class QuestionEntryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 600)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sol panel
        left_panel = QVBoxLayout()

        question_label = QLabel("Soru")
        self.question_text = QTextEdit()
        self.question_text.setPlaceholderText("Soruyu buraya yazın...")

        answer_group = QGroupBox("Yanıtlar ve Doğru Şık")
        answer_layout = QVBoxLayout()
        self.radio_group = QButtonGroup()

        self.answer_inputs = []
        for i in range(5):
            h = QHBoxLayout()
            radio = QRadioButton(f"{i + 1}. Yanıt")
            self.radio_group.addButton(radio, i)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"{i + 1}. yanıtı buraya girin...")
            h.addWidget(radio)
            h.addWidget(line_edit)
            answer_layout.addLayout(h)
            self.answer_inputs.append(line_edit)

        answer_group.setLayout(answer_layout)

        # Butonlar
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Soru Bankasına Ekle")
        export_btn = QPushButton("Soru Bankasını Excel Olarak Kaydet")
        button_layout.addWidget(add_btn)
        button_layout.addWidget(export_btn)

        # Butona işlevsellik ekle
        add_btn.clicked.connect(self.add_question_to_table)
        export_btn.clicked.connect(self.save_to_excel)  # Excel kaydetme fonksiyonunu bağla

        # Sol paneli yerleştir
        left_panel.addWidget(question_label)
        left_panel.addWidget(self.question_text)
        left_panel.addWidget(answer_group)
        left_panel.addLayout(button_layout)

        # Sağ panel: Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([ 
            "Soru", "1. Seçenek", "2. Seçenek", "3. Seçenek", 
            "4. Seçenek", "5. Seçenek", "Cevap" 
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Ana yerleşim
        main_layout.addLayout(left_panel, 3)
        main_layout.addWidget(self.table, 5)

    def add_question_to_table(self):
        question = self.question_text.toPlainText().strip()
        answers = [input.text().strip() for input in self.answer_inputs]
        correct_answer_index = self.radio_group.checkedId()

        if not question or not any(answers):
            QMessageBox.warning(self, "Eksik Veri", "Lütfen tüm alanları doldurun.")
            return

        # Doğru cevabı seçin
        correct_answer = answers[correct_answer_index] if correct_answer_index != -1 else "Belirtilmemiş"

        # Tabloda yeni bir satır oluşturun
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(question))
        for i, ans in enumerate(answers):
            self.table.setItem(row_position, i + 1, QTableWidgetItem(ans))
        self.table.setItem(row_position, 6, QTableWidgetItem(correct_answer))

    def save_to_excel(self):
        data = []

        # Tablodaki verileri al
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # Eğer hücre boşsa, boş bir string ekle
            data.append(row_data)

        # Pandas DataFrame oluştur
        columns = ["Soru", "1. Seçenek", "2. Seçenek", "3. Seçenek", "4. Seçenek", "5. Seçenek", "Cevap"]
        df = pd.DataFrame(data, columns=columns)

        # Dosya kaydetme penceresi
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Soru Bankasını Excel Olarak Kaydet", "", 
                                                   "Excel Dosyaları (*.xlsx);;Tüm Dosyalar (*)", options=options)
        
        if file_path:
            try:
                # Excel dosyasına kaydet
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Başarılı", f"Soru bankası başarıyla kaydedildi:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Excel dosyasına kaydedilirken hata oluştu:\n{e}")