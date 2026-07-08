"""HTML -> PDF: `chrome --headless --print-to-pdf` sarmalayicisi (MASTER_PROMPT #7)."""
from __future__ import annotations

import subprocess
from pathlib import Path

from .rasterize import find_chrome


def html_to_pdf(html_path: Path, pdf_path: Path, *, chrome_path: str | None = None) -> None:
    chrome = chrome_path or find_chrome()
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            f"file://{html_path.resolve()}",
        ],
        check=True,
        capture_output=True,
    )
    if not pdf_path.exists():
        raise RuntimeError(f"PDF uretilemedi: {pdf_path}")
