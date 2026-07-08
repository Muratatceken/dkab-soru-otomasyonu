# DKAB Soru Yazdırma Otomasyonu — Mac Ortamı

İki katman var:
1. **Çok-ajanlı soru üretimi** (asıl otomasyon): `knowledge/` bilgi tabanı +
   `schemas/` veri sözleşmesi + `.claude/agents/` 5 subagent + `.claude/workflows/`
   orchestrator. Blueprint → soru metni+kök → şıklar → acımasız çapraz-okuma →
   düzeltici döngüsü. Bkz. aşağıda "Soru üretimi".
2. **Render backend** (`dkab_pipeline/`): üretilen JSON'ı DOCX/PDF'e çeviren,
   figürleri rasterize eden, A-E cevap dengeleyen mekanik katman — eski Windows
   PowerShell pipeline'ının (`_PIPELINE_DKAB11/`) Python portu.

## Soru üretimi (çok-ajanlı)

**Bilgi tabanı ve kanon:** `knowledge/00_KARAR_KAYDI.md` bağlayıcı kanondur; diğer
`knowledge/*.md` dosyaları ÖSYM TYT/AYT stilini, D1-D11 rubriğini, kalıp havuzunu,
kelime bandını, dinî dili ve DAB/Bloom'u içerir. Ajanlar arası veri sözleşmesi
`schemas/{blueprint,soru,rapor}.schema.json`.

**Ajanlar** `.claude/agents/*.md`: test-kurgu, soru-metni, secenekler,
capraz-okuma, duzeltici. **Orchestrator** `.claude/workflows/soru-uret.js`.

**Çalıştırma (build + workflow):**
```bash
# 1) Ajan md'lerini workflow'a göm (bu ortamda custom agentType tanınmadığı için,
#    md içerikleri general-purpose ajana sistem promptu olarak enjekte edilir).
#    Ajan md'lerini VEYA workflow şablonunu her düzenleyişinde tekrar çalıştır:
python3 pipeline/build_workflow.py    # -> .claude/workflows/soru-uret.built.js

# 2) Workflow'u çalıştır (Claude Code Workflow tool ile):
#    Workflow({ scriptPath: ".../soru-uret.built.js", args: {
#      sinif, unite, sinav_turu, soru_sayisi, tymm_yolu, ders_kitabi_yolu, blueprint_ref } })
```
Çıktı: `{blueprint, sorular[], raporlar[]}`. Sorular JSON `output/` altına yazılır,
sonra render backend ile DOCX/PDF üretilir.

> Not: `_PIPELINE_DKAB11/MASTER_PROMPT_DKAB11.md` eski (tek-akış) yaklaşımın
> referansıdır; yeni çok-ajanlı sistem onun yerine geçer.

## Kurulum

```bash
python3 -m venv pipeline/venv
source pipeline/venv/bin/activate
pip install -r pipeline/requirements.txt
```

Ayrıca sistemde şunlar kurulu olmalı (hepsi bu Mac'te zaten mevcut):
- Homebrew: `pandoc`, `libreoffice` (→ `soffice` komutu, DOCX/PDF dönüşümü ve
  doğrulama için), `poppler` (→ `pdftotext`, `pdftoppm`, ders kitabı PDF'lerini
  okumak için)
- Google Chrome (`/Applications/Google Chrome.app`) — headless screenshot ve
  `--print-to-pdf` için

## Modüller (`dkab_pipeline/`)

- **`docx_builder.py`** — `build_sb_docx2.ps1` / `build_uX_docx.ps1` portu.
  python-docx kullanmadan OOXML XML'ini elle üretip zip olarak paketler.
  Orijinal Word stilleriyle (Arial 10pt, Band/H1a/H2a/Kbox/Cevap/Cozum...)
  birebir aynı görünümü verir. `DocxBuilder().question_block(...)` ile
  KAZANIM satırı + paragraf/kök ayrımı + şıklar + cevap otomatik yazılır.
- **`rasterize.py`** — `rasterize_figs.ps1` / `raster_uX_figs.ps1` portu.
  Zengin HTML'deki `<figure class="fig">` SVG bloklarını ayıklar, Chrome
  headless ile 2x PNG'ye çevirir, alttaki beyaz boşluğu kırpar (Pillow ile,
  orijinal `LockBits` taramasının karşılığı).
- **`tests_processor.py`** — `process_tests.ps1` portu. Pipe-delimited test
  dosyalarını (`TEST|.. Q|.. A|.. ANS|..`) parse eder, kelime sayısı raporu
  çıkarır, A-E cevap dağılımını dengeler (şıkları karıştırıp yeniden yazar).
- **`pdf_render.py`** — `chrome --headless --print-to-pdf` sarmalayıcısı.

## Doğrulama (bu ortamda yapıldı)

- `docx_builder`: üretilen `.docx`, LibreOffice (`soffice --headless
  --convert-to pdf`) ile açılıp PDF'e çevrildi; Türkçe karakterler, stiller,
  tablo ve soru/kök ayrımı `pdftotext` ile doğrulandı.
- `rasterize`: `dkab11_u2_sb_rich.html` içinden gerçek bir figür (Görsel 2.1)
  render edildi; çıktı boyutu (1808×939 px) orijinal Windows çıktısıyla
  **birebir aynı** çıktı.
- `tests_processor`: sentetik 10 soruluk test, A-E'ye 2-2-2-2-2 dengeli
  dağıtıldı.

## Sıradaki adım

Bir sonraki ünitenin (örn. Ünite 2'nin devamı ya da yeni bir ders/sınıf)
içerik üretimi için `_PIPELINE_DKAB11` klasöründeki JSON/HTML kaynaklarını bu
modüllerle birleştiren küçük bir çalıştırma scripti (`build_unit.py` gibi)
yazılabilir — mevcut ünite 1-5 verileri örnek şablon olarak kullanılabilir.
