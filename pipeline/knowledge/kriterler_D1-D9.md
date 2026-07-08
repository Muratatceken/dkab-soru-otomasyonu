# DKAB Test Maddesi Kalite Rubriği — D1–D9 Kanonik Kural Seti

> Bu dosya, "çapraz okuma botu"nun her DKAB test maddesini puanlarken kullanacağı **kanonik, makine-denetlenebilir** kural setidir.
> Kaynaklar: `ENVANTER_VE_SINIFLANDIRMA.md §3a` (D1–D9 özeti), `11_Sinif_Unite1_Elestirel_Degerlendirme_Raporu.docx` (56 maddelik madde-madde eleştiri) ve `11_Sinif_1_Unite_NIHAI_Test_Seti_v2.docx` (revize set — düzeltilmiş örnekler buradan).
> İki katman vardır: **madde düzeyi** (D1–D9, her madde için geç/kal) ve **test/set düzeyi** (SİSTEMİK NORMLAR, bir kitapçık için oransal eşikler). Puanlama en sonda.

Kısaltmalar: **gövde** = soru metni (stimulus) + kök; **kök** = soru cümlesi; **şık/seçenek** = A–E; **içerik kelimesi** = bağlaç/edat/zamir dışı sözcük (durak-kelimeler taranırken atlanır).

---

## Madde Düzeyi Kurallar (D1–D9)

| Kod | Ad | Kural (emredici) | Ağırlık |
|---|---|---|---|
| D1 | Kelime avcılığı | Metindeki anahtar kelimeyi doğru şıkka birebir taşıma; parafraz/sentez kullan. | 12 |
| D2 | Uzunluk/akademiklik ipucu | Doğru şıkkı uzunluk veya akademik dille diğerlerinden öne çıkarma. | 8 |
| D3 | Zıt/eş anlamlı çift | Aynı soruda zıt anlamlı veya eş anlamlı şık çifti bulundurma. | 10 |
| D4 | İşlevsiz çeldirici | Çeldiricileri kavram yanılgısına dayandır; saçma/kolay elenir yapma. | 14 |
| D5 | Yasak sınırlayıcı kelime | Şıklarda mutlak/sınırlayıcı kelime (yalnız, sadece, ama…) kullanma. | 8 |
| D6 | Ortak kelime tekrarı | Beş şıkta tekrarlanan ortak kelimeyi köke taşı, şıklarda tekrarlama. | 6 |
| D7 | Vurgusuz olumsuz kök | Olumsuz/kritik kök kelimesini kalın (bold) veya altı çizili yap. | 8 |
| D8 | İkinci savunulabilir cevap | Tek doğru cevap ilkesini koru; ikinci savunulabilir şık bırakma. | 16 |
| D9 | Son cümle sızıntısı | Cevabı paragrafın/anlatıcının son cümlesinde açık verme; çıkarım ölçtür. | 18 |

Ağırlıklar toplamı = 100. **D8 ve D9 "yapı-bozan" kritik kodlardır** (aşağıdaki puanlama şablonundaki tavan kuralına bak).

---

### D1 — Kelime avcılığı
**Kural:** Doğru şıkkın içerik kelimeleri parçadan birebir kopyalanmamalı; parafraz veya birden çok cümlenin sentezi olmalı.

**İhlal tanımı (bot ne arar):** Doğru şık ile gövde arasında 2+ içerik kelimesinin birebir örtüşmesi; özellikle nadir/teknik terimlerin (ör. *ilahî, takdir, gerçekleşme, tevekkül*) parçadan şıkka aynen taşınması; doğru şıkkın parçadaki bir cümlenin neredeyse tıpatıp kopyası olması.

**KÖTÜ (rapordan):** Tevekkül maddesinde doğru şık, parçadaki *"…sonucu Allah'a bırakmasına tevekkül denir"* cümlesinin birebir kopyasıydı → cevap anahtar-kelime avcılığıyla, konuyu bilmeden bulunuyordu. Benzer şekilde T1S8'in eski A şıkkı *"İmtihanın anlamlı olması, insanın iki yol arasında tercih yapabilmesine bağlıdır"* metindeki *"imtihan alanı olması … iki yolun açık tutulması"* ifadesinin tekrarıydı.

**DÜZELTİLMİŞ (NIHAI v2, T1S8-A):** *"İnsanın ahlaki sorumluluk taşıyabilmesi, seçenekler arasında gerçek bir tercih özgürlüğüne sahip olmasını gerektirir."* — metnin hiçbir anahtar kelimesini (*imtihan, hayır, şer, açık tutulması*) tekrarlamaz; aynı çıkarımı farklı kavramsal sözcüklerle ölçer.

**Otomatik kontrol ipucu:** Durak-kelimeleri çıkardıktan sonra `doğru_şık ∩ gövde` içerik-kelime kesişimini say. **≥ 2 birebir örtüşme → uyarı; ≥ 3 → ihlal.** Ek koşul: doğru şıkkın gövdeyle örtüşme oranı, çeldiricilerin ortalama örtüşme oranından belirgin yüksekse (>1.3×) ihlal işaretle. n-gram (3+ ardışık kelime) birebir eşleşmesi tek başına ihlaldir.

---

### D2 — Uzunluk/akademiklik ipucu
**Kural:** Doğru şık, uzunluk veya akademik dil yoğunluğu bakımından diğer şıklardan ayrışmamalı.

**İhlal tanımı:** Doğru şık şıkların en uzunu ve en "akademik" olanı (ör. *"ilahî takdir"* gibi terim yükü); doğru 10+ kelime iken çeldiriciler 4 kelime; doğru şık iki bölmeli/virgüllü "X…, Y…" kalıbında, çeldiriciler tek yargılı.

**KÖTÜ (rapordan):** *"B 10 kelimeyle en uzun ve en akademik şık ('ilahî takdir'), A yalnız 4 kelime — doğru cevap kendini uzunluk ve kapsamla ele veriyor (D2 ihlali)."*

**DÜZELTİLMİŞ (T1S8):** Doğru şık 12 kelimeye indirilip çeldiricilerin bandına (7–9) yaklaştırıldı, iki bölmeli virgüllü kalıp kaldırıldı, tek yargılı hale getirildi → sözdizimsel simetri sağlandı.

**Otomatik kontrol ipucu:** Beş şıkkın kelime sayılarını al. Doğru şık **en uzunsa VE ortalamanın 1.25×'inden fazlaysa** ihlal. Alternatif eşik: `|len(doğru) − ortalama(çeldiriciler)| > 1.5 × std`. Ayrıca virgül/bağlaç sayısı doğru şıkta çeldirici ortalamasının üstündeyse "yapı asimetrisi" uyarısı.

---

### D3 — Zıt/eş anlamlı çift
**Kural:** Bir soruda birbirinin zıddı veya eş anlamlısı olan iki şık aynı anda bulunmamalı.

**İhlal tanımı:** İki şıkkın doğrudan zıt önerme olması (*bağımsız öğrenilmeli* ↔ *bütünlük oluşturur*; *artırır* ↔ *azaltır*); iki şıkkın fiilen aynı anlama gelmesi. Her ikisi de "cevap bu ikisinden biridir" test-tekniği ipucu sızdırır ya da eş çift birlikte elenir.

**KÖTÜ (rapordan):** *"A (bağımsız öğrenilmeli) ile E (bütünlük oluşturur) doğrudan zıt çift; cevabın ikisinden biri olduğu test tekniğiyle sezilir."* T1S8'in eski A–D şıkları da örtük zıt çiftti.

**DÜZELTİLMİŞ (T1S8):** Yeni A'nın kavramsal çerçevesi (*ahlaki sorumluluk / tercih özgürlüğü*) D'nin çerçevesinden (*hayrı seçenin imtihan dışında kalması*) ayrıştırıldı → doğrudan zıtlık ipucu kaldırıldı.

**Otomatik kontrol ipucu:** Şık çiftleri için (a) zıt-öncek/ek listesi (*-siz/-li, bağımlı/bağımsız, artar/azalır, mümkün/imkânsız, değişir/değişmez*) ve (b) cümle-gömme (embedding) benzerliği taraması. **cos benzerliği > 0.9 → eş anlamlı çift ihlali; negatif kutuplu antonim örüntüsü → zıt çift ihlali.**

---

### D4 — İşlevsiz çeldirici
**Kural:** Her çeldirici, konuyu bilen ama ilişkiyi kuramayan öğrenciyi yakalayan gerçek bir kavram yanılgısına dayanmalı; parçayla anında çürüyen basit olumsuzlama veya saçma önerme olmamalı.

**İhlal tanımı:** Çeldirici, parçadaki bir cümlenin basit olumsuzlaması (*"…gösterir" → "…göstermez"*); parçayla açıkça çelişip saniyede elenir; kriterin bizzat "çeldirici SAYILMAZ" dediği tip (ör. *"Çalışmayı bırakıp sonucu beklemek"*); üç+ çeldirici sağduyuyla, bilgi olmadan elenebiliyor.

**KÖTÜ (rapordan):** Sünnetullah maddesinde çeldiricilerin 3'ü (*su donması, metal genleşmesi, ışığa yönelme*) doğrudan kategori-anahtar-kelime eşleşmesiyle elenir; gerçek ayırt edici yük yalnız doğru şıkka düşer → "kılık değiştirmiş eşleştirme".

**DÜZELTİLMİŞ (T1S3 — tevekkül):** Çeldiriciler *Kanaat, Sabır, Şükür, Rıza* — hepsi tevekküle yakın, gerçek kavram karışması taşıyan tuzaklar; her biri metnin farklı bir yönüyle karıştırılabilir, hiçbiri saçma değil.

**Otomatik kontrol ipucu:** Her çeldirici için (a) parça cümlesinin basit-olumsuz aynası mı? (*değil/yok/-maz* eki eklenmiş kopya) → işaretle; (b) çeldirici alan-sözlüğündeki gerçek bir kavram/yanılgı adı içeriyor mu? İçermiyorsa "çöp seçenek" uyarısı. **Bir maddede 2+ çöp/ayna çeldirici → D4 ihlali.** (Kesin ayrım için LLM-hakem çağrısı önerilir.)

---

### D5 — Yasak sınırlayıcı kelime
**Kural:** Şıklarda mutlak/sınırlayıcı kelime kullanılmamalı (bunlar doğru şıkkı ya da yanlış şıkkı ele verir).

**İhlal tanımı:** Şık içinde sınırlayıcı/mutlak sözcük geçmesi. Kritik: bu sözcükler ölçme değil, test-tekniği sinyali yayar.

**KÖTÜ (rapordan):** *"C şıkkında sınırlayıcı 'yalnız' kullanılmış"* / *"Ayetin yalnız ibadet kolaylıklarını konu edindiğine"*. Not: NIHAI v2 setinde bu ihlal **hâlâ canlı** — şıklarda `yalnız`×13, `ama`×12, `fakat`×2, `sadece`×1 sayıldı.

**DÜZELTİLMİŞ:** Sınırlayıcıyı at ya da yumuşat (*"yalnız X'i konu edindiğine" → "ağırlıklı olarak X'e değindiğine"*), veya kapsamı çeldiricinin kendi mantığından türet.

**Otomatik kontrol ipucu (kesin regex/kelime-listesi):** Şık metninde büyük/küçük harf duyarsız ara —
`yalnız(ca)?, sadece, ama, fakat, ancak, öncelikle, kesinlikle, asla, en çok, en az, hiçbir zaman, her zaman, daima, mutlaka, tamamen, her koşulda, kesin, tek`.
**Eşleşme = ihlal.** (Kök/gövdede geçmesi serbest; kısıt yalnız A–E şıklarına uygulanır.)

---

### D6 — Ortak kelime tekrarı
**Kural:** Beş şıkta da tekrarlanan ortak sözcük/ek, köke taşınmalı; şıklarda yalnız ayırt edici kısım kalmalı.

**İhlal tanımı:** Aynı kelime (*"bir yaklaşım", "yasa", "sorumluluk"*) tüm veya çoğu şıkta yineleniyor, kök bunu üstlenmemiş → şıklar gereksiz uzun, okuma yükü yapay.

**KÖTÜ (rapordan):** *"'bir yaklaşım' ifadesi beş şıkta da tekrarlanıyor; köke taşınmalıydı."* / *"Şıklarda tekrarlanan 'yasa' kelimesi köke taşınmamış (D6)."*

**DÜZELTİLMİŞ:** Kök *"…aşağıdaki yaklaşımlardan hangisidir?"* biçiminde kurulur; şıklar sadece *"-an/-en …"* ayırt edici çekirdeği taşır.

**Otomatik kontrol ipucu:** Beş şıkkın kelime kümelerinin **kesişimini** al. Kesişimde içerik kelimesi (durak-kelime hariç) varsa ve **≥ 4/5 şıkta** geçiyorsa → "köke taşınmalı" ihlali. Baş/son ortak öbek (leading/trailing common phrase) tespiti ayrıca yapılır.

---

### D7 — Vurgusuz olumsuz kök
**Kural:** Kökteki olumsuz/kritik kelime (*hangisi yanlış, söylenemez, ulaşılamaz, değinilmemiştir*) kalın veya altı çizili biçimlenmeli.

**İhlal tanımı:** Kök olumsuz kutuplu ama olumsuz kelime düz metin; öğrenci "hangisi doğru" sanıp yanılır. (Olumlu kökte bu kural devreye girmez — vurgu gereği doğmaz.)

**KÖTÜ (rapordan):** *"(S8: 'örnek gösterilemez') kalın/altı çizili görsel vurgu içermiyor (D7 ihlali)."*

**DÜZELTİLMİŞ (v1→v2):** Setin tek gerçek v2 değişikliği tam buydu — 4 yerde negatif kök kelimesine **bold** eklendi (yalnız D7 kapatıldı).

**Otomatik kontrol ipucu:** Kökte negatif belirteç ara (`yanlış, değildir, söylenemez, ulaşılamaz, değinilmemiş, çıkarılamaz, uygun değildir, hariç`). Bulunursa, o token'ın biçim işaretiyle (`**…**`, `<b>`, `<u>`, run bold=true) sarılı olup olmadığını denetle. **Negatif kök + vurgusuz → ihlal.**

---

### D8 — İkinci savunulabilir cevap
**Kural:** Tek doğru cevap ilkesi mutlaktır; belirli bir okumayla savunulabilecek ikinci bir şık bulunmamalı.

**İhlal tanımı:** Bir çeldirici, teolojik/kavramsal bir okumayla "aslında doğru" savunulabilir; doğru şık ile en güçlü çeldirici arasındaki sınır metinle net çizilmemiş.

**KÖTÜ (rapordan, T1S8 eski C):** *"İnsanın şerri tercih etmesi, imtihan sürecini geçersiz kılar"* — bazı teolojik okumalarda (imtihanın amacı hayrı seçmekse) savunulabilir hale geliyordu → ikinci savunulabilir şık riski.

**DÜZELTİLMİŞ (T1S8 yeni C):** *"Şer tamamen ortadan kalksa dahi imtihanın anlamı değişmez"* — metnin temel önermesiyle (imtihan iki yolun açık olmasına bağlıdır) **tartışmasız çelişir**, savunulabilir okuma bırakmaz.

**Otomatik kontrol ipucu:** Saf regex zayıf kalır; **LLM-hakem** ile: "Her şıkkın parça tarafından açıkça çürütülüp çürütülmediğini işaretle; çürütülmeyen şık sayısı tam 1 olmalı." **≥ 2 çürütülemeyen şık → ihlal.** Ek sinyal: doğru şık ile en yakın çeldirici arasında gömme-benzerliği çok yüksekse el ile inceleme bayrağı.

---

### D9 — Son cümle sızıntısı (en sık ihlal)
**Kural:** Cevap paragrafın/anlatıcının son cümlesinde açıkça verilmemeli; doğru şık, metnin farklı yerlerinden sentezlenen gerçek bir çıkarım olmalı.

**İhlal tanımı:** Paragraf *"Görüldüğü gibi…/Bu, … göstermektedir/…değerlendirilmelidir"* tipi bir anlatıcı-özeti ile bitiyor ve kök tam o özeti şıklaştırıyor; cevap literal olarak son (veya ilk) cümlede hazır. Rapor: 56 maddenin **~%70'inde** bu kusur sistemik.

**KÖTÜ (rapordan):** Senaryo/diyalog gövdeleri zengin görünse de kapanışta *"bu, … göstermektedir"* özeti bırakılmış, soru doğrudan onu sormuş → "okuduğunu bulma", çıkarım değil.

**DÜZELTİLMİŞ (T1S1 — mimar benzetmesi):** Doğru şık C, *"benzetmenin Allah'ın bilgisindeki sınırsızlığı yansıtmakta eksik kaldığı"* — bu yargı hiçbir cümlede yazılı değil; öğretmenin uyarısı ile benzetmenin kendisi karşılaştırılıp **sentezlenerek** üretilir; son cümle cevabı vermez.

**Otomatik kontrol ipucu:** Gövdenin son cümlesini (ve ilk cümlesini) ayır; doğru şık ile bu cümle arasında **cümle-gömme benzerliği** hesapla. **cos > 0.75 → D9 ihlali.** Destekleyici sinyal: son cümlede özet-belirteci (`görüldüğü gibi, dolayısıyla, sonuç olarak, bu … gösterir/ifade eder/değerlendirilir`) + doğru şıkla yüksek kelime örtüşmesi birlikte görülürse ihlal kesinleşir.

---

## SİSTEMİK NORMLAR (Test/Set Düzeyi)

Bir kitapçık (referans: 56 madde) bu oransal eşiklerle ayrıca puanlanır. Parantez içinde NIHAI v2'nin **ölçülen gerçek değeri** verilmiştir.

| Norm | Hedef / Eşik | Sert sınır (otomatik red) |
|---|---|---|
| **Olumsuz kök oranı** | %40–45 (56'da ~22–25 olumsuz kök) | < %35 → red *(v2: ~%27, hâlâ düşük)* |
| **Kelime bandı dağılımı** (gövde) | 30–70: ~%45 · 70–100: ~%35 · 100–150: ~%20 | Herhangi bir bant boş; <30 veya >150 kelime gövde → red |
| **Tek kalıp tavanı** ("…hangisine ulaşılabilir?") | ≤ %30 (56'da ≤ 17) | > %35 → red *(v2: 24/56 ≈ %43, İHLAL)* |
| **I-II-III / "hepsi doğru" tavanı** | I-II-III ≤ %15 (≤ 8 madde); saf "hepsi doğru" = 0 | Öncüllerin hepsi doğru olan madde → red *(v2: 27 tetiklenme, İHLAL)* |
| **Cevap A–E dengesi** | Her harf %15–25 (56'da her harf 8–15) | Bir harf < %12 veya > %28; ardışık 3 soruda aynı cevap → red *(v2: A=20/%36, C=16/%29, D=6/%11, E=6/%11, İHLAL)* |

Ek kalite sinyalleri (uyarı düzeyi, red değil): mükerrer/yarı-mükerrer madde çifti (aynı bilgiyi aynı açıdan ölçen), tek kazanıma yığılma (yaprak testte kabul edilebilir; kapanış/genel testte dengelenmeli), format monotonluğu (ayet-meali/tablo/ikilem hiç yok).

**Otomatik ölçüm ipuçları:** olumsuz kök = kök negatif-belirteç regexi (bkz. D7 listesi) ile bölünen madde sayısı ÷ toplam; kelime bandı = gövde kelime sayısını histograma yaz; kalıp tavanı = kök normalize edilip aynı kalıp string'lerini say; cevap dengesi = `Cevap: [A-E]` frekans tablosu + ardışıklık taraması.

---

## PUANLAMA ŞABLONU

**Adım 1 — Madde puanı (0–100).** Madde 100 puanla başlamaz; **geçilen D-kodlarının ağırlıkları toplanır:**

```
madde_puani = Σ ağırlık(Di)   [Di geçtiyse]
ağırlıklar: D9=18, D8=16, D4=14, D1=12, D3=10, D2=8, D5=8, D7=8, D6=6   (toplam 100)
```

Her Di için bot **geç/kal** üretir (yukarıdaki otomatik ipuçlarıyla). Örnek: yalnız D5 ve D6 kalırsa → 100 − 8 − 6 = **86**.

**Adım 2 — Kritik-tavan kuralı.** D8 veya D9'dan **en az biri kalırsa**, madde ne olursa olsun **tavan 60**'a çekilir ve etiket = `REVİZYON ZORUNLU` olur (bu iki kod "yapıyı bozan" kusurdur: madde çıkarım yerine okuduğunu-bulma ölçer ya da iki savunulabilir cevap taşır). Yani `madde_puani = min(Σağırlık, 60)`.

**Adım 3 — Eşikler.**

| Puan | Etiket | Aksiyon |
|---|---|---|
| 90–100 | Yayına uygun | Kabul |
| 80–89 | Küçük düzeltme | Kalan D-kodlarını gider, yeniden puanla |
| 60–79 | Büyük revizyon | Çeldirici/gövde mimarisi elden geçirilir |
| < 60 | Reddet | Maddeyi at veya sıfırdan yaz |

**Adım 4 — Set puanı.** `set_puani = maddelerin ortalaması`, **ANCAK** SİSTEMİK NORMLAR'da bir "sert sınır" (red) tetiklenmişse set etiketi en fazla `KOŞULLU` olabilir — madde ortalaması yüksek olsa da set yayına giremez (referans: v2 madde-ortalaması iyi olsa bile "ulaşılabilir" kalıbı %43, cevap dengesi ve I-II-III tavanı ihlalde → set `KOŞULLU`). Set raporu her madde için hangi D-kodlarının geçtiğini/kaldığını bir onay-listesi (checklist) olarak taşımalı; salt kozmetik yama (v1→v2 gibi yalnız D7 kapatma) "çözüldü" sayılmaz.
