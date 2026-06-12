# CPM Environment Preflight Checklist

Date: 2026-06-12
Author: R. A. Carucci

Follow this checklist before creating a crime problem. It verifies that the required AGOL content, the ArcGIS Pro project, and the data connections are in place. Complete every check in order. If any check fails, see the last section and stop.

## Section 1: Verify AGOL content is present

1. Sign in to hpd0223.maps.arcgis.com.
2. Confirm the folder CPM_Production exists and contains these 13 items:
   - New Crime Problem (web map)
   - Problem Response Planner (web map)
   - Problem Response Coordinator (web map)
   - Problem Response Monitor (web map)
   - Evaluated Problem Responses (web map)
   - Problem Response Successes (web map)
   - Crime Problem Analyst (web map, item ID d5556e2f375c4adf8c0452e14f34177b)
   - Crime Problem Manager (web map, item ID 25560bc48f5a42158c5ec6f370a2f81d)
   - Crime Problem Dashboard (web map, item ID e3b69c7d65fe4fa791b4854fd80e46e9)
   - Evaluated Responses Library (web map, item ID 3e82306633764cd98d37db1e0110a267)
   - Crime Problem Manager Web Experience (app, item ID 247a7d286a3442beb74c0d46c30beecd)
   - Crime Problem Dashboard Dashboard (app, item ID 7472557349d5437aa011ce7384b8ee14)
   - New Crime Problem Web Mapping Application (app)
3. Confirm the folder shared_production_layers contains these 2 feature layers:
   - Crimes Feature Layer (item ID bc108c0cb375461cb6645b47b80f6837)
   - CallsForService Feature Layer (item ID 44173f3345974fe79a01bfa463350ce2)

Warning: the folder "Crime Problem Management 1" is a stale duplicate deployment. DO NOT use any item from it.

## Section 2: Verify the ArcGIS Pro project

1. Open the CrimeProblemAnalyst Pro project.
2. Complete Step 2 of the project's built-in "Getting started" task: open the Portal tab, then My Content, then add the Crime Problem Analyst web map (item ID d5556e2f375c4adf8c0452e14f34177b, folder CPM_Production).
3. Verify the Crimes and Calls For Service data source URLs match these two authoritative URLs exactly:
   - Crimes: https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/Crimes_2153d1ef33a0414291a8eb54b938507b/FeatureServer
   - Calls For Service: https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/CallsForService_2153d1ef33a0414291a8eb54b938507b/FeatureServer

Warning: a wrong or default layer source points to empty duplicate layers and produces wrong or empty results.

## Section 3: Quick functional check

1. Open the Crime Problem Manager Web Experience (item ID 247a7d286a3442beb74c0d46c30beecd).
2. Confirm it loads problem records and map data.

## Section 4: If a check fails

Stop. Do not create a problem. Report which check failed to the Principal Analyst.

## Cross-reference

For the crime problem creation workflow itself, see how_to_add_a_crime_problem.md.
