import sys
from datetime import datetime

from kisiler import Calisan, Doktor, Hasta, Yonetici
from sistem import KlinikSistemi


GUN_ADLARI = {
    1: "Pazartesi",
    2: "Salı",
    3: "Çarşamba",
    4: "Perşembe",
    5: "Cuma",
    6: "Cumartesi",
    7: "Pazar",
}


def kurumlari_goster(sistem):
    kurumlar = sistem.kurumlari_listele()

    if len(kurumlar) == 0:
        print("Henüz kayıtlı kurum yok.")
        return

    for kurum in kurumlar:
        print(f"{kurum.id} - {kurum.ad}")

        if len(kurum.subeler) == 0:
            print("  Şube eklenmemiş.")
        else:
            for sube in kurum.subeler:
                print(f"  {sube.id} - {sube.ad}")

                for gun in sorted(sube.calisma_saatleri):
                    acilis, kapanis = sube.calisma_saatleri[gun]
                    print(f"    {GUN_ADLARI[gun]}: {acilis:%H:%M} - {kapanis:%H:%M}")

                for bolum in sube.bolumler:
                    print(f"    Bölüm {bolum.id}: {bolum.ad}")

                for hizmet in sube.hizmetler:
                    print(f"    Hizmet {hizmet.id}: {hizmet.ad} (bölüm {hizmet.bolum_id})")
                    print(f"      {hizmet.sure_dakika} dakika, {hizmet.ucret_tl} TL")


def sayi_oku(soru):
    giris = input(soru).strip()

    if not giris.isdigit():
        print("Geçerli bir sayı yazın.")
        return None

    return int(giris)


def saat_oku(soru):
    giris = input(soru).strip()

    try:
        return datetime.strptime(giris, "%H:%M").time()
    except ValueError:
        print("Saati 09:00 gibi yazın.")
        return None


def tarih_saat_oku(soru):
    giris = input(soru).strip()

    try:
        return datetime.strptime(giris, "%d.%m.%Y %H:%M")
    except ValueError:
        print("Tarih ve saati 25.10.2026 09:00 gibi yazın.")
        return None


def sube_sec(sistem, yonetici):
    sube_sayisi = 0

    for kurum in sistem.kurumlari_listele():
        sube_sayisi += len(kurum.subeler)

    if sube_sayisi == 0:
        print("Önce bir şube ekleyin.")
        return None

    kurumlari_goster(sistem)
    sube_no = sayi_oku("Şube numarası: ")

    if sube_no is None:
        return None

    sube = sistem.sube_bul(sube_no)

    if sube is None:
        print("Şube bulunamadı.")
        return None

    if sube.kurum_id != yonetici.kurum_id:
        print("Bu şube başka bir kuruma ait.")
        return None

    return sube


def kurum_ekle_ekrani(sistem):
    ad = input("Kurum adı: ")

    try:
        kurum = sistem.kurum_ekle(ad)
        print(f"{kurum.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def sube_ekle_ekrani(sistem, yonetici):
    ad = input("Şube adı: ")

    try:
        sube = sistem.sube_ekle(yonetici.kurum_id, ad)
        print(f"{sube.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def bolum_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = input("Bölüm adı: ")

    try:
        bolum = sistem.bolum_ekle(sube.id, ad)
        print(f"{bolum.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def hizmet_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    if len(sube.bolumler) == 0:
        print("Önce bu şubeye bölüm ekleyin.")
        return

    bolum_no = sayi_oku("Bölüm numarası: ")

    if bolum_no is None:
        return

    bolum_bulundu = False

    for bolum in sube.bolumler:
        if bolum.id == bolum_no:
            bolum_bulundu = True
            break

    if not bolum_bulundu:
        print("Bölüm bu şubede bulunamadı.")
        return

    ad = input("Hizmet adı: ")
    sure = sayi_oku("Süre (dakika): ")

    if sure is None:
        return

    ucret = sayi_oku("Ücret (TL): ")

    if ucret is None:
        return

    try:
        hizmet = sistem.hizmet_ekle(sube.id, bolum_no, ad, sure, ucret)
        print(f"{hizmet.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def calisma_saati_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    print("Günler: 1 Pazartesi, 2 Salı, 3 Çarşamba, 4 Perşembe")
    print("       5 Cuma, 6 Cumartesi, 7 Pazar")
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
        print("Çalışma saati kaydedildi.")
    except ValueError as hata:
        print(hata)


def kullanicilari_goster(sistem):
    if len(sistem.kullanicilari_listele()) == 0:
        print("Henüz kayıtlı kullanıcı yok.")
        return

    for kullanici in sistem.kullanicilari_listele():
        bilgi = f"{kullanici.id} - {kullanici.ad} ({kullanici.unvan()})"

        if isinstance(kullanici, Doktor):
            bilgi += f", şube {kullanici.sube_id}, {kullanici.uzmanlik}"
        elif isinstance(kullanici, Calisan):
            bilgi += f", şube {kullanici.sube_id}"
        elif isinstance(kullanici, Yonetici):
            bilgi += f", kurum {kullanici.kurum_id}"

        print(bilgi)


def hasta_ekle_ekrani(sistem):
    ad = input("Hasta adı: ")

    try:
        hasta = sistem.hasta_ekle(ad)
        print(f"{hasta.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def doktor_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = input("Doktor adı: ")
    uzmanlik = input("Uzmanlık alanı: ")

    try:
        doktor = sistem.doktor_ekle(ad, sube.id, uzmanlik)
        print(f"{doktor.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def personel_ekle_ekrani(sistem, yonetici):
    sube = sube_sec(sistem, yonetici)

    if sube is None:
        return

    ad = input("Sağlık personeli adı: ")

    try:
        personel = sistem.personel_ekle(ad, sube.id)
        print(f"{personel.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def yonetici_ekle_ekrani(sistem, kurum_id):
    ad = input("Yönetici adı: ")

    try:
        yonetici = sistem.yonetici_ekle(ad, kurum_id)
        print(f"{yonetici.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def calisan_sec(sistem, yonetici):
    calisan_var = False

    for kullanici in sistem.kullanicilari_listele():
        if isinstance(kullanici, Calisan):
            sube = sistem.sube_bul(kullanici.sube_id)

            if sube.kurum_id == yonetici.kurum_id:
                print(f"{kullanici.id} - {kullanici.ad} ({kullanici.unvan()})")
                calisan_var = True

    if not calisan_var:
        print("Önce çalışan ekleyin.")
        return None

    calisan_no = sayi_oku("Çalışan numarası: ")

    if calisan_no is None:
        return None

    calisan = sistem.calisani_bul(calisan_no)

    if calisan is None:
        print("Çalışan bulunamadı.")
        return None

    sube = sistem.sube_bul(calisan.sube_id)

    if sube.kurum_id != yonetici.kurum_id:
        print("Bu çalışan başka bir kuruma ait.")
        return None

    return calisan


def hizmet_ata_ekrani(sistem, yonetici):
    calisan = calisan_sec(sistem, yonetici)

    if calisan is None:
        return

    sube = sistem.sube_bul(calisan.sube_id)

    if len(sube.hizmetler) == 0:
        print("Önce çalışanın şubesine hizmet ekleyin.")
        return

    for hizmet in sube.hizmetler:
        print(f"{hizmet.id} - {hizmet.ad}")

    hizmet_no = sayi_oku("Hizmet numarası: ")

    if hizmet_no is None:
        return

    try:
        hizmet = sistem.calisana_hizmet_ata(calisan.id, hizmet_no)
        print(f"{hizmet.ad}, {calisan.ad} için eklendi.")
    except ValueError as hata:
        print(hata)


def uygunluklari_goster(calisan):
    if len(calisan.uygunluklar) == 0:
        print("Henüz uygunluk eklenmedi.")
        return

    for uygunluk in calisan.uygunluklar:
        print(f"{uygunluk.baslangic:%d.%m.%Y %H:%M} - {uygunluk.bitis:%H:%M}")


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
        print("Uygunluk eklendi.")
    except ValueError as hata:
        print(hata)


def uygunluk_listele_ekrani(sistem, yonetici):
    calisan = calisan_sec(sistem, yonetici)

    if calisan is not None:
        uygunluklari_goster(calisan)


def ilk_kurulum(sistem):
    while True:
        print("\nİlk kurulum")
        print("1 - Kurum ekle")
        print("2 - Yönetici ekle")
        print("0 - Çıkış")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            kurum_ekle_ekrani(sistem)

        elif secim == "2":
            if len(sistem.kurumlari_listele()) == 0:
                print("Önce bir kurum ekleyin.")
                continue

            kurumlari_goster(sistem)
            kurum_no = sayi_oku("Kurum numarası: ")

            if kurum_no is None:
                continue

            if sistem.kurumu_bul(kurum_no) is None:
                print("Kurum bulunamadı.")
                continue

            yonetici_ekle_ekrani(sistem, kurum_no)

            for kullanici in sistem.kullanicilari_listele():
                if isinstance(kullanici, Yonetici):
                    return True

        elif secim == "0":
            return False

        else:
            print("Geçersiz seçim.")


def kullanici_sec(sistem):
    print("\nKullanıcı seçin")
    kullanicilari_goster(sistem)
    kullanici_no = sayi_oku("Kullanıcı numarası (0 çıkış): ")

    if kullanici_no is None or kullanici_no == 0:
        return kullanici_no

    kullanici = sistem.kullaniciyi_bul(kullanici_no)

    if kullanici is None:
        print("Kullanıcı bulunamadı.")

    return kullanici


def yonetici_menu(sistem, yonetici):
    while True:
        print(f"\nYönetici: {yonetici.ad}")
        print("1 - Kurum ve şubeleri listele")
        print("2 - Şube ekle")
        print("3 - Bölüm ekle")
        print("4 - Hizmet ekle")
        print("5 - Çalışma saati ayarla")
        print("6 - Hasta ekle")
        print("7 - Doktor ekle")
        print("8 - Sağlık personeli ekle")
        print("9 - Yönetici ekle")
        print("10 - Çalışana hizmet ata")
        print("11 - Kullanıcıları listele")
        print("12 - Çalışan uygunluğu ekle")
        print("13 - Çalışan uygunluklarını listele")
        print("0 - Kullanıcı değiştir")
        secim = input("Seçiminiz: ").strip()

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
        elif secim == "0":
            return
        else:
            print("Geçersiz seçim.")


def hasta_menu(sistem, hasta):
    while True:
        print(f"\nHasta: {hasta.ad}")
        print("1 - Kurum ve şubeleri listele")
        print("0 - Kullanıcı değiştir")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            kurumlari_goster(sistem)
        elif secim == "0":
            return
        else:
            print("Geçersiz seçim.")


def calisan_menu(sistem, calisan):
    while True:
        print(f"\n{calisan.unvan()}: {calisan.ad}")
        print("1 - Kendi hizmetlerimi gör")
        print("2 - Uygunluklarımı gör")
        print("0 - Kullanıcı değiştir")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            sube = sistem.sube_bul(calisan.sube_id)

            if len(calisan.hizmet_idleri) == 0:
                print("Henüz hizmet atanmadı.")

            for hizmet in sube.hizmetler:
                if hizmet.id in calisan.hizmet_idleri:
                    print(f"{hizmet.id} - {hizmet.ad}")

        elif secim == "2":
            uygunluklari_goster(calisan)
        elif secim == "0":
            return
        else:
            print("Geçersiz seçim.")


def main():
    # yönlendirilmiş çıktıda türkçe harfler bozulmasın
    sys.stdout.reconfigure(encoding="utf-8")
    sistem = KlinikSistemi()

    if not ilk_kurulum(sistem):
        print("Görüşmek üzere.")
        return

    while True:
        kullanici = kullanici_sec(sistem)

        if kullanici == 0:
            print("Görüşmek üzere.")
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
