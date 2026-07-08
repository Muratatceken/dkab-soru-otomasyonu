# DKAB Soru Yazdırma Otomasyonu

Din Kültürü ve Ahlak Bilgisi (DKAB) için **ÖSYM TYT/AYT üslubunda**, özgün ve
ölçme-değerlendirme kriterlerine uygun test soruları üreten **çok-ajanlı** bir
otomasyon. 9/10/11. sınıf kazanımlarına dayanır; soruları üretir, acımasızca
eleştirir (D1–D11 rubriği), düzeltir ve DOCX olarak dizer.

> Not: Bu depo **otomasyon kodunu** içerir. Telifli kaynak materyaller (ders
> kitapları, TYMM kazanım PDF'leri, ÖSYM çıkmış sorular) **depoda yoktur** —
> onları kendin sağlarsın (bkz. [Kaynak materyaller](#5-kaynak-materyalleri-sağla)).

---

## Nasıl çalışır (özet)

```
test-kurgu   → blueprint (test planı) + kaynak bağlamı
   ↓  (her soru bağımsız pipeline)
soru-metni   → gövde metni + soru kökü (iki ayrı paragraf, 30–150 kelime)
secenekler   → 5 şık (A–E) + doğru cevap + çözüm
capraz-okuma → D1–D11 acımasız denetim (puan + etiket)
duzeltici    → açık kuralları GERÇEK içerik değişikliğiyle kapat (≤3 tur)
   ↓
montaj (Python) → A–E dengeleme → DOCX/PDF
```

- **Ajanlar** Claude Code subagent'leridir (`.claude/agents/*.md`), **orchestrator**
  bir Claude Code Workflow'udur (`.claude/workflows/soru-uret.js`).
- **Bilgi tabanı** (`pipeline/knowledge/`) tüm kuralları taşır; `00_KARAR_KAYDI.md`
  bağlayıcı kanondur. Her ajana damıtılmış "kart" olarak gömülür (token tasarrufu).
- **Render backend** (`pipeline/dkab_pipeline/`) saf Python'dur; DOCX üretir.
- Mimarinin tamamı: [`CLAUDE.md`](CLAUDE.md).

---

## Kurulum — sıfırdan (hiçbir şeyi kurulu olmayan bilgisayar)

Aşağıdaki adımlar **macOS** içindir. Linux ve Windows notları en sonda.

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

Terminal'i aç ve şunu çalıştır:

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

Ajan md'lerini veya kartları her değiştirdiğinde bu komutu tekrar çalıştır.

---

## Kullanım — bir test üret

Proje dizininde Claude Code'u aç (`claude`). En kolay yol, doğal dille istemek:

> "11. sınıf 3. ünite için 12 soruluk TYT testi üret."

Claude Code, [`CLAUDE.md`](CLAUDE.md)'yi okuyup şu üç adımı yürütür. İstersen elle de yapabilirsin:

```bash
# 1) Kaynak cache'i garantile + Workflow argümanlarını al
python3 pipeline/uret.py args 11 3 12       # sinif  unite  soru_sayisi  [TYT|AYT]
```

Çıkan JSON ile orchestrator'ı çalıştır (Claude Code Workflow aracı):

```
Workflow({ name: "soru-uret", args: <yukarıdaki JSON> })
```

Orchestrator `{blueprint, sorular[], raporlar[], ozet}` döndürür; bunu
`pipeline/output/DKAB11-U3-T1.json` olarak kaydet, sonra dize:

```bash
# 2) Montaj (A–E dengeleme) + DOCX
python3 pipeline/uret.py render pipeline/output/DKAB11-U3-T1.json
```

Çıktı: `pipeline/output/DKAB11-U3-T1.docx`.

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
- **DOCX üzerine yazılamıyor ("resource busy"):** dosya Word/önizleyicide açık;
  kapat ya da farklı ada yaz.
- **Chrome bulunamadı:** yalnız infografik rasterize / HTML→PDF için gerekir;
  temel test üretimi Chrome'suz çalışır.

---

## Proje düzeni

```
.
├── CLAUDE.md                     # mimarinin tam dökümü (her Claude Code oturumu okur)
├── README.md
├── .claude/
│   ├── agents/                   # 5 subagent tanımı (test-kurgu, soru-metni, ...)
│   └── workflows/soru-uret.js    # orchestrator ŞABLONU (built.js buradan üretilir)
├── pipeline/
│   ├── knowledge/                # BİLGİ TABANI — 00_KARAR_KAYDI.md (kanon) + kurallar
│   │   └── cards/                # ajanlara gömülen damıtılmış kartlar
│   ├── schemas/                  # ajanlar arası JSON veri sözleşmesi
│   ├── dkab_pipeline/            # Python render backend (docx/pdf/figür)
│   ├── build_workflow.py         # ajan md + kart → soru-uret.built.js
│   ├── kaynak_cache.py           # kaynak PDF → txt cache
│   ├── uret.py                   # tek-komut sürücü (args / render)
│   ├── assemble.py               # JSON → A–E dengeleme → DOCX
│   └── requirements.txt
└── (SORU BANKASI/ — telifli kaynak; .gitignore'da, depoda yok)
```

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
