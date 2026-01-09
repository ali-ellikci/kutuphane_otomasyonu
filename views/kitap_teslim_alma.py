from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QMessageBox, QDateEdit
)
from PyQt5.QtCore import QDate
from database.connection import get_connection


class OduncTeslimWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Teslim Alma")
        self.setFixedSize(650, 500)
        self.init_ui()
        self.load_odunc_list()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📦 Kitap Teslim Alma Paneli")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        self.odunc_list = QListWidget()
        layout.addWidget(self.odunc_list)

        date_layout = QHBoxLayout()
        date_label = QLabel("Teslim Tarihi:")
        self.teslim_tarihi_input = QDateEdit()
        self.teslim_tarihi_input.setCalendarPopup(True)
        self.teslim_tarihi_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.teslim_tarihi_input)
        layout.addLayout(date_layout)

        self.teslim_btn = QPushButton("📤 Teslim Al")
        layout.addWidget(self.teslim_btn)

        self.setLayout(layout)

        self.teslim_btn.clicked.connect(self.teslim_al)

    def load_odunc_list(self):
        """Henüz teslim edilmemiş ödünçleri listele"""
        self.odunc_list.clear()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT ODUNC.OduncID, UYE.Ad, UYE.Soyad, KITAP.KitapAdi, ODUNC.SonTeslimTarihi
                        FROM ODUNC
                        JOIN UYE ON ODUNC.UyeID = UYE.UyeID
                        JOIN KITAP ON ODUNC.KitapID = KITAP.KitapID
                        WHERE ODUNC.TeslimTarihi IS NULL
                        ORDER BY ODUNC.OduncID
                    """)
                    for row in cur.fetchall():
                        self.odunc_list.addItem(
                            f"{row[0]} | {row[1]} {row[2]} | {row[3]} | Son Teslim: {row[4]}"
                        )
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def teslim_al(self):
        item = self.odunc_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Hata", "Teslim almak için bir kayıt seç.")
            return

        odunc_id = int(item.text().split("|")[0])
        teslim_tarihi = self.teslim_tarihi_input.date().toPyDate()

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT sp_KitapTeslimAl(%s, %s)", (odunc_id, teslim_tarihi))
                conn.commit()

            QMessageBox.information(self, "Başarılı", "Kitap teslim alındı.")
            self.load_odunc_list()

        except Exception as e:
            QMessageBox.critical(self, "İşlem reddedildi", str(e))
