from kurum import Bolum, Hizmet, Kurum, Sube
from kisiler import Calisan, Doktor, Hasta, SaglikPersoneli, Yonetici
from randevu import Randevu, Uygunluk


class KlinikSistemi:
    def __init__(self):
        self.kurumlar = []
        self.son_kurum_id = 0
        self.son_sube_id = 0
        self.son_bolum_id = 0
        self.son_hizmet_id = 0
        self.kullanicilar = []
        self.son_kullanici_id = 0
        self.randevular = []
        self.son_randevu_id = 0

    def kurumlari_listele(self):
        return self.kurumlar

    def kullanicilari_listele(self):
        return self.kullanicilar

    def kullaniciyi_bul(self, kullanici_id):
        for kullanici in self.kullanicilar:
            if kullanici.id == kullanici_id:
                return kullanici

        return None

    def calisani_bul(self, calisan_id):
        kullanici = self.kullaniciyi_bul(calisan_id)

        if isinstance(kullanici, Calisan):
            return kullanici

        return None

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

    def hizmeti_bul(self, hizmet_id):
        for kurum in self.kurumlar:
            for sube in kurum.subeler:
                for hizmet in sube.hizmetler:
                    if hizmet.id == hizmet_id:
                        return hizmet

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

    def hasta_ekle(self, ad):
        ad = ad.strip()

        if ad == "":
            raise ValueError("Hasta adı boş olamaz.")

        self.son_kullanici_id += 1
        hasta = Hasta(self.son_kullanici_id, ad)
        self.kullanicilar.append(hasta)
        return hasta

    def doktor_ekle(self, ad, sube_id, uzmanlik):
        sube = self.sube_bul(sube_id)

        if sube is None:
            raise ValueError("Şube bulunamadı.")

        ad = ad.strip()
        uzmanlik = uzmanlik.strip()

        if ad == "" or uzmanlik == "":
            raise ValueError("Ad ve uzmanlık boş olamaz.")

        self.son_kullanici_id += 1
        doktor = Doktor(self.son_kullanici_id, ad, sube_id, uzmanlik)
        self.kullanicilar.append(doktor)
        return doktor

    def personel_ekle(self, ad, sube_id):
        sube = self.sube_bul(sube_id)

        if sube is None:
            raise ValueError("Şube bulunamadı.")

        ad = ad.strip()

        if ad == "":
            raise ValueError("Çalışan adı boş olamaz.")

        self.son_kullanici_id += 1
        personel = SaglikPersoneli(self.son_kullanici_id, ad, sube_id)
        self.kullanicilar.append(personel)
        return personel

    def yonetici_ekle(self, ad, kurum_id):
        kurum = self.kurumu_bul(kurum_id)

        if kurum is None:
            raise ValueError("Kurum bulunamadı.")

        ad = ad.strip()

        if ad == "":
            raise ValueError("Yönetici adı boş olamaz.")

        self.son_kullanici_id += 1
        yonetici = Yonetici(self.son_kullanici_id, ad, kurum_id)
        self.kullanicilar.append(yonetici)
        return yonetici

    def calisana_hizmet_ata(self, calisan_id, hizmet_id):
        calisan = self.calisani_bul(calisan_id)

        if calisan is None:
            raise ValueError("Çalışan bulunamadı.")

        sube = self.sube_bul(calisan.sube_id)

        for hizmet in sube.hizmetler:
            if hizmet.id == hizmet_id:
                calisan.hizmet_ekle(hizmet_id)
                return hizmet

        raise ValueError("Hizmet çalışanın şubesinde bulunamadı.")

    def uygunluk_ekle(self, calisan_id, baslangic, bitis):
        calisan = self.calisani_bul(calisan_id)

        if calisan is None:
            raise ValueError("Çalışan bulunamadı.")

        uygunluk = Uygunluk(calisan_id, baslangic, bitis)
        sube = self.sube_bul(calisan.sube_id)

        if not sube.acik_mi(baslangic, bitis):
            raise ValueError("Bu aralık şubenin çalışma saatleri dışında.")

        for kayitli_uygunluk in calisan.uygunluklar:
            if baslangic < kayitli_uygunluk.bitis and bitis > kayitli_uygunluk.baslangic:
                raise ValueError("Bu aralık çalışanın başka bir uygunluğuyla çakışıyor.")

        calisan.uygunluklar.append(uygunluk)
        return uygunluk

    def calisan_uygun_mu(self, calisan_id, baslangic, bitis):
        calisan = self.calisani_bul(calisan_id)

        if calisan is None:
            return False

        sube = self.sube_bul(calisan.sube_id)

        if not sube.acik_mi(baslangic, bitis):
            return False

        for uygunluk in calisan.uygunluklar:
            if uygunluk.kapsar(baslangic, bitis):
                return True

        return False

    def randevu_olustur(self, hasta_id, calisan_id, hizmet_id, baslangic):
        hasta = self.kullaniciyi_bul(hasta_id)

        if not isinstance(hasta, Hasta):
            raise ValueError("Hasta bulunamadı.")

        calisan = self.calisani_bul(calisan_id)

        if calisan is None:
            raise ValueError("Çalışan bulunamadı.")

        hizmet = self.hizmeti_bul(hizmet_id)

        if hizmet is None:
            raise ValueError("Hizmet bulunamadı.")

        if hizmet.sube_id != calisan.sube_id:
            raise ValueError("Hizmet çalışanın şubesinde bulunmuyor.")

        if hizmet.id not in calisan.hizmet_idleri:
            raise ValueError("Bu hizmet çalışana atanmamış.")

        yeni_randevu = Randevu(
            self.son_randevu_id + 1,
            hasta.id,
            calisan.id,
            hizmet.id,
            calisan.sube_id,
            baslangic,
            hizmet.sure_dakika,
            hizmet.ucret_tl,
        )

        sube = self.sube_bul(calisan.sube_id)

        if not sube.acik_mi(yeni_randevu.baslangic, yeni_randevu.bitis):
            raise ValueError("Randevu şubenin çalışma saatleri dışında.")

        if not self.calisan_uygun_mu(calisan.id, yeni_randevu.baslangic, yeni_randevu.bitis):
            raise ValueError("Çalışan bu saatte uygun değil.")

        for eski_randevu in self.calisanin_randevulari(calisan.id):
            if eski_randevu.durum in ("beklemede", "onaylandi"):
                if yeni_randevu.baslangic < eski_randevu.bitis and yeni_randevu.bitis > eski_randevu.baslangic:
                    raise ValueError("Çalışanın bu saatte başka bir randevusu var.")

        self.randevular.append(yeni_randevu)
        self.son_randevu_id = yeni_randevu.id
        return yeni_randevu

    def hastanin_randevulari(self, hasta_id):
        bulunanlar = []

        for randevu in self.randevular:
            if randevu.hasta_id == hasta_id:
                bulunanlar.append(randevu)

        return bulunanlar

    def calisanin_randevulari(self, calisan_id):
        bulunanlar = []

        for randevu in self.randevular:
            if randevu.calisan_id == calisan_id:
                bulunanlar.append(randevu)

        return bulunanlar
