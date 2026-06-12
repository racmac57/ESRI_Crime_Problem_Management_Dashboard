# Python Tips and Tricks for ArcGIS Administration
*Esri Training Seminar — Cleaned transcript with timestamps*

**Presenters:** Timothy Kinlaw (Sr. Instructor) & Jeff Bigos (Principal Technical Lead)
**Moderator:** Allison Rost

---

## Introduction

**[00:08]** Welcome to the live training seminar, Python Tips and Tricks for ArcGIS Administration. Timothy Kinlaw introduces himself (senior instructor, Esri Educational Services, Charlotte NC) and Jeff Bigos (principal technical lead, northeast Massachusetts). Allison Rost is the moderator, tagged as **Host** in chat, curating questions.

**[00:54]** There will be three Q&As; attendees are asked to submit and upvote questions.

**[01:04]** *The problem:* There are millions of items in ArcGIS Online, some mission-critical. Administration gets easier when you can see the story behind your content — not just titles and owners, but metrics and dependencies.

**[01:35]** *Agenda — three topics:* (1) **Reports** — running them with the ArcGIS API for Python and turning them into insights; (2) **Item graphs** — understanding relationships and dependencies; (3) **ArcGIS Notebooks assistant** — using an AI assistant to generate, explain, and troubleshoot code.

## Section 1 — Reports (Jeff)

**[02:09]** Reporting can reveal interesting patterns and support a range of visualizations. A poll is run on who currently uses reporting in Online/Enterprise.

**[02:49]** *Anecdote:* Jeff ran a report and found an item from 2015 using significant storage with **zero** views.

**[04:13]** Reports cover organization-wide usage for ArcGIS Online or Enterprise, designed for administrators. **Through the Python API you must be a "reporter" user type to run them.**

**[05:46]** *Why use Python over manual reports:* it lets you customize and work with the raw report data — filter by specific item types (e.g., focus on feature services or web maps), focus on users, examine trends over time (date columns), apply numeric filters, and build custom visualizations/charts in a notebook.

### Report parameters & the six report types

**[07:36]** **Six report types**, with a description column and a "where it runs" column.

**[07:59]** ArcGIS Online can run **all six**. ArcGIS Enterprise can run only the **content** and **user** reports (it cannot run service usages or item usages).

**[08:27]** Report descriptions:
- **Content report** (Jeff's favorite) — a snapshot of all content items in an organization.
- **Credit report** — credit costs of credit-consuming tools/capabilities in ArcGIS Online.
- **User report** — member details like user types.
- **Activity report** — new/updated/deleted content and org updates for members, groups, passwords.
- **Service usages** — credit usage associated with registered apps.
- **Item usages** — item view counts; **can aggregate by a time period** (e.g., a year's views broken out month-by-month).

**[09:49]** Method parameters: **report type**, **start time** (when the reporting window begins), **duration** (yearly / monthly / weekly), and **time aggregate** (ties to item-usage aggregation).

## Demo 1 — Content report & visualizations (Jeff)

**[12:01]** Workflow: import libraries — the **ArcGIS API for Python**, **pandas** (groupbys/aggregates), and **matplotlib** (visualizations). Authenticate with the `home` keyword as an administrator.

**[13:23]** Run a yearly content report (pre-run for time). It returns an **item** whose data is a resultant **CSV**; use the item's **`get_data`** method to retrieve the raw CSV, then load it with pandas **`read_csv`** into a DataFrame.

**[15:11]** Inspect the DataFrame — date columns, view counts, file storage, item type. A **value count** on the item-type column (then `.plot()`) shows the distribution: mostly feature services and web maps, plus some Experience Builder apps/templates, dashboards, and a story map (e.g., 40 feature services, 25 web maps).

**[17:50]** Analyze **days since modified** by share level and item type — shows which content is active vs. published-but-unmodified.

**[20:25]** Use **`nlargest(10)`** on view counts to find the top-10 most-viewed items (top items: a feature service and a web map).

**[22:14]** A groupby/aggregate/sort on view counts surfaces a publicly shared feature service titled **"Test Features"** with **no view counts**.

**[23:11]** Combine **file storage size** and **feature storage size** into total storage and compare against views.

**[24:31]** The "Test Features" item is traced to its owner — **Tim** — used as a light running gag through the demo.

## Q&A 1

**[25:26]** *Do you need ArcGIS Notebooks to run reports?* No — once authenticated at admin level, Online gives you all six reports; Enterprise gives the content and user reports only.

**[27:16]** *Managing risk when running scripts:* test in a separate (non-production) environment, limit scope by authenticating with as few privileges as possible, and carefully validate scripts.

**[29:03]** *Enterprise reports* don't include detailed app-usage metrics (e.g., last time a user opened ArcGIS Pro).

**[29:03]** *Authenticating without hard-coding credentials:* two common options — (1) a built-in ArcGIS Online account with **OAuth 2.0** and a client ID, or (2) a locally stored **profile** (call it by name; username/password managed behind the scenes). The demo uses a profile.

## Section 2 — Item Graphs (Tim)

**[31:15]** Reports tell you item properties and usage, but "what depends on this item?" is a different question — that's what item graphs answer.

**[32:07]** Item graphs model content as **nodes** (items) and **edges** (relationships) rather than flat tables.

### Node methods

**[33:27]** **`contains`** — items the item of interest directly relies on (e.g., a dashboard's web maps/scenes; a web map's layers).

**[33:54]** **`contained_by`** — reverses direction: what directly consumes the item (e.g., which web maps/scenes a layer is in; which web apps a web map is in).

**[34:22]** **`requires`** — *all* dependencies, top-down, going as deep as the service definition file.

**[34:49]** **`required_by`** — everything consuming the item, all the way up.

### Use cases

**[35:42]** Report web application and web map dependencies; answer "what are this app's dependencies?" or "where is this web map consumed?"; report enterprise geodatabases used for reference layers; **verify migration** of all related content (maps, scenes, layers) between test and production.

**[37:53]** Identify high-value feature services and where they're consumed; perform **impact analysis** before deleting/updating a feature service.

**[38:18]** **Update invalid items** — use the API's **`remap`** method with the item graph as the logical engine to bulk-replace broken layers across web maps, saving manual editing.

## Demo 2 — Building item graphs (Tim)

**[40:07]** *Top-down example:* pass a dashboard to the **`create_dependency_graph`** function's item-list parameter. The function works **recursively** to retrieve all dependencies.

**[40:59]** *Reporting feature-layer usage:* iterate over graph nodes with pandas, extracting title, item, type, and owner of supporting items.

**[42:19]** Map item types to colors for a clearer visualization (dashboard → web map → feature services → service definitions).

**[42:45]** *Bottom-up example:* to report feature-layer consumption, start from the bottom. Use search operations for feature layers, web maps, and applications, then build the graph from that list of items/IDs.

**[44:35]** **Persistence:** save the graph as a **GML file** and reload it later to quickly reproduce the item graph. Report highest-usage feature layers using the **`required_by`** method as the usage metric.

**[45:33]** **Report broken content** — iterate nodes to find broken references (deprecated basemaps, deleted layers, unshared/insufficient-permission content).

## Q&A 2

**[47:25]** *Manually add missing dependencies?* The item graph class is built on **NetworkX's DiGraph**, so you can add nodes/edges in script. A saved GML file can be reopened and extended.

**[49:13]** *Licensing:* No additional license is needed for the item graph (with ArcGIS Knowledge as an Enterprise extension, you can optionally export to a knowledge graph).

**[49:38]** *Label nodes with item names?* Yes — each node holds the full item object; use `node.item.title` as the label.

**[50:05]** *Trace dependencies outside your org (e.g., public layers)?* Yes — it's a parameter of `create_dependency_graph`.

## Section 3 — ArcGIS Notebooks Assistant (Jeff)

**[51:26]** The Notebooks assistant's main function is to **generate, explain, and troubleshoot Python code**, built on ArcGIS-specific references (good with ArcGIS API for Python and ArcPy). Currently **in beta in ArcGIS Online**.

**[53:38]** **Enablement:** turn on **AI assistance** in org settings (review docs against company AI policy). Optionally restrict via an **AI assistant privilege** added to a custom role and assigned to specific users.

### Demo 3 — Generate, explain, find errors

**[55:50]** *Generate:* click **Generate**; a panel slides out with both **code** and an **explanation** (e.g., code that connects to the org, creates users via the user manager, assigns 100 credits).

**[58:00]** Prompts can be recalled and re-run with changes (e.g., 500 credits, 50 users).

**[58:26]** *Explain:* feed in Tim's item-graph code with "can you explain this code:" — it explains the item-graph-to-DataFrame process. Helpful explanations can be rated/submitted as feedback.

**[60:37]** *Find errors:* deliberately introduce a bug (`contents` instead of `content`) producing "GIS object has no attribute contents." The assistant explains the correct property is the **content manager** (`content`, singular) and suggests a search to find the item.

## Q&A 3 & Conclusion

**[63:24]** *Does the assistant remember context within a notebook?* Responses depend on the prompt; it can draw on items, other orgs, and pandas-accessible hosted files.

**[65:10]** *Does it cost credits?* As a beta feature, the Notebooks assistant **does not consume credits**. Available in ArcGIS Online hosted notebooks for now.

**[65:35]** *When in ArcGIS Enterprise?* Beta release planned for **Q4**.

**[66:02]** Closing — not all questions could be answered live; common answers will be posted to **Esri Academy**. More via the **Additional Resources** tab below the video.

**[66:28]** "We hope you all enjoyed the seminar today. Thank you for your time and have a great rest of your day."

---
*Cleaned from the official seminar captions. Transcription typos corrected, filler removed, API names normalized, section headers added. All technical content preserved.*
