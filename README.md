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

Uygulama Python ile konsolda çalışır. Sınıf yapısı, kapsülleme, kalıtım ve çok biçimlilik kullanılır.

## Çalıştırma

Python 3.8 veya üzeri gerekir. Ek paket kurulumu yoktur. Bu klasörde şu komutu çalıştırın:

```text
python main.py
```

Program Python 3.14.3 ile çalıştırılarak kontrol edildi.

Menülerde numarayı yazıp Enter'a basın. Listelerde kurum, şube, hizmet, çalışan ve randevu numaraları görünür. Renk destekli terminallerde başlıklar ve durum mesajları hafif renkli gösterilir.

## Kullanım sırası

1. İlk açılışta `Kurum ekle`, ardından `Yönetici ekle` seçeneklerini kullanın.
2. Kullanıcı listesinden yöneticiyi seçin. Şube, bölüm, hizmet ve çalışma saatini ekleyin. Doktor veya sağlık personeli ekleyip çalışana hizmet atayın. Sonra çalışan uygunluğunu ve hastayı ekleyin.
3. `0 - Kullanıcı değiştir` ile hasta hesabını seçin. `Randevu oluştur` bölümünde hizmeti, çalışanı ve boş aralıktaki başlangıç saatini girin.
4. Yönetici hesabına dönüp bekleyen randevuyu listeleyin ve onaylayın. Çalışan hesabından kendi uygunlukları ve randevuları görülebilir.
5. Bir roldeki `0` seçeneği kullanıcı listesine döner. Kullanıcı listesindeki `0` programı kapatır.

Kayıtlı bir yönetici, menüden yeni bir kurum ve o kurumun yöneticisini oluşturabilir. Yeni yönetici kullanıcı seçiminden seçilerek kendi kurumuna şube ekleyebilir.

Uygunluk eklemeden önce şubenin o güne ait çalışma saatini ayarlayın. Tarih ve saati `25.10.2026 09:00` biçiminde girin. Uygunluk aynı gün içinde ve şubenin çalışma saatlerinde olmalıdır; aynı çalışanın aralıkları çakışamaz.

Hasta menüsünden hizmeti, o hizmete atanmış çalışanı ve randevu zamanını seçebilirsiniz. Çalışanı seçince uygunluk aralıkları, dolu randevu saatleri ve seçilen hizmetin süresine yetecek boş aralıklar ayrı görünür. Her boş aralığın altında randevuya en geç kaçta başlanabileceği de yazılır. Başlangıç saatini bu sınırlar içinde seçebilirsiniz. Randevu, hizmet süresi boyunca şubenin çalışma saatleri ve çalışanın uygunluğu içinde kalmalıdır. Aynı çalışanın bekleyen randevuları da o saati kapatır. Hasta kendi randevularını, çalışan da kendisine ait randevuları görebilir.

Yönetici kendi kurumundaki bekleyen randevuları listeleyip onaylayabilir. Başka kurumun randevusu onaylanamaz; onaylanan randevu ikinci kez onaylanamaz. Onaylanan randevu da çalışanın saatini kapatır.

Kullanıcı seçimi şu an parola kullanmaz.

## Verileri saklama

Başarılı değişiklikler `main.py` ile aynı klasördeki `veriler.json` dosyasına kaydedilir. Program yeniden açıldığında kurumlar, kişiler, uygunluklar ve randevular bu dosyadan yüklenir. Bu dosya ve yazma sırasında kullanılan `veriler.json.tmp` Git'e eklenmez.

Veri dosyası okunamıyorsa program kısa bir hata gösterip açılışı durdurur. Dosya kendiliğinden silinmez veya üzerine boş kayıt yazılmaz.
