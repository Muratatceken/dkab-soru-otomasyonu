#!/usr/bin/env python3
"""
Montaj sonrası deterministik DOĞRULAMA GEÇİDİ (değerlendirmeci geri bildirimi V1/V2).

En yıkıcı hata sınıfı çözüm↔anahtar harf uyuşmazlığıydı (LLM harf muhasebesinde
güvenilmez). Bu geçit harf tutarlılığını, band ve kazanım dengesini KOD ile denetler.
Sert (hard) hata varsa çıktı yayına uygun DEĞİLDİR.

Kullanım:
  python3 pipeline/validate.py pipeline/output/DKAB11-U3-T1.json
Dönüş kodu: 0 = temiz, 1 = sert hata var.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter

LET = ["A", "B", "C", "D", "E"]
BAND = {"30-70": (30, 70), "70-100": (70, 100), "100-150": (100, 150)}

# çözümde "doğru cevap X" geçen TÜM harfler (İ/ı dahil case-insensitive)
_RE_DOGRU_CEVAP = re.compile(r"do[ğg]ru\s+cevap[^A-Ea-e]{0,4}([A-E])", re.IGNORECASE)
_RE_PREFIX = re.compile(r"^\s*do[ğg]ru\s+cevap\s+([A-E])", re.IGNORECASE)


def validate(data: dict) -> dict:
    sorular = data.get("sorular", [])
    hard, warn = [], []

    for q in sorular:
        sid = q.get("id", "?")
        dogru = q.get("dogru")
        sec = q.get("secenekler") or {}
        cozum = q.get("cozum") or ""

        # 1) doğru harf + tüm şıklar mevcut
        if dogru not in LET:
            hard.append(f"{sid}: 'dogru' geçersiz ({dogru!r})")
            continue
        if not all(l in sec and str(sec[l]).strip() for l in LET):
            hard.append(f"{sid}: A-E şıklarından biri eksik/boş")

        # 2) çözüm baş-harfi (V2): "Doğru cevap X:" ile başlamalı ve X==dogru
        mp = _RE_PREFIX.match(cozum)
        if not mp:
            warn.append(f"{sid}: çözüm 'Doğru cevap {dogru}:' ile başlamıyor (biçim kuralı V2)")
        elif mp.group(1).upper() != dogru:
            hard.append(f"{sid}: çözüm baş-harfi {mp.group(1).upper()} ≠ dogru {dogru} (V2 UYUŞMAZLIK)")

        # 3) çözümde geçen TÜM "doğru cevap X" ifadeleri dogru ile aynı olmalı
        for m in _RE_DOGRU_CEVAP.finditer(cozum):
            if m.group(1).upper() != dogru:
                hard.append(f"{sid}: çözümde 'doğru cevap {m.group(1).upper()}' geçiyor ama dogru {dogru} (harf kayması)")
                break

        # 4) hedef_dogru_harf ön-atandıysa dogru ona eşit olmalı (V1)
        hedef = q.get("hedef_dogru_harf")
        if hedef in LET and dogru != hedef:
            warn.append(f"{sid}: dogru {dogru} ≠ hedef_dogru_harf {hedef} (A-E dengesi kayabilir)")

        # 5) band ↔ kelime_sayisi tutarlılığı
        band, ks = q.get("band"), q.get("kelime_sayisi")
        if band in BAND and isinstance(ks, int):
            lo, hi = BAND[band]
            if not (lo <= ks <= hi):
                hard.append(f"{sid}: kelime_sayisi {ks} band {band} dışında ({lo}-{hi})")

    # 6) set-düzeyi: A-E cevap dağılımı
    dist = Counter(q.get("dogru") for q in sorular if q.get("dogru") in LET)
    n = sum(dist.values())
    if n:
        for l in LET:
            oran = dist.get(l, 0) / n
            if oran > 0.28:
                warn.append(f"cevap dağılımı dengesiz: {l} = %{round(oran*100)} (>%28)")

    # 7) set-düzeyi: kazanım dengesi (V8) — her kazanım ort ±1
    kaz = Counter((q.get("kazanim") or {}).get("kod") for q in sorular)
    if kaz:
        vals = list(kaz.values())
        if max(vals) - min(vals) > 2:
            warn.append(f"kazanım dengesizliği (V8): {dict(kaz)} (fark >2)")

    return {"hard": hard, "warn": warn, "soru": len(sorular),
            "cevap_dagilimi": dict(dist), "kazanim_dagilimi": dict(kaz)}


def main():
    if len(sys.argv) < 2:
        print("kullanım: python3 pipeline/validate.py <soru.json>")
        sys.exit(2)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    r = validate(data)
    print(f"Doğrulama: {r['soru']} soru · cevap dağılımı {r['cevap_dagilimi']} · kazanım {r['kazanim_dagilimi']}")
    for w in r["warn"]:
        print(f"  UYARI: {w}")
    if r["hard"]:
        print(f"\n❌ {len(r['hard'])} SERT HATA (yayın engeli):")
        for h in r["hard"]:
            print(f"  - {h}")
        sys.exit(1)
    print("✓ Sert hata yok.")
    sys.exit(0)


if __name__ == "__main__":
    main()
