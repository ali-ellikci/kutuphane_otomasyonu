from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QHBoxLayout, QComboBox
from PyQt5.QtCore import QDate
from database.connection import get_connection

class UyeRaporWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raporlar")
        self.setFixedSize(700, 500)
        self.init_ui()
        self.load_uyeler()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📊 Üye Raporları")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        filter_layout = QHBoxLayout()
        self.uye_combo = QComboBox()
        self.uye_combo.addItem("Tüm Üyeler", None)
        filter_layout.addWidget(QLabel("Üye:"))
        filter_layout.addWidget(self.uye_combo)

        self.baslangic_input = QDateEdit()
        self.baslangic_input.setCalendarPopup(True)
        self.baslangic_input.setDate(QDate.currentDate().addMonths(-1))
        self.bitis_input = QDateEdit()
        self.bitis_input.setCalendarPopup(True)
        self.bitis_input.setDate(QDate.currentDate())
        filter_layout.addWidget(QLabel("Başlangıç:"))
        filter_layout.addWidget(self.baslangic_input)
        filter_layout.addWidget(QLabel("Bitiş:"))
        filter_layout.addWidget(self.bitis_input)

        self.filtre_btn = QPushButton("Filtrele")
        self.filtre_btn.clicked.connect(self.load_rapor_list)
        filter_layout.addWidget(self.filtre_btn)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Üye", "Kitap", "Odunc Tarihi", "Teslim Tarihi"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_uyeler(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT UyeID, Ad || ' ' || Soyad FROM UYE ORDER BY Ad")
                    for row in cur.fetchall():
                        self.uye_combo.addItem(row[1], row[0])
        except Exception as e:
            print("Üye yükleme hatası:", e)

    def load_rapor_list(self):
        self.table.setRowCount(0)
        uye_id = self.uye_combo.currentData()
        baslangic = self.baslangic_input.date().toPyDate()
        bitis = self.bitis_input.date().toPyDate()

        query = """
        SELECT U.Ad || ' ' || U.Soyad, K.KitapAdi, O.OduncTarihi, O.TeslimTarihi
        FROM ODUNC O
        JOIN UYE U ON O.UyeID = U.UyeID
        JOIN KITAP K ON O.KitapID = K.KitapID
        WHERE O.OduncTarihi BETWEEN %s AND %s
        """
        params = [baslangic, bitis]

        if uye_id:
            query += " AND O.UyeID = %s"
            params.append(uye_id)

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
            print("Rapor yükleme hatası:", e)
