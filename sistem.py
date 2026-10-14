from kurum import Kurum, Sube


class KlinikSistemi:
    def __init__(self):
        self.kurumlar = []
        self.son_kurum_id = 0
        self.son_sube_id = 0

    def kurumlari_listele(self):
        return self.kurumlar

    def kurumu_bul(self, kurum_id):
        for kurum in self.kurumlar:
            if kurum.id == kurum_id:
                return kurum

        return None

    def kurum_ekle(self, ad):
        ad = ad.strip()

        if ad == "":
            raise ValueError("Kurum adı boş olamaz.")

        self.son_kurum_id += 1
        kurum = Kurum(self.son_kurum_id, ad)
        self.kurumlar.append(kurum)
        return kurum

    def sube_ekle(self, kurum_id, ad):
        kurum = self.kurumu_bul(kurum_id)

        if kurum is None:
            raise ValueError("Kurum bulunamadı.")

        ad = ad.strip()

        if ad == "":
            raise ValueError("Şube adı boş olamaz.")

        yeni_id = self.son_sube_id + 1
        sube = Sube(yeni_id, kurum_id, ad)
        kurum.sube_ekle(sube)
        self.son_sube_id = yeni_id
        return sube
