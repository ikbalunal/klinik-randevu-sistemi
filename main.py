import sys

from sistem import KlinikSistemi


def main():
    # yönlendirilmiş çıktıda türkçe harfler bozulmasın
    sys.stdout.reconfigure(encoding="utf-8")
    sistem = KlinikSistemi()

    while True:
        print("\nKlinik Randevu Sistemi")
        print("1 - Kurumları listele")
        print("0 - Çıkış")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            kurumlar = sistem.kurumlari_listele()

            if len(kurumlar) == 0:
                print("Henüz kayıtlı kurum yok.")
            else:
                for kurum in kurumlar:
                    print(kurum.ad)

        elif secim == "0":
            print("Görüşmek üzere.")
            break

        else:
            print("Geçersiz seçim. 1 veya 0 yazın.")


if __name__ == "__main__":
    main()
