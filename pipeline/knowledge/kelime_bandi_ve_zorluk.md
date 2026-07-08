# Test Kurgu Blueprint Kuralları — Kelime Bandı, Zorluk ve Kök Polaritesi

> **Amaç:** Test kurgu asistanının **soru üretmeden önce** oluşturacağı planın (blueprint) kurallarıdır. Blueprint, bir testteki her sorunun kelime bandını, zorluğunu, kök polaritesini, kalıbını ve kazanımını önceden sabitler; böylece üretim "rastgele" değil, **kontrollü çeşitlilik** ile yapılır. ÖSYM TYT/AYT DKAB üslubuyla (bkz. `osym_stil_tyt.md`, `osym_stil_ayt.md`) uyumludur.

---

## 1. KELİME BANDI Dağılımı

### 1.1. Kelime sayısı neyi kapsar?
Kelime sayımı **yalnızca soru gövdesini (metni)** kapsar. **Kök (soru cümlesi) ve şıklar (A–E) sayıma DAHİL DEĞİLDİR.**

- **Sayılır:** Açıklama paragrafı, ayet/hadis meali, senaryo/diyalog, alıntı, tanım bloğu — yani öğrencinin okuyup çözümlediği ana metin.
- **Sayılmaz:** "Bu parçadan hareketle… hangisidir?" kökü; beş şıkkın metni; ayet künyesi *(Lokman, 31:20-21)*; "(hadis-i şerif)" etiketi.
- **Sınır:** Gövde toplamı **30–150 kelime** aralığında olmalı. Bu alt sınır köksüz/tek cümlelik soruyu, üst sınır ise okunamayacak kadar uzun metni engeller.

### 1.2. Üç bant ve test başına dağılım
Her test **üç kelime bandına** bölünür; her banttan **3–4 soru** gelir. Tipik test uzunluğu böylece **9–12 soru** olur.

| Bant | Kelime aralığı | Test başına soru | Tipik gövde tipi | ÖSYM karşılığı |
|---|---|---|---|---|
| **Kısa** | 30–70 | 3–4 | Tek açıklama cümlesi, kısa ayet meali, kısa senaryo | TYT'nin 2–4 satırlık gövdesi |
| **Orta** | 70–100 | 3–4 | Açıklama paragrafı + gömülü ayet/hadis | TYT–AYT geçiş bandı |
| **Uzun** | 100–150 | 3–4 | Kelami/felsefi tanım bloğu, çok künyeli ayet, diyalog, kavram tablosu | AYT'nin 4–9 satırlık yoğun gövdesi |

**Toplam:** 9 (3+3+3) ile 12 (4+4+4) arası. Asistan, hedeflenen test uzunluğuna göre bant başına 3 mü 4 mü üreteceğini seçer.

### 1.3. Bant içi çeşitlilik (randomizasyon)
"Her test aynı olmasın" kuralı gereği bandlar mekanik tekrarlanmaz. Randomizasyon iki katmanda uygulanır:

1. **Hedef kelime jitter'ı:** Her soru için bant içinde **rastgele bir `hedef_kelime`** seçilir (ör. Orta bant için 70–100 arası bir sayı: 78, 92, 85…). Amaç, aynı banttaki soruların hepsinin 85 kelime olmaması; ±15 kelime doğal yayılım.
2. **Sıra karıştırma:** Bantlar test içinde **rotasyon halinde dizilmez** (K-O-U-K-O-U gibi düzenli örüntü yasak). Sıra her testte yeniden karılır; ör. O-K-U-O-K-U-K-U-O-K-O-U.
3. **Oran esnetme:** Bazı testlerde bir bant 4, diğeri 3 soru alır (ör. 4 kısa + 3 orta + 4 uzun = 11). 3–4 sınırı korunduğu sürece dağılım kasıtlı olarak **asimetrik** kurulabilir.

---

## 2. ZORLUK Dağılımı

### 2.1. Hedef oran
Bir testte önerilen zorluk karışımı:

| Zorluk | Hedef pay | 12 soruluk testte | 9 soruluk testte |
|---|---|---|---|
| **Kolay** | ~%30 | 3–4 | 2–3 |
| **Orta** | ~%50 | 6 | 4–5 |
| **Zor** | ~%20 | 2 | 1–2 |

Oran **±1 soru** esnetilebilir; her test birebir aynı sayıda olmak zorunda değildir (bir testte 3 kolay/6 orta/3 zor, diğerinde 4/6/2 olabilir).

### 2.2. Zorluk neyle belirlenir?
Zorluk **tek başına kelime sayısıyla eş değildir**; üç eksenin bileşimidir:

| Eksen | Kolay | Orta | Zor |
|---|---|---|---|
| **Metin yoğunluğu** | Tek fikir, somut dil, kısa gövde | 1–2 fikir, gömülü ayet/hadis | Soyut kelami/felsefi terim, çok fikir, künyeli çoklu ayet |
| **Çeldirici inceliği** | Açıkça yanlış / metin dışı çeldirici | Kısmen doğru, vurgu kaydırmalı | Yakın terim seti (Tebliğ-Tebyin-Teşri…), parafraz/sentez çeldirici |
| **Bloom düzeyi** | Hatırla / Anla | Anla / Uygula | Analiz / Değerlendirme-Sentez |

**Kural:** Uzun bant (100–150) çoğunlukla orta-zor besler, kısa bant (30–70) çoğunlukla kolay-orta besler; **ancak birebir bağlı değildir.** Kısa bir gövde de ince terim çeldiricisiyle "zor", uzun bir gövde de tek fikirli okumayla "orta" olabilir. Blueprint bu istisnaları bilinçli serpiştirir.

---

## 3. KÖK POLARİTESİ (Olumlu / Olumsuz)

### 3.1. Hedef oran
ÖSYM normu: TYT'de olumsuz kök oranı **~%40**, AYT'de **~%30**. Karma testler için hedef bant **%35–45 olumsuz**.

| Test uzunluğu | Olumsuz kök hedefi | Olumlu kök |
|---|---|---|
| 9 soru | 3–4 | 5–6 |
| 10–11 soru | 4–5 | 6–7 |
| 12 soru | **5** (≈%42) | 7 |

### 3.2. Biçim ve dağılım kuralları
- **Altı çizili olumsuzlama zorunlu:** Olumsuz kökte sınırlayıcı kelime **daima altı çizili** yazılır: <u>ulaşılamaz</u>, <u>söylenemez</u>, <u>değinilmemiştir</u>, <u>çıkarılamaz</u>, <u>verilemez</u>, <u>yanlıştır</u>, <u>bahsedilmemiştir</u>.
- **Çeldirici mantığı ters döner:** Olumsuz kökte **dört şık metinle doğrulanır, biri doğrulanamaz/çelişir** (aranan odur).
- **Yığılma yasağı:** Olumsuz kökler **ardışık dizilmez** (üst üste 3 olumsuz soru olmaz); teste yayılır.
- **Kalıp çeşitliliği:** Olumsuzlama kelimesi hep aynı olmasın; test içinde en az 3 farklı olumsuz kalıp kullanılır.

---

## 4. BLUEPRINT Formatı

### 4.1. Per-soru sipariş nesnesi (alanlar)
Asistan her soru için şu alanları içeren bir nesne üretir:

| Alan | Tip | Açıklama | Örnek değer |
|---|---|---|---|
| `band` | enum | Kelime bandı | `30-70` / `70-100` / `100-150` |
| `hedef_kelime` | int | Bant içi rastgele hedef gövde uzunluğu | `92` |
| `polarite` | enum | Kök yönü | `olumlu` / `olumsuz` |
| `zorluk` | enum | Kolay/Orta/Zor | `orta` |
| `kalip` | string | Kök kalıbı | `hareketle ulaşılabilir` |
| `kazanim` | string | Ünite/konu hedefi | `Allah-İnsan İlişkisi` |

### 4.2. Örnek 12 soruluk blueprint (dengeli ama standart değil)

| # | band | hedef_kelime | polarite | zorluk | kalıp | kazanım |
|---|---|---|---|---|---|---|
| 1 | 70-100 | 84 | olumlu | orta | asıl anlatılmak istenen | Bilgi ve İnanç |
| 2 | 30-70 | 52 | olumsuz | kolay | <u>söylenemez</u> | Din ve İslam |
| 3 | 100-150 | 132 | olumlu | zor | hareketle ulaşılabilir | İslam Düşüncesinde Yorumlar |
| 4 | 70-100 | 91 | olumsuz | orta | <u>değinilmemiştir</u> | Ahlaki Tutum ve Davranışlar |
| 5 | 30-70 | 47 | olumlu | kolay | vurgulanmaktadır | Din ve Hayat |
| 6 | 100-150 | 118 | olumlu | orta | en kapsamlı ifade eden | Gönül Coğrafyamız |
| 7 | 30-70 | 63 | olumsuz | kolay | <u>çıkarılamaz</u> | Hz. Muhammed ve Gençlik |
| 8 | 100-150 | 145 | olumlu | zor | desteklemektedir | Dünya ve Ahiret |
| 9 | 70-100 | 79 | olumlu | kolay | vurgu yapılmıştır | İslam ve İbadet |
| 10 | 30-70 | 68 | olumsuz | orta | örnek <u>verilemez</u> | Gençlik ve Değerler |
| 11 | 70-100 | 88 | olumlu | orta | sözü edilen … hangisidir | Anadolu'da İslam |
| 12 | 100-150 | 124 | olumsuz | orta | tabloda <u>yanlıştır</u> | Kur'an'a Göre Hz. Muhammed |

**Dağılım denetimi (bu blueprint):**
- **Bant:** 30-70 → 4 (S2,5,7,10) · 70-100 → 4 (S1,4,9,11) · 100-150 → 4 (S3,6,8,12). ✅ 4-4-4
- **Zorluk:** Kolay 4 (S2,5,7,9) · Orta 6 (S1,4,6,10,11,12) · Zor 2 (S3,8). ✅ ≈%33/%50/%17
- **Polarite:** Olumsuz 5 (S2,4,7,10,12 ≈%42) · Olumlu 7. ✅ ardışık olumsuz yok
- **Standart değil:** Bant sırası rotasyon değil (O-K-U-O-K-U-K-U-O-K-O-U); S9 uzun bant değil ama kısa gövdeli kolay, S10 kısa banttan orta — uzunluk-zorluk birebir örtüşmüyor; kalıplar tekrar etmiyor.

---

## 5. CEVAP DENGE Kuralı (A–E Dağılımı)

Doğru cevap harfleri blueprint aşamasında **önceden dengelenir**; üretim sırasında "hep C çıkması" gibi yığılmalar engellenir.

| Kural | İçerik |
|---|---|
| **Eşit yayılım** | 12 soruda her harf ~2–3 kez; hiçbir harf **3'ten fazla** kullanılmaz (9 soruda ≤2–3). |
| **Ardışık tekrar yasağı** | Aynı harf **üst üste en fazla 2 kez**; art arda 3 aynı cevap yasak. |
| **Kenar dengesi** | A ve E (baş/son şık) yeterince temsil edilmeli; cevaplar orta şıklara (C) yığılmamalı. |
| **Rastgele başlangıç** | Cevap dizisi her testte yeniden karılır; sabit örüntü (ABCDE ABCDE) kullanılmaz. |

**Örnek cevap anahtarı (yukarıdaki 12 soruluk test):**
`C · A · E · B · D · A · C · E · B · D · B · A`
→ A=3, B=3, C=2, D=2, E=2 (toplam 12). Ardışık tekrar yok, hiçbir harf 3'ü aşmıyor. ✅

---

## 6. Hızlı Kontrol Listesi (Blueprint onayı öncesi)

- [ ] Üç banttan da **3–4'er** soru var; toplam **9–12**.
- [ ] `hedef_kelime` değerleri bant içinde **dağılmış** (aynı sayı tekrarı yok); tümü **30–150** arası.
- [ ] Kelime sayısı **yalnız gövde**; kök ve şıklar hariç tanımı uygulanmış.
- [ ] Zorluk ≈ **%30 kolay / %50 orta / %20 zor** (±1 soru).
- [ ] Olumsuz kök oranı **%35–45**; olumsuzlar **ardışık değil**, kalıpları **çeşitli**, kelimeleri **altı çizili**.
- [ ] Bant sırası ve kalıplar **mekanik tekrar** etmiyor (her test farklı).
- [ ] Cevap anahtarı **A–E dengeli**; yığılma ve ardışık-3 yok.
