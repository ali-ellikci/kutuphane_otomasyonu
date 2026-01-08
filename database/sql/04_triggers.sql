-- Yeni Ödünç verince mevcutge adet azaltacak log tablosuna yazacak
CREATE OR REPLACE FUNCTION trg_odunc_insert()
RETURN TRIGGER AS $$
BEGIN 
    UPDATE KITAP
    SET MevcutAdet = MevcutAdet - 1
    WHERE KitapID = NEW.KitapID;

    INSERT INTO LOG_ISLEM(TabloAdi, IslemTipi, Aciklama)
    VALUES ('ODUNC', 'INSERT', 'Yeni ödünç kaydı eklendi: OduncID=' || NEW.OduncID);

    RETURN NEW;

END;
$$ LANGUAGE plpsql;

CREATE TRIGGER TR_ODUNC_INSERT
AFTER INSERT ON ODUNC
FOR EACH ROW
EXECUTE FUNCTION trg_odunc_insert();




-- Teslim tarihi null'dan dolu bir dpere geçnice mevcutu bir arttır ve log yaz 
CREATE OR REPLACE FUNCTION trg_odunc_update_teslim()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.TeslimTarihi IS NULL AND NEW.TeslimTarihi IS NOT NULL THEN
        -- Kitap mevcut adedini 1 arttır
        UPDATE KITAP
        SET MevcutAdet = MevcutAdet + 1
        WHERE KitapID = NEW.KitapID;

        -- Log kaydı ekle
        INSERT INTO LOG_ISLEM(TabloAdi, IslemTipi, Aciklama)
        VALUES ('ODUNC', 'UPDATE', 'OduncID=' || NEW.OduncID || ' teslim alındı.');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Yeni ceza ekleninde ToplamBorç bir artsın ve log düşsün
CREATE TRIGGER TR_ODUNC_UPDATE_TESLIM
AFTER UPDATE ON ODUNC
FOR EACH ROW
EXECUTE FUNCTION trg_odunc_update_teslim();

CREATE OR REPLACE FUNCTION trg_ceza_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Üyenin toplam borcunu güncelle
    UPDATE UYE
    SET ToplamBorc = ToplamBorc + NEW.Tutar
    WHERE UyeID = (SELECT UyeID FROM ODUNC WHERE OduncID = NEW.OduncID);

    -- Log kaydı ekle
    INSERT INTO LOG_ISLEM(TabloAdi, IslemTipi, Aciklama)
    VALUES ('CEZA', 'INSERT', 'Yeni ceza eklendi: CezaID=' || NEW.CezaID);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_CEZA_INSERT
AFTER INSERT ON CEZA
FOR EACH ROW
EXECUTE FUNCTION trg_ceza_insert();





-- Aktif ödünç veya borç var ise üyenin silinmesini engelle
CREATE OR REPLACE FUNCTION trg_uye_delete_block()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM ODUNC WHERE UyeID = OLD.UyeID AND TeslimTarihi IS NULL) > 0
       OR OLD.ToplamBorc > 0 THEN
        RAISE EXCEPTION 'Üye silinemez: aktif ödünç veya borç mevcut.';
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_UYE_DELETE_BLOCK
BEFORE DELETE ON UYE
FOR EACH ROW
EXECUTE FUNCTION trg_uye_delete_block();

