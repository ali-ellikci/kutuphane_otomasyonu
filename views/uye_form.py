from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from database.connection import get_connection

class UyeFormWindow(QWidget):
    saved = pyqtSignal()  # Üye kaydedildiğinde ana pencereyi yenilemek için

    def __init__(self, uye_id=None):
        super().__init__()
        self.uye_id = uye_id
        self.setWindowTitle("Üye Formu")
        self.setFixedSize(300, 200)
        self.init_ui()
        if self.uye_id:
            self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ad")
        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyad")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        layout.addWidget(QLabel("Ad:"))
        layout.addWidget(self.ad_input)
        layout.addWidget(QLabel("Soyad:"))
        layout.addWidget(self.soyad_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        self.save_btn = QPushButton("Kaydet")
        self.save_btn.clicked.connect(self.save_uye)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def load_data(self):
        """Var olan üye bilgilerini yükle"""
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT Ad, Soyad, Email FROM UYE WHERE UyeID=%s", (self.uye_id,))
                    row = cur.fetchone()
                    if row:
                        self.ad_input.setText(row[0])
                        self.soyad_input.setText(row[1])
                        self.email_input.setText(row[2])
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def save_uye(self):
        ad = self.ad_input.text().strip()
        soyad = self.soyad_input.text().strip()
        email = self.email_input.text().strip()

        if not ad or not soyad or not email:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalı.")
            return

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    if self.uye_id:
                        # Güncelleme
                        cur.execute("""
                            UPDATE UYE SET Ad=%s, Soyad=%s, Email=%s
                            WHERE UyeID=%s
                        """, (ad, soyad, email, self.uye_id))
                    else:
                        # Yeni üye ekleme
                        cur.execute("""
                            INSERT INTO UYE (Ad, Soyad, Email)
                            VALUES (%s, %s, %s)
                        """, (ad, soyad, email))
                conn.commit()
            QMessageBox.information(self, "Başarılı", "Üye kaydedildi.")
            self.saved.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
