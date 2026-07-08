#!/usr/bin/env python3
"""
tymm kazanım + ders kitabı ünite PDF'lerini bir kez pipeline/kaynak/ altına txt çıkarır.
test-kurgu ajanı her testte pdftotext çalıştırmak yerine cache'li txt'yi okur (token+zaman tasarrufu).

Kullanım:
  python3 pipeline/kaynak_cache.py            # tüm 9/10/11 × 5 üniteyi cachele
  python3 pipeline/kaynak_cache.py 11 2       # tek ünite; cached txt yollarını yazdırır
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Kaynak materyal dizini: içinde `tymm/` ve `DERS KİTAPLARI/` alt klasörleri olmalı.
# Kendi PDF'lerini başka yere koyduysan DKAB_KAYNAK_DIR ortam değişkeniyle göster.
YDK = Path(os.environ.get("DKAB_KAYNAK_DIR")
           or ROOT / "SORU BANKASI" / "SORULAR (AÇI)" / "YENİ DERS KİTAPLARI")
TYMM_DIR = YDK / "tymm"
DERS_DIR = YDK / "DERS KİTAPLARI"
CACHE = ROOT / "pipeline" / "kaynak"

# tymm dosya adları "{sinif}.Sınıf {unite}. ÜNİTE_ ..." ile başlar (glob ile bulunur).
# ders kitabı: "dkab {sinif}_{unite}. ünite.pdf"


def tymm_pdf(sinif: int, unite: int) -> Path | None:
    hits = list(TYMM_DIR.glob(f"{sinif}.Sınıf {unite}. ÜNİTE_*.pdf"))
    return hits[0] if hits else None


def ders_pdf(sinif: int, unite: int) -> Path | None:
    p = DERS_DIR / f"dkab {sinif}_{unite}. ünite.pdf"
    return p if p.exists() else None


def pdftotext(src: Path, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_size > 0:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    env = {"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}
    r = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(src), str(dst)],
        capture_output=True, env={**os.environ, **env},
    )
    return r.returncode == 0 and dst.exists() and dst.stat().st_size > 0


def ensure_unit(sinif: int, unite: int) -> dict:
    """Tek ünitenin tymm+ders txt'sini üretir, yollarını döndürür."""
    out = {"sinif": sinif, "unite": unite, "tymm_txt": None, "ders_txt": None, "eksik": []}
    tp = tymm_pdf(sinif, unite)
    if tp:
        dst = CACHE / f"tymm_{sinif}_{unite}.txt"
        if pdftotext(tp, dst):
            out["tymm_txt"] = str(dst)
        else:
            out["eksik"].append(f"tymm pdftotext başarısız: {tp.name}")
    else:
        out["eksik"].append(f"tymm PDF yok: {sinif}.{unite}")
    dp = ders_pdf(sinif, unite)
    if dp:
        dst = CACHE / f"ders_{sinif}_{unite}.txt"
        if pdftotext(dp, dst):
            out["ders_txt"] = str(dst)
        else:
            out["eksik"].append(f"ders pdftotext başarısız: {dp.name}")
    else:
        out["eksik"].append(f"ders PDF yok: {sinif}.{unite}")
    return out


def main():
    if len(sys.argv) == 3:
        r = ensure_unit(int(sys.argv[1]), int(sys.argv[2]))
        print(f"tymm_txt: {r['tymm_txt']}")
        print(f"ders_txt: {r['ders_txt']}")
        if r["eksik"]:
            print("eksik:", r["eksik"])
        return
    ok, miss = 0, 0
    for sinif in (9, 10, 11):
        for unite in range(1, 6):
            r = ensure_unit(sinif, unite)
            got = sum(1 for k in ("tymm_txt", "ders_txt") if r[k])
            ok += got
            if r["eksik"]:
                miss += len(r["eksik"])
                for e in r["eksik"]:
                    print(f"  UYARI {sinif}.{unite}: {e}")
    print(f"\ncache: {CACHE}  ·  üretilen txt: {ok}  ·  eksik: {miss}")


if __name__ == "__main__":
    main()
