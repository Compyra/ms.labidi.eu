---
id: rb-flow-owner-leaver
title: Flows owned by a leaver: reassign before it breaks
level: L2
subject: power
tags: flow ownership|leaver|connections|service account
related: pa|pp|pp-flowops|ps-pp-flow-owners|ps-pp-environments
verified: 2026-08
---

## Preconditions
- Power Platform Administrator to see and reassign other people's flows.
- The offboarding ticket, ideally before the account is blocked, because this runbook works best while the owner still exists.

## Steps
1. List the leaver's flows across environments before their account is touched; the admin cmdlets enumerate ownership per environment, and business-critical flows hide in the default environment more often than anyone admits.
2. Triage the list with the leaver's team: which flows matter, which are personal experiments to let die.
3. Add a co-owner to every flow that matters, preferably a service account or the team's shared owner group, not the next person who will also leave someday.
4. Check each kept flow's connections: connections authenticate as a person, so a flow co-owned by the team but running on the leaver's credentials dies the moment sign-in is blocked or the password resets.
5. Recreate those connections under the service account and swap them into the flow, then run each flow once to prove it works without the leaver.
6. Do the same sweep for Power Apps the person owned and any custom connectors, which follow the same ownership and credential logic.
7. Only then let the offboarding proceed; note in the offboarding ticket that Power Platform is clear.

## Verify
- Each kept flow runs successfully with the new connections after the leaver's sign-in is blocked.
- Ownership lists show the service account or group, not the leaver.

## Rollback
- Flows stopped by a missed connection restart once someone with access fixes the connection; runs missed in between do not replay themselves, so check what the flow should have processed.

## Escalate when
- A flow uses a premium connector or gateway tied to infrastructure nobody else understands.
- The leaver owned environments themselves, not just flows in them.
- A dead flow was quietly load-bearing for a business process: treat as incident, then fix ownership culture.
