---
id: rb-technician-offboarding
title: MSP technician offboarding: every tenant in an hour
level: L2
subject: msp
tags: gdap|technician leaver|cross-tenant access|secret rotation
related: gdap|lh|partner|sam-model|mspbaseline|tenantoffboard
verified: 2026-08
---

## Preconditions
- Admin rights in the MSP's own tenant over the GDAP security groups, and Partner Center rights to review relationships.
- The access model must already be group-based: GDAP roles assigned to security groups, never to individuals; if that is not true, this runbook starts with fixing that.

## Steps
1. In the MSP home tenant, block the technician's sign-in and revoke sessions; every customer access rides on this one identity, which is exactly why it goes first and fast.
2. Remove the technician from all GDAP security groups; because customer access flows through group membership, this single step severs the delegated access to every customer at once.
3. Sweep for direct assignments that bypassed the model: Partner Center GDAP relationship role assignments, Azure Lighthouse authorizations pinned to the user object, and any customer-tenant guest accounts in the technician's name; remove each.
4. Rotate what the person knew that is not personal: break-glass credentials they had sealed-envelope access to, shared automation secrets, SAM refresh tokens for tooling they operated; assume knowledge, not theft.
5. Check the technician's recent activity per customer where your logging allows: sign-ins and admin actions in the last weeks, so surprises surface now and not from a customer call.
6. Update the operational fabric: on-call rotas, escalation contacts, documentation ownership, and any customer who knew the technician by name gets the replacement contact.
7. Record completion per checklist item with timestamps; MSP offboarding evidence is what customers' auditors ask their MSP for.

## Verify
- The identity cannot sign in and holds no group memberships that map to customer access.
- A spot check on two or three customer tenants confirms the technician's access is dead and no guest object remains.
- Rotated credentials verified working for the people who should still have them.

## Rollback
- Group membership restores access in minutes if the offboarding was premature; rotated secrets stay rotated, redistribute them to authorized staff instead of rolling back.

## Escalate when
- The departure is hostile or the technician held the keys to the automation itself (SAM app ownership, pipeline admin).
- Evidence of unexpected access appears in the per-customer sweep.
- Any customer contractually requires notification of staff changes with access to their tenant.
