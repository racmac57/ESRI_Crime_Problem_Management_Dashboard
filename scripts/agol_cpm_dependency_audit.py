# 🕒 2026-06-12-02-11-18
# ESRI_Crime_Problem_Management_Dashboard/scripts/agol_cpm_dependency_audit.py
# Author: R. A. Carucci
# Purpose: Read-only AGOL audit. Anchors on the authoritative Crimes and Calls For
#          Service FeatureServer URLs (per C. Tenah email), walks UP the dependency
#          chain to find every web map, app, and dashboard consuming them (the KEEP
#          list), then flags all other Crime Problem related org content as stale
#          candidates. Writes a markdown report + CSV. NO deletions performed.
#
# Run from ArcGIS Pro Python window:
#   exec(open(r"C:\Users\carucci_r\OneDrive - City of Hackensack\10_Projects\ESRI_Crime_Problem_Management_Dashboard\scripts\agol_cpm_dependency_audit.py").read())
# Or from command line with the Pro env python.exe.

from pathlib import Path
from datetime import datetime
import csv

from arcgis.gis import GIS

# ---------------------------------------------------------------------------
# CONFIG (top-level constants; exec-compatible, no sys.argv)
# ---------------------------------------------------------------------------

# Authoritative service URLs from Celbrica Tenah's follow-up email.
# Both share the deployment token below; that token is the fingerprint of the
# CORRECT deployment. Any CPM content not tied to it is presumed stale.
AUTH_CRIMES_URL = (
    "https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/"
    "Crimes_2153d1ef33a0414291a8eb54b938507b/FeatureServer"
)
AUTH_CFS_URL = (
    "https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/"
    "CallsForService_2153d1ef33a0414291a8eb54b938507b/FeatureServer"
)
DEPLOYMENT_TOKEN = "2153d1ef33a0414291a8eb54b938507b"

# Title keywords used to sweep the org for ALL Crime Problem related content
# (keep list + stale candidates). Case-insensitive substring match.
CPM_KEYWORDS = [
    "crime problem",
    "crimeproblem",
    "crimes",
    "calls for service",
    "callsforservice",
    "cfs",
]

# Item types that can CONSUME the feature layers (walked upward).
CONSUMER_TYPES_LEVEL1 = ["Web Map", "Web Scene"]
CONSUMER_TYPES_LEVEL2 = [
    "Web Mapping Application",
    "Dashboard",
    "Web Experience",
    "StoryMap",
    "Form",
    "Instant App",
]

OUTPUT_DIR = Path(
    r"C:\Users\carucci_r\OneDrive - City of Hackensack"
    r"\10_Projects\ESRI_Crime_Problem_Management_Dashboard"
    r"\scripts\agol_audit_output"
)

# "pro"  -> use the active ArcGIS Pro sign-in (run from Pro Python window)
# "home" -> use inside a hosted AGOL notebook
AUTH_MODE = "pro"

MAX_ITEMS = 2000  # org sweep ceiling; hpd0223 org is small, this is generous

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def log(msg):
    print(f"[audit] {msg}")


def norm(s):
    return (s or "").strip().lower().rstrip("/")


def item_row(item, role, evidence=""):
    return {
        "role": role,
        "title": item.title,
        "item_id": item.itemid,
        "type": item.type,
        "owner": item.owner,
        "modified": datetime.fromtimestamp(item.modified / 1000).strftime(
            "%Y-%m-%d"
        )
        if item.modified
        else "",
        "views": getattr(item, "numViews", ""),
        "url": getattr(item, "url", "") or "",
        "evidence": evidence,
    }


def webmap_references_token(item, token):
    """True if a web map's operational layers / tables reference the
    deployment token in any service URL."""
    try:
        data = item.get_data() or {}
    except Exception as e:
        log(f"  ! could not read web map JSON for {item.title}: {e}")
        return False
    layers = (data.get("operationalLayers") or []) + (data.get("tables") or [])
    for lyr in layers:
        if token in norm(lyr.get("url", "")) or token in norm(
            str(lyr.get("itemId", ""))
        ):
            return True
    return False


def app_references_ids(item, id_set, token):
    """True if an app/dashboard/experience JSON references any keep-list web map
    item ID or the deployment token directly."""
    try:
        raw = str(item.get_data(try_json=True) or "")
    except Exception as e:
        log(f"  ! could not read app JSON for {item.title}: {e}")
        return False
    raw_l = raw.lower()
    if token in raw_l:
        return True
    return any(i.lower() in raw_l for i in id_set)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log(f"Authenticating (mode='{AUTH_MODE}') ...")
    gis = GIS(AUTH_MODE)
    log(f"Connected to {gis.url} as {gis.users.me.username}")

    keep, stale, review = [], [], []
    keep_ids = set()

    # --- 1. Resolve the two authoritative layer items by URL ---------------
    log("Resolving authoritative feature layer items ...")
    anchor_items = []
    candidates = gis.content.search(
        query=DEPLOYMENT_TOKEN, max_items=100
    ) or gis.content.search(query="", item_type="Feature Service", max_items=MAX_ITEMS)
    for it in candidates:
        if norm(getattr(it, "url", "")) in (norm(AUTH_CRIMES_URL), norm(AUTH_CFS_URL)):
            anchor_items.append(it)
    # Fallback: brute-force scan of all feature services if search index missed
    if len(anchor_items) < 2:
        log("  search fallback: scanning all Feature Services ...")
        for it in gis.content.search(
            query="", item_type="Feature Service", max_items=MAX_ITEMS
        ):
            if norm(getattr(it, "url", "")) in (
                norm(AUTH_CRIMES_URL),
                norm(AUTH_CFS_URL),
            ) and it.itemid not in {a.itemid for a in anchor_items}:
                anchor_items.append(it)

    if not anchor_items:
        log("FATAL: neither authoritative layer found by URL. Verify URLs/sign-in.")
        return

    for it in anchor_items:
        keep.append(item_row(it, "KEEP-anchor", "URL matches Celbrica email"))
        keep_ids.add(it.itemid)
        log(f"  anchor: {it.title} ({it.itemid})")

    # --- 2. Walk UP level 1: web maps that consume the anchor layers -------
    log("Scanning web maps for references to the authoritative deployment ...")
    for it in gis.content.search(
        query="", item_type="Web Map", max_items=MAX_ITEMS
    ):
        if webmap_references_token(it, DEPLOYMENT_TOKEN):
            keep.append(item_row(it, "KEEP-webmap", "references deployment token"))
            keep_ids.add(it.itemid)
            log(f"  keep web map: {it.title}")

    # --- 3. Walk UP level 2: apps/dashboards that consume those web maps ---
    log("Scanning apps/dashboards/experiences ...")
    for t in CONSUMER_TYPES_LEVEL2:
        for it in gis.content.search(query="", item_type=t, max_items=MAX_ITEMS):
            if app_references_ids(it, keep_ids, DEPLOYMENT_TOKEN):
                keep.append(item_row(it, "KEEP-app", f"{t} references keep list"))
                keep_ids.add(it.itemid)
                log(f"  keep app: {it.title} ({t})")

    # --- 4. Org sweep: flag CPM-named content NOT in the keep list ---------
    log("Sweeping org for Crime Problem related content ...")
    seen = set()
    for it in gis.content.search(query="", max_items=MAX_ITEMS):
        if it.itemid in seen:
            continue
        seen.add(it.itemid)
        title_l = norm(it.title)
        if any(k in title_l for k in CPM_KEYWORDS):
            if it.itemid in keep_ids:
                continue
            # Feature services NOT matching the authoritative URLs but with CPM
            # names are prime stale candidates (the empty duplicate layers
            # Celbrica described). Everything else goes to review.
            if it.type == "Feature Service":
                stale.append(
                    item_row(it, "STALE-candidate", "CPM-named, not authoritative URL")
                )
            else:
                review.append(
                    item_row(it, "REVIEW", "CPM-named, no link to keep list found")
                )

    # --- 5. Optional: item graph GML export (arcgis 2.3+ only) -------------
    gml_note = "itemgraph export skipped"
    try:
        from arcgis.apps.itemgraph import create_dependency_graph

        keep_app_ids = [r["item_id"] for r in keep if r["role"] == "KEEP-app"]
        if keep_app_ids:
            graph = create_dependency_graph(
                gis, item_list=[gis.content.get(i) for i in keep_app_ids]
            )
            gml_path = OUTPUT_DIR / f"cpm_keep_graph_{stamp}.gml"
            graph.write_gml(str(gml_path))
            gml_note = f"itemgraph saved: {gml_path.name}"
    except ImportError:
        gml_note = "arcgis.apps.itemgraph not available in this env (needs arcgis 2.3+); skipped"
    except Exception as e:
        gml_note = f"itemgraph export failed (non-fatal): {e}"
    log(gml_note)

    # --- 6. Write report ----------------------------------------------------
    rows = keep + stale + review
    csv_path = OUTPUT_DIR / f"cpm_audit_{stamp}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    md_path = OUTPUT_DIR / f"cpm_audit_{stamp}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# AGOL CPM Dependency Audit (READ-ONLY)\n\n")
        f.write(f"Run: {stamp} | Org: {gis.url} | User: {gis.users.me.username}\n\n")
        f.write(f"Note: {gml_note}\n\n")
        for label, group in (
            ("KEEP (move these to the dedicated production folder)", keep),
            ("STALE CANDIDATES (verify, then delete on cleanup day)", stale),
            ("REVIEW (CPM-named, unresolved; inspect manually)", review),
        ):
            f.write(f"## {label} ({len(group)})\n\n")
            f.write("| Title | Type | Item ID | Owner | Modified | Views | Evidence |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for r in group:
                f.write(
                    f"| {r['title']} | {r['type']} | {r['item_id']} | {r['owner']} "
                    f"| {r['modified']} | {r['views']} | {r['evidence']} |\n"
                )
            f.write("\n")

    log(f"DONE. Keep: {len(keep)} | Stale candidates: {len(stale)} | Review: {len(review)}")
    log(f"Report: {md_path}")
    log(f"CSV:    {csv_path}")


if __name__ == "__main__":
    main()
else:
    # exec() from the Pro Python window lands here
    main()
