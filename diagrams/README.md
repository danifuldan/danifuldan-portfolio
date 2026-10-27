# Diagram sources

Editable sources for the diagrams used in case studies. This folder is not
published; Eleventy only copies `src/`.

Workflow: open a `.excalidraw` file at https://excalidraw.com (Open → file),
edit, then Export image → PNG at scale 2 with background on, and save the PNG
under `src/img/<case-study>/`. The existing order-form PNGs are 1370px wide;
match that for consistency.

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
