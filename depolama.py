import json
import os
from datetime import datetime, time
from pathlib import Path

from kurum import Bolum, Hizmet, Kurum, Sube
from kisiler import Calisan, Doktor, Hasta, SaglikPersoneli, Yonetici
from randevu import Randevu, Uygunluk
from sistem import KlinikSistemi


def sistemi_sozluge_cevir(sistem):
    veri = {"kurumlar": [], "kullanicilar": [], "randevular": []}

    for kurum in sistem.kurumlar:
        kurum_verisi = {"id": kurum.id, "ad": kurum.ad, "subeler": []}

        for sube in kurum.subeler:
            sube_verisi = {
                "id": sube.id,
                "ad": sube.ad,
                "calisma_saatleri": {},
                "bolumler": [],
                "hizmetler": [],
            }

            for gun, saatler in sube.calisma_saatleri.items():
                acilis, kapanis = saatler
                sube_verisi["calisma_saatleri"][str(gun)] = [acilis.isoformat(), kapanis.isoformat()]

            for bolum in sube.bolumler:
                sube_verisi["bolumler"].append({"id": bolum.id, "ad": bolum.ad})

            for hizmet in sube.hizmetler:
                sube_verisi["hizmetler"].append({
                    "id": hizmet.id,
                    "bolum_id": hizmet.bolum_id,
                    "ad": hizmet.ad,
                    "sure_dakika": hizmet.sure_dakika,
                    "ucret_tl": hizmet.ucret_tl,
                })

            kurum_verisi["subeler"].append(sube_verisi)

        veri["kurumlar"].append(kurum_verisi)

    for kullanici in sistem.kullanicilar:
        kullanici_verisi = {"id": kullanici.id, "ad": kullanici.ad}

        if isinstance(kullanici, Doktor):
            kullanici_verisi["tur"] = "doktor"
            kullanici_verisi["sube_id"] = kullanici.sube_id
            kullanici_verisi["uzmanlik"] = kullanici.uzmanlik
        elif isinstance(kullanici, SaglikPersoneli):
            kullanici_verisi["tur"] = "personel"
            kullanici_verisi["sube_id"] = kullanici.sube_id
        elif isinstance(kullanici, Hasta):
            kullanici_verisi["tur"] = "hasta"
        elif isinstance(kullanici, Yonetici):
            kullanici_verisi["tur"] = "yonetici"
            kullanici_verisi["kurum_id"] = kullanici.kurum_id

        if isinstance(kullanici, Calisan):
            kullanici_verisi["hizmet_idleri"] = kullanici.hizmet_idleri[:]
            kullanici_verisi["uygunluklar"] = []

            for uygunluk in kullanici.uygunluklar:
                kullanici_verisi["uygunluklar"].append({
                    "baslangic": uygunluk.baslangic.isoformat(),
                    "bitis": uygunluk.bitis.isoformat(),
                })

        veri["kullanicilar"].append(kullanici_verisi)

    for randevu in sistem.randevular:
        veri["randevular"].append({
            "id": randevu.id,
            "hasta_id": randevu.hasta_id,
            "calisan_id": randevu.calisan_id,
            "hizmet_id": randevu.hizmet_id,
            "sube_id": randevu.sube_id,
            "baslangic": randevu.baslangic.isoformat(),
            "sure_dakika": randevu.sure_dakika,
            "ucret_tl": randevu.ucret_tl,
            "durum": randevu.durum,
        })

    return veri


def sozlukten_sistem_kur(veri):
    sistem = KlinikSistemi()

    for kurum_verisi in veri["kurumlar"]:
        kurum = Kurum(kurum_verisi["id"], kurum_verisi["ad"])
        sistem.kurumlar.append(kurum)
        sistem.son_kurum_id = max(sistem.son_kurum_id, kurum.id)

        for sube_verisi in kurum_verisi["subeler"]:
            sube = Sube(sube_verisi["id"], kurum.id, sube_verisi["ad"])
            kurum.sube_ekle(sube)
            sistem.son_sube_id = max(sistem.son_sube_id, sube.id)

            for gun, saatler in sube_verisi["calisma_saatleri"].items():
                acilis = time.fromisoformat(saatler[0])
                kapanis = time.fromisoformat(saatler[1])
                sube.calisma_saati_ayarla(int(gun), acilis, kapanis)

            for bolum_verisi in sube_verisi["bolumler"]:
                bolum = Bolum(bolum_verisi["id"], sube.id, bolum_verisi["ad"])
                sube.bolum_ekle(bolum)
                sistem.son_bolum_id = max(sistem.son_bolum_id, bolum.id)

            for hizmet_verisi in sube_verisi["hizmetler"]:
                hizmet = Hizmet(
                    hizmet_verisi["id"],
                    sube.id,
                    hizmet_verisi["bolum_id"],
                    hizmet_verisi["ad"],
                    hizmet_verisi["sure_dakika"],
                    hizmet_verisi["ucret_tl"],
                )
                sube.hizmet_ekle(hizmet)
                sistem.son_hizmet_id = max(sistem.son_hizmet_id, hizmet.id)

    for kullanici_verisi in veri["kullanicilar"]:
        tur = kullanici_verisi["tur"]
        id = kullanici_verisi["id"]
        ad = kullanici_verisi["ad"]

        if tur == "hasta":
            kullanici = Hasta(id, ad)
        elif tur == "doktor":
            kullanici = Doktor(id, ad, kullanici_verisi["sube_id"], kullanici_verisi["uzmanlik"])
        elif tur == "personel":
            kullanici = SaglikPersoneli(id, ad, kullanici_verisi["sube_id"])
        elif tur == "yonetici":
            kullanici = Yonetici(id, ad, kullanici_verisi["kurum_id"])
        else:
            raise ValueError("Bilinmeyen kullanıcı türü.")

        sistem.kullanicilar.append(kullanici)
        sistem.son_kullanici_id = max(sistem.son_kullanici_id, kullanici.id)

        if isinstance(kullanici, Calisan):
            for hizmet_id in kullanici_verisi["hizmet_idleri"]:
                sistem.calisana_hizmet_ata(kullanici.id, hizmet_id)

            for uygunluk_verisi in kullanici_verisi["uygunluklar"]:
                uygunluk = Uygunluk(
                    kullanici.id,
                    datetime.fromisoformat(uygunluk_verisi["baslangic"]),
                    datetime.fromisoformat(uygunluk_verisi["bitis"]),
                )
                kullanici.uygunluklar.append(uygunluk)

    for randevu_verisi in veri["randevular"]:
        randevu = Randevu(
            randevu_verisi["id"],
            randevu_verisi["hasta_id"],
            randevu_verisi["calisan_id"],
            randevu_verisi["hizmet_id"],
            randevu_verisi["sube_id"],
            datetime.fromisoformat(randevu_verisi["baslangic"]),
            randevu_verisi["sure_dakika"],
            randevu_verisi["ucret_tl"],
        )

        if randevu_verisi["durum"] == "onaylandi":
            randevu.onayla()
        elif randevu_verisi["durum"] != "beklemede":
            raise ValueError("Bilinmeyen randevu durumu.")

        sistem.randevular.append(randevu)
        sistem.son_randevu_id = max(sistem.son_randevu_id, randevu.id)

    return sistem


def kaydet(sistem, dosya_yolu):
    dosya_yolu = Path(dosya_yolu)
    gecici_dosya = Path(str(dosya_yolu) + ".tmp")
    veri = sistemi_sozluge_cevir(sistem)

    with gecici_dosya.open("w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=2)

    os.replace(gecici_dosya, dosya_yolu)


def yukle(dosya_yolu):
    dosya_yolu = Path(dosya_yolu)

    if not dosya_yolu.exists():
        return KlinikSistemi()

    try:
        with dosya_yolu.open("r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        return sozlukten_sistem_kur(veri)
    except (OSError, KeyError, TypeError, ValueError) as hata:
        raise ValueError("Veri dosyası okunamadı. Dosya değiştirilmedi.") from hata
