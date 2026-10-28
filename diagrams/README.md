# Diagram sources

Editable sources for the diagrams used in case studies. This folder is not
published; Eleventy only copies `src/`.

Workflow: open a `.excalidraw` file at https://excalidraw.com (Open → file),
edit, save the file back here, then export a PNG into `src/img/<case-study>/`.

Export by hand: Export image → PNG, scale 2x, background on. Or scripted,
which drives excalidraw.com's own export dialog in headless Chrome (needs
Playwright; the budget-itemizer project has it installed):

    NODE_PATH=~/Dev/budget-itemizer/node_modules node diagrams/export-excalidraw.js \
      diagrams/inventory-ops-pipeline.excalidraw /tmp/preview.png src/img/inventory-ops/pipeline.png

Keep canvases roughly 700–800 units wide so labels display at the same size
as the order-form diagrams (drawn ~685 wide) in the ~720px case-study column.

- `inventory-ops-before.excalidraw` — the spreadsheet loop the tool replaced;
  rough draft from the brain dumps, steps to be corrected by Daniel.
- `inventory-ops-pipeline.excalidraw` — the Plan → Order → Inbound → Receive →
  Monitor stages, with At Risk as the overstock side state.
- `inventory-ops-dataflow.excalidraw` — reports in, local database, working
  pages, outputs; dashed boundary = one machine.
- `generate-inventory-ops.py` — the script that produced the first drafts of
  the two files above on 2026-10-27. After hand edits in Excalidraw the
  `.excalidraw` files are the source of truth; rerunning the script would
  overwrite them.

The order-form diagrams' source is still at
`~/Downloads/order form workflows.excalidraw`; copy it here when convenient.
