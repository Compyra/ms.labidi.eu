---
id: rb-phishing-triage
title: Phishing report triage: assess, purge, block
level: L2
subject: defender
tags: phishing|submissions|explorer|purge|tenant allow block
related: scenario-phishing|desubmissions|deexplorer|detallow|deqre|kql-phish-inbox|kql-url-clicks
verified: 2026-08
---

## Preconditions
- Security Reader gets you through assessment; purge actions need the Search and Purge role, and Tenant Allow/Block List changes need Security Administrator.
- Threat Explorer requires Defender for Office 365 Plan 2; on Plan 1 you work from real-time detections and the email entity page instead.

## Steps
1. Open the user-reported message in Submissions and read Microsoft's verdict as your starting hint, not the final answer.
2. Judge the message yourself: sender authentication results, the actual URLs behind the display text, urgency of language, and whether the "vendor" exists.
3. Benign: close it and tell the reporter thanks; a desk that answers every report keeps getting reports, which is what you want.
4. Malicious: scope the blast in Explorer by sender, subject and URL to find every recipient, not just the reporter.
5. Purge the campaign from mailboxes with Take action, soft delete, so users stop clicking while you work; soft delete is recoverable.
6. Check who already clicked with the URL click data, and treat anyone who clicked and entered credentials under the account compromise runbook.
7. Block what the campaign reused: sender or domain and URL entries in the Tenant Allow/Block List, with an expiry rather than forever.
8. Submit a sample to Microsoft when the filter missed it: that improves the verdict for everyone and documents the miss.

## Verify
- Explorer shows the purge completed and the message count for the campaign stops growing.
- New sends from the blocked sender or URL are quarantined.
- Every clicker is accounted for: reset done or cleared as no credential entry.

## Rollback
- Soft-deleted mail can be restored from the user's recoverable items if the verdict flips to benign.
- Remove allow or block entries you added once the campaign is dead; stale entries are debt.

## Escalate when
- Anyone entered credentials or an admin account received and opened the message.
- The campaign is targeted at your org specifically rather than commodity spray.
- Internal-to-internal phishing shows up: that means an account is already compromised.
