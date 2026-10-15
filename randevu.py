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
