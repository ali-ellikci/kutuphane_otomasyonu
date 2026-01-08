# Üniversite Kütüphanesi Yönetim Sistemi
## Library Management System

**Veritabanı Yönetim Sistemleri Final Projesi** | Database Management Systems Final Project

---

## 📚 Proje Amacı (Project Purpose)

Bu masaüstü uygulaması, üniversite kütüphanesi işlemlerinin tam otomasyonunu sağlayan kapsamlı bir yönetim sistemidir.

**This desktop application is a comprehensive management system providing complete automation of university library operations.**

### Ana Fonksiyonlar:
- ✅ Üyelerin kayıt ve yönetimi
- ✅ Kitap envanteri ve stok takibi
- ✅ Ödünç-teslim işlemleri
- ✅ Otomatik ceza hesaplaması (geciken kitaplar)
- ✅ Veritabanı seviyesinde iş kuralları (Stored Procedures & Triggers)
- ✅ Dinamik raporlama sistemi
- ✅ İşlem güvenliği ve yetkilendirme

---

## 🛠️ Teknoloji Yığını (Technology Stack)

| Bileşen | Teknoloji |
|---------|-----------|
| **Programlama Dili** | Python 3.x |
| **GUI Framework** | PyQt5 |
| **Veritabanı** | PostgreSQL |
| **Bağlantı** | psycopg2 |
| **Stil** | QSS (Qt Style Sheets) |

---

## 📁 Proje Yapısı (Project Structure)

```
kutuphane_otomasyonu/
├── main.py                    # Ana uygulama giriş noktası
├── README.md                  # Bu dosya
├── assets/
│   └── style.qss              # GUI stil dosyası
├── controllers/
│   ├── __init__.py
│   └── auth_controller.py     # Kimlik doğrulama kontrolleri
├── database/
│   ├── __init__.py
│   ├── connection.py          # Veritabanı bağlantı yönetimi
│   └── schema.sql             # Veritabanı şeması ve prosedürler
├── models/
│   ├── __init__.py
│   ├── uye.py                 # Üye (Member) modeli
│   ├── kitap.py               # Kitap (Book) modeli
│   └── odunc.py               # Ödünç (Loan) modeli
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Yardımcı fonksiyonlar
└── views/
    ├── __init__.py
    └── login_window.py        # Giriş ekranı
```

---

## 📋 Veritabanı Şeması (Database Schema)

### Zorunlu Tablolar

| Tablo | Açıklama |
|-------|----------|
| **KULLANICI** | Sistem kullanıcıları (admin, görevli) - Giriş bilgileri |
| **UYE** | Kütüphane üyeleri (öğrenciler) - Ad, soyad, iletişim, toplam borç |
| **KATEGORI** | Kitap kategorileri |
| **KITAP** | Kitap bilgileri - Başlık, yazar, yayınevi, toplam adet, mevcut adet |
| **ODUNC** | Ödünç işlemleri - Üye, kitap, ödünç tarihi, son teslim tarihi, teslim tarihi |
| **CEZA** | Ceza kayıtları - Üye, ceza tutarı, tarihi, nedeni |
| **LOG_ISLEM** | İşlem logları - Hangi tablo, ne işlem, zamanı, açıklaması |

### İlişkiler (Relationships)
```
KULLANICI (1) ──────── (*) ODUNC
UYE       (1) ──────── (*) ODUNC
UYE       (1) ──────── (*) CEZA
KITAP     (1) ──────── (*) ODUNC
KATEGORI  (1) ──────── (*) KITAP
```

---

## 🔧 Saklı Yordamlar (Stored Procedures)

### 1. **sp_YeniOduncVer**
**Amaç:** Üyeye yeni kitap ödünç vermek
```
Parametreler: UyeID, KitapID, IslemYapanKullaniciID
- Üyenin aktif ödünç sayısını kontrol (max 5)
- Kitabın stok durumunu kontrol
- Yeni ödünç kaydı oluştur
- Stok (MevcutAdet) azalt
- Son teslim tarihini otomatik hesapla (ödünç tarihi + 15 gün)
```

### 2. **sp_KitapTeslimAl**
**Amaç:** Ödünç alınan kitabın iadesini almak
```
Parametreler: OduncID, TeslimTarihiParam
- Ödünç kaydının teslim tarihini güncelle
- Kitabın stok (MevcutAdet) artır
- Gecikme günü hesapla (TeslimTarihi > SonTeslimTarihi)
- Gecikme varsa otomatik ceza kaydı oluştur (gün başına 5 TL)
- Cezayı üyenin toplam borcuna ekle
```

### 3. **sp_UyeOzetRapor**
**Amaç:** Üyenin özet bilgilerini raporlamak
```
Parametreler: UyeID
Döndürülen Bilgiler:
- Toplam aldığı kitap sayısı
- Halen iade etmediği aktif kitap sayısı
- Toplam ceza tutarı
```

---

## 🔔 Tetikleyiciler (Triggers)

### 1. **TR_ODUNC_INSERT**
- Yeni ödünç verme işlemi sırasında KITAP.MevcutAdet'i azalt
- LOG_ISLEM tablosuna işlem kaydını ekle

### 2. **TR_ODUNC_UPDATE_TESLIM**
- Kitap teslimi sırasında KITAP.MevcutAdet'i artır
- LOG_ISLEM tablosuna işlem kaydını ekle

### 3. **TR_CEZA_INSERT**
- Ceza eklendiğinde UYE.ToplamBorc'u güncelle
- LOG_ISLEM tablosuna ceza işlemini kaydet

### 4. **TR_UYE_DELETE_BLOCK**
- Aktif ödünç kaydı veya borcu olan üyenin silinmesini engelle
- Uygun hata mesajı döndür

---

## 🖥️ Uygulama Ekranları (Application Screens)

### 1. **Giriş Ekranı (Login Screen)**
- Kullanıcı adı ve şifre giriş alanları
- Kimlik doğrulama (KULLANICI tablosuna karşı)
- Başarısız giriş uyarısı

### 2. **Ana Menü / Dashboard**
- Hoş geldiniz mesajı ve kullanıcı adı gösterimi
- Tüm işlevlere erişim düğmeleri:
  - Üye Yönetimi
  - Kitap Yönetimi
  - Ödünç İşlemleri
  - Kitap Teslim Alma
  - Ceza Görüntüleme
  - Raporlar
  - Dinamik Sorgu Ekranı
  - Çıkış

### 3. **Üye Yönetimi**
- Üyeleri listele (tablo/grid)
- Arama: Ad, Soyad, Email filtresi
- Yeni üye ekleme (Ad, Soyad, Telefon, Email)
- Üye bilgisi güncelleme
- Üye silme (borcu/aktif ödünç varsa uyarı)

### 4. **Kitap Yönetimi**
- Kitap listesi ve arama (Kitap adı, yazar)
- Yeni kitap ekleme:
  - Kitap Adı, Yazar, Kategori, Yayınevi, Basım Yılı, Toplam Adet (zorunlu)
  - Mevcut Adet = Toplam Adet (otomatik)
- Kitap güncelleme
- Kategori yönetimi (alt ekran)

### 5. **Ödünç Verme**
- Üye seçimi (liste/arama)
- Kitap seçimi (liste/arama) - Mevcut adet gösterilir
- "Ödünç Ver" düğmesi → sp_YeniOduncVer çağrısı
- Başarı/hata mesajları gösterilir
- Aktif ödünçler listesi (bonus)

### 6. **Kitap Teslim Alma**
- Aktif ödünçler listesi (TeslimTarihi NULL olanlar)
- Filtreler: Üye, Kitap, Tarih aralığı
- Seçili kayıt detayı gösterimi
- "Teslim Al" → sp_KitapTeslimAl çağrısı
- Gecikme varsa otomatik ceza oluşturma ve gösterimi

### 7. **Ceza Görüntüleme**
- Üyelere göre ceza listeleme
- Filtreler: Üye seçimi, Tarih aralığı
- Toplam borç gösterimi
- Ceza detayları

---

## 📊 Raporlama Sistemleri (Reports)

### Statik Raporlar (En az 3 zorunlu)

#### 1. **Tarih Aralığına Göre Ödünç Raporu**
- Parametreler: Başlangıç tarihi, Bitiş tarihi, (İsteğe bağlı) Üye, Kategori
- Gösterim: Ödünç kaydı, Üye, Kitap, Tarihleri, Durum

#### 2. **Geciken Kitaplar Raporu**
- Koşul: SonTeslimTarihi < Bugün ve TeslimTarihi IS NULL
- Kolonlar: Üye, Kitap, OduncTarihi, SonTeslimTarihi, GecikmeGunu (hesaplanmış)
- Sıralama: Gecikme gün sayısına göre (en çok gecikmiş ilk)

#### 3. **En Çok Ödünç Alınan Kitaplar Raporu**
- Tarih aralığı seçimi
- Gösterim: Kitap Adı, Ödünç Sayısı (COUNT), Yazarı
- Sıralama: Ödünç sayısına göre azalan

### Dinamik Sorgu & Raporlama Ekranı (Zorunlu)

**Amaç:** Kitap arama ve filtreleme ile dinamik rapor oluşturma

**Filtre Alanları:**
- 📝 Kitap Adı (Metin kutusu - kısmi uyum/LIKE)
- 📝 Yazar (Metin kutusu)
- 📋 Kategori (ComboBox)
- 📅 Basım Yılı Min (Sayı)
- 📅 Basım Yılı Max (Sayı)
- ☑️ Sadece Mevcut Kitaplar (Checkbox - MevcutAdet > 0)

**Özellikler:**
- Boş alanlar sorguda kullanılmaz
- Dolu alanlar dinamik WHERE koşulları oluşturur
- İsteğe bağlı sıralama seçeneği (Sütun + Artan/Azalan)
- Sonuçları Excel/PDF formatında indirme (bonus)

---

## 🚀 Kurulum ve Çalıştırma (Installation & Setup)

### Gereksinimler (Requirements)
```
Python 3.7+
PyQt5
PostgreSQL 10+
psycopg2 (PostgreSQL adaptörü)
```

### Kurulum Adımları

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/username/kutuphane_otomasyonu.git
cd kutuphane_otomasyonu
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Gerekli kütüphaneleri yükleyin:**
```bash
pip install PyQt5
pip install psycopg2-binary
```

4. **Veritabanını oluşturun:**
   - `database/schema.sql` dosyasını veritabanı sunucunuzda çalıştırın
   - Bağlantı ayarlarını `database/connection.py` dosyasında yapılandırın

5. **Uygulamayı çalıştırın:**
```bash
python main.py
```

---

## 🔐 Bağlantı Ayarları (Database Connection Configuration)

[database/connection.py](database/connection.py) dosyasında PostgreSQL bağlantı parametrelerini ayarlayın:

```python
# PostgreSQL Bağlantı Ayarları
DB_CONFIG = {
    'host': 'localhost',
    'database': 'kutuphanedb',
    'user': 'postgres',
    'password': 'your_password',
    'port': 5432
}
```

### PostgreSQL Kurulumu ve Veritabanı Oluşturma

1. **PostgreSQL sunucusunun çalıştığından emin olun**
```bash
# Linux/Mac
psql --version

# Windows - pgAdmin kullanabilirsiniz
```

2. **PostgreSQL'de yeni veritabanı oluşturun:**
```bash
createdb kutuphanedb -U postgres
```

3. **Schema ve tabloları oluşturun:**
```bash
psql -U postgres -d kutuphanedb -f database/schema.sql
```

4. **Bağlantı parametrelerini güncelleyin:**
   - `database/connection.py` dosyasını açın
   - Host, username, password ve port bilgilerini PostgreSQL konfigürasyonunuza göre ayarlayın

---

## 📖 Kullanım Örnekleri (Usage Examples)

### Yeni Üye Ekleme
1. Ana menüden "Üye Yönetimi" seçin
2. "Yeni Üye Ekle" düğmesini tıklayın
3. Ad, Soyad, Telefon, Email bilgilerini girin
4. "Kaydet" düğmesini tıklayın

### Kitap Ödünç Verme
1. "Ödünç Verme" ekranını açın
2. Üyelistesinden üye seçin
3. Kitap listesinden kitap seçin
4. "Ödünç Ver" düğmesini tıklayın
5. Sistem otomatik olarak teslim tarihini hesaplar (14 gün sonrası)

### Kitap Teslimi
1. "Kitap Teslim Alma" ekranını açın
2. Aktif ödünçler tablosundan kaydı seçin
3. "Teslim Al" düğmesini tıklayın
4. Gecikme varsa otomatik ceza oluşturulur

---

## 📊 Puanlama Kriterleri (Grading Rubric)

| Kriter | Puan |
|--------|------|
| Veritabanı Tasarımı | 20 |
| Constraint'ler ve Veri Bütünlüğü | 10 |
| Saklı Yordamlar (3+ prosedür) | 15 |
| Tetikleyiciler (2+ trigger) | 15 |
| CRUD Ekranları Fonksiyonelliği | 15 |
| Raporlama Ekranları (3+ rapor) | 10 |
| Dinamik Sorgu Ekranı | 10 |
| Proje Raporu ve Sunum | 5 |
| **TOPLAM** | **100** |

---

## 📝 Teslim Dosyaları (Deliverables)

✅ Veritabanı script'i (CREATE TABLE, PROCEDURE, TRIGGER komutları)
✅ Derlenebilir ve çalıştırılabilir uygulama kaynak kodu
✅ Bağlantı ayarlarının yapılandırılması hakkında kısa not
✅ Proje raporu (3-5 sayfa):
  - Veritabanı şeması ve ER diyagramı
  - Prosedür ve trigger'lar listesi
  - Ekran görüntüleri ve açıklamaları

---

## 🤝 Katkıda Bulunma (Contributing)

Bu proje akademik amaçlı bir final projesidir. Katkılar hoş karşılanır!

---

## 📄 Lisans (License)

Bu proje eğitim amaçlıdır.

---

## ✍️ Yazar Bilgisi

**Proje:** Üniversite Kütüphanesi Yönetim Sistemi  
**Ders:** Veritabanı Yönetim Sistemleri Final Projesi  
**Tarih:** 2025

---

## 📞 İletişim (Contact)

Sorular ve önerileriniz için lütfen issue açınız.

---

**Başarılı çalışmalar! 🎓**
