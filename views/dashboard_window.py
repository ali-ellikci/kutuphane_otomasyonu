from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from views.uye_yonetimi import UyeYonetimiWindow
from views.kitap_yonetimi import KitapYonetimiWindow
from views.odunc_verme import OduncVermeWindow
from views.ceza_goruntuleme import CezaGoruntuleWindow
from views.uye_rapor import UyeRaporWindow
from views.dinamik_sorgu import DinamikSorguWindow

class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Kütüphane Otomasyonu - Ana Menü")
        self.setFixedSize(400, 500)
        self.init_ui(username)

    def init_ui(self, username):
        layout = QVBoxLayout()

        title = QLabel(f"Hoş geldiniz, {username}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        self.buttons = {}
        menu_items = [
            "Üye Yönetimi",
            "Kitap Yönetimi",
            "Ödünç İşlemleri",
            "Ceza Görüntüleme",
            "Raporlar",
            "Dinamik Sorgu Ekranı",
            "Çıkış"
        ]

        for item in menu_items:
            btn = QPushButton(item)
            btn.setFixedHeight(40)
            layout.addWidget(btn)
            self.buttons[item] = btn

        self.buttons["Üye Yönetimi"].clicked.connect(self.open_uye_yonetimi)
        self.buttons["Kitap Yönetimi"].clicked.connect(self.open_kitap_yonetimi)
        self.buttons["Ödünç İşlemleri"].clicked.connect(self.open_odunc)
        self.buttons["Ceza Görüntüleme"].clicked.connect(self.open_ceza)
        self.buttons["Raporlar"].clicked.connect(self.open_rapor)
        self.buttons["Dinamik Sorgu Ekranı"].clicked.connect(self.open_dinamik)
        self.buttons["Çıkış"].clicked.connect(self.close)

        self.setLayout(layout)

    def open_uye_yonetimi(self):
        self.uye_window = UyeYonetimiWindow()
        self.uye_window.show()

    def open_kitap_yonetimi(self):
        self.kitap_window = KitapYonetimiWindow()
        self.kitap_window.show()

    def open_odunc(self):
        self.odunc_window = OduncVermeWindow()
        self.odunc_window.show()

    def open_ceza(self):
        self.ceza_window = CezaGoruntuleWindow()
        self.ceza_window.show()

    def open_rapor(self):
        self.rapor_window = UyeRaporWindow()
        self.rapor_window.show()

    def open_dinamik(self):
        self.dinamik_window = DinamikSorguWindow()
        self.dinamik_window.show()
