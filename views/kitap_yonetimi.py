from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox
)
from database.connection import get_connection

class KitapYonetimiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Yönetimi")
        self.setFixedSize(550, 550)
        self.init_ui()
        self.kitaplari_yukle()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("📚 Kitap Yönetimi Paneli")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        # Arama alanları
        search_layout = QHBoxLayout()
        self.kitap_adi_search = QLineEdit()
        self.kitap_adi_search.setPlaceholderText("Kitap adına göre ara")
        self.yazar_search = QLineEdit()
        self.yazar_search.setPlaceholderText("Yazara göre ara")
        search_layout.addWidget(self.kitap_adi_search)
        search_layout.addWidget(self.yazar_search)
        main_layout.addLayout(search_layout)

        # Kitap ekleme alanları
        self.kitap_adi = QLineEdit()
        self.kitap_adi.setPlaceholderText("Kitap Adı")
        self.yazar = QLineEdit()
        self.yazar.setPlaceholderText("Yazar")
        self.yayin_evi = QLineEdit()
        self.yayin_evi.setPlaceholderText("Yayın Evi")
        self.basim_yili = QLineEdit()
        self.basim_yili.setPlaceholderText("Basım Yılı")
        self.toplam_adet = QLineEdit()
        self.toplam_adet.setPlaceholderText("Toplam Adet")
        self.kategori_id = QLineEdit()
        self.kategori_id.setPlaceholderText("Kategori ID (örn: 1)")

        main_layout.addWidget(self.kitap_adi)
        main_layout.addWidget(self.yazar)
        main_layout.addWidget(self.yayin_evi)
        main_layout.addWidget(self.basim_yili)
        main_layout.addWidget(self.toplam_adet)
        main_layout.addWidget(self.kategori_id)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.ekle_btn = QPushButton("Kitap Ekle")
        self.sil_btn = QPushButton("Seçili Kitabı Sil")
        self.yenile_btn = QPushButton("Yenile")
        btn_layout.addWidget(self.ekle_btn)
        btn_layout.addWidget(self.sil_btn)
        btn_layout.addWidget(self.yenile_btn)
        main_layout.addLayout(btn_layout)

        self.kitap_list = QListWidget()
        main_layout.addWidget(self.kitap_list)

        self.setLayout(main_layout)

        # Buton bağlantıları
        self.ekle_btn.clicked.connect(self.kitap_ekle)
        self.sil_btn.clicked.connect(self.kitap_sil)
        self.yenile_btn.clicked.connect(self.kitaplari_yukle)
        self.kitap_adi_search.textChanged.connect(self.kitaplari_yukle)
        self.yazar_search.textChanged.connect(self.kitaplari_yukle)

    def kitaplari_yukle(self):
        self.kitap_list.clear()
        ad_filter = self.kitap_adi_search.text().strip()
        yazar_filter = self.yazar_search.text().strip()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    query = """
                        SELECT KitapID, KitapAdi, Yazar, MevcutAdet
                        FROM KITAP
                        WHERE (%s='' OR KitapAdi ILIKE %s)
                          AND (%s='' OR Yazar ILIKE %s)
                        ORDER BY KitapID
                    """
                    cur.execute(query, (
                        ad_filter, f"%{ad_filter}%",
                        yazar_filter, f"%{yazar_filter}%"
                    ))
                    for row in cur.fetchall():
                        self.kitap_list.addItem(f"{row[0]} | {row[1]} | {row[2]} | Mevcut: {row[3]}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def kitap_ekle(self):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CALL sp_KitapEkleVeyaGuncelle(
                            %s, %s, %s, %s, %s, %s, NULL
                        )
                    """, (
                        self.kitap_adi.text(),
                        self.yazar.text(),
                        self.yayin_evi.text(),
                        int(self.basim_yili.text()),
                        int(self.toplam_adet.text()),
                        int(self.kategori_id.text())
                    ))
                conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap eklendi.")
            self.kitaplari_yukle()
            self.temizle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def kitap_sil(self):
        secili = self.kitap_list.currentItem()
        if not secili:
            QMessageBox.warning(self, "Hata", "Kitap seçmedin.")
            return

        kitap_id = int(secili.text().split("|")[0])
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Aktif ödünç kontrolü
                    cur.execute("SELECT COUNT(*) FROM ODUNC WHERE KitapID=%s AND TeslimTarihi IS NULL", (kitap_id,))
                    aktif_odunc = cur.fetchone()[0]
                    if aktif_odunc > 0:
                        QMessageBox.warning(self, "Silme Engellendi",
                                            "Bu kitap üzerinde aktif ödünç kaydı var, silme yapılamaz.")
                        return
                    cur.execute("DELETE FROM KITAP WHERE KitapID=%s", (kitap_id,))
                conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap silindi.")
            self.kitaplari_yukle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def temizle(self):
        self.kitap_adi.clear()
        self.yazar.clear()
        self.yayin_evi.clear()
        self.basim_yili.clear()
        self.toplam_adet.clear()
        self.kategori_id.clear()
