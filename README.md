# DKAB Soru Yazdırma Otomasyonu

Din Kültürü ve Ahlak Bilgisi (DKAB) için **ÖSYM TYT/AYT üslubunda**, özgün ve
ölçme-değerlendirme kriterlerine uygun test soruları üreten **çok-ajanlı**
bir otomasyon. 9/10/11. sınıf kazanımlarına dayanır; soruları üretir,
acımasızca eleştirir (D1–D11 rubriği), gerçek içerik değişikliğiyle düzeltir
ve DOCX/PDF olarak dizer.

> Not: Bu depo **otomasyon kodunu** içerir. Telifli kaynak materyaller (ders
> kitapları, TYMM kazanım PDF'leri, ÖSYM çıkmış sorular) **depoda yoktur** —
> onları kendin sağlarsın (bkz. [Kaynak materyalleri sağla](#5-kaynak-materyalleri-sağla)).

---

## İçindekiler

1. [Ne yapar, nasıl çalışır](#ne-yapar-nasıl-çalışır)
2. [Mimari](#mimari)
3. [Ajanlar (kim ne yazar)](#ajanlar-kim-ne-yazar)
4. [Bilgi tabanı ve KANON](#bilgi-tabanı-ve-kanon)
5. [Veri sözleşmesi (şemalar)](#veri-sözleşmesi-şemalar)
6. [Kurulum — sıfırdan](#kurulum--sıfırdan)
7. [Kullanım — bir test üret](#kullanım--bir-test-üret)
8. [Bilgi tabanını güncelleme iş akışı](#bilgi-tabanını-güncelleme-iş-akışı)
9. [Doğrulama geçidi (validate.py)](#doğrulama-geçidi-validatepy)
10. [Proje düzeni](#proje-düzeni)
11. [Sözlük](#sözlük)
12. [Bilinen sınırlamalar / yol haritası](#bilinen-sınırlamalar--yol-haritası)
13. [Sorun giderme](#sorun-giderme)
14. [Linux / Windows](#linux--windows)
15. [Lisans](#lisans)

---

## Ne yapar, nasıl çalışır

Girdi olarak `{sınıf, ünite, sınav türü, soru sayısı}` verirsin; çıktı olarak
ÖSYM tarzı, kaynağa dayalı, çapraz okumadan geçmiş bir DOCX/PDF test alırsın.
Aradaki iş beş ayrı **subagent**'in bir **orchestrator** tarafından
koordine edildiği bir üretim hattıdır:

```
                       ┌────────────────────────────────────────┐
                       │   test-kurgu (1×, tüm test için)        │
                       │   kaynağı okur → blueprint + kazanım    │
                       │   bağlamı kurar (N adet "sipariş")      │
                       └───────────────────┬──────────────────────┘
                                            │  N sipariş (paralel pipeline)
              ┌─────────────────────────────┼─────────────────────────────┐
              ▼                             ▼                             ▼
      sipariş #1                    sipariş #2                   sipariş #N
      soru-metni → seçenekler       soru-metni → seçenekler      soru-metni → seçenekler
              │                             │                             │
              ▼                             ▼                             ▼
      capraz-okuma (D1–D11) ──gecti≠Yayina_uygun──► düzeltici ──► capraz-okuma (tekrar)
              │  (≤3 tur; G9)                                              │
              ▼                                                           ▼
              └─────────────────────── {soru, rapor} ─────────────────────┘
                                            │
                                            ▼
                     orchestrator dönüşü: {blueprint, sorular[], raporlar[], ozet}
                                            │
                                            ▼
                 validate.py (deterministik geçit: harf/band/kazanım) ─► HARD hata varsa DUR
                                            │
                                            ▼
                     assemble.py (A–E dengeleme, montaj) → DOCX/PDF
```

Önemli tasarım kararları:

- **Her soru bağımsız bir pipeline'dır** — bir sorunun düzeltme döngüsü
  diğerini beklemez/etkilemez (`Workflow` `pipeline()` ile modellenir).
- **Doğru cevap harfi montajda karıştırılmaz.** `test-kurgu` her siparişe
  baştan dengeli bir `hedef_dogru_harf` atar; `seçenekler` doğru şıkkı tam o
  harfe yazar; `assemble.py` shuffle yapmaz. Bu, projenin en yıkıcı geçmiş
  hatasını (çözüm metni ↔ cevap anahtarı harf kayması) **yapısal olarak**
  imkânsız kılar (KANON V1/V2).
- **Çapraz okuma kayırmaz.** `capraz-okuma` ajanı "şüphede kalırsan kaldı
  ver" talimatıyla çalışır; puanı düşürmek onun işi, soruyu geçirmek değil.
- **Düzeltme kozmetik olamaz.** `düzeltici` yalnızca raporda `gecti=false`
  olan kodları gerçek içerik değişikliğiyle kapatır; hiçbir şey kapatmadıysa
  turu geçersiz sayar (KANON G9).
- **Son sözü kod söyler, LLM değil.** `validate.py`, çözüm↔cevap anahtarı
  harf tutarlılığını regex ile deterministik denetler; LLM'in harf
  muhasebesine güvenilmez (V2). Sert hata varsa render **durur**.

---

## Mimari

Üç katman:

1. **Bilgi tabanı** — `pipeline/knowledge/`. `00_KARAR_KAYDI.md` **bağlayıcı
   kanondur**; çelişkide bu geçerlidir. Diğer dosyalar (ÖSYM stil DNA'sı,
   D1–D9 rubriği, kalıp havuzu, kelime bandı, dinî dil kuralları, DAB/Bloom)
   insan-editable kaynak-doğruluk dosyalarıdır. `cards/*.card.md` her ajan
   rolü için KB'den damıtılmış, build sırasında sistem promptuna gömülen
   "lean kart"tır (ajan runtime'da tam KB'yi okumaz → token tasarrufu).
2. **Veri sözleşmesi** — `pipeline/schemas/{blueprint,soru,rapor}.schema.json`.
   Ajanlar arası akan kanonik JSON'un tek doğruluk kaynağı.
3. **Ajanlar + orchestrator + render** — `.claude/agents/*.md` (5 subagent),
   `.claude/workflows/soru-uret.js` (orchestrator şablonu; `build_workflow.py`
   ajan md + kart içeriklerini buraya gömüp çalıştırılabilir
   `soru-uret.built.js`'i üretir), `pipeline/dkab_pipeline/` (Python render
   backend), `pipeline/validate.py` (deterministik doğrulama geçidi).

Neden "gömme" (build) adımı var? Bu ortamda Claude Code Workflow'ları
custom `agentType` tanımıyor; bu yüzden her subagent'in `.md` sistem
promptu + kartı, `build_workflow.py` tarafından `general-purpose` ajana
verilecek bir string olarak `soru-uret.built.js` içine JSON literal olarak
gömülür. **Sonuç:** ajan md'lerini veya kartlarını her düzenlediğinde
`python3 pipeline/build_workflow.py` çalıştırmadan değişiklik etkili olmaz.

---

## Ajanlar (kim ne yazar)

| Ajan | Girdi | Çıktı | Görev |
|---|---|---|---|
| **test-kurgu** | `{sinif, unite, sinav_turu, soru_sayisi, tymm_yolu, ders_kitabi_yolu}` | `{blueprint, kaynak_baglami}` | Kaynağı (TYMM kazanımları + ders kitabı) okuyup kazanım kapsamını çıkarır; N soruyu kelime bandı/polarite/zorluk/kalıp/Bloom açısından **dengeli-ama-standart-olmayan** biçimde dağıtır (bkz. [KANON](#bilgi-tabanı-ve-kanon) K3/K7/K8/K9). Her siparişe bir `hedef_dogru_harf` de atar (V1). |
| **soru-metni** | tek bir blueprint siparişi + kazanım bağlamı | gövde metni + kök | Sorunun **gövde metnini** (stimulus, 30–150 kelime, band'a uygun) ve **soru kökünü** (ayrı paragraf) yazar. Şık yazmaz, doğru cevabı ima etmez. |
| **seçenekler** | gövde+kök hazır soru | `secenekler{A..E}, dogru, cozum` | 5 şık, doğru cevap ve çözüm yazar. Metinden birebir taşımaz, zıt/eş çift içermez, çeldiricileri kavram yanılgısına dayandırır, doğru şıkkı `hedef_dogru_harf`e yerleştirir. |
| **capraz-okuma** | tam soru nesnesi | `rapor.schema.json` (D1–D11 + puan + etiket) | Soruyu **acımasızca** denetler; her D-kodu için kanıt ve somut düzeltme önerisi üretir. Şüphede "kaldı" verir. |
| **düzeltici** | `{soru, rapor, tur}` | güncellenmiş soru nesnesi | Açık D-kodlarını **gerçek içerik değişikliğiyle** kapatır (kozmetik yama yasak). Blueprint'ten gelen band/polarite/kazanım/zorluğu korur. 2. tur sonunda D8/D9 hâlâ açıksa sıfırdan yeniden yazar. |

Bu beşi `.claude/agents/*.md` dosyalarında tanımlıdır — her biri kendi
"ÖNCE OKU" listesiyle hangi KB dosyalarını temel aldığını belirtir (build
adımında bu liste kartla değiştirilir, ajan runtime'da KB dosyasını
okumaz). **Orchestrator** (`.claude/workflows/soru-uret.js`) bir subagent
değildir — Workflow scripti olarak yukarıdaki akışı koordine eden 6. roldür
(KANON G10).

---

## Bilgi tabanı ve KANON

`pipeline/knowledge/00_KARAR_KAYDI.md`, sistemin en sık karşılaşılan
belirsizliklerini önceden çözmüş bağlayıcı bir kural kümesidir. Rehber
amaçlı, en önemlileri:

| Kod | Kural (özet) |
|---|---|
| K2 | Olumsuz/sınırlayıcı vurgu `vurgu:{sozcuk, bicim:"alti_cizili"}` ile işaretlenir; olumsuz kökte zorunlu. |
| K3 | Olumsuz kök oranı testte ~%40 (%35–45); altına düşerse set RED. |
| K7 | Kelime bandı: 30–70 / 70–100 / 100–150 arası her birinden 3–4 soru (yalnız gövde sayılır). |
| K8 | Aynı kök kalıbı bir testte ≤%25; iki ardışık soru aynı kalıpta olamaz. |
| K9 | Bloom profili `sinav_turu`na bağlı (TYT: Analiz ağırlıklı ~%45; AYT: Değerlendirme de girer). |
| K10 | A–E dengesi **montaj** katmanında; hiçbir harf testte >%28. |
| V1/V2 | Doğru harf **blueprint'te ön atanır**, montajda shuffle yok; çözüm "Doğru cevap X:" ile başlar ve harfler tutarlı olmalı — bu depoda en kritik kural (bkz. [Ne yapar, nasıl çalışır](#ne-yapar-nasıl-çalışır)). |
| V3–V9b | Çeldirici "karikatür" yasağı, doğru şıkkın tek-cümle-parafrazı olamaması, tek savunulabilir doğru, uzunluk paritesi, "seçenek mühendisliği cümlesi" yasağı, kazanım dengesi, gerçek bilişsel düzey (Analiz etiketi şişirilemez). |
| F1–F4 | **v3 — 10/10 hedefi** (en güncel katman): gerçek analiz arketipleri ≥%40, "vurgu" kökünde metin-içi doğrulanabilir çeldirici yasağı, editoryal cila (dolgu cümle yok, aynı kaynaktan ≤1 soru, hiçbir şık gövde cümlesinin parafrazı değil) ve **çok-mercekli doğrulama paneli** (tek-doğru avukatı / bilişsel-derinlik hakemi / editör merceği — bkz. [Bilinen sınırlamalar](#bilinen-sınırlamalar--yol-haritası)). |

D1–D11 madde-denetim kodlarının tam tanımı `pipeline/knowledge/kriterler_D1-D9.md`
ve `00_KARAR_KAYDI.md` §D'dedir; kısa özet:

| Kod | Ne denetler |
|---|---|
| D1 | Şıkta gövdeden birebir/kelime-avcılığı taşıma |
| D2 | Doğru şıkkın uzunluk/akademiklikle kendini ele vermesi |
| D3 | Aynı beşlide zıt veya eş anlamlı şık çifti |
| D4 | İşlevsiz/saçma çeldirici (kavram yanılgısına dayanmalı) |
| D5 | Şıklarda yasak pekiştireç (yalnız/sadece/kesinlikle/asla…) |
| D6 | Beş şıkta tekrarlanan, köke taşınması gereken ortak kelime |
| D7 | Olumsuz kökte `vurgu` alanının doluluğu |
| D8 | İkinci savunulabilir doğru şık (tek-doğru ihlali) |
| D9 | Cevabın gövdenin son cümlesinde açıkça sızması (en sık hata) |
| D10 | Olgusal/itikadî doğruluk |
| D11 | Dinî künye/kaynak doğruluğu (ayet, meal, hadis atfı) |

Puanlama: 0–100, **D8/D9 açıksa tavan 60**, **D10/D11 açıksa otomatik Reddet**.
Etiketler: `Yayina_uygun` (≥85) / `Kucuk_duzeltme` (70–84) / `Buyuk_revizyon`
(50–69) / `Reddet` (<50 veya D10/D11) / `REVIZYON_ZORUNLU` (3 tur sonrası
D8/D9 hâlâ açık).

Okuma sırası ve her dosyanın kim tarafından okunduğu:
[`pipeline/knowledge/README.md`](pipeline/knowledge/README.md).

---

## Veri sözleşmesi (şemalar)

Üç JSON şeması (`pipeline/schemas/`) ajanlar arası **bağlayıcı** sözleşmedir:

- **`blueprint.schema.json`** — test-kurgu çıktısı: `siparisler[]` (her biri
  bir soruya karşılık gelir: `band, hedef_kelime, kok_tipi, zorluk, kalip,
  metin_turu, bloom, kazanim_kod, hedef_dogru_harf`) + `dagilim_ozeti`
  (planın kendi normlarına uyduğunun öz-denetimi).
- **`soru.schema.json`** — kanonik soru nesnesi: `metin` (gövde) + `kok`
  ayrı alanlar, `secenekler{A..E}`, `dogru`, `cozum`, `qc`/`qc_icerik`
  (D1–D11 sonuçları), `revizyon_gecmisi`.
- **`rapor.schema.json`** — çapraz-okuma çıktısı: her D-kodu için
  `{gecti, kanit, oneri}`, `madde_puani`, `etiket`, `en_kritik_sorunlar`.

Minik bir `soru` örneği (alanlar kısaltıldı):

```json
{
  "id": "DKAB11-U2-007",
  "sinif": 11, "sinav_turu": "TYT", "unite": 2,
  "kazanim": { "kod": "11.2.1", "serbest_konu": "Din ve felsefe ilişkisi" },
  "bloom": "Analiz", "zorluk": "orta",
  "metin": "…(gövde, 70-100 kelime bandında)…",
  "metin_turu": "aciklama", "kelime_sayisi": 84, "band": "70-100",
  "kok": "Bu parçaya göre din ile felsefe arasındaki ilişki için…",
  "kok_tipi": "olumsuz", "kalip": "K-N2",
  "vurgu": { "sozcuk": "söylenemez", "bicim": "alti_cizili" },
  "secenekler": { "A": "…", "B": "…", "C": "…", "D": "…", "E": "…" },
  "dogru": "C",
  "cozum": "Doğru cevap C: … (A) … çünkü …"
}
```

---

## Kurulum — sıfırdan

Aşağıdaki adımlar **macOS** içindir. Linux/Windows notları [en sonda](#linux--windows).

### 0. Neye ihtiyacın var (özet)

| Bileşen | Zorunlu mu? | Ne için |
|---|---|---|
| Git | ✅ | depoyu klonlamak |
| Python 3.9+ | ✅ | render backend, cache, runner |
| Poppler (`pdftotext`) | ✅ | kaynak PDF'leri okumak |
| **Claude Code CLI** + Anthropic hesabı (Opus erişimi) | ✅ | ajanları/orchestrator'ı çalıştırmak |
| Google Chrome | ➖ opsiyonel | infografik rasterize / HTML→PDF (temel test üretimi için gerekmez) |
| LibreOffice (`soffice`) | ➖ opsiyonel | DOCX→PDF önizleme |
| Pandoc | ➖ opsiyonel | DOCX okuma/dönüştürme |
| unrar | ➖ opsiyonel | elinde .rar arşivler varsa açmak |

### 1. Homebrew'i kur (paket yöneticisi)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Kurulum bittiğinde ekrandaki "Next steps" talimatını uygula (Apple Silicon'da
genelde `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile` gibi bir
satır). Doğrula: `brew --version`.

### 2. Sistem araçlarını kur

```bash
# Zorunlu
brew install git python@3.12 poppler

# Opsiyonel (önizleme/dönüştürme ve arşivler için)
brew install pandoc libreoffice
brew install --cask google-chrome
brew install carlocab/personal/unrar   # veya: brew install rar
```

Doğrula:

```bash
git --version
python3 --version        # 3.9+ olmalı
pdftotext -v             # poppler
```

### 3. Claude Code'u kur ve giriş yap

Otomasyonun ajanları/orchestrator'ı Claude Code içinde çalışır (Opus modeli).

```bash
# Node gerektirir; yoksa: brew install node
npm install -g @anthropic-ai/claude-code

# Proje dizininde bir kez giriş yap (tarayıcıdan Anthropic hesabı / API anahtarı)
claude
```

> Claude Code hakkında ayrıntı: <https://docs.claude.com/claude-code>. Opus 4.x
> erişimi olan bir Anthropic hesabı/aboneliği gerekir.

### 4. Depoyu klonla ve Python ortamını kur

```bash
git clone https://github.com/Muratatceken/dkab-soru-otomasyonu.git
cd dkab-soru-otomasyonu

python3 -m venv pipeline/venv
source pipeline/venv/bin/activate
pip install --upgrade pip
pip install -r pipeline/requirements.txt
```

### 5. Kaynak materyalleri sağla

Depoda **telifli materyal yoktur.** Kendi PDF'lerini şu yapıda bir klasöre koy:

```
<kaynak_dizini>/
├── tymm/                                   # resmî TYMM kazanım PDF'leri
│   ├── 11.Sınıf 3. ÜNİTE_ ....pdf          # ad "{sınıf}.Sınıf {ünite}. ÜNİTE_" ile başlamalı
│   └── ...
└── DERS KİTAPLARI/                         # ders kitabı ünite PDF'leri
    ├── dkab 11_3. ünite.pdf                # ad "dkab {sınıf}_{ünite}. ünite.pdf" olmalı
    └── ...
```

Varsayılan konum `SORU BANKASI/SORULAR (AÇI)/YENİ DERS KİTAPLARI`'dır. Başka yere
koyduysan ortam değişkeniyle göster:

```bash
export DKAB_KAYNAK_DIR="/tam/yol/kaynak_dizini"
```

Sonra bir kez PDF'leri metne cachele (her testte pdftotext çalışmasın diye):

```bash
python3 pipeline/kaynak_cache.py            # tüm 9/10/11 × 5 üniteyi cacheler
# veya tek ünite: python3 pipeline/kaynak_cache.py 11 3
```

### 6. Orchestrator'ı derle (build)

Ajan md'leri + kartları çalıştırılabilir workflow'a gömer:

```bash
python3 pipeline/build_workflow.py          # -> .claude/workflows/soru-uret.built.js
```

Ajan md'lerini veya kartları her değiştirdiğinde bu komutu tekrar çalıştır
(bkz. [Bilgi tabanını güncelleme iş akışı](#bilgi-tabanını-güncelleme-iş-akışı)).

---

## Kullanım — bir test üret

Proje dizininde Claude Code'u aç (`claude`). En kolay yol, doğal dille istemek:

> "11. sınıf 3. ünite için 12 soruluk TYT testi üret."

Claude Code, [`CLAUDE.md`](CLAUDE.md)'yi okuyup şu adımları yürütür. İstersen
elle de yapabilirsin, ya da `/soru-uret` skill'ini çağırabilirsin:

```bash
# 1) Kaynak cache'i garantile + Workflow argümanlarını al
python3 pipeline/uret.py args 11 3 12       # sinif  unite  soru_sayisi  [TYT|AYT]
```

Çıkan JSON ile orchestrator'ı çalıştır (Claude Code Workflow aracı):

```
Workflow({ name: "soru-uret", args: <yukarıdaki JSON> })
```

Orchestrator ilerlemeyi 4 fazda gösterir (**Kurgu → Yaz → Denetle → Düzelt**)
ve tamamlanınca `{blueprint, sorular[], raporlar[], ozet}` döndürür. Bunu
`pipeline/output/DKAB11-U3-T1.json` olarak kaydet, sonra dize:

```bash
# 2) Doğrulama geçidi + montaj (A–E dengeleme) + DOCX
python3 pipeline/uret.py render pipeline/output/DKAB11-U3-T1.json
```

Çıktı: `pipeline/output/DKAB11-U3-T1.docx` (+ `.pdf`, LibreOffice kuruluysa).
`render` komutu önce `validate.py`'yi çalıştırır; sert hata varsa (ör. çözüm↔
cevap anahtarı harf uyuşmazlığı) **DOCX yazılmaz**, önce düzeltici/çapraz-okuma
turunu tekrarlaman ya da soruyu yeniden üretmen istenir.

Tek bir soru veya sipariş üzerinde tekrar çalışmak istersen, `soru-uret`
workflow'unu `resumeFromRunId` ile devam ettirebilirsin (bkz. Claude Code
Workflow dokümantasyonu) — değişmeyen `agent()` çağrıları cache'ten döner,
yalnız değişen sipariş yeniden çalışır.

---

## Bilgi tabanını güncelleme iş akışı

Bir kural değişecekse (örn. yeni bir D-kodu, farklı bir bant dağılımı,
yeni bir stil kısıtı), sırayla:

1. **Önce kanon** — `pipeline/knowledge/00_KARAR_KAYDI.md`'ye yeni kararı
   veya değişikliği işle (çelişkide bu dosya kazanır).
2. **Sonra ilgili KB dosyası** — kuralın ayrıntılı gerekçesi/örneği hangi
   dosyaya aitse (`kriterler_D1-D9.md`, `osym_stil_*.md`,
   `soru_kalip_havuzu.md`, `kelime_bandi_ve_zorluk.md`,
   `dini_dil_kurallari.md`, `dab_becerileri_bloom.md`) orayı güncelle.
3. **Sonra ilgili kart(lar)** — `pipeline/knowledge/cards/*.card.md`; hangi
   ajanın davranışı değişecekse onun kartına **kısa, uygulanabilir** bir
   madde ekle (kart, tam KB dosyasının yerini alan damıtılmış versiyondur —
   ajan runtime'da tam KB'yi okumaz, yalnız kartı görür).
4. **Ajan md'sini gerekiyorsa güncelle** — `.claude/agents/*.md` (nadiren;
   çoğu kural değişikliği yalnız kartla çözülür).
5. **Yeniden derle** — `python3 pipeline/build_workflow.py`. Bu adımı
   atlarsan değişiklik hiçbir etki yapmaz (çalışan dosya `soru-uret.built.js`'dir,
   `soru-uret.js` yalnızca şablondur ve git'e commit'lenir; `built.js`
   `.gitignore`'dadır, her geliştirici kendi makinesinde üretir).
6. **Doğrula** — küçük bir smoke test üret (`soru_sayisi` düşük, örn. 3) ve
   çapraz-okuma raporlarının yeni kuralı gerçekten uyguladığını kontrol et.

---

## Doğrulama geçidi (validate.py)

`pipeline/validate.py`, LLM'lerin harf muhasebesinde güvenilmez olduğu
gerçeğinden hareketle eklenmiş **deterministik, kod-tabanlı** bir son
kontroldür. `uret.py render` montajdan önce bunu otomatik çalıştırır;
elle de çağırabilirsin:

```bash
python3 pipeline/validate.py pipeline/output/DKAB11-U3-T1.json
```

Denetlediği şeyler:

- **Sert hatalar (render durur):** `dogru` geçersiz/eksik şık; çözümün
  baş harfi `dogru`dan farklı; çözüm içinde geçen herhangi bir "doğru cevap
  X" ifadesinin `dogru`yla çelişmesi; `kelime_sayisi`nin `band` dışına
  taşması.
- **Uyarılar (render durmaz ama işaretlenir):** çözüm "Doğru cevap X:" biçim
  kalıbına tam uymuyor; `dogru`, blueprint'in ön-atadığı `hedef_dogru_harf`ten
  farklı; set genelinde bir harf %28'i aşıyor; kazanım dağılımında fark >2
  (V8).

---

## Proje düzeni

```
.
├── CLAUDE.md                     # mimarinin tam dökümü (her Claude Code oturumu okur)
├── README.md                     # bu dosya
├── .claude/
│   ├── agents/                   # 5 subagent tanımı (test-kurgu, soru-metni, ...)
│   └── workflows/
│       ├── soru-uret.js          # orchestrator ŞABLONU (git'e commit'lenir)
│       └── soru-uret.built.js    # build_workflow.py çıktısı — ÇALIŞTIRILAN dosya (.gitignore'da)
├── pipeline/
│   ├── knowledge/                # BİLGİ TABANI — 00_KARAR_KAYDI.md (kanon) + kurallar
│   │   ├── 00_KARAR_KAYDI.md     # bağlayıcı kanon (K-kodları, G-boşluk politikaları, V/F sıkılaştırmaları)
│   │   ├── kriterler_D1-D9.md    # yapısal madde-yazım rubriği
│   │   ├── osym_stil_{tyt,ayt}.md# ÖSYM üslup DNA'sı
│   │   ├── soru_kalip_havuzu.md  # kök kalıbı + metin türü havuzu
│   │   ├── kelime_bandi_ve_zorluk.md
│   │   ├── dini_dil_kurallari.md # dinî dil/terminoloji + kazanım kod yapısı
│   │   ├── dab_becerileri_bloom.md
│   │   ├── tr_stopwords.txt      # D1/D6 için durak-kelime listesi
│   │   └── cards/                # ajanlara gömülen damıtılmış kartlar
│   ├── schemas/                  # ajanlar arası JSON veri sözleşmesi
│   │   └── {blueprint,soru,rapor}.schema.json
│   ├── dkab_pipeline/             # Python render backend
│   │   ├── docx_builder.py       # OOXML/DOCX üretimi (python-docx kullanmaz)
│   │   ├── rasterize.py          # HTML figürleri Chrome headless ile PNG'e çevirir
│   │   ├── tests_processor.py    # pipe-delimited test parse + A-E dengeleme
│   │   └── pdf_render.py         # chrome --headless --print-to-pdf sarmalayıcısı
│   ├── kaynak/                   # kaynak PDF'lerin txt cache'i (30 dosya, 9/10/11×5 ünite×2)
│   ├── output/                   # üretilen json/docx/pdf çıktıları
│   ├── build_workflow.py         # ajan md + kart → soru-uret.built.js
│   ├── kaynak_cache.py           # kaynak PDF → txt cache
│   ├── uret.py                   # tek-komut sürücü (args / render)
│   ├── assemble.py               # JSON → doğrulama → A–E dengeleme → DOCX
│   ├── validate.py               # deterministik doğrulama geçidi (V1/V2/V8)
│   └── requirements.txt
└── (SORU BANKASI/ — telifli kaynak; .gitignore'da, depoda yok)
```

---

## Sözlük

Sistemin kendi terimleriyle konuştuğu için kısa bir sözlük:

| Terim | Anlamı |
|---|---|
| **blueprint** | Soru üretilmeden önce testin planı; her biri bir soruya karşılık gelen `siparişler` listesi. |
| **sipariş** | Blueprint'teki tek bir madde planı: `{band, hedef_kelime, kok_tipi, zorluk, kalip, metin_turu, bloom, kazanim_kod, hedef_dogru_harf}`. |
| **band** | Gövde metninin kelime sayısı aralığı: `30-70` / `70-100` / `100-150`. |
| **kök (kok)** | Soru cümlesi; gövdeden ayrı, "Bu parçaya göre…" tarzı köprüyle bağlanan paragraf. |
| **kok_tipi** | `olumlu` veya `olumsuz` (olumsuzda `vurgu` alanı zorunlu). |
| **kalıp** | Kök kalıp kodu (`soru_kalip_havuzu.md`'den, ör. `K-N2`); tekdüzeliği önlemek için çeşitlendirilir. |
| **vurgu** | Olumsuz/sınırlayıcı kökte altı çizilecek sözcük: `{sozcuk, bicim:"alti_cizili"}`. |
| **D-kodu (D1–D11)** | çapraz-okuma'nın denetlediği madde-yazım/olgusal kusur kategorileri (bkz. tablo yukarıda). |
| **K-kodu / G-kodu / V-kodu / F-kodu** | `00_KARAR_KAYDI.md`'deki kural kimlikleri: K=çelişki çözümü, G=boşluk politikası, V=v2 sıkılaştırması, F=v3 ("10/10 hedefi") sıkılaştırması. |
| **etiket** | çapraz-okuma'nın madde için verdiği nihai karar: `Yayina_uygun` / `Kucuk_duzeltme` / `Buyuk_revizyon` / `Reddet` / `REVIZYON_ZORUNLU`. |
| **kart (card)** | Bir ajan rolüne özel, tam KB'den damıtılmış kısa kural özeti; build sırasında ajan sistem promptuna gömülür. |
| **montaj** | `assemble.py`'nin yaptığı son adım: A–E harflerini dengeler (şu an shuffle YOK, V1 sonrası), DOCX'e diz. |

---

## Bilinen sınırlamalar / yol haritası

- **F4 çok-mercekli panel henüz orchestrator döngüsüne bağlı değil.**
  `00_KARAR_KAYDI.md` §F4, yayına uygunluğun "tek-doğru avukatı /
  bilişsel-derinlik hakemi / editör merceği" gibi bağımsız merceklerin
  HEPSİ geçince verilmesini şart koşuyor; `soru-uret.js` içinde bu
  merceklerin prompt'ları (`LENS_TEKDOGRU`, `LENS_DERINLIK`, `LENS_EDITOR`)
  tanımlı ama Stage 3 (denetle/düzelt) döngüsüne henüz **kablolanmadı** —
  şu an yalnız tek bir `capraz-okuma` çağrısı D1–D11'i denetliyor. Bunu
  etkinleştirmek için Stage 3'te çapraz-okuma sonrası (etiket geçtiyse bile)
  3 mercek ajanının paralel çağrılması ve herhangi biri `gecti=false`
  dönerse düzeltici döngüsüne sokulması gerekir.
- **9/10. sınıf kazanım kodları eksik.** `dini_dil_kurallari.md` şu an
  yalnız 11. sınıfın resmî kazanım kodlarını içeriyor. 9/10. sınıf
  üretiminden önce ilgili `tymm/` PDF'inden kodlar çıkarılıp bu dosyaya
  eklenmeli (uydurma yasak — KANON G6).
- **Ayet/meal referans veritabanı yok.** D11 (dinî künye) şu an LLM-hakem
  makullük denetimi + şüpheli künye işaretlemesiyle çalışıyor; kesin
  doğrulama için ileride bir meal/ayet referans DB'si eklenebilir.
- **Setler arası mükerrer-soru dedup günlüğü yok.** Bir set içindeki
  yarı-mükerrerleri çapraz-okuma yakalıyor (G15); farklı setler/testler
  arası tekrarı takip eden bir "görülen sorular" günlüğü henüz yok.
- **Olumsuz vurgu docx'te altı çizili değil, BÜYÜK HARF.** KANON K2 kanonik
  render'ın altı çizili (`<u>`/`w:u`) olmasını şart koşuyor;
  `docx_builder.py`'ye bir underline-run eklenerek ÖSYM'nin gerçek
  biçimine geçilebilir.

---

## Sorun giderme

- **Türkçe karakterler bozuk (mojibake):** kabuğun UTF-8 değil. PDF/dosya adı
  işlemlerinde `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` kullan (kod bunu zaten
  ayarlar; elle `pdftotext` çalıştırırken sen de kullan).
- **`pdftotext: command not found`:** `brew install poppler`.
- **Kaynak bulunamadı / "tymm PDF yok":** PDF adları beklenen kalıpta mı
  (`{sınıf}.Sınıf {ünite}. ÜNİTE_...` ve `dkab {sınıf}_{ünite}. ünite.pdf`)?
  `DKAB_KAYNAK_DIR` doğru mu?
- **Workflow argümanları görmezden geliniyor (hep 11.2 / 12 soru çıkıyor):**
  eski bir `built.js` olabilir; `python3 pipeline/build_workflow.py` ile yeniden
  derle. (args string/obje sorunu için script içinde guard var.)
- **Kart/ajan md'de yaptığım değişiklik hiç etki etmiyor:** `build_workflow.py`'yi
  çalıştırmayı unutmuş olabilirsin — çalışan dosya `soru-uret.built.js`'dir,
  `soru-uret.js` yalnız şablondur (bkz. [Bilgi tabanını güncelleme iş akışı](#bilgi-tabanını-güncelleme-iş-akışı)).
- **`render` "SERT HATA" ile duruyor:** `validate.py` çözüm↔cevap anahtarı
  harf uyuşmazlığı ya da band-dışı kelime sayısı bulmuş demektir; ilgili
  soruyu düzeltici turuna sokup yeniden değerlendirin ya da o siparişi
  yeniden üretin.
- **DOCX üzerine yazılamıyor ("resource busy"):** dosya Word/önizleyicide açık;
  kapat ya da farklı ada yaz.
- **Chrome bulunamadı:** yalnız infografik rasterize / HTML→PDF için gerekir;
  temel test üretimi Chrome'suz çalışır.

---

## Linux / Windows

- **Linux (Ubuntu/Debian):** `sudo apt install git python3 python3-venv poppler-utils`
  (+ opsiyonel `pandoc libreoffice`); Chrome için `google-chrome-stable`. Sonra
  README'nin 3–5. adımları aynı. `rasterize.py`/`pdf_render.py` Chrome yolunu
  `/Applications/...` altında arar; Linux'ta yol farklıysa `find_chrome()` listesine
  kendi yolunu ekle.
- **Windows:** WSL2 (Ubuntu) önerilir; yukarıdaki Linux adımlarını izle.

---

## Lisans

Kod: MIT (bkz. [`LICENSE`](LICENSE)). Kaynak materyaller (ders kitapları, ÖSYM
soruları vb.) bu depoda yer almaz ve kendi telif koşullarına tabidir.
