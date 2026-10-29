#!/usr/bin/env python3
"""Generate the three Inventory Ops .excalidraw files (before, pipeline,
dataflow). Helpers and style notes live in excalidraw_lib.py."""
import json, random, sys
from pathlib import Path

from excalidraw_lib import (BLUE, GREEN, GREY, LINE_H, MUTED, PINK, YELLOW,
                            arrow, doc, labeled_box, rect, text)

random.seed(20261027)


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

    # No caption on the image: the "a SKU can sit in several stages" point
    # belongs in the page prose next to the diagram, not baked into the PNG.
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


# ---------------------------------------------------------------- Diagram 0
# The "before": the spreadsheet loop. Drawn in the register of the order-form
# before diagram (2026-10-28 look at src/img/workflow-form/before.png): a few
# single-label boxes, green start, pink for the steps that hurt, dotted pink
# for where things trail off. Rough draft from the brain dumps; Daniel will
# correct the steps.
def before():
    els = []
    cx, W, H = 520, 340, 90
    lx, LW = 160, 280
    ys = {"A": 80, "B": 250, "E": 420, "F": 590, "G": 780}
    els += labeled_box(cx, ys["A"], W, H, "new reports in\nthe warehouse portal", None, GREEN)
    els += labeled_box(cx, ys["B"], W, H, "download, paste\ninto the sheet")
    els += labeled_box(cx, ys["E"], W, H, "read off what\nneeds ordering")
    els += labeled_box(cx, ys["F"], W, H, "talk it over;\nplace orders")
    els += labeled_box(cx, ys["G"], W, H, "status, notes, tracking:\nin my head and email", None, PINK, "dotted")
    for a, b in [("A", "B"), ("B", "E"), ("E", "F"), ("F", "G")]:
        els.append(arrow(cx, ys[a] + H / 2 + 6, cx, ys[b] - H / 2 - 6))

    # The breakage loop off the paste step: new SKU -> patch formulas -> paste again.
    els += labeled_box(lx, ys["B"], LW, H, "a new SKU\nbreaks the sheet", None, PINK)
    els += labeled_box(lx, ys["B"] + 170, LW, H, "patch the formulas", None, PINK)
    els.append(arrow(cx - W / 2 - 6, ys["B"], lx + LW / 2 + 6, ys["B"]))
    els.append(arrow(lx, ys["B"] + H / 2 + 6, lx, ys["B"] + 170 - H / 2 - 6))
    els.append(arrow(lx + LW / 2 + 6, ys["B"] + 170 - 10, cx - W / 2 - 6, ys["B"] + H / 2 + 10))

    # The second output of the sheet: the stock-level email, assembled by hand
    # (Daniel, 2026-10-28). Branches off the read-off step beside the orders path.
    ey = ys["F"]
    els += labeled_box(lx, ey, LW, H, "stock-level email,\nassembled by hand")
    els.append(arrow(cx - W / 2 - 6, ys["E"] + 20, lx + LW / 2 + 6, ey - 20))

    # And the whole thing runs again next time.
    rx = cx + W / 2 + 70
    els.append(arrow(cx + W / 2 + 4, ys["G"], rx, ys["G"], head=None))
    els.append(arrow(rx, ys["G"], rx, ys["A"], head=None))
    els.append(arrow(rx, ys["A"], cx + W / 2 + 4, ys["A"]))
    els.append(text(rx + 12, (ys["A"] + ys["G"]) / 2 - 12, "next\ntime", 16, "left", MUTED))
    return doc(els)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventory-ops-before.excalidraw").write_text(json.dumps(before(), indent=1))
    (out / "inventory-ops-pipeline.excalidraw").write_text(json.dumps(pipeline(), indent=1))
    (out / "inventory-ops-dataflow.excalidraw").write_text(json.dumps(dataflow(), indent=1))
    print("wrote", out)
