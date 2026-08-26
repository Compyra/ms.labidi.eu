---
id: rb-ingest-cost-spike
title: Ingestion cost spike: find and trim the offender
level: L2
subject: sentinel
tags: cost|usage|dcr transform|daily cap|commitment tier
related: sencost|azdcr|set-sen-dailycap|set-sen-commitment|set-sen-tableplan|kql-usage-cost|kql-ingest-trend
verified: 2026-08
---

## Preconditions
- Sentinel Reader to investigate; Log Analytics Contributor to change DCRs, caps and tiers.
- Yesterday's bill or alert that triggered this, so you can define "normal".

## Steps
1. Run the usage query grouped by data type over the last 30 days and sort by billable volume: the offender is almost always one table, not a general rise.
2. Plot that table's daily trend to date the spike, then match the date against changes: new connector, diagnostic setting flipped on, an agent rollout, or verbosity change upstream.
3. Drill into the table to find the noisy source dimension: which computer, which resource, which event ID or category dominates rows.
4. Prefer fixing the source first: drop the debug/verbose category in the resource's diagnostic settings, or tune the upstream product's logging level.
5. When the source must stay, add a DCR transformation that filters or projects away the junk before ingestion; transforms act on supported workflows at ingestion time, so the savings are real but nothing already ingested shrinks.
6. Re-evaluate the table's plan: high-volume, low-query data may belong on a cheaper table plan rather than analytics.
7. Use the daily cap only as an emergency tourniquet and remove it when done: a cap stops security data collection when hit, which is exactly what an attacker would order.
8. When the new normal is stable, redo the commitment tier math; both directions, a spike fixed can also mean you are over-committed.

## Verify
- The usage trend for the offending table returns to the expected line.
- No detection depends on data you filtered out: search analytics rules for the table and columns you dropped.
- Any temporary daily cap is removed.

## Rollback
- Remove or edit the DCR transform to restore full ingestion; data dropped by the transform while it ran is gone, which is why detection impact gets checked before, not after.

## Escalate when
- The spike is caused by security-relevant volume, like an actual attack generating events.
- Trimming would blind an active detection or a compliance-mandated log.
- Costs need contractual answers: commitment tiers and reservations are a budget-owner conversation.
