import sys

from sistem import KlinikSistemi


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


def main():
    # yönlendirilmiş çıktıda türkçe harfler bozulmasın
    sys.stdout.reconfigure(encoding="utf-8")
    sistem = KlinikSistemi()

    while True:
        print("\nKlinik Randevu Sistemi")
        print("1 - Kurumları listele")
        print("2 - Kurum ekle")
        print("3 - Şube ekle")
        print("0 - Çıkış")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            kurumlari_goster(sistem)

        elif secim == "2":
            ad = input("Kurum adı: ")

            try:
                kurum = sistem.kurum_ekle(ad)
                print(f"{kurum.ad} eklendi.")
            except ValueError as hata:
                print(hata)

        elif secim == "3":
            if len(sistem.kurumlari_listele()) == 0:
                print("Önce bir kurum ekleyin.")
                continue

            kurumlari_goster(sistem)
            kurum_no = input("Kurum numarası: ").strip()

            if not kurum_no.isdigit():
                print("Geçerli bir kurum numarası yazın.")
                continue

            if sistem.kurumu_bul(int(kurum_no)) is None:
                print("Kurum bulunamadı.")
                continue

            ad = input("Şube adı: ")

            try:
                sube = sistem.sube_ekle(int(kurum_no), ad)
                print(f"{sube.ad} eklendi.")
            except ValueError as hata:
                print(hata)

        elif secim == "0":
            print("Görüşmek üzere.")
            break

        else:
            print("Geçersiz seçim. 0, 1, 2 veya 3 yazın.")


if __name__ == "__main__":
    main()
