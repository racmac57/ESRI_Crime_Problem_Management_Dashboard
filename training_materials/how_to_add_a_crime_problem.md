# How to Add a Crime Problem -- Step-by-Step Guide

A crime problem in the Crime Problem Management (CPM) framework is a defined area and time window where a pattern of crime or disorder warrants focused attention. Documenting a problem creates a shared record that ties incidents, calls for service, responses, and evaluations together so analysts and command staff can plan, act, and measure results. This guide walks an HPD SSOCC analyst through creating a new crime problem end to end using two tools: the Crime Problem Manager (an Experience Builder web app on AGOL) and the Crime Problem Analyst Desktop App (an ArcGIS Pro project).

## Prerequisites

- AGOL access at Creator level or higher (required to create and edit problems). Contributor-level access can view but not edit.
- ArcGIS Pro 3.x installed and signed in to the same AGOL organization.
- Crime Problem Manager open in Experience Builder.
- Crimes and Calls for Service (CFS) feature layers loaded and accessible in both the web app and the Pro project.

Before creating a problem area in the CrimeProblemAnalyst ArcGIS Pro project, complete Step 2 of the project's built-in "Getting started" task: open the Portal tab, then My Content, then add the Crime Problem Analyst web map (item ID d5556e2f375c4adf8c0452e14f34177b, AGOL folder CPM_Production). This web map carries the preconfigured layers required for problem creation. Source: C. Tenah follow-up email, confirmed 2026.

## Section 1: Open the Crime Problem Manager (Experience Builder)

1. Sign in to ArcGIS Online at the HPD organization URL.
2. From the Content or Apps menu, locate the Crime Problem Manager app.
3. Click the app to launch it in Experience Builder.
4. Confirm you are signed in with an account that has Creator-level access.
5. Navigate to the Problem creation interface (the main problems panel or list view).

## Section 2: Create a New Problem Record

1. Click New Problem.
2. Fill in the required fields:
   - Name: a short descriptive title for the problem.
   - Type: the problem category (for example, burglary pattern, robbery series).
   - District: the HPD district the problem falls in.
   - Priority: the assigned priority level.
   - Start date: the beginning of the problem time window.
   - Description / narrative: a summary of the pattern and why it is being tracked.
3. Review the entries for accuracy.
4. Click Save to commit the initial problem record.
5. Note the problem name or ID. You will reference it in ArcGIS Pro.

## Section 3: Define the Problem Boundary in ArcGIS Pro (Analyst Desktop App)

1. Open the Crime Problem Analyst Desktop App (the ArcGIS Pro project).
2. Open the task pane and select the draw boundary task.
3. Activate the polygon sketch tool from the task step.
4. Sketch the problem boundary on the map around the affected area.
5. Attribute the boundary to the problem record created in Section 2 (select the matching problem name or ID).
6. Save the edits to commit the boundary.

## Section 4: Associate Incidents with the Problem

1. In the ArcGIS Pro task pane, select the incident association task.
2. Confirm the task is targeting the active problem and its boundary.
3. Run the task to link Crimes and CFS records that fall within the boundary and the problem time range.
4. Review the count of associated incidents returned by the task.
5. Save the results.

## Section 5: Document the Initial Response

1. Return to the Crime Problem Manager in Experience Builder.
2. Open the problem record you created.
3. Add a response entry describing the planned or initial action.
4. Set the problem status to Active.
5. Save the record.

## Section 6: Verify the Problem Appears on the Crime Problem Dashboard

1. Open the Crime Problem Dashboard from AGOL.
2. Confirm the new problem is visible in the active problems list.
3. Check that district, priority, and incident count display correctly.
4. If anything is missing, return to the relevant tool and confirm the record was saved.

## Notes and Gotchas

- The Crimes layer AGOL ID ends in 6837. Note that 6837 is the last four characters of the layer ITEM ID (full item ID: bc108c0cb375461cb6645b47b80f6837), not the service URL. The service URL uses a different token, so do not match on 6837 when setting the data source by URL. Confirm this exact layer is set in the ArcGIS Pro project data source settings before associating incidents. A wrong layer source will produce wrong or empty results. Authoritative service URLs confirmed by C. Tenah:
  - Crimes: https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/Crimes_2153d1ef33a0414291a8eb54b938507b/FeatureServer
  - Calls For Service: https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/CallsForService_2153d1ef33a0414291a8eb54b938507b/FeatureServer
- As of the Training and Knowledge Transfer phase, the dashboard is not yet fully operational. Some display issues may be present and are expected.
- Captain Weber is on Contributor-level access and cannot edit problems. He can view only. Creator upgrade is pending.

---

Author: R. A. Carucci | HPD SSOCC | Document date: 2026-06-05
