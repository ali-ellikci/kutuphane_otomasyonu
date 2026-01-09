from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from database.connection import get_connection


class UyeYonetimiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Üye Yönetimi")
        self.setFixedSize(650, 500)
        self.init_ui()
        self.load_uyeler()

    def init_ui(self):
        layout = QVBoxLayout()

        # Arama alanları
        search_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Ad")
        self.search_surname = QLineEdit()
        self.search_surname.setPlaceholderText("Soyad")
        self.search_email = QLineEdit()
        self.search_email.setPlaceholderText("Email")
        search_btn = QPushButton("Ara")
        search_btn.clicked.connect(self.load_uyeler)
        search_layout.addWidget(self.search_name)
        search_layout.addWidget(self.search_surname)
        search_layout.addWidget(self.search_email)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # Üye tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["UyeID", "Ad", "Soyad", "Email"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Yeni Üye Ekle")
        self.update_btn = QPushButton("Güncelle")
        self.delete_btn = QPushButton("Sil")
        self.add_btn.clicked.connect(self.add_uye)
        self.update_btn.clicked.connect(self.update_uye)
        self.delete_btn.clicked.connect(self.delete_uye)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_uyeler(self):
        """Üyeleri filtreleyerek tabloya yükle"""
        name = self.search_name.text().strip()
        surname = self.search_surname.text().strip()
        email = self.search_email.text().strip()

        query = "SELECT UyeID, Ad, Soyad, Email FROM UYE WHERE 1=1"
        params = []

        if name:
            query += " AND Ad ILIKE %s"
            params.append(f"%{name}%")
        if surname:
            query += " AND Soyad ILIKE %s"
            params.append(f"%{surname}%")
        if email:
            query += " AND Email ILIKE %s"
            params.append(f"%{email}%")

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()

            self.table.setRowCount(0)
            for row_data in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, item in enumerate(row_data):
                    self.table.setItem(row, col, QTableWidgetItem(str(item)))
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def add_uye(self):
        from views.uye_form import UyeFormWindow  # ayrı form penceresi
        self.form = UyeFormWindow()
        self.form.saved.connect(self.load_uyeler)
        self.form.show()

    def update_uye(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Hata", "Güncellemek için bir üye seçin.")
            return
        uye_id = int(self.table.item(selected, 0).text())
        from views.uye_form import UyeFormWindow
        self.form = UyeFormWindow(uye_id=uye_id)
        self.form.saved.connect(self.load_uyeler)
        self.form.show()

    def delete_uye(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Hata", "Silmek için bir üye seçin.")
            return

        uye_id = int(self.table.item(selected, 0).text())

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Aktif ödünç veya borç kontrolü
                    cur.execute("""
                        SELECT COUNT(*) FROM ODUNC
                        WHERE UyeID = %s AND TeslimTarihi IS NULL
                    """, (uye_id,))
                    active = cur.fetchone()[0]
                    cur.execute("SELECT ToplamBorc FROM UYE WHERE UyeID=%s", (uye_id,))
                    borc = cur.fetchone()[0]

                    if active > 0 or borc > 0:
                        QMessageBox.warning(
                            self, "Hata",
                            "Bu üye silinemez. Aktif ödünç veya borç bulunuyor."
                        )
                        return

                    # Silme işlemi
                    confirm = QMessageBox.question(
                        self, "Onay", "Üyeyi silmek istediğinize emin misiniz?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if confirm == QMessageBox.Yes:
                        cur.execute("DELETE FROM UYE WHERE UyeID=%s", (uye_id,))
                        conn.commit()
                        QMessageBox.information(self, "Başarılı", "Üye silindi.")
                        self.load_uyeler()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
