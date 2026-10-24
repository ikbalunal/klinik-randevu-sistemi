import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

from depolama import kaydet, yukle
from kisiler import Calisan, Doktor, Hasta, Yonetici


GUN_ADLARI = {
    1: "Pazartesi",
    2: "Salı",
    3: "Çarşamba",
    4: "Perşembe",
    5: "Cuma",
    6: "Cumartesi",
    7: "Pazar",
}
VERI_DOSYASI = Path(__file__).with_name("veriler.json")


def renkli(metin, renk):
    if not sys.stdout.isatty():
        return metin

    renkler = {
        "baslik": "\033[1;36m",
        "secim": "\033[36m",
        "basari": "\033[32m",
        "hata": "\033[31m",
    }
    return f"{renkler[renk]}{metin}\033[0m"


def cizgi():
    genislik = shutil.get_terminal_size((64, 20)).columns - 4

    if genislik > 60:
        genislik = 60
    if genislik < 20:
        genislik = 20

    return "─" * genislik


def baslik_goster(baslik, aciklama=""):
    print()
    print("  " + renkli(cizgi(), "secim"))
    print("  " + renkli(baslik, "baslik"))

    if aciklama:
        print("  " + aciklama)

    print("  " + renkli(cizgi(), "secim"))


def menu_goster(baslik, secenekler, aciklama=""):
    baslik_goster(baslik, aciklama)

    for numara, metin in secenekler:
        numara_metni = renkli(f"{numara:>2}", "secim")
        print(f"  {numara_metni}  {metin}")

    print()


def liste_basligi(baslik):
    print()
    print("  " + renkli(baslik, "baslik"))
    print("  " + renkli("─" * 36, "secim"))


def liste_satiri(numara, metin, ayrinti=""):
    numara_metni = renkli(f"{numara:>3}", "secim")
    print(f"  {numara_metni}  {metin}")

    if ayrinti:
        print(f"       {ayrinti}")


def durum_yaz(metin, tur="bilgi"):
    simgeler = {"bilgi": "·", "basari": "✓", "hata": "!"}
    simge = simgeler[tur]

    if tur == "basari" or tur == "hata":
        simge = renkli(simge, tur)

    print(f"  {simge} {metin}")


def girdi_oku(soru):
    return input("  › " + soru)


def verileri_kaydet(sistem):
    try:
        kaydet(sistem, VERI_DOSYASI)
    except OSError as hata:
        durum_yaz(f"Veriler kaydedilemedi: {hata}", "hata")
        raise SystemExit(1)


def kurumlari_goster(sistem):
    kurumlar = sistem.kurumlari_listele()
    liste_basligi("Kurumlar ve şubeler")

    if len(kurumlar) == 0:
        durum_yaz("Henüz kayıtlı kurum yok.")
        return

    for kurum in kurumlar:
        liste_satiri(kurum.id, kurum.ad)

        if len(kurum.subeler) == 0:
            print("       Şube eklenmemiş.")
        else:
            for sube in kurum.subeler:
                print(f"       ↳ {renkli(str(sube.id), 'secim')}  {sube.ad}")

                for gun in sorted(sube.calisma_saatleri):
                    acilis, kapanis = sube.calisma_saatleri[gun]
                    print(f"           {GUN_ADLARI[gun]}: {acilis:%H:%M} - {kapanis:%H:%M}")

                for bolum in sube.bolumler:
                    print(f"           Bölüm {bolum.id}: {bolum.ad}")

                for hizmet in sube.hizmetler:
                    print(f"           Hizmet {hizmet.id}: {hizmet.ad} (bölüm {hizmet.bolum_id})")
                    print(f"             {hizmet.sure_dakika} dakika · {hizmet.ucret_tl} TL")


def sayi_oku(soru):
    giris = girdi_oku(soru).strip()

    if not giris.isdigit():
        durum_yaz("Geçerli bir sayı yazın.", "hata")
        return None

    return int(giris)


def saat_oku(soru):
    giris = girdi_oku(soru).strip()

    try:
        return datetime.strptime(giris, "%H:%M").time()
    except ValueError:
        durum_yaz("Saati 09:00 gibi yazın.", "hata")
        return None


def tarih_saat_oku(soru):
    giris = girdi_oku(soru).strip()

    try:
        return datetime.strptime(giris, "%d.%m.%Y %H:%M")
    except ValueError:
        durum_yaz("Tarih ve saati 25.10.2026 09:00 gibi yazın.", "hata")
        return None


def sube_sec(sistem, yonetici):
    sube_sayisi = 0

    for kurum in sistem.kurumlari_listele():
        sube_sayisi += len(kurum.subeler)

    if sube_sayisi == 0:
        durum_yaz("Önce bir şube ekleyin.")
        return None

    kurumlari_goster(sistem)
    sube_no = sayi_oku("Şube numarası: ")

    if sube_no is None:
        return None

    sube = sistem.sube_bul(sube_no)

    if sube is None:
        durum_yaz("Şube bulunamadı.", "hata")
        return None

    if sube.kurum_id != yonetici.kurum_id:
        durum_yaz("Bu şube başka bir kuruma ait.", "hata")
        return None

    return sube


def kurum_ekle_ekrani(sistem):
    ad = girdi_oku("Kurum adı: ")

    try:
        kurum = sistem.kurum_ekle(ad)
        verileri_kaydet(sistem)
        durum_yaz(f"{kurum.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def yeni_kurum_ekrani(sistem, yonetici):
    kurum_adi = girdi_oku("Yeni kurum adı: ")
    yonetici_adi = girdi_oku("Yeni kurumun yöneticisi: ")

    try:
        kurum, yeni_yonetici = sistem.yeni_kurum_ve_yonetici_ekle(
            yonetici.id, kurum_adi, yonetici_adi
        )
        verileri_kaydet(sistem)
        mesaj = f"{kurum.ad} eklendi. Yönetici: {yeni_yonetici.ad}"
        durum_yaz(f"{mesaj} (numara {yeni_yonetici.id}).", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def sube_ekle_ekrani(sistem, yonetici):
    ad = girdi_oku("Şube adı: ")

    try:
        sube = sistem.sube_ekle(yonetici.kurum_id, ad)
        verileri_kaydet(sistem)
        durum_yaz(f"{sube.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def bolum_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = girdi_oku("Bölüm adı: ")

    try:
        bolum = sistem.bolum_ekle(sube.id, ad)
        verileri_kaydet(sistem)
        durum_yaz(f"{bolum.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def hizmet_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    if len(sube.bolumler) == 0:
        durum_yaz("Önce bu şubeye bölüm ekleyin.")
        return

    liste_basligi("Bu şubenin bölümleri")
    for bolum in sube.bolumler:
        liste_satiri(bolum.id, bolum.ad)

    bolum_no = sayi_oku("Bölüm numarası: ")

    if bolum_no is None:
        return

    bolum_bulundu = False

    for bolum in sube.bolumler:
        if bolum.id == bolum_no:
            bolum_bulundu = True
            break

    if not bolum_bulundu:
        durum_yaz("Bölüm bu şubede bulunamadı.", "hata")
        return

    ad = girdi_oku("Hizmet adı: ")
    sure = sayi_oku("Süre (dakika): ")

    if sure is None:
        return

    ucret = sayi_oku("Ücret (TL): ")

    if ucret is None:
        return

    try:
        hizmet = sistem.hizmet_ekle(sube.id, bolum_no, ad, sure, ucret)
        verileri_kaydet(sistem)
        durum_yaz(f"{hizmet.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def calisma_saati_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    liste_basligi("Haftanın günleri")
    for gun_numarasi, gun_adi in GUN_ADLARI.items():
        liste_satiri(gun_numarasi, gun_adi)
    gun = sayi_oku("Gün numarası: ")

    if gun is None:
        return

    acilis = saat_oku("Açılış saati: ")

    if acilis is None:
        return

    kapanis = saat_oku("Kapanış saati: ")

    if kapanis is None:
        return

    try:
        sistem.calisma_saati_ayarla(sube.id, gun, acilis, kapanis)
        verileri_kaydet(sistem)
        durum_yaz("Çalışma saati kaydedildi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def kullanicilari_goster(sistem):
    liste_basligi("Kullanıcılar")

    if len(sistem.kullanicilari_listele()) == 0:
        durum_yaz("Henüz kayıtlı kullanıcı yok.")
        return

    for kullanici in sistem.kullanicilari_listele():
        bilgi = f"{kullanici.ad}  ·  {kullanici.unvan()}"
        ayrinti = ""

        if isinstance(kullanici, Doktor):
            ayrinti = f"Şube {kullanici.sube_id} · {kullanici.uzmanlik}"
        elif isinstance(kullanici, Calisan):
            ayrinti = f"Şube {kullanici.sube_id}"
        elif isinstance(kullanici, Yonetici):
            ayrinti = f"Kurum {kullanici.kurum_id}"

        liste_satiri(kullanici.id, bilgi, ayrinti)


def hasta_ekle_ekrani(sistem):
    ad = girdi_oku("Hasta adı: ")

    try:
        hasta = sistem.hasta_ekle(ad)
        verileri_kaydet(sistem)
        durum_yaz(f"{hasta.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def doktor_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = girdi_oku("Doktor adı: ")
    uzmanlik = girdi_oku("Uzmanlık alanı: ")

    try:
        doktor = sistem.doktor_ekle(ad, sube.id, uzmanlik)
        verileri_kaydet(sistem)
        durum_yaz(f"{doktor.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def personel_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = girdi_oku("Sağlık personeli adı: ")

    try:
        personel = sistem.personel_ekle(ad, sube.id)
        verileri_kaydet(sistem)
        durum_yaz(f"{personel.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def yonetici_ekle_ekrani(sistem, kurum_id):
    ad = girdi_oku("Yönetici adı: ")

    try:
        yonetici = sistem.yonetici_ekle(ad, kurum_id)
        verileri_kaydet(sistem)
        durum_yaz(f"{yonetici.ad} eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def calisan_sec(sistem, yonetici):
    calisan_var = False
    liste_basligi("Çalışanlar")

    for kullanici in sistem.kullanicilari_listele():
        if isinstance(kullanici, Calisan):
            sube = sistem.sube_bul(kullanici.sube_id)

            if sube.kurum_id == yonetici.kurum_id:
                bilgi = f"{kullanici.ad}  ·  {kullanici.unvan()}"
                liste_satiri(kullanici.id, bilgi, sube.ad)
                calisan_var = True

    if not calisan_var:
        durum_yaz("Önce çalışan ekleyin.")
        return None

    calisan_no = sayi_oku("Çalışan numarası: ")

    if calisan_no is None:
        return None

    calisan = sistem.calisani_bul(calisan_no)

    if calisan is None:
        durum_yaz("Çalışan bulunamadı.", "hata")
        return None

    sube = sistem.sube_bul(calisan.sube_id)

    if sube.kurum_id != yonetici.kurum_id:
        durum_yaz("Bu çalışan başka bir kuruma ait.", "hata")
        return None

    return calisan


def hizmet_ata_ekrani(sistem, yonetici):
    calisan = calisan_sec(sistem, yonetici)

    if calisan is None:
        return

    sube = sistem.sube_bul(calisan.sube_id)

    if len(sube.hizmetler) == 0:
        durum_yaz("Önce çalışanın şubesine hizmet ekleyin.")
        return

    liste_basligi("Bu şubenin hizmetleri")

    for hizmet in sube.hizmetler:
        ayrinti = f"{hizmet.sure_dakika} dakika · {hizmet.ucret_tl} TL"
        liste_satiri(hizmet.id, hizmet.ad, ayrinti)

    hizmet_no = sayi_oku("Hizmet numarası: ")

    if hizmet_no is None:
        return

    try:
        hizmet = sistem.calisana_hizmet_ata(calisan.id, hizmet_no)
        verileri_kaydet(sistem)
        durum_yaz(f"{hizmet.ad}, {calisan.ad} için eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def uygunluklari_goster(calisan):
    liste_basligi("Uygunluk aralıkları")

    if len(calisan.uygunluklar) == 0:
        durum_yaz("Henüz uygunluk eklenmedi.")
        return

    for numara, uygunluk in enumerate(calisan.uygunluklar, start=1):
        aralik = f"{uygunluk.baslangic:%d.%m.%Y %H:%M} - {uygunluk.bitis:%H:%M}"
        liste_satiri(numara, aralik)


def dolu_saatleri_goster(sistem, calisan):
    liste_basligi("Dolu randevu saatleri:")
    dolu_saat_var = False

    for randevu in sistem.calisanin_randevulari(calisan.id):
        if randevu.durum in ("beklemede", "onaylandi"):
            aralik = f"{randevu.baslangic:%d.%m.%Y %H:%M} - {randevu.bitis:%H:%M}"
            liste_satiri(randevu.id, aralik)
            dolu_saat_var = True

    if not dolu_saat_var:
        durum_yaz("Dolu saat yok.")


def uygunluk_ekle_ekrani(sistem, yonetici):
    calisan = calisan_sec(sistem, yonetici)

    if calisan is None:
        return

    baslangic = tarih_saat_oku("Başlangıç (GG.AA.YYYY SS:DD): ")

    if baslangic is None:
        return

    bitis = tarih_saat_oku("Bitiş (GG.AA.YYYY SS:DD): ")

    if bitis is None:
        return

    try:
        sistem.uygunluk_ekle(calisan.id, baslangic, bitis)
        verileri_kaydet(sistem)
        durum_yaz("Uygunluk eklendi.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def uygunluk_listele_ekrani(sistem, yonetici):
    calisan = calisan_sec(sistem, yonetici)

    if calisan is not None:
        uygunluklari_goster(calisan)


def randevu_olustur_ekrani(sistem, hasta):
    hizmet_var = False
    liste_basligi("Hizmet seçin")

    for kurum in sistem.kurumlari_listele():
        for sube in kurum.subeler:
            for hizmet in sube.hizmetler:
                ad = f"{kurum.ad} / {sube.ad} / {hizmet.ad}"
                ayrinti = f"{hizmet.sure_dakika} dakika · {hizmet.ucret_tl} TL"
                liste_satiri(hizmet.id, ad, ayrinti)
                hizmet_var = True

    if not hizmet_var:
        durum_yaz("Henüz hizmet eklenmedi.")
        return

    hizmet_no = sayi_oku("Hizmet numarası: ")

    if hizmet_no is None:
        return

    hizmet = sistem.hizmeti_bul(hizmet_no)

    if hizmet is None:
        durum_yaz("Hizmet bulunamadı.", "hata")
        return

    calisan_var = False
    liste_basligi("Çalışan seçin")

    for kullanici in sistem.kullanicilari_listele():
        if isinstance(kullanici, Calisan):
            if kullanici.sube_id == hizmet.sube_id and hizmet.id in kullanici.hizmet_idleri:
                liste_satiri(kullanici.id, kullanici.ad, kullanici.unvan())
                calisan_var = True

    if not calisan_var:
        durum_yaz("Bu hizmet için çalışan bulunamadı.")
        return

    calisan_no = sayi_oku("Çalışan numarası: ")

    if calisan_no is None:
        return

    calisan = sistem.calisani_bul(calisan_no)

    if calisan is None:
        durum_yaz("Çalışan bulunamadı.", "hata")
        return

    if calisan.sube_id != hizmet.sube_id or hizmet.id not in calisan.hizmet_idleri:
        durum_yaz("Bu hizmet bu çalışana atanmamış.", "hata")
        return

    uygunluklari_goster(calisan)
    dolu_saatleri_goster(sistem, calisan)

    bos_araliklar = sistem.bos_randevu_araliklari(calisan.id, hizmet.id)
    liste_basligi(f"{hizmet.sure_dakika} dakikalık randevu için boş aralıklar:")

    if len(bos_araliklar) == 0:
        durum_yaz("Bu hizmet için boş aralık yok.")
        return

    for bos_baslangic, bos_bitis in bos_araliklar:
        son_baslangic = bos_bitis - timedelta(minutes=hizmet.sure_dakika)
        aralik = f"{bos_baslangic:%d.%m.%Y %H:%M} - {bos_bitis:%H:%M}"
        liste_satiri("•", aralik, f"en geç {son_baslangic:%H:%M} saatinde başlanabilir")

    baslangic = tarih_saat_oku("Randevu zamanı (GG.AA.YYYY SS:DD): ")

    if baslangic is None:
        return

    try:
        randevu = sistem.randevu_olustur(hasta.id, calisan_no, hizmet.id, baslangic)
        verileri_kaydet(sistem)
        durum_yaz(f"Randevu {randevu.id} oluşturuldu. Durum: {randevu.durum}.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def randevulari_goster(sistem, randevular):
    liste_basligi("Randevular")

    if len(randevular) == 0:
        durum_yaz("Henüz randevu yok.")
        return

    for randevu in randevular:
        hizmet = sistem.hizmeti_bul(randevu.hizmet_id)
        calisan = sistem.calisani_bul(randevu.calisan_id)
        hasta = sistem.kullaniciyi_bul(randevu.hasta_id)
        zaman = f"{randevu.baslangic:%d.%m.%Y %H:%M} - {randevu.bitis:%H:%M}"
        bilgi = f"{hizmet.ad} · {calisan.ad} · hasta: {hasta.ad}"
        ayrinti = f"{bilgi} · {randevu.ucret_tl} TL · {randevu.durum}"
        liste_satiri(randevu.id, zaman, ayrinti)


def bekleyen_randevulari_goster(sistem, yonetici):
    randevular = sistem.bekleyen_randevulari(yonetici.id)

    if len(randevular) == 0:
        durum_yaz("Bekleyen randevu yok.")
        return

    randevulari_goster(sistem, randevular)


def randevu_onay_ekrani(sistem, yonetici):
    randevular = sistem.bekleyen_randevulari(yonetici.id)

    if len(randevular) == 0:
        durum_yaz("Bekleyen randevu yok.")
        return

    randevulari_goster(sistem, randevular)
    randevu_no = sayi_oku("Onaylanacak randevu numarası: ")

    if randevu_no is None:
        return

    try:
        randevu = sistem.randevu_onayla(yonetici.id, randevu_no)
        verileri_kaydet(sistem)
        durum_yaz(f"Randevu {randevu.id} onaylandı.", "basari")
    except ValueError as hata:
        durum_yaz(str(hata), "hata")


def ilk_kurulum(sistem):
    while True:
        menu_goster("Klinik Randevu Sistemi", [
            (1, "Kurum ekle"),
            (2, "Yönetici ekle"),
            (0, "Çıkış"),
        ], "İlk kurulum")
        secim = girdi_oku("Seçiminiz: ").strip()

        if secim == "1":
            kurum_ekle_ekrani(sistem)

        elif secim == "2":
            if len(sistem.kurumlari_listele()) == 0:
                durum_yaz("Önce bir kurum ekleyin.")
                continue

            kurumlari_goster(sistem)
            kurum_no = sayi_oku("Kurum numarası: ")

            if kurum_no is None:
                continue

            if sistem.kurumu_bul(kurum_no) is None:
                durum_yaz("Kurum bulunamadı.", "hata")
                continue

            yonetici_ekle_ekrani(sistem, kurum_no)

            for kullanici in sistem.kullanicilari_listele():
                if isinstance(kullanici, Yonetici):
                    return True

        elif secim == "0":
            return False

        else:
            durum_yaz("Geçersiz seçim.", "hata")


def kullanici_sec(sistem):
    baslik_goster("Kullanıcı seçin", "İşlem yapmak için listedeki numarayı yazın.")
    kullanicilari_goster(sistem)
    kullanici_no = sayi_oku("Kullanıcı numarası (0 çıkış): ")

    if kullanici_no is None or kullanici_no == 0:
        return kullanici_no

    kullanici = sistem.kullaniciyi_bul(kullanici_no)

    if kullanici is None:
        durum_yaz("Kullanıcı bulunamadı.", "hata")

    return kullanici


def yonetici_menu(sistem, yonetici):
    while True:
        menu_goster(f"Yönetici  /  {yonetici.ad}", [
            (1, "Kurum ve şubeleri listele"),
            (2, "Şube ekle"),
            (3, "Bölüm ekle"),
            (4, "Hizmet ekle"),
            (5, "Çalışma saati ayarla"),
            (6, "Hasta ekle"),
            (7, "Doktor ekle"),
            (8, "Sağlık personeli ekle"),
            (9, "Yönetici ekle"),
            (10, "Çalışana hizmet ata"),
            (11, "Kullanıcıları listele"),
            (12, "Çalışan uygunluğu ekle"),
            (13, "Çalışan uygunluklarını listele"),
            (14, "Bekleyen randevuları listele"),
            (15, "Randevu onayla"),
            (16, "Yeni kurum ekle"),
            (0, "Kullanıcı değiştir"),
        ], "Kurum, çalışan ve randevu işlemleri")
        secim = girdi_oku("Seçiminiz: ").strip()

        if secim == "1":
            kurumlari_goster(sistem)
        elif secim == "2":
            sube_ekle_ekrani(sistem, yonetici)
        elif secim == "3":
            bolum_ekle_ekrani(sistem, yonetici)
        elif secim == "4":
            hizmet_ekle_ekrani(sistem, yonetici)
        elif secim == "5":
            calisma_saati_ekrani(sistem, yonetici)
        elif secim == "6":
            hasta_ekle_ekrani(sistem)
        elif secim == "7":
            doktor_ekle_ekrani(sistem, yonetici)
        elif secim == "8":
            personel_ekle_ekrani(sistem, yonetici)
        elif secim == "9":
            yonetici_ekle_ekrani(sistem, yonetici.kurum_id)
        elif secim == "10":
            hizmet_ata_ekrani(sistem, yonetici)
        elif secim == "11":
            kullanicilari_goster(sistem)
        elif secim == "12":
            uygunluk_ekle_ekrani(sistem, yonetici)
        elif secim == "13":
            uygunluk_listele_ekrani(sistem, yonetici)
        elif secim == "14":
            bekleyen_randevulari_goster(sistem, yonetici)
        elif secim == "15":
            randevu_onay_ekrani(sistem, yonetici)
        elif secim == "16":
            yeni_kurum_ekrani(sistem, yonetici)
        elif secim == "0":
            return
        else:
            durum_yaz("Geçersiz seçim.", "hata")


def hasta_menu(sistem, hasta):
    while True:
        menu_goster(f"Hasta  /  {hasta.ad}", [
            (1, "Kurum ve şubeleri listele"),
            (2, "Randevu oluştur"),
            (3, "Randevularımı gör"),
            (0, "Kullanıcı değiştir"),
        ])
        secim = girdi_oku("Seçiminiz: ").strip()

        if secim == "1":
            kurumlari_goster(sistem)
        elif secim == "2":
            randevu_olustur_ekrani(sistem, hasta)
        elif secim == "3":
            randevulari_goster(sistem, sistem.hastanin_randevulari(hasta.id))
        elif secim == "0":
            return
        else:
            durum_yaz("Geçersiz seçim.", "hata")


def calisan_menu(sistem, calisan):
    while True:
        menu_goster(f"{calisan.unvan()}  /  {calisan.ad}", [
            (1, "Kendi hizmetlerimi gör"),
            (2, "Uygunluklarımı gör"),
            (3, "Randevularımı gör"),
            (0, "Kullanıcı değiştir"),
        ])
        secim = girdi_oku("Seçiminiz: ").strip()

        if secim == "1":
            sube = sistem.sube_bul(calisan.sube_id)
            liste_basligi("Hizmetlerim")

            if len(calisan.hizmet_idleri) == 0:
                durum_yaz("Henüz hizmet atanmadı.")

            for hizmet in sube.hizmetler:
                if hizmet.id in calisan.hizmet_idleri:
                    liste_satiri(hizmet.id, hizmet.ad, f"{hizmet.sure_dakika} dakika")

        elif secim == "2":
            uygunluklari_goster(calisan)
        elif secim == "3":
            randevulari_goster(sistem, sistem.calisanin_randevulari(calisan.id))
        elif secim == "0":
            return
        else:
            durum_yaz("Geçersiz seçim.", "hata")


def main():
    # yönlendirilmiş çıktıda türkçe harfler bozulmasın
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sistem = yukle(VERI_DOSYASI)
    except ValueError as hata:
        durum_yaz(str(hata), "hata")
        return

    yonetici_var = False

    for kullanici in sistem.kullanicilari_listele():
        if isinstance(kullanici, Yonetici):
            yonetici_var = True
            break

    if not yonetici_var:
        if not ilk_kurulum(sistem):
            durum_yaz("Görüşmek üzere.")
            return

    while True:
        kullanici = kullanici_sec(sistem)

        if kullanici == 0:
            durum_yaz("Görüşmek üzere.")
            break

        if kullanici is None:
            continue

        if isinstance(kullanici, Yonetici):
            yonetici_menu(sistem, kullanici)
        elif isinstance(kullanici, Hasta):
            hasta_menu(sistem, kullanici)
        elif isinstance(kullanici, Calisan):
            calisan_menu(sistem, kullanici)


if __name__ == "__main__":
    main()
