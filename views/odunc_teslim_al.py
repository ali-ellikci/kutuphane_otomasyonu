from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QMessageBox
)
from database.connection import get_connection

class OduncTeslimAlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Teslim Alma")
        self.setFixedSize(650, 500)
        self.init_ui()
        self.load_odunc()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📥 Ödünç Teslim Alma")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        self.odunc_list = QListWidget()
        layout.addWidget(self.odunc_list)

        btn_layout = QHBoxLayout()
        self.teslim_btn = QPushButton("📤 Teslim Al")
        btn_layout.addWidget(self.teslim_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.teslim_btn.clicked.connect(self.teslim_al)

    def load_odunc(self):
        self.odunc_list.clear()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT ODUNC.OduncID, UYE.Ad, UYE.Soyad, KITAP.KitapAdi, ODUNC.SonTeslimTarihi, ODUNC.TeslimTarihi
                        FROM ODUNC
                        JOIN UYE ON ODUNC.UyeID = UYE.UyeID
                        JOIN KITAP ON ODUNC.KitapID = KITAP.KitapID
                        WHERE ODUNC.TeslimTarihi IS NULL
                        ORDER BY ODUNC.OduncID
                    """)
                    for o in cur.fetchall():
                        self.odunc_list.addItem(f"{o[0]} | {o[1]} {o[2]} | {o[3]} | Son Teslim: {o[4]}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def teslim_al(self):
        item = self.odunc_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Hata", "Teslim almak için bir kayıt seçin.")
            return

        odunc_id = int(item.text().split("|")[0])

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL sp_KitapTeslimAl(%s, CURRENT_DATE)", (odunc_id,))
                conn.commit()

            QMessageBox.information(self, "Başarılı", "Kitap teslim alındı.")
            self.load_odunc()

        except Exception as e:
            QMessageBox.critical(self, "İşlem reddedildi", str(e))
