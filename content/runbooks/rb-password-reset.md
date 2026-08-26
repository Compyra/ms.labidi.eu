---
id: rb-password-reset
title: Password reset: verify, reset, revoke
level: L1
subject: entra
tags: password reset|helpdesk|identity verification
related: enusers|ensign|mymfa|ps-revoke-sessions|kql-risky-signins
verified: 2026-08
---

## Preconditions
- Helpdesk Administrator can reset non-admin users; Privileged Authentication Administrator is needed for admins.
- Your desk's identity verification procedure; password resets are the classic social engineering request.

## Steps
1. Verify the caller's identity first per procedure: callback to the number on file, manager confirmation, or video; never skip this for "urgent" requests.
2. Check the user's sign-in logs before touching anything: unfamiliar locations or impossible travel means you switch to the account compromise runbook instead of doing a plain reset.
3. Reset from Entra admin center, Users, select the user, Reset password; use the auto-generated temporary password and leave "require change at next sign-in" on.
4. Deliver the temporary password out of band: read it over the verified call; never mail it to the mailbox the user may be locked out of.
5. If the reset is security-motivated, also revoke sessions so existing tokens die; a password change alone leaves live sessions running.
6. If the account was blocked by risk policy, a reset by itself may not clear the risk state: with Entra ID P2, a secure password change by the user remediates user risk, otherwise dismiss the risk manually after you are sure it is a false positive.

## Verify
- The user signs in with the new password and completes MFA.
- The sign-in log shows the fresh successful sign-in and nothing suspicious after it.

## Rollback
- There is nothing to restore: an old password cannot be brought back. If you reset the wrong account, help that user set a new password and note the mistake in the ticket.

## Escalate when
- You cannot verify the caller's identity to your standard.
- Sign-in logs show signs of compromise: switch to the account compromise runbook.
- The target is an admin account or a VIP with elevated exposure.
