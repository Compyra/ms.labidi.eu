---
id: rb-shared-mailbox
title: Shared mailbox: create, grant, and the automap gotcha
level: L1
subject: m365
tags: shared mailbox|full access|send as|automapping
related: ex|ps-convert-shared|ps-grant-fullaccess|ps-grant-sendas
verified: 2026-08
---

## Preconditions
- Exchange Administrator or Exchange Recipient Administrator.
- The owner's answers: who reads, who sends, and whether replies should come from the shared address.

## Steps
1. Create the shared mailbox in the Exchange admin center; no license is needed while it stays under the 50 GB tier and without features like archive or litigation hold.
2. Grant Full Access to the members who read and manage it, and decide the sending model: Send As (mail appears from the shared address) or Send on Behalf (shows "on behalf of"); pick one deliberately, most teams want Send As.
3. Expect automapping: Full Access via the portal adds the mailbox to members' Outlook automatically within an hour or so; when someone does not want it auto-attached, grant Full Access via PowerShell with automapping off and let them add it manually.
4. Block, or confirm blocked, sign-in for the account behind the shared mailbox; nobody should ever log into a shared mailbox directly, and an unblocked shared account with a guessable password is a classic intrusion path.
5. Set sensible defaults with the owner: whether Sent Items copy into the shared mailbox's Sent folder (off by default, most teams want it on), and who cleans up.
6. Tell the members what to expect: mailbox appears on its own in Outlook, mobile needs the mailbox added explicitly, and permission changes take up to an hour to bite.

## Verify
- Members see the mailbox in Outlook and can open it.
- A test send goes out as the shared address and lands in the shared Sent Items (if enabled).
- Sign-in for the mailbox account is blocked.

## Rollback
- Remove the Full Access or Send As grants to detach members; automapped mailboxes disappear from their Outlook after the grant is removed.

## Escalate when
- The mailbox nears the unlicensed size limit or needs hold/archive: it needs a license and maybe a design rethink.
- The request is really a distribution list or a Team in disguise: route the design question, not the ticket.
- Multiple teams fight over the same shared identity: ownership first, permissions later.
