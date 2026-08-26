---
id: rb-mail-not-arriving
title: Mail not arriving: trace it end to end
level: L1
subject: m365
tags: message trace|mail flow|delivery
related: exmt|deqre|detallow|exforwarding|ps-message-trace
verified: 2026-08
---

## Preconditions
- Exchange Administrator or Exchange Recipient Administrator (read is enough to trace).
- Ask the user for: sender address, expected recipient, rough time, and subject.

## Steps
1. Confirm the service is healthy first: check Service health for Exchange Online, so you do not debug a known incident.
2. Open Message trace and search on recipient plus a time window that brackets the reported send.
3. Read the status column: Delivered, Filtered as spam, Quarantined, Failed, or Pending.
4. If nothing is listed at all, the message never reached the service: verify the sender actually sent it and check the sender domain's MX and SPF records.
5. If Quarantined, open Quarantine, inspect the message, and release it only if it is legitimate.
6. If Filtered, open the message detail to see which policy acted, then decide policy tuning or a Tenant Allow entry with an expiry.
7. If Failed, read the NDR code in the detail view: 5.1.x means recipient/address, 5.7.x means policy or authentication.
8. If Delivered but the user cannot see it, check for an inbox rule or forwarding that moved it.

## Verify
- The message shows Delivered to the mailbox and the user confirms they can see it.
- If you released from quarantine, re-trace to confirm final delivery.

## Rollback
- If you added a Tenant Allow entry, remove it once the root cause is fixed; allow entries weaken filtering.
- If you disabled an inbox rule, note the rule contents before deleting so the user can rebuild it.

## Escalate when
- The trace shows Pending for more than an hour with no service health advisory.
- Mail is failing for an entire domain rather than one recipient.
- You suspect compromise: an unexplained inbox rule or forwarding address means switch to the account compromise runbook.
