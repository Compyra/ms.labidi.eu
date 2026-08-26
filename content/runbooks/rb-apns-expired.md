---
id: rb-apns-expired
title: APNs certificate expired: recover iOS management
level: L2
subject: intune
tags: apns|apple push|certificate renewal|ios enrollment
related: intenant|inios|inenroll
verified: 2026-08
---

## Preconditions
- Intune Administrator, plus access to the Apple ID that created the current APNs certificate.
- Know that Apple ID: the whole recovery hinges on it. It should be a managed org account, never a personal one.

## Steps
1. Confirm the state in Intune under iOS enrollment, Apple MDM push certificate: expired means iOS devices have already stopped checking in; they are not unenrolled, just unreachable.
2. Renew, do not replace: download the CSR from Intune, sign in to Apple's push certificates portal with the same Apple ID that issued the current certificate, and use the renew action on the existing certificate.
3. Upload the renewed certificate to Intune. Devices resume checking in on their own; no user action and no re-enrollment.
4. If the same Apple ID is truly gone, contact Apple support to recover it before accepting defeat: creating a brand-new certificate with a different topic invalidates the existing enrollment.
5. Only as a last resort create a new certificate with a new Apple ID, and plan a re-enrollment wave of every iOS device; treat this as a project, not a ticket.
6. Once healthy, put the expiry date in your team calendar with a reminder well ahead: this outage is fully preventable and the renewal takes minutes when done on time.

## Verify
- The certificate shows active in Intune with a fresh expiry a year out.
- iOS devices check in again over the following hours without user action.

## Rollback
- There is no rollback for an expiry. After a wrong-Apple-ID replacement, the only path is re-enrolling devices.

## Escalate when
- Nobody can access the original Apple ID and its recovery contact details are stale.
- Devices still do not check in a day after a correct renewal.
- The estate includes ADE (automated enrollment) devices whose tokens also expired: those are separate renewals in the same portal family.
