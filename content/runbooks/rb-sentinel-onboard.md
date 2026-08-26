---
id: rb-sentinel-onboard
title: Sentinel onboarding: workspace to first detections
level: L2
subject: sentinel
tags: onboarding|workspace|connectors|analytics rules
related: set-sen-onboard|azloganalytics|sencontenthub|senconnectors|xdranalytics|senautomation|sencost|kql-table-freshness
verified: 2026-08
---

## Preconditions
- Owner or Contributor on the target resource group, plus Sentinel Contributor going forward.
- A region decision (data residency) and a rough daily-GB estimate for cost expectations.

## Steps
1. Create a dedicated Log Analytics workspace in the agreed region; one workspace per tenant is the default choice until a data boundary forces more.
2. Enable Microsoft Sentinel on that workspace; the first 31 days of a trial benefit apply per workspace, so start when you mean to use it.
3. Install solutions from Content hub for the sources you actually own, starting with Microsoft Entra ID, Microsoft Defender XDR, and Microsoft 365; solutions bring the connectors, rule templates, workbooks and parsers together.
4. Configure each data connector and confirm tables receive data; free sources like most Microsoft alert signals are on by default economics, while log sources such as sign-in logs start the meter.
5. Turn on analytics rules from the installed templates, beginning with the high-fidelity ones tied to the connectors you enabled; skip anything whose data source you do not ingest, it can only misfire.
6. Set up the basics of automation: an automation rule that tags and assigns incidents, before any fancy playbooks.
7. Watch the first week of ingestion against the estimate with the usage query, then set a commitment tier once the daily volume is stable and the math favors it.
8. Wire the operational guardrails: ingestion health monitoring, and agree who triages incidents from day one, otherwise the queue rots immediately.

## Verify
- Connector pages show connected and their tables show fresh rows.
- At least one test detection fires end to end and lands as an incident with an owner.
- Week-one cost matches the estimate to the right order of magnitude.

## Rollback
- Removing Sentinel from the workspace stops the Sentinel meter but keeps the Log Analytics data until retention runs out; get the order of operations right by reading the removal setting card before pulling anything.

## Escalate when
- Data residency, multi-tenant, or MSSP requirements appear mid-build: architecture first, connectors later.
- Ingestion lands far above estimate and the offender is a verbose source you cannot simply turn off.
