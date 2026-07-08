# DKAB Soru Üretimi — Dinî Dil, Terminoloji ve Kazanım Kodu Kuralları

Bu belge, DKAB (Din Kültürü ve Ahlak Bilgisi) konu anlatımlı soru bankası üretiminde **bağlayıcı** olan dinî dil, terminoloji ve kazanım kodu kurallarını toplar. Kaynak: `_PIPELINE_DKAB11/MASTER_PROMPT_DKAB11.md` (§5 dinî dil, §6 dizgi, §9 kazanım kodları, §10 iş akışı) ve resmî TYMM kazanım dosyası (11. sınıf 2. ünite). Kurallardan sapma, projede **"berbat"** olarak değerlendirilir.

---

## 1) Dinî Dil Kuralları (bağlayıcı)

Aşağıdaki liste hem soru köklerinde hem de konu anlatımı metninde geçerlidir.

| # | Kural | DOĞRU | YANLIŞ |
|---|-------|-------|--------|
| 1 | "Allah" sözcüğünden sonra **(cc) / (c.c.) KONMAZ** | `Allah` | `Allah (c.c.)`, `Allah'ın (cc)` |
| 2 | "Hz. Peygamber" / "Peygamberimiz" gibi ifadelerden sonra **(sav) KONMAZ** | `Hz. Peygamber`, `Peygamberimiz` | `Hz. Peygamber (sav.)` |
| 3 | Salavat **yalnızca tam ad "Hz. Muhammed" ile** ve `(sav.)` biçiminde yazılır | `Hz. Muhammed (sav.)` | `Hz. Muhammed sav`, `Hz. Muhammed (s.a.v.)` |
| 4 | Soru kökünde **"ulaşılabilir"** kullanılır (arkaik/hatalı "ulaşılır" değil) | `…hangisine ulaşılabilir?` | `…hangisine ulaşılır?` |
| 5 | Olumsuz kök **seyrek** kurulur; olumsuz sözcük **BÜYÜK HARFLE** vurgulanır | `…hangisi SÖYLENEMEZ?`, `…DEĞİLDİR?` | `…hangisi söylenemez?` |
| 6 | Kök ve şıklarda **yasak pekiştireç** yok | (nötr ifade) | `sadece`, `yalnız`, `en çok`, `kesinlikle`, `asla` |

**Ayet künyesi biçimi.** Ayet, **kısa/öz meal + parantez içinde künye** olarak verilir. Biçim: `(Sure adı, sure:ayet)`.
- Örnek: `"…Göklerin ve yerin yaratılışında… akıl sahipleri için ibretler vardır." (Âl-i İmrân, 3:190)`
- Aralık için: `(Âl-i İmrân, 3:190-191)`. Sure adı Türkçe imlâsıyla ve tam yazılır (Âl-i İmrân, Rûm, Hadîd). Meal uzun tutulmaz; ayetin tamamı kopyalanmaz.

**Ton kuralı.** Metin **tarafsız, bilgilendirici ve ölçme odaklı**; **vaaz veren / öğüt veren** üslup yasaktır. "Unutmayalım ki…", "Rabbimiz bizden…", buyurgan ahlak dersi cümleleri kullanılmaz. Amaç bilgi/kavrama ölçmek, nasihat etmek değil.

**Hurafe ve mezhepçilik yasağı.** Hurafe, batıl inanç, dayanaksız keramet/olağanüstülük anlatıları **gerçek gibi** sunulmaz. Bir mezhep/ekol diğerine üstün gösterilmez; tartışmalı fıkhî-itikadî görüşler **tek doğru** olarak dayatılmaz. İçerik **MEB sınırları içinde**, abartıdan uzak kalır.

**Kök ve şık dili (§5–§6 dizgi ile birlikte).**
- Kök = **derli toplu kurumsal açıklama paragrafı (45–110 kelime)** ya da ayet/hadis + **kısa kalıp soru** ("Bu parçada aşağıdakilerden hangisi vurgulanmaktadır?", "…hangisine ulaşılabilir?", "…hangisi söylenemez?").
- **Senaryo/diyalog kökü YASAK** ("İki arkadaş konuşuyor / Ali dedi ki…").
- Şıklar **kısa, paralel** kavram/önerme öbekleri; **"çünkü…"li uzun şık yasak**. Metin birebir tekrar edilmez. **Tek tartışmasız doğru** cevap bulunur; cevaplar A–E'ye dengeli dağıtılır.

> **Önemli ayrım (kaynaklar arası çelişki):** Resmî TYMM kazanım dosyası kendi metninde `Allah'ın (cc)` biçimini kullanır (ör. 11.2.3 açıklaması). Soru bankası bu kullanımı **kaldırır** (Kural 1). Resmî dosyadan içerik alınırken `(cc)` ve benzeri kısaltmalar **temizlenmelidir**.

---

## 2) Kazanım Kod Yapısı

**Resmî format:** `DKAB.SINIF.ÜNİTE.KAZANIM` — nokta ile ayrılmış dört bileşen.
Örnek (resmî dosyadan birebir): `DKAB.11.2.1`, `DKAB.11.2.4`. Her kazanımın altında **öğrenme çıktısı süreç bileşenleri** `a) b) c) ç) d)` harfleriyle sıralanır.

**Kod normalleştirme kuralı.** Soru bankası içi kullanımda kod, `DKAB.` ön eki düşürülerek kısaltılır ve her sorunun başına **"KAZANIM 11.Ü.K. …"** satırı olarak yazılır (§6).
- Resmî: `DKAB.11.2.1` → Soru bankası satırı: `KAZANIM 11.2.1. Din tanımlarını ve din ile ilgili yaklaşımları genelleyebilme`
- Alt çıktı gerektiğinde harf korunur: `DKAB.11.2.4.c` → `11.2.4.c`.
- Sınıf her zaman 9/10/11; ünite ve kazanım numaraları resmî dosyadaki numaralandırmayla **bire bir** eşleşmelidir (uydurma alt kazanım üretilmez).

### 11. Sınıf ünite ve kazanım başlıkları (MASTER_PROMPT §9 + resmî dosya)

| Ünite | Başlık | Kazanım kodları (özet) |
|-------|--------|------------------------|
| Ü1 | İ­slam Düşüncesinde Yorumlar (Altın Standart) | 11.1.x |
| Ü2 | Din, Felsefe, Bilim ve Sanat | 11.2.1 Din tanımları/yaklaşımlar · 11.2.2 Din–felsefe–bilim ilişkisi · 11.2.3 Din–sanat · 11.2.4 Âl-i İmrân 190-191 |
| Ü3 | İslam Medeniyeti ve Gönül Coğrafyamız | 11.3.1 Medeniyetin oluşumu · 11.3.2 İzleri · 11.3.3 Bugünü-geleceği · 11.3.4 Rûm 9 |
| Ü4 | İnançla İlgili Meseleler | 11.4.1 Felsefî yaklaşımlar · 11.4.2 Kötülük problemi · 11.4.3 Din istismarı / yeni dinî hareketler · 11.4.4 Hadîd 1-5 |
| Ü5 | Yahudilik ve Hristiyanlık | 11.5.1 (+ alt kazanımlar — tam ifadeler resmî dosyadan alınır) |

### 11.2 kazanımlarının resmî tam ifadesi (örnek — birebir)

| Kod | Öğrenme çıktısı | Süreç bileşenleri |
|-----|-----------------|-------------------|
| DKAB.11.2.1 | Din tanımlarını ve din ile ilgili yaklaşımları **genelleyebilme** | a) bilgi toplar · b) ortak özellik · c) ortak olmayan özellik · ç) önermede bulunur |
| DKAB.11.2.2 | Dinin felsefe ve bilimle ilişkisini **sorgulayabilme** | a) merak · b) soru sorar · c) bilgi toplar · ç) doğruluğu değerlendirir · d) çıkarım |
| DKAB.11.2.3 | Din ve sanat arasındaki ilişkiyi **çözümleyebilme** | a) unsurları araştırır · b) ilişkileri tespit eder |
| DKAB.11.2.4 | Âl-i İmrân 190-191. ayetlerin mesajlarını **özetleyebilme** | a) çözümleme · b) sınıflandırma · c) açıklama |

> **Not:** 9. ve 10. sınıf ünite başlıkları bu kaynaklarda yer almadığından uydurulmamalı; her sınıf için ilgili resmî TYMM kazanım dosyasından (`…/tymm/…ÜNİTE… .pdf`) doğrulanarak alınmalıdır. Kod formatı ve normalleştirme kuralı üç sınıf için de aynıdır.

---

## 3) İçerik Doğruluğu ve Özgünlük

**Kelam / fıkıh terminolojisinde dikkat.**
- Kelamî görüşler **ekol adıyla** ve **tarafsız** verilir (ör. kötülük problemi 11.4.2'de bir ekolü "haklı" ilan etmeden aktarılır). İtikadî tartışmada tek doğru dayatılmaz.
- Terimler doğru ve tutarlı imlâyla yazılır. Resmî dosyanın anahtar kavramları esas alınır: **âlim, Beytülhikme, darülhadis, darülkurra, filozof, ilim, medrese, rasathane** (resmî metnin gövdesinde geçen `darulkurra` gibi hatalı biçimler düzeltilir → **darülkurra**).
- "Din" ile "din anlayışı/yorumu" ayrımı korunur (11.2.1 açıkça bunu ister: din anlayışının dinden farkına vurgu). Felsefe/bilim ile din **çelişmeyen, etkileşim hâlindeki** alanlar olarak sunulur (11.2.2 çıkarımı).
- Ayet atfı ve nüzul/bağlam bilgisi doğru olmalı; meal **Diyanet İşleri Başkanlığı meali** ölçütünde, künye hatasız verilir.

**Devlet ders kitabını kopyalamama (özgünlük).** İçerik temeli olarak ders kitabı ve resmî kazanım okunur, **atıf yapılır**, ancak cümleler **birebir kopyalanmaz** (§10). Paragraflar özgün ifadeyle yeniden yazılır; kazanımın ölçtüğü davranışa (genelleme, sorgulama, çözümleme, özetleme) uygun, TYT/AYT ölçme çizgisinde özgün kök ve şıklar üretilir. Kopya metin, hatalı künye, hurafe/abartı ve mezhepçilik projede kabul edilmez.
