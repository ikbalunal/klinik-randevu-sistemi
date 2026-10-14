import sys
from datetime import datetime

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


def sube_sec(sistem):
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

    return sube


def kurum_ekle_ekrani(sistem):
    ad = input("Kurum adı: ")

    try:
        kurum = sistem.kurum_ekle(ad)
        print(f"{kurum.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def sube_ekle_ekrani(sistem):
    if len(sistem.kurumlari_listele()) == 0:
        print("Önce bir kurum ekleyin.")
        return

    kurumlari_goster(sistem)
    kurum_no = sayi_oku("Kurum numarası: ")

    if kurum_no is None:
        return

    if sistem.kurumu_bul(kurum_no) is None:
        print("Kurum bulunamadı.")
        return

    ad = input("Şube adı: ")

    try:
        sube = sistem.sube_ekle(kurum_no, ad)
        print(f"{sube.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def bolum_ekle_ekrani(sistem):
    sube = sube_sec(sistem)

    if sube is None:
        return

    ad = input("Bölüm adı: ")

    try:
        bolum = sistem.bolum_ekle(sube.id, ad)
        print(f"{bolum.ad} eklendi.")
    except ValueError as hata:
        print(hata)


def hizmet_ekle_ekrani(sistem):
    sube = sube_sec(sistem)

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


def calisma_saati_ekrani(sistem):
    sube = sube_sec(sistem)

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


def main():
    # yönlendirilmiş çıktıda türkçe harfler bozulmasın
    sys.stdout.reconfigure(encoding="utf-8")
    sistem = KlinikSistemi()

    while True:
        print("\nKlinik Randevu Sistemi")
        print("1 - Kurum ve şubeleri listele")
        print("2 - Kurum ekle")
        print("3 - Şube ekle")
        print("4 - Bölüm ekle")
        print("5 - Hizmet ekle")
        print("6 - Çalışma saati ayarla")
        print("0 - Çıkış")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            kurumlari_goster(sistem)

        elif secim == "2":
            kurum_ekle_ekrani(sistem)

        elif secim == "3":
            sube_ekle_ekrani(sistem)

        elif secim == "4":
            bolum_ekle_ekrani(sistem)

        elif secim == "5":
            hizmet_ekle_ekrani(sistem)

        elif secim == "6":
            calisma_saati_ekrani(sistem)

        elif secim == "0":
            print("Görüşmek üzere.")
            break

        else:
            print("Geçersiz seçim. Menüdeki numaralardan birini yazın.")


if __name__ == "__main__":
    main()
