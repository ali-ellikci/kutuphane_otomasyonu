CREATE OR REPLACE FUNCTION sp_YeniOduncVer(
    p_UyeID INT
    p_KitapID INT,
    p_IslemYapanKullaniciID INT
)
RETURNS VOID AS $$
DECLARE
    -- Üyenin aktif ödünç sayısını kontrol et
    SELECT COUNT(*) INTO v_AktifOdunc
    FROM ODUNC
    WHERE UyeID = p_UyeID AND TeslimTarihi IS NULL;

    IF v_AktifOdunc >=5 THEN
        RAISE EXCEPTION 'Bu üye zaten 5 ödünç kitapta. Limit aşıldı.';
    END IF ;
    -- Kitabın mevcut adedini kontrol et
    SELECT MevcutAdet INTO v_MevuctAdet
    FROM KITAP
    WHERE KitapID = p_KitapID;

    IF v_MevcutAdet <= 0 THEN
        RAISE EXCEPTION 'Bu kitap stokta yok.';
    END IF;

    -- ODUNC kaydı ekle

    INSERT INTO ODUNC(UyeID, GorevliID, KitapID, OduncTarihi, SonTeslimTarihi)
    VALUES (
        p_UyeID,
        p_IslemYapanKullaniciID,
        p_KitapID,
        CURRENT_DATE,
        CURRENT_DATE + INTERVAL '15 days' 
    )
END;
$$ LANGUAGE plpsql;



CREATE OR REPLACE FUNCTION sp_KitapTeslimAl(
    p_OduncID INT,
    p_TeslimTarihi DATE
)
RETURNS VOID AS $$
DECLARE
    v_SonTeslim DATE;
    v_UyeID INT;
    v_GecikmeGun INT;
    v_CezaTutar NUMERIC := 5; -- her gün 5 TL ceza
BEGIN
    -- Teslim tarihini güncelle
    UPDATE ODUNC
    SET TeslimTarihi = p_TeslimTarihi
    WHERE OduncID = p_OduncID;

    -- Gerekli bilgiler
    SELECT SonTeslimTarihi, UyeID INTO v_SonTeslim, v_UyeID
    FROM ODUNC
    WHERE OduncID = p_OduncID;

    -- Kitap mevcut adedini 1 arttır (trigger veya burada)
    UPDATE KITAP
    SET MevcutAdet = MevcutAdet + 1
    WHERE KitapID = (SELECT KitapID FROM ODUNC WHERE OduncID = p_OduncID);

    -- Gecikme kontrolü
    IF p_TeslimTarihi > v_SonTeslim THEN
        v_GecikmeGun := p_TeslimTarihi - v_SonTeslim;

        -- CEZA kaydı oluştur
        INSERT INTO CEZA(Tutar, CezaTarihi, OduncID)
        VALUES (v_GecikmeGun * v_CezaTutar, CURRENT_DATE, p_OduncID);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION sp_UyeOzetRapor(
    p_UyeID INT
)
RETURNS TABLE(
    ToplamAlinanKitap INT,
    HalenIadeEdilmeyen INT,
    ToplamCeza NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM ODUNC WHERE UyeID = p_UyeID) AS ToplamAlinanKitap,
        (SELECT COUNT(*) FROM ODUNC WHERE UyeID = p_UyeID AND TeslimTarihi IS NULL) AS HalenIadeEdilmeyen,
        (SELECT COALESCE(SUM(Tutar),0) FROM CEZA
         JOIN ODUNC ON CEZA.OduncID = ODUNC.OduncID
         WHERE ODUNC.UyeID = p_UyeID) AS ToplamCeza;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION sp_KitapEkleVeyaGuncelle(
    p_KitapID INT DEFAULT NULL, -- NULL ise yeni ekleme
    p_KitapAdi VARCHAR,
    p_Yazar VARCHAR,
    p_YayinEvi VARCHAR,
    p_BasimYili NUMERIC,
    p_ToplamAdet NUMERIC,
    p_KategoriID INT
)
RETURNS VOID AS $$
BEGIN
    IF p_KitapID IS NULL THEN
        -- Yeni kitap ekle
        INSERT INTO KITAP(KitapAdi, Yazar, YayinEvi, BasimYili, ToplamAdet, MevcutAdet, KategoriID)
        VALUES (p_KitapAdi, p_Yazar, p_YayinEvi, p_BasimYili, p_ToplamAdet, p_ToplamAdet, p_KategoriID);
    ELSE
        -- Var olan kitabı güncelle
        UPDATE KITAP
        SET KitapAdi = p_KitapAdi,
            Yazar = p_Yazar,
            YayinEvi = p_YayinEvi,
            BasimYili = p_BasimYili,
            ToplamAdet = p_ToplamAdet,
            MevcutAdet = LEAST(MevcutAdet, p_ToplamAdet), -- Mevcut adeti toplamın üzerine çıkarmamak için
            KategoriID = p_KategoriID
        WHERE KitapID = p_KitapID;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION sp_KitapAra(
    p_KitapAdi VARCHAR DEFAULT NULL,
    p_Yazar VARCHAR DEFAULT NULL,
    p_KategoriID INT DEFAULT NULL,
    p_BasimYiliMin NUMERIC DEFAULT NULL,
    p_BasimYiliMax NUMERIC DEFAULT NULL,
    p_SadeceMevcut BOOLEAN DEFAULT FALSE
)
RETURNS TABLE(
    KitapID INT,
    KitapAdi VARCHAR,
    Yazar VARCHAR,
    YayinEvi VARCHAR,
    BasimYili NUMERIC,
    ToplamAdet NUMERIC,
    MevcutAdet NUMERIC,
    KategoriID INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM KITAP
    WHERE (p_KitapAdi IS NULL OR KitapAdi ILIKE '%' || p_KitapAdi || '%')
      AND (p_Yazar IS NULL OR Yazar ILIKE '%' || p_Yazar || '%')
      AND (p_KategoriID IS NULL OR KategoriID = p_KategoriID)
      AND (p_BasimYiliMin IS NULL OR BasimYili >= p_BasimYiliMin)
      AND (p_BasimYiliMax IS NULL OR BasimYili <= p_BasimYiliMax)
      AND (NOT p_SadeceMevcut OR MevcutAdet > 0);
END;
$$ LANGUAGE plpgsql;