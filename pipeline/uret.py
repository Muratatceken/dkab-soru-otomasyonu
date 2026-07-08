#!/usr/bin/env python3
"""
DKAB soru üretim otomasyonunun tek-komut sürücüsü.

İki alt komut:
  args   -> kaynak cache'i garantiler, soru-uret Workflow'una verilecek args JSON'ını basar.
            (Claude bu JSON'ı Workflow({name:'soru-uret', args:<JSON>}) çağrısında kullanır.)
  render -> workflow çıktısı JSON'ından montaj + DOCX üretir (assemble.py sarmalayıcısı).

Örnek:
  python3 pipeline/uret.py args 11 2 12
  # ... Workflow çalışır, çıktı pipeline/output/DKAB11-U2-T1.json'a yazılır ...
  python3 pipeline/uret.py render pipeline/output/DKAB11-U2-T1.json "2. ÜNİTE: DİN, FELSEFE, BİLİM VE SANAT"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from kaynak_cache import ensure_unit  # noqa: E402

UNITE_BASLIK = {
    (11, 1): "1. ÜNİTE: KADER, İRADE VE SORUMLULUK",
    (11, 2): "2. ÜNİTE: DİN, FELSEFE, BİLİM VE SANAT",
    (11, 3): "3. ÜNİTE: İSLAM MEDENİYETİ VE GÖNÜL COĞRAFYAMIZ",
    (11, 4): "4. ÜNİTE: İNANÇLA İLGİLİ MESELELER",
    (11, 5): "5. ÜNİTE: YAHUDİLİK VE HRİSTİYANLIK",
}


def cmd_args(sinif: int, unite: int, soru_sayisi: int, sinav_turu: str = "TYT"):
    r = ensure_unit(sinif, unite)
    if r["eksik"]:
        print(json.dumps({"hata": r["eksik"]}, ensure_ascii=False), file=sys.stderr)
    payload = {
        "sinif": sinif,
        "unite": unite,
        "sinav_turu": sinav_turu,
        "soru_sayisi": soru_sayisi,
        "blueprint_ref": f"DKAB{sinif}-U{unite}-T1",
        # cache'li txt yolları (test-kurgu bunları doğrudan Read eder, pdftotext gerekmez)
        "tymm_yolu": r["tymm_txt"] or "",
        "ders_kitabi_yolu": r["ders_txt"] or "",
    }
    print(json.dumps(payload, ensure_ascii=False))


def cmd_render(json_path: str, baslik: str | None = None):
    from assemble import build_docx
    from validate import validate
    data = json.load(open(json_path, encoding="utf-8"))

    # V1/V2: montajdan ÖNCE deterministik doğrulama geçidi
    rap = validate(data)
    for w in rap["warn"]:
        print(f"  UYARI: {w}")
    if rap["hard"]:
        print(f"\n❌ {len(rap['hard'])} SERT HATA — bu çıktı yayına uygun DEĞİL, render durduruldu:")
        for h in rap["hard"]:
            print(f"  - {h}")
        print("Düzeltici/çapraz-okuma turunu tekrarlayın ya da soruyu yeniden üretin.")
        sys.exit(1)

    bp = data.get("blueprint", {})
    sinif, unite = bp.get("sinif"), bp.get("unite")
    if not baslik:
        baslik = UNITE_BASLIK.get((sinif, unite), f"{unite}. ÜNİTE")
    out, n = build_docx(json_path, baslik)
    print(f"✓ doğrulama temiz · yazıldı: {out}  ({n} soru)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sub = sys.argv[1]
    if sub == "args":
        sinif = int(sys.argv[2]); unite = int(sys.argv[3])
        soru = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        sinav = sys.argv[5] if len(sys.argv) > 5 else "TYT"
        cmd_args(sinif, unite, soru, sinav)
    elif sub == "render":
        jp = sys.argv[2]
        baslik = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_render(jp, baslik)
    else:
        print(f"bilinmeyen komut: {sub}\n{__doc__}")
        sys.exit(1)
