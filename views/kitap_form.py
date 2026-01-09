from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QComboBox, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from database.connection import get_connection

class KitapFormWindow(QWidget):
    saved = pyqtSignal()  # Kitap kaydedildiğinde ana pencereyi yenilemek için

    def __init__(self, kitap_id=None):
        super().__init__()
        self.kitap_id = kitap_id
        self.setWindowTitle("Kitap Formu")
        self.setFixedSize(350, 350)
        self.init_ui()
        if self.kitap_id:
            self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        self.kitapadi_input = QLineEdit()
        self.kitapadi_input.setPlaceholderText("Kitap Adı")
        self.yazar_input = QLineEdit()
        self.yazar_input.setPlaceholderText("Yazar")
        self.kategori_input = QLineEdit()
        self.kategori_input.setPlaceholderText("Kategori")
        self.yayinevi_input = QLineEdit()
        self.yayinevi_input.setPlaceholderText("Yayınevi")
        self.basim_input = QSpinBox()
        self.basim_input.setRange(1900, 2100)
        self.basim_input.setValue(2026)
        self.toplam_input = QSpinBox()
        self.toplam_input.setRange(1, 1000)
        self.toplam_input.setValue(1)
        self.mevcut_input = QSpinBox()
        self.mevcut_input.setRange(0, 1000)
        self.mevcut_input.setValue(1)

        layout.addWidget(QLabel("Kitap Adı:"))
        layout.addWidget(self.kitapadi_input)
        layout.addWidget(QLabel("Yazar:"))
        layout.addWidget(self.yazar_input)
        layout.addWidget(QLabel("Kategori:"))
        layout.addWidget(self.kategori_input)
        layout.addWidget(QLabel("Yayınevi:"))
        layout.addWidget(self.yayinevi_input)
        layout.addWidget(QLabel("Basım Yılı:"))
        layout.addWidget(self.basim_input)
        layout.addWidget(QLabel("Toplam Adet:"))
        layout.addWidget(self.toplam_input)
        layout.addWidget(QLabel("Mevcut Adet:"))
        layout.addWidget(self.mevcut_input)

        self.save_btn = QPushButton("Kaydet")
        self.save_btn.clicked.connect(self.save_kitap)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def load_data(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT KitapAdi, Yazar, Kategori, Yayinevi, BasimYili, ToplamAdet, MevcutAdet
                        FROM KITAP WHERE KitapID=%s
                    """, (self.kitap_id,))
                    row = cur.fetchone()
                    if row:
                        self.kitapadi_input.setText(row[0])
                        self.yazar_input.setText(row[1])
                        self.kategori_input.setText(row[2])
                        self.yayinevi_input.setText(row[3])
                        self.basim_input.setValue(row[4])
                        self.toplam_input.setValue(row[5])
                        self.mevcut_input.setValue(row[6])
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def save_kitap(self):
        kitapadi = self.kitapadi_input.text().strip()
        yazar = self.yazar_input.text().strip()
        kategori = self.kategori_input.text().strip()
        yayinevi = self.yayinevi_input.text().strip()
        basim = self.basim_input.value()
        toplam = self.toplam_input.value()
        mevcut = self.mevcut_input.value()

        if not kitapadi or not yazar or not kategori or not yayinevi:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalı.")
            return

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    if self.kitap_id:
                        cur.execute("""
                            UPDATE KITAP
                            SET KitapAdi=%s, Yazar=%s, Kategori=%s,
                                Yayinevi=%s, BasimYili=%s, ToplamAdet=%s, MevcutAdet=%s
                            WHERE KitapID=%s
                        """, (kitapadi, yazar, kategori, yayinevi, basim, toplam, mevcut, self.kitap_id))
                    else:
                        cur.execute("""
                            INSERT INTO KITAP
                            (KitapAdi, Yazar, Kategori, Yayinevi, BasimYili, ToplamAdet, MevcutAdet)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (kitapadi, yazar, kategori, yayinevi, basim, toplam, mevcut))
                conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap kaydedildi.")
            self.saved.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
