---
id: rb-offboarding
title: Offboarding: the leaver checklist in order
level: L1
subject: m365
tags: leaver|offboarding|shared mailbox|onedrive transfer|license reclaim
related: usermgmt|musers|restorematrix|ps-block-user|ps-revoke-sessions|ps-convert-shared|ps-set-autoreply|ps-intune-wipe
verified: 2026-08
---

## Preconditions
- User Administrator plus Exchange rights; SharePoint admin for the OneDrive step.
- HR's effective date and the manager's decisions: mail handling, file handover, device fate.

## Steps
1. At the agreed moment, block sign-in and revoke sessions together; the block stops new sign-ins, the revoke kills the sessions that already exist.
2. Deal with mail before touching the license: convert the mailbox to shared while the account is still licensed, then mail keeps working without a license as long as the shared mailbox stays under the size limit and needs no litigation hold.
3. Set the auto-reply and, if the manager wants it, delegate access to the shared mailbox instead of forwarding; visible delegation beats silent forwards.
4. Hand over OneDrive: grant the manager access to the leaver's OneDrive and remind them the content is retained for the configured period after deletion (30 days by default) before it is gone.
5. Transfer ownership of what the person ran: Teams they own, groups they own, Power Platform flows and connections (see the flow-owner runbook), and any app registrations in their name.
6. Wipe or retire their devices per the device runbook, matching ownership: corporate wipes, BYOD retires.
7. Now reclaim the license, remove group memberships, and after the retention decisions are confirmed, delete or keep the account per policy; deleted users are restorable for 30 days.
8. Close the loop with a checklist comment in the ticket: every step above with who did it and when, because offboarding is the audit's favorite sample.

## Verify
- Sign-in attempts fail and no active sessions remain.
- Mail to the address lands in the shared mailbox and the manager can open it.
- The license shows back in the available pool.

## Rollback
- Within 30 days a deleted user can be restored with most state; a shared mailbox converts back to a user mailbox by re-licensing. After the retention windows, rollback stops being a concept.

## Escalate when
- The leaver is under investigation or legal hold: nothing gets deleted, legal drives the plan.
- The account owns critical automation or is a global admin: plan the succession before the block.
- Termination is hostile: security does the block-and-revoke in real time with HR on the phone.
