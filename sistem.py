from datetime import datetime, timedelta

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

    def yeni_kurum_ve_yonetici_ekle(self, olusturan_yonetici_id, kurum_adi, yonetici_adi):
        olusturan = self.kullaniciyi_bul(olusturan_yonetici_id)

        if not isinstance(olusturan, Yonetici):
            raise ValueError("Bu işlem için yönetici seçilmeli.")

        if kurum_adi.strip() == "" or yonetici_adi.strip() == "":
            raise ValueError("Kurum ve yönetici adı boş olamaz.")

        kurum = self.kurum_ekle(kurum_adi)
        yonetici = self.yonetici_ekle(yonetici_adi, kurum.id)
        return kurum, yonetici

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

    def bos_randevu_araliklari(self, calisan_id, hizmet_id):
        calisan = self.calisani_bul(calisan_id)
        hizmet = self.hizmeti_bul(hizmet_id)

        if calisan is None:
            raise ValueError("Çalışan bulunamadı.")

        if hizmet is None:
            raise ValueError("Hizmet bulunamadı.")

        if hizmet.sube_id != calisan.sube_id or hizmet.id not in calisan.hizmet_idleri:
            raise ValueError("Bu hizmet bu çalışana atanmamış.")

        sube = self.sube_bul(calisan.sube_id)
        sonuc = []
        hizmet_suresi = timedelta(minutes=hizmet.sure_dakika)

        for uygunluk in calisan.uygunluklar:
            gun = uygunluk.baslangic.isoweekday()

            if gun not in sube.calisma_saatleri:
                continue

            acilis, kapanis = sube.calisma_saatleri[gun]
            acilis_zamani = datetime.combine(uygunluk.baslangic.date(), acilis)
            kapanis_zamani = datetime.combine(uygunluk.baslangic.date(), kapanis)
            baslangic = max(uygunluk.baslangic, acilis_zamani)
            bitis = min(uygunluk.bitis, kapanis_zamani)

            if baslangic >= bitis:
                continue

            bos_araliklar = [(baslangic, bitis)]

            for randevu in self.calisanin_randevulari(calisan.id):
                if randevu.durum not in ("beklemede", "onaylandi"):
                    continue

                kalan_araliklar = []

                for bos_baslangic, bos_bitis in bos_araliklar:
                    if randevu.baslangic < bos_bitis and randevu.bitis > bos_baslangic:
                        if bos_baslangic < randevu.baslangic:
                            kalan_araliklar.append((bos_baslangic, randevu.baslangic))

                        if randevu.bitis < bos_bitis:
                            kalan_araliklar.append((randevu.bitis, bos_bitis))
                    else:
                        kalan_araliklar.append((bos_baslangic, bos_bitis))

                bos_araliklar = kalan_araliklar

            for bos_baslangic, bos_bitis in bos_araliklar:
                if bos_bitis - bos_baslangic >= hizmet_suresi:
                    sonuc.append((bos_baslangic, bos_bitis))

        sonuc.sort()
        return sonuc

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
            raise ValueError("Randevu süresi çalışanın uygun saatlerine sığmıyor.")

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

    def bekleyen_randevulari(self, yonetici_id):
        yonetici = self.kullaniciyi_bul(yonetici_id)

        if not isinstance(yonetici, Yonetici):
            raise ValueError("Yönetici bulunamadı.")

        bulunanlar = []

        for randevu in self.randevular:
            sube = self.sube_bul(randevu.sube_id)

            if sube.kurum_id == yonetici.kurum_id and randevu.durum == "beklemede":
                bulunanlar.append(randevu)

        return bulunanlar

    def randevu_onayla(self, yonetici_id, randevu_id):
        yonetici = self.kullaniciyi_bul(yonetici_id)

        if not isinstance(yonetici, Yonetici):
            raise ValueError("Yönetici bulunamadı.")

        for randevu in self.randevular:
            if randevu.id == randevu_id:
                sube = self.sube_bul(randevu.sube_id)

                if sube.kurum_id != yonetici.kurum_id:
                    raise ValueError("Bu randevu başka bir kuruma ait.")

                randevu.onayla()
                return randevu

        raise ValueError("Randevu bulunamadı.")
