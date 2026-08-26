---
id: rb-name-change
title: Name change: rename everywhere, know what breaks
level: L1
subject: m365
tags: rename|upn change|primary smtp|display name
related: musers|enusers|usermgmt|teamscache
verified: 2026-08
---

## Preconditions
- User Administrator plus Exchange rights for the SMTP part.
- For hybrid identities the change happens in on-prem AD and syncs; doing it cloud-side gets overwritten.

## Steps
1. Change the display name, the UPN, and the primary SMTP address together in one pass; half-renamed accounts confuse everyone for weeks.
2. Keep the old SMTP address as an alias so mail to the old name keeps arriving forever; never delete the old address during the rename.
3. Tell the user their sign-in changes to the new UPN everywhere, and that mobile mail profiles and desktop apps may each ask for a fresh sign-in once.
4. Set expectations on what lags or persists: colleagues' Outlook may keep suggesting the old name from their local nickname cache, Teams can show the old display name until its cache refreshes (clearing the Teams cache is the fix), and the OneDrive URL keeps the old name because it does not change on rename.
5. Check the aftermath spots that commonly snag: calendar delegations still work (they follow the mailbox, not the name), shared mailbox and Send As grants remain, and any scripts or integrations pinned to the old UPN need updating.
6. If the person is also changing legal identity, ask HR which surfaces matter most and prioritize those; a rename is often emotionally loaded, so leftover old names are not a cosmetic bug to the person involved.

## Verify
- Sign-in with the new UPN works on a fresh session.
- Test mail to both old and new addresses lands in the mailbox.
- The GAL, Teams and SharePoint show the new display name after caches settle.

## Rollback
- All three changes reverse the same way they were made; addresses kept as aliases make the reversal lossless.

## Escalate when
- The OneDrive URL containing the old name is a real problem for the user: a OneDrive re-provision/migration is a project decision, not part of the standard rename.
- The rename hits a hybrid identity mid-migration or an account used as a service identity.
