---
id: rb-who-deleted
title: Who deleted this: answer it from the audit log
level: L1
subject: purview
tags: audit search|file deleted|inbox rule|attribution
related: puaudit|ps-audit-search|ps-audit-logs|kql-audit-user-lifecycle
verified: 2026-08
---

## Preconditions
- A Purview audit role (Audit Reader suffices for search) rather than broad admin.
- The narrowest facts you can get: what was deleted or changed, roughly when, and where it lived.

## Steps
1. Confirm auditing has the data before promising answers: Audit (Standard) keeps 180 days and Audit (Premium) one year by default; anything older is a backup question, not an audit question.
2. Search with a tight window and the right activities: file operations like FileDeleted or FileRecycled for documents, New-InboxRule and Set-InboxRule for mailbox rules, and user administration activities for account changes.
3. Add what you know as filters: the user if suspected, the file name or site URL as keywords; unfiltered tenant-wide searches drown you in noise.
4. Expect latency on recent events: audit records can take from minutes up to hours to become searchable, so "it happened 10 minutes ago and audit shows nothing" is normal.
5. Read the winning record fully: actor, timestamp, IP, and the detail payload; SharePoint deletions show the recycle path, mailbox events show the client used.
6. Export the results to CSV for the ticket when someone will act on the answer; screenshots age badly and CSV preserves the detail columns.
7. When the trail shows the actor is an unexpected account or an app identity, stop and re-read it as a possible compromise rather than a "who pressed delete" question.

## Verify
- The exported records answer who, when, from where, and with what client.
- The requester confirms the object and time match their report.

## Rollback
- Not applicable: audit search changes nothing. The recovery of whatever was deleted is its own path (recycle bin, retention, backup).

## Escalate when
- Records that should exist do not: gaps in auditing are themselves a security finding.
- The actor is a service account, an unfamiliar app, or a just-offboarded user.
- Legal or HR will rely on the answer: chain-of-custody expectations exceed a desk export.
