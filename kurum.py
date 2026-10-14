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
