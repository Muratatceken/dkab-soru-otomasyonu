#!/usr/bin/env python3
"""
.claude/agents/*.md subagent sistem promptlarını, her rolün damıtılmış KARTIYLA
(pipeline/knowledge/cards/*.card.md) birleştirip .claude/workflows/soru-uret.js
şablonundaki `const AJAN = {/*__AJAN__*/}` placeholder'ına gömer; çalıştırılabilir
soru-uret.built.js üretir.

Token optimizasyonu: agent md'deki "## ÖNCE OKU (5 tam KB dosyası, ~45KB)" bölümü
built prompttan ÇIKARILIR ve yerine rolün lean kartı (~7KB) gömülür. Böylece ajan
runtime'da KB dosyası OKUMAZ; kurallar sistem promptunda (prompt-cache dostu) durur.

Kaynak-doğruluk: knowledge/*.md (tam) + cards/*.card.md (damıtılmış). Kural değişince
önce knowledge, sonra ilgili kart güncellenir, sonra bu script çalıştırılır.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".claude" / "agents"
CARDS = ROOT / "pipeline" / "knowledge" / "cards"
TEMPLATE = ROOT / ".claude" / "workflows" / "soru-uret.js"
OUT = ROOT / ".claude" / "workflows" / "soru-uret.built.js"

# workflow'daki AJAN anahtarı -> (md dosyası, kart dosyası)
ROL = {
    "test_kurgu": ("test-kurgu.md", "test-kurgu.card.md"),
    "soru_metni": ("soru-metni.md", "soru-metni.card.md"),
    "secenekler": ("secenekler.md", "secenekler.card.md"),
    "capraz_okuma": ("capraz-okuma.md", "capraz-okuma.card.md"),
    "duzeltici": ("duzeltici.md", "duzeltici.card.md"),
}

KART_NOTU = (
    "\n## KURALLAR\n"
    "Bu görevin tüm bağlayıcı kuralları, sistem promptunun sonundaki **KART** "
    "bölümüne gömülüdür — onu uygula. Runtime'da `pipeline/knowledge/*.md` "
    "dosyalarını OKUMA (token tasarrufu); yalnız `tr_stopwords.txt` gibi açıkça "
    "belirtilen küçük dosyaları veya kaynak metni okuyabilirsin.\n"
)


def strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n(.*)$", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def strip_once_oku(body: str) -> str:
    """'## ÖNCE OKU ...' bölümünü (bir sonraki ## başlığına kadar) KART_NOTU ile değiştirir."""
    new, n = re.subn(r"\n## ÖNCE OKU.*?(?=\n## )", KART_NOTU, body, flags=re.DOTALL)
    return new if n else body


def main():
    prompts = {}
    for rol, (md_name, card_name) in ROL.items():
        md_p = AGENTS / md_name
        card_p = CARDS / card_name
        if not md_p.exists():
            raise SystemExit(f"eksik subagent md: {md_p}")
        if not card_p.exists():
            raise SystemExit(f"eksik kart: {card_p}")
        body = strip_once_oku(strip_frontmatter(md_p.read_text(encoding="utf-8")))
        card = card_p.read_text(encoding="utf-8").strip()
        prompts[rol] = body + "\n\n=====================\n" + card + "\n"

    template = TEMPLATE.read_text(encoding="utf-8")
    placeholder = "{/*__AJAN__*/}"
    if placeholder not in template:
        raise SystemExit("şablonda {/*__AJAN__*/} placeholder bulunamadı")

    injected = template.replace(placeholder, json.dumps(prompts, ensure_ascii=False))
    OUT.write_text(injected, encoding="utf-8")
    print(f"yazıldı: {OUT}")
    for rol, p in prompts.items():
        print(f"  {rol}: {len(p)} char sistem promptu (md + kart)")
    print(f"toplam gömülü: {sum(len(v) for v in prompts.values())} char")


if __name__ == "__main__":
    main()
