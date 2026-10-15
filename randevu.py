from datetime import timedelta


class Uygunluk:
    def __init__(self, calisan_id, baslangic, bitis):
        if baslangic >= bitis:
            raise ValueError("Başlangıç bitişten önce olmalı.")

        if baslangic.date() != bitis.date():
            raise ValueError("Uygunluk aynı gün içinde olmalı.")

        self.calisan_id = calisan_id
        self.baslangic = baslangic
        self.bitis = bitis

    def kapsar(self, baslangic, bitis):
        if baslangic >= bitis or baslangic.date() != bitis.date():
            return False

        return self.baslangic <= baslangic and bitis <= self.bitis


class Randevu:
    def __init__(self, id, hasta_id, calisan_id, hizmet_id, sube_id, baslangic, sure_dakika, ucret_tl):
        if sure_dakika <= 0:
            raise ValueError("Randevu süresi sıfırdan büyük olmalı.")

        if ucret_tl < 0:
            raise ValueError("Randevu ücreti negatif olamaz.")

        self.id = id
        self.hasta_id = hasta_id
        self.calisan_id = calisan_id
        self.hizmet_id = hizmet_id
        self.sube_id = sube_id
        self.baslangic = baslangic
        self.sure_dakika = sure_dakika
        self.ucret_tl = ucret_tl
        self.bitis = baslangic + timedelta(minutes=sure_dakika)
        self.durum = "beklemede"
