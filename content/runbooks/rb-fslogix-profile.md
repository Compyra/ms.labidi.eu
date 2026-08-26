---
id: rb-fslogix-profile
title: FSLogix profile will not load: recover the session
level: L2
subject: windows
tags: fslogix|temp profile|avd|profile container
related: azavd|avdweb|kql-wvd-errors|kql-wvd-sessions
verified: 2026-08
---

## Preconditions
- Admin on the session hosts and read access to the profile share.
- Know the storage backing the profiles (Azure Files, file server) and where its permissions are managed.

## Steps
1. Identify the symptom class first: user lands on a temporary profile, or sign-in hangs at profile load; both start in the FSLogix Apps Operational event log on the session host the user hit.
2. Read the event around the failed logon: the log names the reason, with "cannot attach, VHD in use" (a stale lock) and access denied (permissions) covering most real cases.
3. For a lock: find where the disk is still attached. The user may have a ghost session on another host; log off that session from the host pool view. If no session exists, the file server side still holds an open handle on the VHDX; close that handle on the storage side and have the user retry.
4. For access denied: verify the user has the documented NTFS/share rights on the profile share and that nothing "fixed" permissions recently; test by creating a file as the user path allows.
5. For disk full: check both the profile share capacity and the VHDX's own size limit; expanding the share or the disk beats deleting a user's data under pressure.
6. Corruption as last resort: with the user logged off everywhere, rename the profile folder (never delete it), let FSLogix create a fresh profile on next sign-in, then copy the user's data (Documents, Desktop, browser profiles they need) from the renamed folder into the new profile.
7. If many users fail at once, stop treating it per-user: check the storage itself (throttling, connectivity from hosts, recent permission or key change) and the host pool's recent image change.

## Verify
- The user signs in and gets their normal profile, and the Operational log shows a clean attach.
- No stale sessions or open handles remain for that user.

## Rollback
- The renamed profile folder is the rollback: rename it back if the fresh-profile route was wrong. Delete it only after the user confirms nothing is missing, with a grace period.

## Escalate when
- Storage-level throttling or outage is the cause: infrastructure owns it.
- Corruption recurs for the same user or spreads across users: suspect the storage path, antivirus exclusions being wrong, or the FSLogix version.
- The user lost data that predates any rename you performed.
