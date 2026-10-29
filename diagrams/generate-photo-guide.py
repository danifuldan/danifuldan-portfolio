#!/usr/bin/env python3
"""Generate the Photo Guide layout mock: the shape of one page of the
equipment guide, with grey blocks where the photos go. The real pages show
the employer's product, so the case study shows the format instead
(Daniel's call, 2026-10-28). Helpers and style notes live in excalidraw_lib.py."""
import json, random, sys
from pathlib import Path

from excalidraw_lib import GREY, LINE_H, MUTED, arrow, doc, labeled_box, rect, text

random.seed(20261028)


def layout():
    els = []
    L, R, T = 80, 720, 50               # page margins
    els.append(rect(40, 20, 720, 960, "#ffffff"))

    # Header: item name, page number, rule.
    els.append(text(L, T, "Item name", 20))
    els.append(text(R, T + 2, "p. 42", 16, "right", MUTED))
    els.append(arrow(L, T + 42, R, T + 42, head=None))

    # Photos: one main shot, two angles.
    def block(x, y, w, h, label):
        els.append(rect(x, y, w, h, GREY))
        els.append(text(x + w / 2, y + h / 2 - LINE_H * 0.8 / 2, label, 16, "center", MUTED))
    block(L, 130, 400, 300, "photo")
    block(510, 130, 210, 140, "side")
    block(510, 290, 210, 140, "ports")

    # Description: plain terms, then what it does and where it goes.
    els.append(text(L, 470, "What it is, in plain terms.", 20))
    els.append(text(L, 505, "What it does, where it goes,\nand what it plugs into.", 16, "left", MUTED))

    # Relationships: each row links to another page of the guide.
    els.append(text(L, 600, "Related", 20))
    rows = [("works with", "item · p. 17"), ("ships with", "item · p. 23"), ("part of kit", "kit · p. 5")]
    for i, (label, link) in enumerate(rows):
        y = 660 + i * 70
        els.append(text(L, y + 2, label, 16, "left", MUTED))
        els += labeled_box(390, y + 12, 260, 44, link)
    return doc(els)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "photo-guide-layout.excalidraw").write_text(json.dumps(layout(), indent=1))
    print("wrote", out)
