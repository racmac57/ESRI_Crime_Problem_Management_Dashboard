# Python Tips & Tricks for ArcGIS Administration — Quick Reference
*Condensed technical reference from the Esri training seminar*

---

## 1. Reports

**Access requirement:** Must be a **"reporter" user type** (admin level) to run reports via the ArcGIS API for Python.

**Why use Python (vs. manual reports):** work with raw CSV data — filter by item type, focus on users, analyze trends over time, apply numeric filters, and build custom visualizations in a notebook.

### Report types

| Report | What it shows | ArcGIS Online | ArcGIS Enterprise |
|---|---|:---:|:---:|
| **Content** | Snapshot of all content items in the org | ✅ | ✅ |
| **User** | Member details (e.g., user types) | ✅ | ✅ |
| **Credit** | Credit costs of credit-consuming tools/capabilities | ✅ | ❌ |
| **Activity** | New/updated/deleted content; org updates for members, groups, passwords | ✅ | ❌ |
| **Service usages** | Credit usage associated with registered apps | ✅ | ❌ |
| **Item usages** | Item view counts; can aggregate by time period | ✅ | ❌ |

> Enterprise can run **only** the Content and User reports.
> Enterprise reports **do not** include detailed app-usage metrics (e.g., last ArcGIS Pro open).

### Report method parameters

| Parameter | Purpose |
|---|---|
| **report type** | Which of the six reports to run |
| **start time** | When the reporting window begins |
| **duration** | Window length: yearly / monthly / weekly |
| **time aggregate** | Aggregation grouping (used with the Item usages report) |

### Typical reporting workflow

```python
from arcgis.gis import GIS
import pandas as pd
import matplotlib.pyplot as plt

gis = GIS("home")                     # admin authentication

# 1. Run the report -> returns an item whose data is a CSV
report_item = gis.admin.usage_reports...   # report type, start time, duration

# 2. Pull the raw CSV from the item
csv_data = report_item.get_data()

# 3. Load into a DataFrame
df = pd.read_csv(csv_data)

# 4. Analyze / visualize
df["item_type"].value_counts().plot(kind="pie")   # distribution by type
df.nlargest(10, "views")                           # top-10 viewed items
```

**Useful analyses shown:** item-type distribution (value_counts), days-since-modified by share level / item type, top-N views (nlargest), total storage (file + feature storage) vs. views.

---

## 2. Item Graphs

Model content as **nodes** (items) and **edges** (relationships) to answer dependency questions that flat reports can't.

### Node methods

| Method | Direction | Returns |
|---|---|---|
| **`contains`** | down, direct | Items this item directly relies on (dashboard → web maps; web map → layers) |
| **`contained_by`** | up, direct | What directly consumes this item (layer → web maps; web map → web apps) |
| **`requires`** | down, full | ALL dependencies top-down, as deep as the service definition file |
| **`required_by`** | up, full | Everything consuming this item, all the way up (good as a usage metric) |

### Building a graph

```python
from arcgis.apps.itemgraph import create_dependency_graph

# Top-down (recursive): from an app/dashboard down through its dependencies
graph = create_dependency_graph(gis, item_list=[dashboard_item])

# Bottom-up: search for feature layers / web maps / apps, then build from IDs
graph = create_dependency_graph(gis, item_list=[*layer_ids, *map_ids, *app_ids])

# Iterate nodes -> pandas report
rows = [(n.item.title, n.item.itemid, n.item.type, n.item.owner) for n in graph.nodes]
```

### Key facts
- Built on **NetworkX `DiGraph`** — you can add nodes/edges manually in script.
- **Persist** a graph as a **GML file**; reload later to reproduce it quickly.
- Node labels: use `node.item.title`.
- Can include **items outside your org** (e.g., public layers) — a parameter of `create_dependency_graph`.
- **No extra license** required (optional export to ArcGIS Knowledge as an Enterprise extension).

### Use cases
- Report app / web map dependencies ("what does this app depend on?" / "where is this map used?").
- Verify migration brings all related maps, scenes, and layers (test → production).
- Impact analysis before deleting/updating a feature service (`required_by`).
- Report broken content (deprecated basemaps, deleted/unshared layers).
- **`remap`** method: bulk-replace broken layers across web maps using the graph as the logic engine.

---

## 3. ArcGIS Notebooks Assistant (beta)

**Purpose:** generate, explain, and troubleshoot Python code; tuned for the ArcGIS API for Python and ArcPy.

| Topic | Detail |
|---|---|
| **Availability** | Beta, **ArcGIS Online hosted notebooks** only |
| **Enterprise** | Beta release planned for **Q4** |
| **Credits** | **Free** during beta (no credit consumption) |
| **Enable** | Org settings → turn on **AI assistance** |
| **Restrict access** | Add the **AI assistant privilege** to a custom role, assign to specific users |

**Three functions:** *Generate* (code + explanation panel), *Explain* (prefix code with a prompt like "can you explain this code:"), *Find errors* (paste the error; it explains and suggests a fix — e.g., `content` is the correct content-manager property, not `contents`).

---

## Authentication patterns

| Method | Notes |
|---|---|
| `GIS("home")` | Run inside a hosted notebook as the signed-in (admin) user |
| **Profile** | Locally stored named credential; call by name, username/password managed behind the scenes |
| **OAuth 2.0 + client ID** | Built-in ArcGIS Online account; avoids storing username/password locally |

**Script safety:** test in a separate non-production environment; authenticate with the fewest privileges needed; validate scripts before production runs.

---
*Companion to: python-admin-seminar-transcript.md*
