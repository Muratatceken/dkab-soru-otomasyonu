# DKAB Soru Yazdırma Otomasyonu

11. (ve 9/10.) sınıf Din Kültürü ve Ahlak Bilgisi için, ÖSYM TYT/AYT üslubunda,
özgün ve ölçme-değerlendirme kriterlerine uygun test soruları üreten **çok-ajanlı
otomasyon**. Kaynak materyal `SORU BANKASI/` altında (resmî ders kitapları, tymm
kazanımları, ÖSYM çıkmış sorular, eski soru bankaları).

## Sistem mimarisi

Üç katman:

1. **Bilgi tabanı** — `pipeline/knowledge/`
   - `00_KARAR_KAYDI.md` = **BAĞLAYICI KANON** (çelişkide bu geçerli). K1–K12 kural
     kararları + G1–G16 boşluk politikaları + D-kodu puanlama.
   - `kriterler_D1-D9.md` (madde-yazım rubriği), `osym_stil_{tyt,ayt}.md` (ÖSYM DNA),
     `soru_kalip_havuzu.md`, `kelime_bandi_ve_zorluk.md`, `dini_dil_kurallari.md`,
     `dab_becerileri_bloom.md` — insan-editable **kaynak-doğruluk** dosyaları.
   - `cards/*.card.md` — her ajan rolü için KB'den **damıtılmış lean kart**
     (build sırasında ajan sistem promptuna gömülür; ajan runtime'da tam KB'yi
     OKUMAZ → token tasarrufu). Kural değişince: önce ilgili `knowledge/*.md`,
     sonra `cards/` yenilenir, sonra `build_workflow.py`.
   - `tr_stopwords.txt` — D1/D6 için Türkçe durak-kelime listesi.

2. **Veri sözleşmesi** — `pipeline/schemas/{blueprint,soru,rapor}.schema.json`
   Ajanlar arası akan kanonik JSON. `soru` nesnesi: metin+kök (ayrı), band,
   kok_tipi, kalip, vurgu, secenekler{A..E}, dogru, cozum, qc{D1..D11}, etiket.

3. **Ajanlar + orchestrator + render**
   - `.claude/agents/*.md` — 5 subagent: **test-kurgu** (blueprint+kaynak bağlamı),
     **soru-metni** (gövde+kök), **secenekler** (5 şık+doğru+çözüm),
     **capraz-okuma** (acımasız D1-D11 denetimi), **duzeltici** (gerçek düzeltme).
   - `.claude/workflows/soru-uret.js` — orchestrator **şablonu**. `build_workflow.py`
     ajan md+kart içeriklerini buraya gömüp `soru-uret.built.js` üretir (çalıştırılan
     dosya budur; bu ortamda custom agentType tanınmadığı için gömme gerekiyor).
   - `pipeline/dkab_pipeline/` — Python render backend (docx/pdf/figür, A-E dengeleme).
   - `pipeline/kaynak/` — tymm+ders kitabı ünite PDF'lerinin txt cache'i (30 dosya).

Akış: `test-kurgu → blueprint + kaynak_baglami → pipeline(soru-metni → secenekler)
→ capraz-okuma (adversarial verify) → duzeltici döngü (≤3 tur, KANON G9) → montaj (Python) → docx`.

## Bir test üretmek (tam otomasyon)

```bash
source pipeline/venv/bin/activate

# 1) Kaynak cache'i garantile + Workflow args JSON'ı al:
python3 pipeline/uret.py args 11 2 12          # sinif unite soru_sayisi [sinav_turu]
```
Sonra Claude bu args ile orchestrator'ı çağırır:
`Workflow({ name: 'soru-uret', args: <yukarıdaki JSON> })`
(veya `/soru-uret` skill'i). Çıktı `{blueprint, sorular[], raporlar[], ozet}`;
`pipeline/output/DKAB{sinif}-U{unite}-T1.json`'a yaz.

```bash
# 2) Montaj + DOCX/PDF:
python3 pipeline/uret.py render pipeline/output/DKAB11-U2-T1.json
```

Ajan md'lerini veya kartları düzenledikten sonra **mutlaka** yeniden gömle:
```bash
python3 pipeline/build_workflow.py            # -> .claude/workflows/soru-uret.built.js
```

## Kesin kurallar (her zaman)

- **Türkçe içerik**, UTF-8. Shell'de Türkçe dosya adları/PDF için
  `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` kullan (yoksa mojibake olur).
- Kaynak PDF okurken önce `pipeline/kaynak/*.txt` cache'ini dene; yoksa
  `pdftotext -enc UTF-8 -layout`; bozuksa `pdftoppm -png` ile görsel oku.
- **Kanon (`00_KARAR_KAYDI.md`) diğer her dosyanın üstündedir.** Bir kural değişecekse
  önce kanona işle, sonra ilgili kartı yenile, sonra `build_workflow.py`.
- **Kozmetik yama yasak** (düzeltici gerçek içerik değişikliği yapar — envanterdeki
  "v2" hatası). `revizyon_gecmisi.kapatilan_D` boş olamaz.
- Kazanım kodları `SORU BANKASI/.../tymm/` resmî dosyalarından; **uydurma yok**.
  9/10. sınıf üretiminden önce o sınıfın kazanım kodları `dini_dil_kurallari.md`'ye
  eklenmeli (şu an yalnız 11. sınıf tam).
- Yeni docx üretirken hedef dosya açıksa üzerine yazılamaz; kapat ya da yeni ada yaz.

## Bilinen durum / sonraki işler
- ÖSYM'ye benzerlik pilotu (11.2) yapıldı: 11 soru, 9'u "Yayına uygun" (90-100 puan).
- Küçük iş: docx'te olumsuz vurgu şu an BÜYÜK harf; ÖSYM'nin altı-çizili biçimi için
  `docx_builder`'a underline-run eklenebilir.
- İleride: ayet/meal doğrulama için referans DB (D11 şu an LLM-hakem makullük denetimi);
  setler arası mükerrer-soru dedup günlüğü.
