---
id: rb-quarantine-release
title: Quarantine release: when to free a message
level: L1
subject: defender
tags: quarantine|release|false positive|end user request
related: deqre|deqp|desubmissions|ps-quarantine-release
verified: 2026-08
---

## Preconditions
- Quarantine Administrator or Security Administrator for admin release across recipients.
- Understand which quarantine policy applied: it decides whether the user could have released it themselves.

## Steps
1. Find the message in Quarantine and read why it is there: spam, phish, high confidence phish, malware, or a mail flow rule; the reason drives how careful you are.
2. Preview the message and check the sender's authentication results and URLs; the preview is safe, attachments are not delivered to you.
3. Spam or bulk false positive from a real business sender: release to all recipients and report it to Microsoft as a false positive in the same flow, so filtering learns.
4. Phish verdicts: release only when you can positively explain the false positive, for example a known partner's mail relay misconfigured SPF; when in doubt, keep it in quarantine.
5. Malware or high confidence phish: do not release on user request alone; verify independently with the sender through a known-good channel, and involve security if the business insists.
6. Repeated false positives from the same legitimate sender: fix the pattern with the sender's IT (their SPF/DKIM), or a targeted allow entry with expiry, rather than releasing message by message.
7. Tell the user the outcome either way; unanswered quarantine requests train users to bypass the desk.

## Verify
- A released message arrives in the recipient's inbox (trace it if in doubt).
- A false-positive report is on record with Microsoft when you released against a filter verdict.

## Rollback
- A release cannot be pulled back once delivered: if you released malware, switch immediately to incident handling: purge from mailboxes, warn recipients, and check for clicks.

## Escalate when
- Anything with a malware verdict "must" be released per a VIP: security signs off, not the desk.
- The same campaign floods quarantine across many users: that is tuning or attack, not release requests.
- A release request itself looks like social engineering: attacker asking to free their own mail happens.
