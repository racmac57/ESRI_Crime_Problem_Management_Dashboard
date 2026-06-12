# AGOL Production Folder Structure

Documents the 2026-06-12 ArcGIS Online (AGOL) reorganization for the Crime Problem Management (CPM) deployment. Records which items live in which folder, why the shared data layers were separated, and which folder is a stale duplicate slated for deletion.

## Folder: CPM_Production (13 items)

The production home for all CPM application content. The Crime Problem Analyst web map referenced by the ArcGIS Pro project now lives here (item ID d5556e2f375c4adf8c0452e14f34177b).

Web maps:

- New Crime Problem
- Problem Response Planner
- Problem Response Coordinator
- Problem Response Monitor
- Evaluated Problem Responses
- Problem Response Successes
- Crime Problem Analyst (d5556e2f375c4adf8c0452e14f34177b)
- Crime Problem Manager (25560bc48f5a42158c5ec6f370a2f81d)
- Crime Problem Dashboard (e3b69c7d65fe4fa791b4854fd80e46e9)
- Evaluated Responses Library (3e82306633764cd98d37db1e0110a267)

Apps:

- Crime Problem Manager Web Experience (247a7d286a3442beb74c0d46c30beecd)
- Crime Problem Dashboard Dashboard (7472557349d5437aa011ce7384b8ee14)
- New Crime Problem Web Mapping Application

## Folder: shared_production_layers (2 items)

- Crimes Feature Layer (bc108c0cb375461cb6645b47b80f6837)
- CallsForService Feature Layer (44173f3345974fe79a01bfa463350ce2)

Rationale: these are org-wide data sources consumed by CPM, Daily Calls, Daily Crimes, SCRPA, CCTV, and statistics content. They are kept outside any single project folder so that future project archiving cannot orphan them. Do not move these layers into a project folder.

## Folder: Crime Problem Management 1

Confirmed stale duplicate deployment holding the abandoned twin copies. DO NOT USE. Deletion candidate pending required_by verification on cleanup day.

Known stale twin item IDs (full IDs from scripts/agol_audit_output/cpm_audit_20260612_023104.md, STALE CANDIDATES section):

- Crime Problem Manager Web Map: 7e4287b37a6743fcad3b9f46cded2b96
- Crime Problem Dashboard Web Map: e8af4a85d0e5464fbf895cf446c5ad49

## Verification

Verification on 2026-06-12 confirmed that the Crime Problem Manager Web Experience and the Daily Calls Dashboard load live data after the move.

---

Author: R. A. Carucci | HPD SSOCC | Document date: 2026-06-12
