#!/usr/bin/env python3
"""Generate two .excalidraw files for the Inventory Ops case study.

Element shapes and style values are copied from Daniel's existing
'order form workflows.excalidraw' (inspected 2026-10-27): fontFamily 5,
fontSize 20, roughness 1, strokeWidth 2, roundness type 3 on rectangles,
type 2 on arrows, pastel solid fills, unbound arrows.

Layouts are vertical and about 800 canvas units wide. The case-study column
on the site is ~720 CSS px and the order-form diagrams were drawn ~685 units
wide, so this width keeps label sizes on the page consistent with those.
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
    elif align == "right":
        x = x - w
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
    """Box centered at (cx, cy) with a title and optional smaller subtitle."""
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
MUTED = "#5c5c5c"


# ---------------------------------------------------------------- Diagram 1
# The pipeline a SKU moves through, stacked top to bottom. Labels under each
# stage are the operator's job there, from the per-SKU checklist.
def pipeline():
    els = []
    stages = [
        ("Plan", "decide quantity and\nthe vendor's item", YELLOW),
        ("Order", "place it; record\nreference and ETA", BLUE),
        ("Inbound", "add tracking; tell\nthe warehouse", BLUE),
        ("Receive", "verify received\nvs. shipped", GREEN),
        ("Monitor", "no open tasks;\nwatch demand", GREY),
    ]
    W, H, GAP = 300, 100, 46
    cx, y0 = 360, 40
    cys = []
    for i, (t, sub, fill) in enumerate(stages):
        cy = y0 + H / 2 + i * (H + GAP)
        cys.append(cy)
        els += labeled_box(cx, cy, W, H, t, sub, fill)
        if i > 0:
            els.append(arrow(cx, cy - H / 2 - GAP + 6, cx, cy - H / 2 - 6))

    # Monitor loops back to Plan when stock drops below the reorder point:
    # out of Monitor's left side, up the left margin, into Plan's left side.
    lx = cx - W / 2 - 60
    els.append(arrow(cx - W / 2 - 4, cys[-1], lx, cys[-1], head=None))
    els.append(arrow(lx, cys[-1], lx, cys[0], head=None))
    els.append(arrow(lx, cys[0], cx - W / 2 - 4, cys[0]))
    els.append(text(lx - 12, (cys[0] + cys[-1]) / 2 - 40,
                    "stock falls\nbelow the\nreorder point:\nback to Plan", 16, "right", MUTED))

    # At Risk: a side state off Monitor, dotted like the reference's limbo box.
    arx = cx + W / 2 + 60 + 110
    els += labeled_box(arx, cys[-1], 220, 90, "At risk", "more stock than\ndemand supports", PINK, "dotted")
    els.append(arrow(cx + W / 2 + 4, cys[-1], arx - 110 - 6, cys[-1]))

    # Caption.
    bottom = cys[-1] + H / 2 + 40
    els.append(text(lx - 150, bottom,
                    "Each monitored SKU sits in exactly one stage. The tool lists what is\n"
                    "waiting on you at each stage; the dashboard is the union of those lists.",
                    16, "left", MUTED))
    return doc(els)


# ---------------------------------------------------------------- Diagram 2
# Where data comes from and where it goes, top to bottom.
def dataflow():
    els = []
    cx = 400

    # Inputs: three reports side by side across the top.
    W_in, H_in = 220, 70
    in_xs = [cx - 250, cx, cx + 250]
    in_y = 120
    els.append(text(cx, 40, "Inputs", 20, "center"))
    for s, x in zip(["inventory report", "orders report", "receiving report"], in_xs):
        els += labeled_box(x, in_y, W_in, H_in, s, None, YELLOW)
    els.append(text(cx, in_y + H_in / 2 + 8, "downloaded from the warehouse management system", 16, "center", MUTED))

    # Import page -> local database.
    imp_y, db_y = 270, 420
    els += labeled_box(cx, imp_y, 280, 80, "Import page", "auto-import unless\nsomething is wrong", BLUE)
    for x in in_xs:
        els.append(arrow(x, in_y + H_in / 2 + 30, cx + (x - cx) * 0.4, imp_y - 40 - 6))
    els += labeled_box(cx, db_y, 280, 90, "Local database", "SQLite, on this\nmachine only", GREY)
    els.append(arrow(cx, imp_y + 40 + 6, cx, db_y - 45 - 6))

    # Working pages: a 2x2 grid inside a dashed container.
    pages = [
        ("Inventory", "SKUs by stage;\ndetail and action panes"),
        ("SKU management", "monitored? needs PO?\nnotes"),
        ("SKU logic", "equivalents and kits"),
        ("Vendors", "contacts, part numbers,\nship-to"),
    ]
    PW, PH = 310, 90
    c_top = db_y + 45 + 60
    grid = [(cx - 170, c_top + 90), (cx + 170, c_top + 90), (cx - 170, c_top + 200), (cx + 170, c_top + 200)]
    c_left, c_right = cx - 170 - PW / 2 - 20, cx + 170 + PW / 2 + 20
    c_bottom = c_top + 200 + PH / 2 + 20
    els.append(rect(c_left, c_top, c_right - c_left, c_bottom - c_top, "transparent", "dashed"))
    els.append(text(cx, c_top + 8, "Working pages", 20, "center"))
    for (t, sub), (x, y) in zip(pages, grid):
        els += labeled_box(x, y, PW, PH, t, sub, GREEN)
    els.append(arrow(cx, db_y + 45 + 6, cx, c_top - 6))

    # Outputs: three side by side along the bottom, fed from the pages group.
    outs = [
        ("Dashboard", "what's waiting\non you"),
        ("Stock-level email", "high-value parts:\non hand, on order"),
        ("Forecasting", "planned vs. actual\npurchasing; sales"),
    ]
    OW, OH = 230, 90
    out_y = c_bottom + 110
    out_xs = [cx - 250, cx, cx + 250]
    for (t, sub), x in zip(outs, out_xs):
        els += labeled_box(x, out_y, OW, OH, t, sub, PINK)
        els.append(arrow(cx + (x - cx) * 0.3, c_bottom + 6, x, out_y - OH / 2 - 6))
    els.append(text(cx + 250 + OW / 2, out_y - OH / 2 - 34, "Outputs", 20, "right"))

    # Outer boundary: everything is on one machine.
    bx, by, bw = 20, 10, 2 * (cx - 20)
    bh = out_y + OH / 2 + 60 - by
    els.append(rect(bx, by, bw, bh, "transparent", "dashed"))
    els.append(text(cx, by + bh - 36, "everything inside the dashed line runs on one machine; nothing is exposed to the internet",
                    16, "center", MUTED))
    return doc(els)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventory-ops-pipeline.excalidraw").write_text(json.dumps(pipeline(), indent=1))
    (out / "inventory-ops-dataflow.excalidraw").write_text(json.dumps(dataflow(), indent=1))
    print("wrote", out)
