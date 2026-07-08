#!/usr/bin/env python3
"""
Üretilen soru JSON'unu (soru-uret workflow çıktısı) montajlayıp DOCX üretir:
1. A-E cevap dengeleme (KANON K10 — montaj katmanında).
2. docx_builder ile Arial 10pt DOCX (KAZANIM + gövde + kök + şıklar + CEVAP + çözüm + cevap anahtarı).

Kullanım: python3 pipeline/assemble.py pipeline/output/DKAB11-U2-T1.json "2. ÜNİTE: DİN, FELSEFE, BİLİM VE SANAT"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dkab_pipeline.docx_builder import DocxBuilder

LET = ["A", "B", "C", "D", "E"]

# V1 (değerlendirmeci geri bildirimi): Cevap harfi artık blueprint'te ön-atanır ve
# üretimde sabitlenir. Montajda A-E KARIŞTIRMASI YAPILMAZ — çünkü karıştırma çözüm
# metnindeki harf atıflarını bozup çözüm↔anahtar uyuşmazlığı üretiyordu. Dize ve
# render as-is; tutarlılık validate.py ile deterministik denetlenir.


def build_docx(json_path, unite_baslik, out_path=None):
    data = json.load(open(json_path, encoding="utf-8"))
    sorular = data["sorular"]

    d = DocxBuilder()
    d.heading("DİN KÜLTÜRÜ VE AHLAK BİLGİSİ 11", "Title")
    d.heading(unite_baslik, "Subtitle")
    d.paragraph("Konu Kavrama Testi · TYT ölçme çizgisi · çok-ajanlı otomasyon çıktısı", "Note")
    d.heading("KONU KAVRAMA TESTİ", "Band")

    for i, q in enumerate(sorular, 1):
        kaz = q.get("kazanim", {})
        kazline = f"KAZANIM {kaz.get('kod', '')} · {kaz.get('serbest_konu', '')}"
        sec = [q["secenekler"][l] for l in LET]
        # kök: olumsuz vurgu kelimesini BÜYÜK yaz (docx altı-çizili run yerine geçici)
        kok = q.get("kok", "")
        v = q.get("vurgu")
        if v and v.get("sozcuk"):
            kok = kok.replace(v["sozcuk"], v["sozcuk"].upper())
        d.question_block(str(i), kazline, q["metin"], sec, q["dogru"],
                         kok_override=kok, cozum=q.get("cozum", ""))

    d.heading("CEVAP ANAHTARI", "H2a")
    d.paragraph(" · ".join(f"{i}-{q['dogru']}" for i, q in enumerate(sorular, 1)), "Item")

    out = out_path or str(Path(json_path).with_suffix(".docx"))
    d.save(out)
    return out, len(sorular)


if __name__ == "__main__":
    jp = sys.argv[1] if len(sys.argv) > 1 else "pipeline/output/DKAB11-U2-T1.json"
    baslik = sys.argv[2] if len(sys.argv) > 2 else "2. ÜNİTE"
    out, n = build_docx(jp, baslik)
    print(f"yazıldı: {out}  ({n} soru)")
