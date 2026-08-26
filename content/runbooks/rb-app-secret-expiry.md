---
id: rb-app-secret-expiry
title: App credential expiring: rotate without downtime
level: L2
subject: entra
tags: app registration|client secret|certificate|expiry rotation
related: enappreg|enapps|ps-app-secrets-expiring|ps-sp-signins
verified: 2026-08
---

## Preconditions
- Application Administrator, or ownership of the app registration.
- Know what consumes the credential before you touch it: script, service, integration, vendor product.

## Steps
1. Inventory upcoming expiries across the tenant on a schedule instead of waiting for outages; the expiring-credentials script gives the list with days left.
2. Identify the owner and the consumer of each credential; if nobody claims it, check the service principal's sign-in activity to see whether it is used at all before assuming it matters.
3. Create the new secret or certificate first: old and new stay valid in parallel, so a rotation done in this order has no downtime window.
4. Prefer a certificate over a client secret for anything long-lived, and store the private key or secret value in a vault, never in the script file.
5. Update the consuming side: app config, Key Vault reference, or pipeline variable, then deploy and confirm the app authenticates using the new credential.
6. Remove the old credential only after you see successful sign-ins with the new one in the service principal sign-in logs.

## Verify
- Service principal sign-ins keep succeeding after the old credential is deleted.
- The expiry inventory no longer lists the app inside the warning window.

## Rollback
- If the consumer breaks after removal, add a fresh secret or certificate and update the consumer; expired or deleted secret values can never be read back, so rollback means issuing a new one.

## Escalate when
- The app is orphaned: no owner, no documentation, but real sign-in traffic.
- The credential turns out to be hardcoded in source or shipped software.
- The app is multi-tenant and the change affects customers beyond your tenant.
