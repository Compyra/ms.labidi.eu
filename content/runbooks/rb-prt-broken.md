---
id: rb-prt-broken
title: Work account sign-in loop: repair the PRT
level: L2
subject: toolbox
tags: prt|sso broken|dsregcmd|sign-in loop
related: dsregcmd|wherelogs|ensign|endevices
verified: 2026-08
---

## Preconditions
- Local admin on the device helps but the first diagnostics run as the user.
- Symptom family: SSO stopped, Office apps loop on "sign in with your work account", or Conditional Access suddenly treats a joined device as unregistered.

## Steps
1. Run "dsregcmd /status" as the logged-on user and read three things: AzureAdJoined (device state), AzureAdPrt (the token this runbook is about), and the error fields under SSO state.
2. If AzureAdPrt is NO, try the cheap fix first: have the user lock and unlock, then sign out and fully sign in again; the PRT is acquired and refreshed around sign-in, so a real sign-in (not just unlock) often restores it.
3. Still NO: check the plumbing the PRT depends on. Confirm the device can reach the Microsoft sign-in endpoints without TLS inspection breaking them, the system time is correct, and no VPN or proxy blocks the out-of-box traffic before logon.
4. Read the dsregcmd diagnostics section for concrete errors, and pair it with the AAD operational event log (Event Viewer, AAD, Operational) around the sign-in time; server error codes there name the failing leg.
5. Check device health server-side: the device object in Entra must exist and be enabled; a deleted or disabled device object means the device must re-register.
6. For a hybrid-joined device whose object is gone or broken, re-registration is automatic once the cause is fixed: "dsregcmd /leave" as SYSTEM followed by a reboot and the next scheduled task run re-joins; do this only after the network and sync prerequisites are confirmed, or it re-breaks the same way.
7. If the loop is per-application while dsregcmd looks healthy, move the suspicion to the app: clear that app's token cache (for Office, signing out of all accounts in one app usually resets the shared cache) instead of re-joining the device.

## Verify
- "dsregcmd /status" shows AzureAdPrt YES after a fresh sign-in.
- The user opens an Office app or portal without an interactive prompt (SSO works).
- Conditional Access sign-in logs show the device as compliant/registered again.

## Rollback
- Nothing destructive happened unless you ran the leave/re-join path; if a re-join misfires, the device falls back to unregistered state and the fix is completing the join prerequisites, not undoing them.

## Escalate when
- Many devices lose their PRT together: look at network changes (TLS inspection, proxy) or a federation/CA change, not at individual machines.
- The device re-registers but CA still blocks: the token cache on the service side may need time, and persistent mismatch is a support case.
- TPM errors appear in the diagnostics: hardware-backed key problems are their own path and may need a TPM reset with BitLocker handled first.
