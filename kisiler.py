class Kullanici:
    def __init__(self, id, ad):
        self.id = id
        self.ad = ad

    def unvan(self):
        return "Kullanıcı"


class Hasta(Kullanici):
    def unvan(self):
        return "Hasta"


class Calisan(Kullanici):
    def __init__(self, id, ad, sube_id):
        super().__init__(id, ad)
        self.sube_id = sube_id
        self.hizmet_idleri = []
        self.uygunluklar = []

    def unvan(self):
        return "Çalışan"

    def hizmet_ekle(self, hizmet_id):
        if hizmet_id in self.hizmet_idleri:
            raise ValueError("Bu hizmet çalışana zaten atanmış.")

        self.hizmet_idleri.append(hizmet_id)


class Doktor(Calisan):
    def __init__(self, id, ad, sube_id, uzmanlik):
        super().__init__(id, ad, sube_id)
        self.uzmanlik = uzmanlik

    def unvan(self):
        return "Doktor"


class SaglikPersoneli(Calisan):
    def unvan(self):
        return "Sağlık personeli"


class Yonetici(Kullanici):
    def __init__(self, id, ad, kurum_id):
        super().__init__(id, ad)
        self.kurum_id = kurum_id

    def unvan(self):
        return "Yönetici"
