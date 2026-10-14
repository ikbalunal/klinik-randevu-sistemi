class Kurum:
    def __init__(self, id, ad):
        self.id = id
        self.ad = ad
        self.subeler = []

    def sube_ekle(self, sube):
        if sube.kurum_id != self.id:
            raise ValueError("Şube başka bir kuruma ait.")

        for kayitli_sube in self.subeler:
            if kayitli_sube.id == sube.id or kayitli_sube.ad.lower() == sube.ad.lower():
                raise ValueError("Bu şube zaten kayıtlı.")

        self.subeler.append(sube)


class Sube:
    def __init__(self, id, kurum_id, ad):
        self.id = id
        self.kurum_id = kurum_id
        self.ad = ad
        self.bolumler = []
        self.hizmetler = []
        self.calisma_saatleri = {}

    def bolum_ekle(self, bolum):
        if bolum.sube_id != self.id:
            raise ValueError("Bölüm başka bir şubeye ait.")

        for kayitli_bolum in self.bolumler:
            if kayitli_bolum.ad.lower() == bolum.ad.lower():
                raise ValueError("Bu bölüm zaten kayıtlı.")

        self.bolumler.append(bolum)

    def hizmet_ekle(self, hizmet):
        if hizmet.sube_id != self.id:
            raise ValueError("Hizmet başka bir şubeye ait.")

        for kayitli_hizmet in self.hizmetler:
            if kayitli_hizmet.ad.lower() == hizmet.ad.lower():
                raise ValueError("Bu hizmet zaten kayıtlı.")

        self.hizmetler.append(hizmet)

    def calisma_saati_ayarla(self, gun, acilis, kapanis):
        if gun < 1 or gun > 7:
            raise ValueError("Gün numarası 1 ile 7 arasında olmalı.")

        if acilis >= kapanis:
            raise ValueError("Açılış saati kapanıştan önce olmalı.")

        self.calisma_saatleri[gun] = (acilis, kapanis)

    def acik_mi(self, baslangic, bitis):
        if baslangic >= bitis or baslangic.date() != bitis.date():
            return False

        gun = baslangic.isoweekday()

        if gun not in self.calisma_saatleri:
            return False

        acilis, kapanis = self.calisma_saatleri[gun]
        return acilis <= baslangic.time() and bitis.time() <= kapanis


class Bolum:
    def __init__(self, id, sube_id, ad):
        self.id = id
        self.sube_id = sube_id
        self.ad = ad


class Hizmet:
    def __init__(self, id, sube_id, bolum_id, ad, sure_dakika, ucret_tl):
        if sure_dakika <= 0:
            raise ValueError("Hizmet süresi sıfırdan büyük olmalı.")

        if ucret_tl < 0:
            raise ValueError("Hizmet ücreti negatif olamaz.")

        self.id = id
        self.sube_id = sube_id
        self.bolum_id = bolum_id
        self.ad = ad
        self.sure_dakika = sure_dakika
        self.ucret_tl = ucret_tl
