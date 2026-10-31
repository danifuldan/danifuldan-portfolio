---
title: Inventory Ops
description: A small ERP I built for our team's inventory replenishment, replacing a spreadsheet that broke on every new SKU. It imports the warehouse reports, tracks each order from plan to receipt, and runs locally.
role: Problem definition, design & build
timeline: 2026 – present
outcome: In weekly use — 143 SKUs, ~20 vendors; still in development
order: 2
---

## The workflow and where it broke

My boss and I have a weekly meeting to check in about all of the inventory at our warehouse. We plan orders, check inbound shipments, verify receipts and more. 

For a long while, we worked out of a shared Excel document. It's a pretty difficult tool to use, to be honest. The reporting must be manually exported from the warehouse's web portal, so I would have to download the file, open it, copy data, and paste it into the correct sheet. Additions to the SKU list (updates at the warehouse) would throw off the sheet and data without manual adjustments. It was difficult to create and manage more complex relationships between the SKUs. And the stock update email that we started sending out ended up just using a (pretty ugly) direct copy of a pivot table. 

## The insight

We could use a better tool for managing these processes - an ERP (enterprise resource planning tool) - but realistically, we're a four person team with only two to three total people dealing with this data on a regular basis. Proposing the expense for an external tool would have been, shall we say, optimistic.

Around the same time, we were all given ChatGPT Enterprise access, which included ChatGPT Codex. So I figured: why not build it myself? 

## The build

In order to build a proof of concept and not be restricted by access to APIs (or lack thereof), I built a tool that runs locally, since I am the primary user. It imports the report files from before (no more copy and paste) and loads them into a SQLite database covering 143 SKUs — 46 currently active — across roughly 20 vendors. It also gracefully handles new SKU additions with a simple approval process for the new SKU. There are expanded reporting capabilities for weekly reporting and financial forecasting. It also has tools for tracking a SKU through the stages of the replenishment lifecycle, from planning to receiving, and seeing SKU history across equivalent SKUs for a complete picture of historical demand. We can manage the SKU relationships (kits, equivalent pieces, etc.) and vendors. 

## What changed

This project is still a WIP, but we are already seeing significant progress. During our weekly meeting, we are now able to quickly zoom in to focus on the specific SKUs that we need to pay attention to. We can quickly generate and export reporting, track status, generate purchase orders for vendors, and more. I will be building out more reporting capabilities to assist my boss with forecasting functions in the near future. 

## Reflection

This project has already exceeded the scope of the original tool because I can do so much more with Codex (good old scope creep!). So I, on the one hand, will need more time to work on this development because we keep adding things. But on the other hand, it also is doing more than the Excel sheet ever could.