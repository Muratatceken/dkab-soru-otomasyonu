"""
rasterize_figs.ps1 / raster_u2..u5_figs.ps1'in Python portu.

Zengin HTML kaynaklarindaki (`dkab11_uX_sb_rich.html`) <figure class="fig">
bloklarini (SVG infografikler) ayiklar, her birini bagimsiz bir HTML sayfasina
sarar, Chrome headless ile 2x cozunurlukte PNG'ye "screenshot" alir ve alttaki
beyaz bosluğu kirpar (orijinal PowerShell'deki LockBits taramasinin Pillow
karsiligi).
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image

FIGURE_RE = re.compile(r"<figure class=\"fig\">.*?</figure>", re.DOTALL)
STYLE_RE = re.compile(r"<style>.*?</style>", re.DOTALL)
VIEWBOX_RE = re.compile(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"')

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    raise FileNotFoundError(
        "Google Chrome bulunamadi. /Applications altinda kurulu oldugunu dogrulayin."
    )


def extract_css(html_source: str) -> str:
    m = STYLE_RE.search(html_source)
    return m.group(0) if m else ""


def extract_figures(html_source: str, caption_pattern: str) -> dict[str, str]:
    """caption_pattern ornek: r'Görsel (2\\.\\d)' -> {'2.1': '<figure ...>...</figure>', ...}"""
    caption_re = re.compile(caption_pattern)
    figures: dict[str, str] = {}
    for m in FIGURE_RE.finditer(html_source):
        block = m.group(0)
        cap = caption_re.search(block)
        if not cap:
            continue
        key = cap.group(1)
        figures[key] = block
    return figures


def viewbox_of(fig_html: str) -> tuple[float, float] | None:
    m = VIEWBOX_RE.search(fig_html)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def render_figure(
    css: str,
    fig_html: str,
    out_png: Path,
    *,
    render_width: float = 880.0,
    extra_height: int = 260,
    scale: int = 2,
    chrome_path: str | None = None,
    workdir: Path | None = None,
) -> None:
    """Bir <figure> bloğunu bağımsız HTML sayfasına sarar, Chrome headless ile
    PNG screenshot alır, ardından alttaki beyaz boşluğu kırpar."""
    chrome = chrome_path or find_chrome()
    vb = viewbox_of(fig_html)
    if vb:
        vw, vh = vb
        svg_h = render_width * (vh / vw)
    else:
        svg_h = render_width
    win_h = int(svg_h) + extra_height + 1

    html = (
        '<!doctype html><html><head><meta charset="utf-8">' + css + "</head>"
        '<body style="background:#ffffff;margin:0">'
        '<div class="book" style="background:#ffffff;padding:8px">'
        f'<div style="max-width:{int(render_width)}px">{fig_html}</div>'
        "</div></body></html>"
    )

    tmp_dir = workdir or out_png.parent
    tmp_html = tmp_dir / f"_render_{out_png.stem}.html"
    tmp_html.write_text(html, encoding="utf-8")

    if out_png.exists():
        out_png.unlink()

    win_w = int(render_width) + 24
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--force-device-scale-factor={scale}",
            f"--window-size={win_w},{win_h}",
            f"--screenshot={out_png}",
            f"file://{tmp_html.resolve()}",
        ],
        check=True,
        capture_output=True,
    )
    tmp_html.unlink(missing_ok=True)

    if not out_png.exists():
        raise RuntimeError(f"Chrome screenshot uretemedi: {out_png}")

    crop_bottom_whitespace(out_png)


def crop_bottom_whitespace(png_path: Path, *, threshold: int = 248, sample_stride: int = 3, pad: int = 24) -> None:
    """PowerShell'deki LockBits taramasinin karsiligi: en alttan yukari dogru
    beyaz-olmayan ilk satiri bulup altina `pad` piksel boşluk birakarak kırpar."""
    img = Image.open(png_path).convert("RGB")
    w, h = img.size
    px = img.load()
    last = h - 1
    for y in range(h - 1, -1, -1):
        nonwhite = False
        for x in range(0, w, sample_stride):
            r, g, b = px[x, y]
            if r < threshold or g < threshold or b < threshold:
                nonwhite = True
                break
        if nonwhite:
            last = y
            break
    new_h = min(h, last + pad)
    if new_h < h:
        img.crop((0, 0, w, new_h)).save(png_path)


def render_all_figures(
    rich_html_path: Path,
    caption_pattern: str,
    out_dir: Path,
    key_to_filename,
    **render_kwargs,
) -> list[str]:
    """Bir uniteye ait butun figurleri bulup PNG'ye cevirir.
    key_to_filename: '2.1' -> 'fig_2_1.png' gibi bir donusum fonksiyonu."""
    src = rich_html_path.read_text(encoding="utf-8")
    css = extract_css(src)
    figures = extract_figures(src, caption_pattern)
    done = []
    for key in sorted(figures):
        out_png = out_dir / key_to_filename(key)
        render_figure(css, figures[key], out_png, workdir=out_dir, **render_kwargs)
        done.append(key)
    return done
