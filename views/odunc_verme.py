from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QMessageBox
)

from database.connection import get_connection


class OduncVermeWindow(QWidget):
    def __init__(self, gorevli_id=1):  # şimdilik admin=1 varsaydık
        super().__init__()
        self.gorevli_id = gorevli_id
        self.setWindowTitle("Ödünç Verme Paneli")
        self.setFixedSize(650, 500)
        self.init_ui()
        self.load_uyeler()
        self.load_kitaplar()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("Ödünç Verme İşlemleri")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        lists_layout = QHBoxLayout()

        self.uye_list = QListWidget()
        self.kitap_list = QListWidget()

        lists_layout.addWidget(self.uye_list)
        lists_layout.addWidget(self.kitap_list)

        main_layout.addLayout(lists_layout)

        self.odunc_btn = QPushButton("📤 Ödünç Ver")
        main_layout.addWidget(self.odunc_btn)

        self.setLayout(main_layout)

        self.odunc_btn.clicked.connect(self.odunc_ver)

    # ---------------------------
    # VERİ YÜKLEME
    # ---------------------------

    def load_uyeler(self):
        self.uye_list.clear()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT UyeID, Ad, Soyad FROM UYE ORDER BY UyeID")
                    for u in cur.fetchall():
                        self.uye_list.addItem(f"{u[0]} | {u[1]} {u[2]}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def load_kitaplar(self):
        self.kitap_list.clear()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT KitapID, KitapAdi, MevcutAdet 
                        FROM KITAP ORDER BY KitapID
                    """)
                    for k in cur.fetchall():
                        self.kitap_list.addItem(
                            f"{k[0]} | {k[1]} (Mevcut: {k[2]})"
                        )
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    # ---------------------------
    # ÖDÜNÇ VERME
    # ---------------------------

    def odunc_ver(self):
        uye_item = self.uye_list.currentItem()
        kitap_item = self.kitap_list.currentItem()

        if not uye_item or not kitap_item:
            QMessageBox.warning(self, "Hata", "Üye ve kitap seçmelisin.")
            return

        uye_id = int(uye_item.text().split("|")[0])
        kitap_id = int(kitap_item.text().split("|")[0])

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT sp_YeniOduncVer(%s, %s, %s)",
                                (uye_id, kitap_id, self.gorevli_id))
                conn.commit()

            QMessageBox.information(self, "Başarılı", "Ödünç verme tamamlandı.")
            self.load_kitaplar()

        except Exception as e:
            QMessageBox.critical(self, "İşlem reddedildi", str(e))