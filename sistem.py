from kurum import Bolum, Hizmet, Kurum, Sube


class KlinikSistemi:
    def __init__(self):
        self.kurumlar = []
        self.son_kurum_id = 0
        self.son_sube_id = 0
        self.son_bolum_id = 0
        self.son_hizmet_id = 0

    def kurumlari_listele(self):
        return self.kurumlar

    def kurumu_bul(self, kurum_id):
        for kurum in self.kurumlar:
            if kurum.id == kurum_id:
                return kurum

        return None

    def sube_bul(self, sube_id):
        for kurum in self.kurumlar:
            for sube in kurum.subeler:
                if sube.id == sube_id:
                    return sube

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

    def bolum_ekle(self, sube_id, ad):
        sube = self.sube_bul(sube_id)

        if sube is None:
            raise ValueError("Şube bulunamadı.")

        ad = ad.strip()

        if ad == "":
            raise ValueError("Bölüm adı boş olamaz.")

        yeni_id = self.son_bolum_id + 1
        bolum = Bolum(yeni_id, sube_id, ad)
        sube.bolum_ekle(bolum)
        self.son_bolum_id = yeni_id
        return bolum

    def hizmet_ekle(self, sube_id, bolum_id, ad, sure_dakika, ucret_tl):
        sube = self.sube_bul(sube_id)

        if sube is None:
            raise ValueError("Şube bulunamadı.")

        bolum_bulundu = False

        for bolum in sube.bolumler:
            if bolum.id == bolum_id:
                bolum_bulundu = True
                break

        if not bolum_bulundu:
            raise ValueError("Bölüm bu şubede bulunamadı.")

        ad = ad.strip()

        if ad == "":
            raise ValueError("Hizmet adı boş olamaz.")

        yeni_id = self.son_hizmet_id + 1
        hizmet = Hizmet(yeni_id, sube_id, bolum_id, ad, sure_dakika, ucret_tl)
        sube.hizmet_ekle(hizmet)
        self.son_hizmet_id = yeni_id
        return hizmet

    def calisma_saati_ayarla(self, sube_id, gun, acilis, kapanis):
        sube = self.sube_bul(sube_id)

        if sube is None:
            raise ValueError("Şube bulunamadı.")

        sube.calisma_saati_ayarla(gun, acilis, kapanis)
