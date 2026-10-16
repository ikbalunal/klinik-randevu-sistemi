# Klinik Randevu Sistemi

Klinik ve hastanelerin hizmetlerini, çalışanlarını, uygunluk saatlerini ve randevularını tek yerden yönetmesini sağlayan uygulama.

## İşlevsel gereksinimler

### Kurum ve şube yönetimi

- Yetkili yöneticiler klinik veya hastane tanımlayabilir.
- Sistem hem tek kurumlu hem de çok şubeli sağlık kuruluşlarını destekler.
- Her kurum veya şube için çalışma saatleri ve bölümler tanımlanabilir.
- Genel muayene, radyoloji ve laboratuvar gibi sağlık hizmetleri kaydedilebilir.
- Her hizmetin süresi ve ücreti ayrı ayrı belirlenebilir.

### Çalışan yönetimi

- Doktorlar ve diğer sağlık personeli sisteme kaydedilebilir.
- Doktorların uzmanlık alanları ve sunabildikleri hizmetler tanımlanabilir.
- Çalışanların uygun oldukları tarih ve saat aralıkları belirlenebilir.
- Hastalar yalnızca ilgili çalışanın uygun olduğu saatlere randevu alabilir.

### Randevu yönetimi

- Hasta, hizmeti ve uygun çalışanı seçerek randevu oluşturabilir.
- Randevu süresi dikkate alınarak aynı çalışan için zaman çakışması önlenir.
- Randevuda hizmet, süre, ücret, çalışan, tarih ve saat bilgileri saklanır.
- Randevular için onay süreci bulunur.

### Kullanıcı rolleri

- **Hasta:** Uygun saatleri görüntüler ve randevu oluşturur.
- **Doktor veya sağlık personeli:** Kendisine ait uygunluk ve randevu bilgilerini görüntüler.
- **Klinik veya hastane yöneticisi:** Kurum, bölüm, hizmet ve çalışan tanımlarını yönetir; randevuları onaylar.

## Teknik yaklaşım

Uygulama Python ile konsolda çalışır. Sınıf yapısı, kapsülleme, kalıtım ve çok biçimlilik ilkeleri geliştirme sırasında kullanılacaktır.

## Çalıştırma

Python kuruluysa bu klasörde şu komutu çalıştırın:

```text
python main.py
```

İlk açılışta bir kurum ve yönetici oluşturulur. Yönetici şube, bölüm, hizmet, çalışma saati ve kişi kayıtlarını ekleyebilir; çalışanlara kendi şubelerindeki hizmetleri atayabilir. Yönetici, çalışanın uygun olduğu tarih ve saat aralıklarını da ekleyip listeleyebilir. Çalışan kendi uygunluklarını görebilir. Hasta ve çalışan için ayrı menüler vardır.

Uygunluk eklemeden önce şubenin o güne ait çalışma saatini ayarlayın. Tarih ve saati `25.10.2026 09:00` biçiminde girin. Uygunluk aynı gün içinde ve şubenin çalışma saatlerinde olmalıdır; aynı çalışanın aralıkları çakışamaz.

Hasta menüsünden hizmeti, o hizmete atanmış çalışanı ve randevu zamanını seçebilirsiniz. Randevu, hizmet süresi boyunca şubenin çalışma saatleri ve çalışanın uygunluğu içinde kalmalıdır. Aynı çalışanın bekleyen randevuları da o saati kapatır. Hasta kendi randevularını, çalışan da kendisine ait randevuları görebilir.

Yönetici kendi kurumundaki bekleyen randevuları listeleyip onaylayabilir. Başka kurumun randevusu onaylanamaz; onaylanan randevu ikinci kez onaylanamaz. Onaylanan randevu da çalışanın saatini kapatır.

Kullanıcı seçimi şu an parola kullanmaz. Veriler yalnızca program açıkken tutulur.
