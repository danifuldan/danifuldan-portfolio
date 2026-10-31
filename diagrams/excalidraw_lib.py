"""Shared helpers for generating .excalidraw files.

Element shapes and style values are copied from Daniel's existing
'order form workflows.excalidraw' (inspected 2026-10-27): fontFamily 5,
fontSize 20, roughness 1, strokeWidth 2, roundness type 3 on rectangles,
type 2 on arrows, pastel solid fills, unbound arrows.

Keep canvases roughly 700-800 units wide: the case-study column is ~720 CSS px
and the order-form diagrams were drawn ~685 wide, so that width keeps label
sizes on the page consistent with them.
"""
import json, random, sys, time
from pathlib import Path

NOW = int(time.time() * 1000)
_ids = 0


def nid():
    global _ids
    _ids += 1
    return f"inv{_ids:03d}"


def base(kind, x, y, w, h, **kw):
    e = {
        "id": nid(), "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "index": None, "roundness": None, "seed": random.randint(1, 2**31),
        "version": 1, "versionNonce": random.randint(1, 2**31), "isDeleted": False,
        "boundElements": None, "updated": NOW, "link": None, "locked": False,
    }
    e.update(kw)
    return e


# Approximate glyph widths for the hand-drawn font at size 20 so text can be
# centered. Excalidraw re-measures on load (autoResize), so this only needs to
# be close.
CHAR_W = 10.4
LINE_H = 25


def text(x, y, s, size=20, align="left", color="#1e1e1e"):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * CHAR_W * (size / 20)
    h = LINE_H * (size / 20) * len(lines)
    if align == "center":
        x = x - w / 2
    elif align == "right":
        x = x - w
    return base("text", x, y, w, h, text=s, originalText=s, fontSize=size,
                fontFamily=5, textAlign=align, verticalAlign="top", containerId=None,
                autoResize=True, lineHeight=1.25, strokeColor=color)


def rect(x, y, w, h, fill="transparent", stroke="solid"):
    return base("rectangle", x, y, w, h, backgroundColor=fill, strokeStyle=stroke,
                roundness={"type": 3}, boundElements=[])


def ellipse(x, y, w, h, fill="transparent"):
    return base("ellipse", x, y, w, h, backgroundColor=fill, boundElements=[])


def arrow(x1, y1, x2, y2, head="arrow", stroke="solid"):
    return base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1),
                points=[[0, 0], [x2 - x1, y2 - y1]], startBinding=None, endBinding=None,
                startArrowhead=None, endArrowhead=head, elbowed=False,
                roundness={"type": 2}, strokeStyle=stroke)


def labeled_box(cx, cy, w, h, title, sub=None, fill="transparent", stroke="solid"):
    """Box centered at (cx, cy) with a title and optional smaller subtitle."""
    els = [rect(cx - w / 2, cy - h / 2, w, h, fill, stroke)]
    if sub:
        sub_lines = sub.count("\n") + 1
        total = LINE_H + 8 + sub_lines * LINE_H * 0.8
        ty = cy - total / 2
        els.append(text(cx, ty, title, 20, "center"))
        els.append(text(cx, ty + LINE_H + 8, sub, 16, "center", "#5c5c5c"))
    else:
        n = title.count("\n") + 1
        els.append(text(cx, cy - n * LINE_H / 2, title, 20, "center"))
    return els


def doc(elements):
    for i, e in enumerate(elements):
        e["index"] = "a" + format(i, "03d")
    return {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": 20, "gridStep": 5, "gridModeEnabled": False,
                     "viewBackgroundColor": "#ffffff", "lockedMultiSelections": {}},
        "files": {},
    }


# Pastels from the reference file plus Excalidraw's standard palette.
PINK, GREEN, BLUE, YELLOW, GREY = "#ffc9c9", "#b2f2bb", "#a5d8ff", "#ffec99", "#e9ecef"
MUTED = "#5c5c5c"
