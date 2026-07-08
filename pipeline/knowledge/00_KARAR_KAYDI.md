# 00 — KARAR KAYDI (Bağlayıcı Kanon)

> **Bu dosya en yüksek önceliklidir.** Diğer bilgi tabanı dosyalarındaki (osym_stil_*, kriterler_D1-D9, soru_kalip_havuzu, kelime_bandi_ve_zorluk, dini_dil_kurallari, dab_becerileri_bloom) herhangi bir ifade bu dosyayla çelişirse, **bu dosya geçerlidir.** Tüm ajanlar çalışmaya başlamadan önce ÖNCE bu dosyayı okur.
>
> Amaç: kapsam kritiğinin bulduğu 12 çelişkiyi ve kritik boşlukları tek kanona bağlamak; ajanlar arası veri sözleşmesini (soru/blueprint/rapor JSON şemaları) sabitlemek.

---

## A) ÇELİŞKİ ÇÖZÜMLERİ (12 madde → tek kanon)

**K1 — Senaryo/diyalog metin türü: SINIRLI İZİNLİ.** ÖSYM DKAB'da senaryo/diyalog ~%3 sıklıkta *gerçekten vardır*. Kanon: bir testte **en fazla 1 senaryo/diyalog sorusu (~%5 tavan), asla baskın değil.** İzin verilen biçim: kısa, kurumsal vinyet veya birkaç kişinin *görüş* bildirdiği kompakt paragraf. Yasak biçim: "Ali dedi ki… / iki arkadaş sohbet ediyor" tarzı gevşek, günlük sohbet. → dini_dil'deki mutlak "YASAK" ifadesi bu tavan lehine iptal edilmiştir. *(Kullanıcı onayı bekliyor — eski MASTER_PROMPT senaryoyu tümden yasaklıyordu; ÖSYM'ye benzerlik için sınırlı izin verildi.)*

**K2 — Olumsuz/sınırlayıcı vurgu biçimi: ANLAMSAL saklanır, kanonik render = ALTI ÇİZİLİ.** JSON'da vurgu `vurgu:{sozcuk, bicim}` olarak semantik tutulur. Kanonik `bicim = "alti_cizili"` (ÖSYM TYT verisinin fiili normu). Render: HTML `<u>`, docx `w:u`, markdown `<u>`. → dini_dil'in "BÜYÜK HARF" zorunluluğu ve D7'nin "bold veya altı çizili" belirsizliği kaldırıldı; **her olumsuz kökte `vurgu` alanı zorunlu ve dolu.**

**K3 — Olumsuz kök oranı: %40 (±5).** Hedef %40, kabul aralığı %35–45, **<%35 → set-düzeyi RED.** → dini_dil'in "seyrek" ifadesi iptal.

**K4 — Yasak pekiştireç (yalnız/sadece/ama/kesinlikle/asla/en çok/hiçbir zaman) kapsamı: YALNIZ A–E ŞIKLARINDA yasak.** Kök/gövdede serbesttir (ÖSYM kökte altı çizili "öncelikle/yalnızca" kullanır). → kriterler_D5 geçerli; dini_dil'in "kök ve şıklarda" kapsamı daraltıldı.

**K5 — I-II-III formatındaki "Yalnız I / Yalnız II" istisnası.** Bu ifadeler yapısal seçicidir, D5 kapsamındaki retorik pekiştireç değildir → **muaf.**

**K6 — I-II-III / "hepsi doğru": ≤1 / test (çoğu test 0).** Kullanıldığında **cevap "I, II ve III" (hepsi doğru) OLAMAZ**; en az bir öncül yanlış olmalı (gerçek ayırt edicilik). Saf "hepsi doğru" madde → RED.

**K7 — Kelime bandı dağılımı: KULLANICI SPESİFİKASYONU GEÇERLİDİR.** Kanon: bir testte **30–70 arası 3–4 soru · 70–100 arası 3–4 soru · 100–150 arası 3–4 soru** (dengeli üç bant, tipik test 9–12 soru). → kriterler'in %45/%35/%20 (kısa-ağırlıklı) ÖSYM normu, kullanıcının "her bantta pratik" isteği nedeniyle **bağlayıcı değil, yalnız bilgilendiricidir.** Kelime sayısı YALNIZ `metin` (gövde) üzerinden; kök ve şıklar HARİÇ.

**K8 — Tek kök-kalıbı tavanı: ≤ %25 / test + ardışık tekrar YASAK.** 12 soruluk testte aynı kalıp ≤3; ayrıca iki ardışık soru aynı kök kalıbında olamaz. "…ulaşılabilir/ulaşılamaz?" ailesi bu tavana dahildir. → %15 vs %30 belirsizliği %25 lehine çözüldü.

**K9 — Bloom profili `sinav_turu` alanına bağlıdır.**
- `TYT`: Hatırla ~%5 · Anla ~%35 · Uygula ~%15 · Analiz ~%45 · Değerlendirme ~0.
- `AYT`: Anla ~%20 · Uygula ~%15 · Analiz ~%45 · Değerlendirme ~%15–20.
- `karma`: iki profilin ortalaması.
Varsayılan: `TYT` (içerik ağırlıklı TYT pratiği). → osym_tyt vs dab/AYT çelişkisi çözüldü.

**K10 — Cevap A–E dengesi: ASSEMBLY (montaj) katmanında uygulanır.** Seçenekler ajanı doğru şıkkın *içeriğini* üretir; **hangi harfe düşeceğine montaj adımı karar verir** (Python `tests_processor.rebalance`). Kanon: montajlanmış testte hiçbir harf **>%28 veya <%12** olamaz; 12'lik testte hiçbir harf >3, ardışık ≤2 aynı harf. → blueprint doğru harfi ÖN-ATAMAZ (bkz. B-boşluk G2).

**K11 — (cc)/(c.c.)/(sav) temizliği: pipeline aktif ayıklar.** Resmî içerikten gelen "(cc)", "(c.c.)", "Hz. Peygamber (sav.)" → temizlenir; yalnız "Hz. Muhammed (sav.)" korunur. (Python `CleanH` fonksiyonu bunu yapar; ajanlar da üretimde uymalıdır.)

**K12 — Köksüz (gövdesiz doğrudan bilgi) soru: ≤ %3 (çoğu test 0).** Mutlak yasak değil; ÖSYM'de nadir vardır. → soru_kalip'in mutlak yasağı "nadir izinli"ye çevrildi.

---

## B) BOŞLUK POLİTİKALARI (16 madde)

**G1 — `cozum` üretim kuralı (ZORUNLU alan).** Her soruda çözüm = 2–4 cümle: (1) doğru şıkkın **metne dayalı** gerekçesi (metinden hangi çıkarımla varıldığı), (2) her çeldiricinin **neden yanlış** olduğu (kısa, tek tümce). D8/D9 denetimi çözüm olmadan yapılamaz; çözüm zorunludur.

**G2 — Doğru cevap harfi ATAMASI montajda.** Blueprint doğru harf atamaz. Seçenekler ajanı doğru şıkkın içeriğini işaretler (`dogru` = içerikçe doğru şık). Montaj adımı A–E'yi dengeleyerek nihai harfleri belirler ve `cevap_kilit=true` yapar. Çeldirici sırası montajda kilitlenir.

**G3 — D1/D6 denetim aracı.** Çapraz-okuma botu bir LLM-hakemdir; anlamsal örtüşmeyi (D1) ve ortak-kelime tekrarını (D6) doğrudan okuyup yargılar — ayrı embedding altyapısı gerekmez. Deterministik ön-eleme için `pipeline/knowledge/tr_stopwords.txt` (kanonik Türkçe durak-kelime listesi) kullanılır: D1 kelime-kesişiminde ve D6 ortak-kelime tespitinde durak kelimeler sayılmaz.

**G4 + G5 — Olgusal/dinî doğruluk katmanı: D10 ve D11 (YENİ).** D1–D9 yapısaldır; buna ek `qc_icerik` katmanı:
- **D10 — Olgusal doğruluk:** doğru şık itikadî/olgusal olarak doğru mu; dört çeldirici gerçekten yanlış mı.
- **D11 — Dinî künye/kaynak doğruluğu:** ayet künyesi (Sure adı, sure:ayet) gerçek mi; meal Diyanet ölçütünde mi; hadis atfı makul mü; mezhepçilik/hurafe yok mu.
Çapraz-okuma botu bu iki kodu da puanlar. Ayet/meal için şimdilik LLM-hakem makullük denetimi + şüpheli künyeleri **işaretleme**; ileride bir meal/ayet referans DB'si eklenebilir (bkz. sonraki-iş). Yapısal olarak kusursuz ama D10/D11'i geçemeyen madde **yayına uygun değildir.**

**G6 + G7 — Kazanım kodları ve eşleme.** Kanon: kazanım kodları **`tymm/` resmî dosyalarından** alınır, ASLA uydurulmaz. `kazanim` alanı hem resmî kodu (`11.2.1`) hem serbest konu adını taşır. 9/10. sınıf tam kod listesi henüz çıkarılmadı → **9/10 üretiminden önce** ilgili tymm dosyasından çıkarılıp `kazanim_kodlari.md`'ye yazılmalı (11. sınıf pilotu için gerekli değil; 11 kodları dini_dil_kurallari.md'de var).

**G8 — Görsel soru temsili.** `gorsel:{tur, veri, alt_metin}|null`. Görselli soru v1'de nadir; kelime sayısı `metin`ten hesaplanır (görsel hariç). Çapraz-okuma `alt_metin`i okuyarak denetler; okunamayan görselli soru "manuel inceleme" etiketiyle işaretlenir.

**G9 — Düzeltici (fixer) iş akışı ve durma koşulu.**
- En fazla **3 revizyon turu.**
- Her tur **≥1 açık D-kodunu gerçek içerik değişikliğiyle** kapatmalı; salt biçimsel/kozmetik değişiklik (bkz. envanterdeki "v2" hatası) tur sayılmaz → `revizyon_gecmisi[].kapatilan_D` boşsa tur reddedilir.
- Revizyon blueprint'ten gelen **band / polarite / kazanım / hedef zorluğu KORUR.**
- Tur 2 sonunda hâlâ **D8 veya D9 açıksa** → yamala değil, **sıfırdan yeniden yaz** (aynı blueprint siparişiyle).
- 3 tur sonunda geçmezse → `etiket = "REVIZYON_ZORUNLU"`, insana bırakılır.

**G10 — 6 rol netleştirme.** Roller: (1) **soru-metni**, (2) **seçenekler**, (3) **test-kurgu** (blueprint + kazanım/DAB/Bloom planlaması bu role dahil), (4) **çapraz-okuma**, (5) **düzeltici** → 5 subagent. (6) **orchestrator** = Workflow scripti (subagent değil, koordinatör). Planlama/kazanım-seçimi ayrı bir ajan değildir; test-kurgu içindedir.

**G11 — DAB/Bloom etiketi blueprint'te doğar, çapraz-okuma doğrular.** test-kurgu her siparişe hedef `bloom` ve `dab_kodu` atar; soru-metni bunları gözeterek yazar; çapraz-okuma tutup tutmadığını denetler.

**G12 — Kelime toleransı.** `kelime_sayisi` **band sınırları içinde olmalı** (tolerans yok — bant ihlali RED). `hedef_kelime`'ye göre ±10 kelime sapma kabul (jitter). Çapraz-okuma bant dışını işaretler.

**G13 — Test hiyerarşisi.** soru → **test (9–12 soru)** → set/kitapçık (çok test). Set-düzeyi normlar (A–E %, olumsuz oran %, kalıp çeşitliliği) **tek test için test düzeyinde**, çok testli kitapçık için kitapçık düzeyinde uygulanır. `blueprint_ref` bağlayıcı katmanı belirtir.

**G14 — Çıktı/dizgi.** Kanonik temsil = semantik JSON. Render: altı çizili `<u>`/`w:u`, künye italik, şıklar Python backend'de dizilir (kısa şıklar 2–3 sütun, uzun şıklar alt alta). D7 botu `vurgu` alanının varlığını denetler (render'ı değil).

**G15 — Kimlik ve dedup.** `id = "DKAB{sinif}-U{unite}-{sira3}"` (ör. `DKAB11-U2-007`). Çapraz-okuma bir set içinde anlamsal yarı-mükerrerleri işaretler. Setler arası dedup: ileride tutulacak "görülen sorular" günlüğü (v2).

**G16 — Zorluk doğrulaması.** Çapraz-okuma atanan `zorluk`un gerçekten tuttuğunu denetler (metin yoğunluğu + çeldirici inceliği + Bloom düzeyi ekseninde); uyumsuzsa işaretler.

---

## C) VERİ SÖZLEŞMESİ (kanonik şemalar)

Üç JSON şeması `pipeline/schemas/` altında **bağlayıcıdır**; ajanlar bunlara birebir uyar:
- `blueprint.schema.json` — test-kurgu çıktısı (test planı + per-soru siparişleri).
- `soru.schema.json` — soru-metni + seçenekler ajanlarının doldurduğu kanonik soru nesnesi.
- `rapor.schema.json` — çapraz-okuma çıktısı (per-soru D1–D11 + etiket).

Handoff zinciri:
```
test-kurgu → blueprint.json (N sipariş)
  ↓ (her sipariş)
soru-metni → soru.metin, soru.kok, soru.vurgu, soru.metin_turu, kelime_sayisi, band
  ↓
seçenekler → soru.secenekler{A..E}, soru.dogru(içerik), soru.cozum
  ↓
çapraz-okuma → rapor.json (D1..D11, madde_puani, etiket)
  ↓ (etiket ≠ Yayina_uygun ise)
düzeltici → güncellenmiş soru.json (+revizyon_gecmisi) → tekrar çapraz-okuma (≤3 tur)
  ↓ (tüm sorular Yayina_uygun)
montaj (Python) → A–E dengeleme + docx/pdf
```

---

## D) PUANLAMA (kanon)

Madde puanı 0–100. Her D-kodu ağırlıklı; **D8 (ikinci doğru) veya D9 (son cümle sızıntısı) açıksa madde tavanı 60** (yayına uygun olamaz). D10/D11 (olgusal/dinî) açıksa **madde otomatik RED** (puandan bağımsız).

| Etiket | Koşul |
|---|---|
| `Yayina_uygun` | puan ≥ 85, D1–D11 hepsi geçti |
| `Kucuk_duzeltme` | 70 ≤ puan < 85, yalnız hafif D-kodları açık |
| `Buyuk_revizyon` | 50 ≤ puan < 70 |
| `Reddet` | puan < 50 **veya** D10/D11 açık |
| `REVIZYON_ZORUNLU` | 3 düzeltici turu sonrası D8/D9 hâlâ açık |

---

## E) v2 — DEĞERLENDİRMECİ GERİ BİLDİRİMİ SIKILAŞTIRMALARI (BAĞLAYICI; öncekilerle çelişirse BUNLAR geçerli)

Bir insan değerlendirmecinin çapraz okuması sonrası eklendi. En yıkıcı bulgu: montaj sonrası A–E karıştırması çözüm metnindeki harf atıflarını bozuyordu (11 soruda 7 çözüm↔anahtar uyuşmazlığı) ve bu, çapraz-okumadan SONRA gerçekleştiği için QC yakalayamıyordu.

**V1 — Cevap harfi BLUEPRINT'te ÖN-ATANIR; montajda shuffle YOKTUR (K10 revize).**
- test-kurgu her siparişe **dengeli** bir `hedef_dogru_harf` atar (A–E ~eşit; 12 soruda ör. A×3,B×2,C×3,D×2,E×2 — karıştırılmış).
- seçenekler doğru şıkkı **tam o harfe** yerleştirir, `dogru = hedef_dogru_harf` yapar ve çözümü **NİHAİ** harflere göre yazar.
- `assemble.py` **shuffle YAPMAZ**; sadece dizer. Böylece çözüm harfleri her zaman doğrudur.

**V2 — Çözüm harf tutarlılığı ZORUNLU + sabit biçim.**
- `cozum` **"Doğru cevap X: ..."** ile başlar (X = `dogru`). Devamda anılan tüm şık harfleri (`X şıkkı`, `X seçeneği`) NİHAİ `secenekler`/`dogru` ile birebir tutarlı olmalı.
- `validate.py` (yeni deterministik geçit) çözüm baş-harfini, tüm harf atıflarını ve cevap anahtarını `dogru` ile karşılaştırır; **herhangi bir uyuşmazlık = yayın engeli.** capraz-okuma da bunu denetler (harf muhasebesini asla LLM'e bırakma — deterministik geçit esastır).

**V3 — Çeldirici "karikatür yasağı" (D4 sıkılaştırma).** Çeldiriciler öğrenci yanılgısından / eksik-yanlış kavrayıştan üretilir. Sağduyuyla anında elenen aşırı, ideolojik ya da deyimsel çeldirici YASAK (ör. "dünyadan el etek çekmek", "kaçınılmaz çatışma", "diğerlerinden daha yetkin"). **Test:** "Bu çeldiriciyi, konuyu HİÇ bilmeyen biri bile eleyebilir mi?" → evet ise D4 KALDI. Her çeldirici, metni yarım/yanlış anlayan öğrenciyi çekecek kadar makul olmalı.

**V4 — Doğru şık TEK cümle parafrazı OLAMAZ (D1/D9 sıkılaştırma).** Doğru şık, gövdedeki tek bir cümlenin (ÖZELLİKLE son/sonuç cümlesinin) eş anlamlı tekrarı olamaz; en az iki ayrı bilgiden **sentezle** kurulur. **Test:** "Doğru şık, gövdeden tek bir cümle bulunup eş anlamlı yazılarak bulunabiliyor mu?" → evet ise D1 veya D9 KALDI. Analiz/Değerlendirme etiketli soruda bu ihlal aynı zamanda `bloom_uyum=false`.

**V5 — Tek savunulabilir cevap; aktif çürütme (D8 sıkılaştırma).** capraz-okuma doğru dışındaki **en güçlü** şıkkı seçip onu AKTİF savunmaya çalışır; savunulabiliyorsa D8 KALDI. "Vurgu / ana fikir / ulaşılabilir" köklerinde risk yüksektir: çeldiriciler "daha az merkezi ama yine de doğru" OLAMAZ — açıkça metin-dışı veya yanlış olmalı. Olumlu-çıkarım ("ulaşılabilir") kökünde birden çok şık metinden çıkarılabiliyorsa madde geçersizdir.

**V6 — Doğru şık uzunluk/kapsam PARİTESİ (D2 sıkılaştırma).** Doğru şık, diğerlerinden görünür biçimde daha uzun / daha kapsayıcı / daha akademik OLAMAZ. Doğru şık bir sentez ise, çeldiriciler de aynı kapsam ve uzunlukta (ama yanlış) yazılır. **Test:** en uzun şık = doğru şık ve diğerlerinden belirgin uzun ise D2 KALDI.

**V7 — Gövdede "seçenek mühendisliği" cümlesi YASAK (soru-metni + capraz-okuma).** Gövde kendi iç tutarlılığı için yazılır; yalnızca bir çeldiriciyi elemek veya bir şıkkı kurmak için eklenmiş, doğal bilgi akışını bozan cümle içeremez. **Test:** "Gövdede, çıkarıldığında metnin bütünlüğü bozulmayan ama tam da bir şıkkı doğrulayan/eleyen 'yerleştirilmiş' bir cümle var mı?" → varsa işaretle (soru-metni yazmamalı, capraz-okuma yakalamalı).

**V8 — Kazanım dengesi (test-kurgu).** Bir testte kazanımlar olabildiğince eşit dağıtılır: her kazanım **ortalama ±1 soru**. Bir kazanımı tek soruyla temsil edip başka birine 4 soru vermek YASAK (9–12 soru / 4 kazanım → her biri 2–3).

**V9 — Gerçek bilişsel düzey (soru-metni + secenekler + capraz-okuma).** Analiz/Değerlendirme etiketli sorularda görev "metindeki cümleyi eş anlamlı bul" OLAMAZ; en az iki öğeyi birleştiren çıkarım / karşılaştırma / genelleme gerekir. Bir testin **en az yarısı** gerçek çıkarım/analiz olmalı (salt anlama-parafraz maddeleri ≤ %50). capraz-okuma `bloom_uyum`u bu ölçütle sıkı uygular.

**V9b — Olumsuz "yerini bul" kökleri Analiz DEĞİLDİR (etiket dürüstlüğü).** "değinilmemiştir / bahsedilmemiştir / örnek gösterilemez" gibi, dört doğrulanabilir öncülü ayıklayıp aykırı olanı bulmaya dayanan olumsuz kökler biliş düzeyi olarak **Anla**'dır; bunları Analiz etiketleme. Gerçek Analiz payını şu köklerle doldur: çok-öğeli sentez ("ulaşılamaz" + gövdeden birleştirme), karşılaştırma (iki_gorus), öncül değerlendirme (I-II-III), çıkarım. test-kurgu Bloom profilini bu dürüstlükle kurar; capraz-okuma `bloom_uyum`u buna göre denetler (etiket Analiz ama görev "aykırı olanı bul" ise bloom_uyum=false).
