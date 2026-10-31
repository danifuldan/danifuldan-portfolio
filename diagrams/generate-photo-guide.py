#!/usr/bin/env python3
"""Generate the Photo Guide layout mock: two pages of the equipment guide
side by side, with grey blocks where the photos go. The real pages show the
employer's product, so the case study shows the format instead.

Page shapes per Daniel (2026-10-30): an item page is a centered photo, a
short phrase, and a page number; words naming other items are links to
their pages. A kit page shows the group photo with numbered call-outs and
a list of the contents, each linked. Helpers live in excalidraw_lib.py."""
import json, random, sys
from pathlib import Path

from excalidraw_lib import GREY, LINE_H, MUTED, doc, ellipse, rect, text

random.seed(20261030)
LINK = "#1971c2"   # Excalidraw's standard blue, for words that are links


def layout():
    els = []
    PW, PH, TOP = 340, 470, 20

    def page(x, number):
        els.append(rect(x, TOP, PW, PH, "#ffffff"))
        els.append(text(x + PW / 2, TOP + PH - 40, str(number), 16, "center", MUTED))
        return x + PW / 2

    # Item page: photo, phrase with one linked word, page number.
    cx = page(40, 14)
    els.append(rect(cx - 120, TOP + 50, 240, 190, GREY))
    els.append(text(cx, TOP + 50 + 95 - LINE_H * 0.4, "photo", 16, "center", MUTED))
    els.append(text(cx, TOP + 270, "Shipping box for the", 20, "center"))
    els.append(text(cx, TOP + 270 + LINE_H, "camera", 20, "center", LINK))

    # Kit page: group photo with numbered call-outs, linked contents list.
    cx = page(420, 5)
    els.append(text(cx, TOP + 36, "Contents of the kit", 20, "center"))
    gx, gy, gw, gh = cx - 140, TOP + 80, 280, 170
    els.append(rect(gx, gy, gw, gh, GREY))
    spots = [(gx + 50, gy + 40), (gx + 160, gy + 30), (gx + 200, gy + 110)]
    for i, (sx, sy) in enumerate(spots, 1):
        els.append(ellipse(sx - 14, sy - 14, 28, 28, "#ffffff"))
        els.append(text(sx, sy - LINE_H * 0.4, str(i), 16, "center"))
    items = ["camera", "mount", "power supply"]
    for i, name in enumerate(items, 1):
        y = gy + gh + 30 + (i - 1) * 34
        els.append(text(cx - 90, y, f"{i}", 20))
        els.append(text(cx - 60, y, name, 20, "left", LINK))
    return doc(els)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "photo-guide-layout.excalidraw").write_text(json.dumps(layout(), indent=1))
    print("wrote", out)
