"""
process_tests.ps1'in Python portu: pipe-delimited test dosyalarini parse eder,
kelime sayisi dogrulama raporu cikarir ve A-E cevap dagilimini dengeler
(secenekleri yeniden siralayarak, hicbir harfte yigilma olmayacak sekilde).
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field

LETTERS = ["A", "B", "C", "D", "E"]


@dataclass
class Question:
    band: str
    stem: str
    opts: dict[str, str] = field(default_factory=dict)  # {'A': ..., 'B': ...}
    ans: str = ""
    sol: str = ""


@dataclass
class Test:
    id: str
    title: str
    questions: list[Question] = field(default_factory=list)


def word_count(s: str) -> int:
    return len([w for w in re.split(r"\s+", s) if w])


def parse_file(path: str) -> list[Test]:
    """TEST|id|title / Q|band|stem / A|.. B|.. C|.. D|.. E|.. / ANS|X / SOL|.. formatini okur."""
    tests: list[Test] = []
    cur: Test | None = None
    q: Question | None = None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for ln in lines:
        if not ln:
            continue
        i = ln.find("|")
        if i < 0:
            continue
        tag, v = ln[:i], ln[i + 1:]
        if tag == "TEST":
            if q and cur:
                cur.questions.append(q)
                q = None
            test_id, title = v.split("|", 1)
            cur = Test(id=test_id, title=title)
            tests.append(cur)
        elif tag == "Q":
            if q and cur:
                cur.questions.append(q)
            band, stem = v.split("|", 1)
            q = Question(band=band, stem=stem)
        elif tag in ("A", "B", "C", "D", "E") and q:
            q.opts[tag] = v
        elif tag == "ANS" and q:
            q.ans = v.strip()
        elif tag == "SOL" and q:
            q.sol = v
    if q and cur:
        cur.questions.append(q)
    return tests


def balanced_targets(n: int, rng: random.Random | None = None) -> list[str]:
    """n soruyu A-E harflerine mumkun oldugunca esit dagitip karistirir."""
    rng = rng or random
    base, rem = divmod(n, 5)
    arr: list[str] = []
    for i, letter in enumerate(LETTERS):
        count = base + (1 if i < rem else 0)
        arr.extend([letter] * count)
    rng.shuffle(arr)
    return arr


def rebalance(test: Test, rng: random.Random | None = None) -> None:
    """Her sorunun dogru secenegini hedef harfe tasir, digerlerini rastgele
    doldurur -> cevap dagilimi A-E arasinda dengeli olur."""
    rng = rng or random
    targets = balanced_targets(len(test.questions), rng)
    for q, target in zip(test.questions, targets):
        if q.ans not in q.opts:
            continue
        correct_text = q.opts[q.ans]
        others = [q.opts[l] for l in LETTERS if l != q.ans]
        new_arr = [""] * 5
        target_ix = LETTERS.index(target)
        new_arr[target_ix] = correct_text
        m = 0
        for i in range(5):
            if i != target_ix:
                new_arr[i] = others[m]
                m += 1
        q.opts = {LETTERS[i]: new_arr[i] for i in range(5)}
        q.ans = target


def wordcount_report(tests: list[Test]) -> list[str]:
    lines = []
    for t in tests:
        wcs = [word_count(q.stem) for q in t.questions]
        long_ = sum(1 for w in wcs if w > 100)
        over = sum(1 for w in wcs if w > 150)
        under = sum(1 for w in wcs if w < 30)
        lines.append(
            f"{t.id:<8} n={len(t.questions):2d}  min={min(wcs):3d} max={max(wcs):3d}"
            f"  >100:{long_}  >150:{over}  <30:{under}"
        )
    return lines


def answer_distribution_report(tests: list[Test]) -> list[str]:
    lines = []
    for t in tests:
        d = {l: 0 for l in LETTERS}
        for q in t.questions:
            d[q.ans] += 1
        lines.append(f"{t.id:<8} " + " ".join(f"{l}:{d[l]}" for l in LETTERS))
    return lines
