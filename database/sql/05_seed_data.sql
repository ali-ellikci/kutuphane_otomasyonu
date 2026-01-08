INSERT INTO KULLANICI(Ad, Sifre, Rol)
VALUES
('Admin', '1234', 'Admin'),
('Ali Gorevli', 'abcd', 'Gorevli'),
('Lachin Gorevli', 'qwer', 'Gorevli');

INSERT INTO UYE(Ad, Soyad, Email, ToplamBorc)
VALUES
('Ahmet', 'Yilmaz', 'ahmet@mail.com', 0),
('Lachin', 'Demir', 'lachin@mail.com', 0),
('Mehmet', 'Kara', 'mehmet@mail.com', 0);


INSERT INTO KATEGORI(KategoriAdi)
VALUES
('Roman'),
('Bilim'),
('Tarih');

INSERT INTO KITAP(KitapAdi, Yazar, YayinEvi, BasimYili, ToplamAdet, MevcutAdet, KategoriID)
VALUES
('Suc ve Ceza', 'Dostoyevski', 'Can Yayinlari', 1886, 5, 5, 1),
('Python 101', 'John Doe', 'Kod Akademi', 2020, 3, 3, 2),
('Dunya Tarihi', 'Jane Smith', 'Tarih Yayin Evi', 2015, 4, 4, 3);


INSERT INTO ODUNC(OduncTarihi, SonTeslimTarihi, TeslimTarihi, UyeID, GorevliID, KitapID)
VALUES
('2026-01-01', '2026-01-16', NULL, 1, 2, 1),
('2026-01-02', '2026-01-17', NULL, 2, 3, 2);

INSERT INTO ODUNC(OduncTarihi, SonTeslimTarihi, TeslimTarihi, UyeID, GorevliID, KitapID)
VALUES
('2025-12-15', '2025-12-30', '2025-12-28', 3, 2, 3);


INSERT INTO CEZA(Tutar, CezaTarihi, OduncID)
VALUES
(10.00, '2026-01-05', 1);  -- Ahmet'in gecikmesi


INSERT INTO LOG_ISLEM(TabloAdi, IslemTipi, Aciklama)
VALUES
('KULLANICI', 'INSERT', 'Admin kullanici eklendi'),
('UYE', 'INSERT', '3 uye eklendi'),
('KITAP', 'INSERT', '3 kitap eklendi');