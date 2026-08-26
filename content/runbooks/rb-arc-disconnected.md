---
id: rb-arc-disconnected
title: Arc agent disconnected: bring the server back
level: L2
subject: azure
tags: arc|connected machine agent|heartbeat|hybrid
related: azarc-onboard|azhybridcompute|azdcr|kql-agents-silent|kql-agent-versions
verified: 2026-08
---

## Preconditions
- Local admin (or root) on the affected server, and Azure Connected Machine Resource Administrator or similar on the Azure side.
- The machine's expected network path to Azure: direct, proxy, or Private Link, because most disconnects live there.

## Steps
1. Confirm the symptom in Azure first: the machine resource shows disconnected and the last heartbeat time tells you when it broke; one machine is a machine problem, a whole site at once is network or proxy.
2. On the server, run "azcmagent show" and read the agent status, last heartbeat, and the endpoint connectivity it reports.
3. Check the agent services are running (himds and the extension/guest config services); restart them if stopped and watch whether the heartbeat returns.
4. Test connectivity with "azcmagent check": it validates reachability of the required endpoints through whatever proxy is configured; fix proxy settings with "azcmagent config" when the environment changed.
5. Look at the expiry angle: a machine left disconnected long enough has an expired managed identity certificate and will never reconnect on its own; the fix is to disconnect and re-onboard the agent (its Azure resource identity is recreated).
6. Check the agent version against the currently supported window and update an outdated agent; silent version drift is a common root cause after a year of neglect.
7. After reconnection, confirm downstream data flows resumed: AMA is shipping to the DCR destinations and extensions show healthy.

## Verify
- The machine shows connected in Azure with a fresh heartbeat.
- "azcmagent show" is clean and dependent extensions report success.
- Log tables fed by this machine show new rows.

## Rollback
- Re-onboarding creates a new resource identity: re-link anything that referenced the old resource ID (DCR associations, alerts, policy assignments) or apply them to the new resource.

## Escalate when
- A whole segment disconnects together and network denies changing anything: bring the firewall owner into the ticket.
- The server is domain-critical and re-onboarding needs a change window.
- Arc-enabled ESU activation rides on this machine: expiry has licensing consequences beyond monitoring.
