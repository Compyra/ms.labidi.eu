---
id: rb-mfa-reregister
title: MFA re-registration: verify first, then TAP
level: L1
subject: entra
tags: mfa|temporary access pass|lost phone|authentication methods
related: enpumfa|enmfaunblock|mymfa|ps-create-tap|ps-list-mfa-methods
verified: 2026-08
---

## Preconditions
- Authentication Administrator (non-admins) or Privileged Authentication Administrator (admins).
- Temporary Access Pass enabled in the Authentication methods policy if you want the TAP flow.
- Strict identity verification: an MFA reset is the single most valuable thing an attacker can ask a helpdesk for.

## Steps
1. Verify identity harder than for a password reset: known callback number, manager on the call, or video with ID, per your policy; log how you verified.
2. List the user's registered authentication methods and note what exists before you change anything.
3. Delete only the methods the user no longer controls, such as the number of a lost phone; leave working methods in place.
4. Use "Require re-register multifactor authentication" on the user so they are pushed through fresh registration at next sign-in; note this by itself does not delete existing methods.
5. Issue a Temporary Access Pass, short-lived and one-time-use, so the user can sign in without the lost method and register the new one.
6. Point the user at My security info to add the new method, and stay on the line until it works.

## Verify
- The methods list shows the new method registered.
- The user completes a real MFA prompt with the new method.
- The TAP is consumed or expired; delete it if it is still live.

## Rollback
- Delete the Temporary Access Pass immediately if it was issued in error: a live TAP is a working bypass credential.
- Re-add a deleted method only by having the user register it themselves.

## Escalate when
- Identity cannot be verified to the standard this action deserves.
- The account shows risk events around the request: treat as compromise, not as a lost phone.
- The target holds an admin role: apply the stricter admin verification path.
