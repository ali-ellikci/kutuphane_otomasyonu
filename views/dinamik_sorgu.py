from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem
)
from database.connection import get_connection

class DinamikSorguWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dinamik Sorgu")
        self.setFixedSize(800, 500)
        self.init_ui()
        self.load_kategoriler()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🔍 Dinamik Kitap Sorgu")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        filter_layout = QHBoxLayout()

        self.kitap_input = QLineEdit()
        self.kitap_input.setPlaceholderText("Kitap Adı")
        filter_layout.addWidget(self.kitap_input)

        self.yazar_input = QLineEdit()
        self.yazar_input.setPlaceholderText("Yazar")
        filter_layout.addWidget(self.yazar_input)

        self.kategori_combo = QComboBox()
        self.kategori_combo.addItem("Tüm Kategoriler", None)
        filter_layout.addWidget(self.kategori_combo)

        self.basim_min = QSpinBox()
        self.basim_min.setRange(0, 3000)
        self.basim_min.setPrefix("Min: ")
        filter_layout.addWidget(self.basim_min)

        self.basim_max = QSpinBox()
        self.basim_max.setRange(0, 3000)
        self.basim_max.setPrefix("Max: ")
        filter_layout.addWidget(self.basim_max)

        self.sadece_mevcut = QCheckBox("Sadece mevcut kitaplar")
        filter_layout.addWidget(self.sadece_mevcut)

        self.sorgu_btn = QPushButton("Sorgula")
        self.sorgu_btn.clicked.connect(self.run_query)
        filter_layout.addWidget(self.sorgu_btn)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Kitap", "Yazar", "Kategori", "Basım Yılı", "MevcutAdet"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_kategoriler(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT KategoriID, KategoriAdi FROM KATEGORI ORDER BY KategoriAdi")
                    for row in cur.fetchall():
                        self.kategori_combo.addItem(row[1], row[0])
        except Exception as e:
            print("Kategori yükleme hatası:", e)

    def run_query(self):
        self.table.setRowCount(0)
        filters = []
        params = []

        if self.kitap_input.text():
            filters.append("KitapAdi ILIKE %s")
            params.append(f"%{self.kitap_input.text()}%")
        if self.yazar_input.text():
            filters.append("Yazar ILIKE %s")
            params.append(f"%{self.yazar_input.text()}%")
        if self.kategori_combo.currentData():
            filters.append("KategoriID = %s")
            params.append(self.kategori_combo.currentData())
        if self.basim_min.value() > 0:
            filters.append("BasimYili >= %s")
            params.append(self.basim_min.value())
        if self.basim_max.value() > 0:
            filters.append("BasimYili <= %s")
            params.append(self.basim_max.value())
        if self.sadece_mevcut.isChecked():
            filters.append("MevcutAdet > 0")

        query = "SELECT KitapAdi, Yazar, Kategori, BasimYili, MevcutAdet FROM KITAP"
        if filters:
            query += " WHERE " + " AND ".join(filters)

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    for row_data in cur.fetchall():
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        for col, val in enumerate(row_data):
                            self.table.setItem(row, col, QTableWidgetItem(str(val)))
        except Exception as e:
            print("Sorgu hatası:", e)
