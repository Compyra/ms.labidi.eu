---
id: rb-license-feature-check
title: Feature "missing": prove whether it is licensing
level: L1
subject: licensing
tags: service plans|license assignment|feature availability
related: enlicense|adlicense|ps-user-licenses|ps-list-sku|ps-license-errors
verified: 2026-08
---

## Preconditions
- License Administrator or User Administrator read access.
- The exact feature name and where the user expects to see it; "Teams thing is gone" needs one clarifying question first.

## Steps
1. Find which service plan carries the feature: the product documentation names the plan, and the licensing pages map plan to SKU; write down the plan name before touching the user.
2. Check the user's assigned licenses and expand to service plan level: the SKU can be assigned while the specific plan inside it is turned off for the user or group assignment.
3. Check the plan's status value: only Success means provisioned; PendingProvisioning or PendingActivation explain a feature that exists on paper but not in the client yet.
4. If the license comes via group, check the user for a license assignment error state; group-based licensing fails quietly per-user when seats run out or SKUs conflict.
5. Confirm seats exist at tenant level: consumed versus purchased for that SKU; assignment silently blocked by seat exhaustion looks identical to "missing feature" from the user's side.
6. When licensing is all green, stop blaming it: the feature may need an admin toggle in its own admin center, be mid-rollout per the message center, or need the client updated or signed out and in; check those before reassigning licenses randomly.
7. Fix the actual finding: enable the plan, fix the group error, buy or free a seat, or route to the feature's admin setting; then have the user sign out and in so the token picks up the change.

## Verify
- The service plan shows Success on the user and the feature appears in the client after a fresh sign-in.
- No license error remains on the user and seat counts are inside purchased limits.

## Rollback
- License and plan changes reverse cleanly by restoring the previous assignment state; note what you changed in the ticket so the next person sees the history.

## Escalate when
- Provisioning stays pending for many hours across multiple users.
- The fix needs a purchase decision or a SKU redesign, which belongs with license management, not the desk.
- The feature is entitled and provisioned but absent: that is a support case with Microsoft, and your evidence trail is exactly what the case needs.
