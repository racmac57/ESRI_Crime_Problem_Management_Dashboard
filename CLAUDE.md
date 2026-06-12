# CLAUDE.md

## Project Identity

HPD SSOCC deployment of the Esri Crime Problem Management (CPM) solution version 2.0 on ArcGIS Online (AGOL). This repository holds training materials, dashboard files, scripts, and documentation that support analyst and command staff use of CPM.

## Folder Conventions

| Folder | Purpose |
|--------|---------|
| `training_materials/` | Session notes, recordings, step-by-step guides. |
| `dashboard_files/` | AGOL exports, config files, screenshots (placeholder until operational). |
| `scripts/` | Python and ArcPy automation scripts. |
| `docs/` | Generated training documentation for distribution. |

## Naming Conventions

- Use underscores, not dashes, in all filenames and folder names.
- Use descriptive lowercase filenames.
- All markdown files use the `.md` extension.

## Output Rules

- Never use em-dashes or en-dashes in any file content. Use plain ASCII hyphens or rewrite the sentence.
- Agent sessions (Claude in Chrome, Claude in Excel, etc.) must write logs to `scripts/agol_audit_output/session_logs/` or another dedicated log path. Never save a log to the path of an existing data file.

## How Claude Agents Should Help

- Draft step-by-step training guides from session notes or transcripts.
- Write ArcPy or Python scripts for AGOL content architecture analysis.
- Generate command staff briefing documents from analyst notes.
- Update `CHANGELOG.md` when new files or features are added.

## Author Standard for Code File Headers

Every code file begins with a four-line header:

```
// [timestamp YYYY-MM-DD-HH-MM-SS EST]
// [project]/[filename]
// Author: R. A. Carucci
// Purpose: [concise description]
```
