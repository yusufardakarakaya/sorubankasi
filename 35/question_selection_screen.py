import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QAbstractItemView, QTableWidgetItem, QHeaderView, QPushButton, QTableWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QRectF, QSizeF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QAbstractTextDocumentLayout

class QuestionSelectionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Soru Bankasından Soru Seçimi")
        self.setFixedSize(1300, 300)

        # Ana layout
        self.main_layout = QVBoxLayout(self)

        # Tablo
        self.tableWidget = QTableWidget(self)
        self.main_layout.addWidget(self.tableWidget)

        # Butonlar
        self.buttons_layout = QHBoxLayout()

        # Dosya Seç Butonu
        self.pushButton = QPushButton("YAZDIRILACAK SORU BANKASINA AİT DOSYAYI SEÇİNİZ", self)
        self.pushButton.clicked.connect(self.open_file_and_load_questions)
        self.buttons_layout.addWidget(self.pushButton)

        # Yazdır Butonu
        self.pushButton_2 = QPushButton("Yazdır", self)
        self.pushButton_2.clicked.connect(self.print_selected_questions)
        self.buttons_layout.addWidget(self.pushButton_2)

        self.main_layout.addLayout(self.buttons_layout)

        # Tablo ayarları
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Başlıklar
        headers = ["Seç", "Soru", "1. Seçenek", "2. Seçenek", "3. Seçenek", "4. Seçenek", "5. Seçenek", "Cevap"]
        self.tableWidget.setColumnCount(len(headers))
        for i, h in enumerate(headers):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(h))

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i in range(2, len(headers)):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def open_file_and_load_questions(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Question Bank", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            df = pd.read_excel(file_path)

            # Verileri tabloya ekle
            self.tableWidget.setRowCount(len(df))

            for row_index, row_data in df.iterrows():
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def print_selected_questions(self):
        # Yazdırma işlemi
        selected_rows = []
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).isSelected():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.warning(self, "Seçim Hatası", "Lütfen yazdırmak için en az bir soru seçin.")
            return

        # PDF dosyasının kaydedileceği yeri sormak
        file_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "PDF Dosyaları (*.pdf)")

        if not file_path:
            QMessageBox.warning(self, "Dosya Seçilmedi", "Lütfen bir dosya yolu seçin.")
            return

        # Yazdırılacak soruları ve seçenekleri topla
        document = QTextDocument()

        html = "<html><body>"
        for idx, row in enumerate(selected_rows, 1):
            question = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else "Soru Yok"
            options = [self.tableWidget.item(row, i).text() if self.tableWidget.item(row, i) else "Seçenek Yok" for i in range(2, 7)]
            correct_answer = self.tableWidget.item(row, 7).text() if self.tableWidget.item(row, 7) else "Belirtilmemiş"

            html += f"<h3>{idx}. {question}</h3>"
            for i, option in enumerate(options, 1):
                html += f"<p>{chr(64 + i)}. {option}</p>"  # A, B, C, D, E seçenekleri için
            html += f"<p><b>Doğru Cevap:</b> {correct_answer}</p><br>"

        html += "</body></html>"

        document.setHtml(html)

        # Yazıcı ayarları
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)

        # Yazdırma işlemi
        document.print(printer)

        QMessageBox.information(self, "Başarılı", "Sorular PDF olarak yazdırıldı.")