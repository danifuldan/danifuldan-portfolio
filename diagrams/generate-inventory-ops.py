#!/usr/bin/env python3
"""Generate two .excalidraw files for the Inventory Ops case study.

Element shapes and style values are copied from Daniel's existing
'order form workflows.excalidraw' (inspected 2026-10-27): fontFamily 5,
fontSize 20, roughness 1, strokeWidth 2, roundness type 3 on rectangles,
type 2 on arrows, pastel solid fills, unbound arrows.
"""
import json, random, sys, time
from pathlib import Path

random.seed(20261027)
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
    return base("text", x, y, w, h, text=s, originalText=s, fontSize=size,
                fontFamily=5, textAlign=align, verticalAlign="top", containerId=None,
                autoResize=True, lineHeight=1.25, strokeColor=color)


def rect(x, y, w, h, fill="transparent", stroke="solid"):
    return base("rectangle", x, y, w, h, backgroundColor=fill, strokeStyle=stroke,
                roundness={"type": 3}, boundElements=[])


def arrow(x1, y1, x2, y2, head="arrow", stroke="solid"):
    return base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1),
                points=[[0, 0], [x2 - x1, y2 - y1]], startBinding=None, endBinding=None,
                startArrowhead=None, endArrowhead=head, elbowed=False,
                roundness={"type": 2}, strokeStyle=stroke)


def labeled_box(cx, cy, w, h, title, sub=None, fill="transparent", stroke="solid"):
    """Box centered at (cx, cy) with a bold-ish title and optional smaller subtitle."""
    els = [rect(cx - w / 2, cy - h / 2, w, h, fill, stroke)]
    if sub:
        sub_lines = sub.count("\n") + 1
        total = LINE_H + 8 + sub_lines * LINE_H * 0.8
        ty = cy - total / 2
        els.append(text(cx, ty, title, 20, "center"))
        els.append(text(cx, ty + LINE_H + 8, sub, 16, "center", "#5c5c5c"))
    else:
        els.append(text(cx, cy - LINE_H / 2, title, 20, "center"))
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

# ---------------------------------------------------------------- Diagram 1
# The pipeline a SKU moves through. Labels under each stage are the operator's
# job there, taken from the per-SKU checklist in the brain dump.
def pipeline():
    els = []
    stages = [
        ("Plan", "decide quantity and\nthe vendor's item", YELLOW),
        ("Order", "place it; record\nreference and ETA", BLUE),
        ("Inbound", "add tracking; tell\nthe warehouse", BLUE),
        ("Receive", "verify received\nvs. shipped", GREEN),
        ("Monitor", "no open tasks;\nwatch demand", GREY),
    ]
    W, H, GAP = 190, 120, 60
    y = 200
    x0 = 100
    centers = []
    for i, (t, sub, fill) in enumerate(stages):
        cx = x0 + W / 2 + i * (W + GAP)
        centers.append(cx)
        els += labeled_box(cx, y, W, H, t, sub, fill)
        if i > 0:
            els.append(arrow(cx - W / 2 - GAP + 6, y, cx - W / 2 - 6, y))

    # Monitor loops back to Plan when stock drops below the reorder point.
    top = y - H / 2
    loop_y = top - 70
    els.append(arrow(centers[-1], top - 4, centers[-1], loop_y))          # up
    els.append(arrow(centers[-1], loop_y, centers[0], loop_y, head=None))  # across
    els.append(arrow(centers[0], loop_y, centers[0], top - 4))            # down
    els.append(text((centers[0] + centers[-1]) / 2, loop_y - 34,
                    "stock falls below the reorder point → back to Plan", 16, "center", "#5c5c5c"))

    # At Risk: a side state off Monitor, dotted like the reference's limbo box.
    ar_cy = y + H / 2 + 110
    els += labeled_box(centers[-1], ar_cy, W, 90, "At risk", "more stock than\ndemand supports", PINK, "dotted")
    els.append(arrow(centers[-1], y + H / 2 + 4, centers[-1], ar_cy - 45 - 4))

    # Caption.
    els.append(text(x0, ar_cy + 90, "Each SKU being monitored sits in exactly one stage. The tool lists what is\n"
                    "waiting on you at every stage; the dashboard is the union of those lists.",
                    16, "left", "#5c5c5c"))
    return doc(els)


# ---------------------------------------------------------------- Diagram 2
# Where data comes from and where it goes.
def dataflow():
    els = []
    # Column x-centers
    cx_in, cx_mid, cx_pages, cx_out = 180, 520, 880, 1240
    W, H = 220, 80

    # Inputs (left)
    els.append(text(cx_in, 60, "Inputs", 20, "center"))
    inputs = ["inventory report", "orders report", "receiving report"]
    in_ys = [160, 280, 400]
    for s, yy in zip(inputs, in_ys):
        els += labeled_box(cx_in, yy, W, H, s, None, YELLOW)
    els.append(text(cx_in, 460, "downloaded from the\nwarehouse management system", 16, "center", "#5c5c5c"))

    # Middle: import -> database
    els += labeled_box(cx_mid, 160, W, H, "Import page", "auto-import unless\nsomething is wrong", BLUE)
    els += labeled_box(cx_mid, 400, W, H + 20, "Local database", "SQLite, on this\nmachine only", GREY)
    for yy in in_ys:  # every report feeds the one import page
        els.append(arrow(cx_in + W / 2 + 6, yy, cx_mid - W / 2 - 6, 160))
    els.append(arrow(cx_mid, 160 + H / 2 + 4, cx_mid, 400 - (H + 20) / 2 - 4))

    # Pages (working surfaces) — right of database, inside a dashed container so
    # the output arrows have a visible origin: the group of pages, not one page.
    pages = [
        ("Inventory", "SKUs by stage;\ndetail and action panes"),
        ("SKU management", "monitored? needs PO?\nnotes"),
        ("SKU logic", "equivalents and kits"),
        ("Vendors", "contacts, part numbers,\nship-to"),
    ]
    p_ys = [180, 295, 410, 525]
    pad = 22
    c_left, c_right = cx_pages - W / 2 - pad, cx_pages + W / 2 + pad
    c_top, c_bottom = 85, p_ys[-1] + 45 + pad
    els.append(rect(c_left, c_top, c_right - c_left, c_bottom - c_top, "transparent", "dashed"))
    els.append(text(cx_pages, c_top + 10, "Working pages", 20, "center"))
    for (t, sub), yy in zip(pages, p_ys):
        els += labeled_box(cx_pages, yy, W, 90, t, sub, GREEN)
    # database -> pages
    for yy in p_ys:
        els.append(arrow(cx_mid + W / 2 + 6, 400, c_left - 6, yy))

    # Outputs (far right), fed from the pages container.
    c_mid_y = (c_top + c_bottom) / 2
    els.append(text(cx_out, 60, "Outputs", 20, "center"))
    outs = [
        ("Dashboard", "what's waiting on you"),
        ("Stock-level email", "high-value components:\non hand, on order, notes"),
        ("Forecasting", "planned vs. actual\npurchasing, sales forecast"),
    ]
    o_ys = [c_mid_y - 150, c_mid_y, c_mid_y + 150]
    for (t, sub), yy in zip(outs, o_ys):
        els += labeled_box(cx_out, yy, W, 90, t, sub, PINK)
    for yy in o_ys:
        els.append(arrow(c_right + 6, c_mid_y, cx_out - W / 2 - 6, yy))

    # Outer boundary: everything is on one machine.
    bottom = c_bottom + 50
    els.append(rect(40, 20, cx_out + W / 2 + 40 - 40, bottom - 20, "transparent", "dashed"))
    els.append(text(60, bottom - 32, "everything inside the dashed line runs on one machine; nothing is exposed to the internet",
                    16, "left", "#5c5c5c"))
    return doc(els)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventory-ops-pipeline.excalidraw").write_text(json.dumps(pipeline(), indent=1))
    (out / "inventory-ops-dataflow.excalidraw").write_text(json.dumps(dataflow(), indent=1))
    print("wrote", out)
