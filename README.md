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
├── requirements.txt           # Python bağımlılıkları
├── assets/
│   └── style.qss              # GUI stil dosyası
├── controllers/
│   ├── __init__.py
│   └── auth_controller.py     # Kimlik doğrulama kontrolleri
├── database/
│   ├── __init__.py
│   ├── config.py              # PostgreSQL bağlantı ayarları (ENV ile aşılabilir)
│   ├── connection.py          # Veritabanı bağlantı yönetimi
│   ├── setup_db.py            # Veritabanı oluşturma yardımcı betiği
│   └── sql/                   # Şema, constraint, prosedür ve tetikleyiciler
│       ├── 01_tables.sql
│       ├── 02_constraints.sql
│       ├── 03_procedures.sql
│       ├── 04_triggers.sql
│       └── 05_seed_data.sql
└── views/
  ├── __init__.py
  ├── login_window.py        # Giriş ekranı
  ├── dashboard_window.py    # Ana menü
  ├── uye_yonetimi.py        # Üye yönetimi
  ├── uye_form.py            # Üye formu
  ├── kitap_yonetimi.py      # Kitap yönetimi
  ├── odunc_verme.py         # Ödünç verme
  ├── ceza_goruntuleme.py    # Ceza görüntüleme
  ├── uye_rapor.py           # Üye raporları
  └── dinamik_sorgu.py       # Dinamik sorgu ekranı
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

### ⚠ Seed Verisi ve Tetikleyici Etkileşimi (Önemli)
- `ODUNC` için tetikleyici insert sırasında stok azaltır. Eğer seed verisinde bir ödünç kaydı `TeslimTarihi` dolu olarak eklenirse, stok azaltılır fakat teslim tetikleyicisi çalışmaz; bu da stokta net −1 etkiye yol açar.
- Önerilen yaklaşımlar:
  - Seed sırasında önce `TeslimTarihi = NULL` ile ekleyip ardından `UPDATE` ile `TeslimTarihi` set edin (INSERT → stok −1, UPDATE → stok +1, net 0).
  - Alternatif: `ODUNC` insert tetikleyicisini yalnızca `NEW.TeslimTarihi IS NULL` olduğunda stok azaltacak şekilde tasarlayın.
- Seed dosyasını tekrar çalıştırma durumunda idempotentlik için sabit ID'ler yerine alt sorgu ile referans alın (ör. kategori/üye/kullanıcı/kitap ID'lerini isim veya email ile bulun).
- Gerekirse ilk çalıştırmadan önce `TRUNCATE ... RESTART IDENTITY CASCADE;` ile temiz başlangıç yapın.

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
PostgreSQL komut satırı aracı (psql) — opsiyonel ama önerilir
```

### ⚡ Hızlı Başlangıç (Windows PowerShell)

```powershell
# 1) Sanal ortam oluştur ve etkinleştir
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Bağımlılıkları yükle
pip install -r requirements.txt

# 3) (Önerilen) Ortam değişkenleriyle DB bağlantısını tanımla
$env:PGDATABASE = "kutuphanedb"
$env:PGUSER = "postgres"
$env:PGPASSWORD = "<sifre>"
$env:PGHOST = "localhost"
$env:PGPORT = "5432"

# 4) Veritabanını oluştur (yoksa oluşturur)
python database/setup_db.py

# 5) Şema ve verileri uygula (psql ile)
# Not: psql yoksa pgAdmin üzerinden dosyaları sırayla çalıştırabilirsin.
psql -U $env:PGUSER -d $env:PGDATABASE -h $env:PGHOST -p $env:PGPORT -f database/sql/01_tables.sql
psql -U $env:PGUSER -d $env:PGDATABASE -h $env:PGHOST -p $env:PGPORT -f database/sql/02_constraints.sql
psql -U $env:PGUSER -d $env:PGDATABASE -h $env:PGHOST -p $env:PGPORT -f database/sql/03_procedures.sql
psql -U $env:PGUSER -d $env:PGDATABASE -h $env:PGHOST -p $env:PGPORT -f database/sql/04_triggers.sql
psql -U $env:PGUSER -d $env:PGDATABASE -h $env:PGHOST -p $env:PGPORT -f database/sql/05_seed_data.sql

# 6) Bağlantıyı test et (opsiyonel)
python test_db.py

# 7) Uygulamayı çalıştır
python main.py
```

> psql komutu tanınmıyorsa, PostgreSQL kurulumundaki `bin` klasörünü PATH'e ekleyin
> (ör: `C:\Program Files\PostgreSQL\16\bin`). Alternatif olarak pgAdmin ile `.sql`
> dosyalarını sırayla çalıştırabilirsiniz.

### Kurulum Adımları (Detaylı)

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/ali-ellikci/kutuphane_otomasyonu
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
  - `database/sql/01_tables.sql` → `05_seed_data.sql` dosyalarını sırasıyla çalıştırın
  - Bağlantı ayarlarını `database/config.py` içinde veya ortam değişkenleriyle yapılandırın

5. **Uygulamayı çalıştırın:**
```bash
python main.py
```

### Sık Karşılaşılan Sorunlar (Troubleshooting)
- psql bulunamadı: PostgreSQL `bin` klasörünü PATH'e ekleyin veya pgAdmin kullanın.
- Bağlantı hatası: PostgreSQL servisinin çalıştığını ve `database/config.py`/ortam
  değişkenlerinin doğru ayarlandığını doğrulayın (host, port, kullanıcı, şifre, DB adı).
- Yetki hataları: `postgres` kullanıcısının ilgili veritabanında gerekli yetkilere
  sahip olduğundan emin olun.
- Stil dosyası yüklenmiyor: `assets/style.qss` dosyası isteğe bağlıdır; eksikse uygulama
  çalışmaya devam eder.

---

## 🔐 Bağlantı Ayarları (Database Connection Configuration)

[database/config.py](database/config.py) dosyasında PostgreSQL bağlantı parametreleri tanımlıdır ve ortam değişkenleriyle aşılabilir:

```python
DB_NAME = os.getenv("PGDATABASE", "kutuphanedb")
DB_USER = os.getenv("PGUSER", "admin")  # varsayılan kullanıcı: admin
DB_PASSWORD = os.getenv("PGPASSWORD", "<şifreniz>")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = int(os.getenv("PGPORT", "5432"))
```

Örnek kullanım (Windows PowerShell):

```powershell
$env:PGDATABASE = "kutuphanedb"
$env:PGUSER = "admin"       # kendi DB kullanıcınızı yazın
$env:PGPASSWORD = "<sifre>"  # şifrenizi girin
$env:PGHOST = "localhost"
$env:PGPORT = "5432"
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
psql -U postgres -d kutuphanedb -f database/sql/01_tables.sql
psql -U postgres -d kutuphanedb -f database/sql/02_constraints.sql
psql -U postgres -d kutuphanedb -f database/sql/03_procedures.sql
psql -U postgres -d kutuphanedb -f database/sql/04_triggers.sql
psql -U postgres -d kutuphanedb -f database/sql/05_seed_data.sql
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







