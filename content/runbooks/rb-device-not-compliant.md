---
id: rb-device-not-compliant
title: Device not compliant: walk the evaluation chain
level: L2
subject: intune
tags: compliance|conditional access|grace period|check-in
related: incompliance|incompsettings|in-checkin|introubleshoot|ps-intune-sync|ps-intune-noncompliant|kql-intune-noncompliant
verified: 2026-08
---

## Preconditions
- Intune read access at minimum; Conditional Access read helps when access is being blocked downstream.
- The device name or user, and the exact error the user sees.

## Steps
1. Check the last check-in time first: a device that has not talked to Intune in days is reporting stale state, so trigger a sync and wait before debugging settings.
2. Open the device's Device compliance blade and see which policy and which setting is failing; each policy lists per-setting status.
3. Cross-check the built-in "Default Device Compliance Policy" entries: if the failure is there rather than in your policy, the cause is enrollment state, not a setting.
4. If the device has no compliance policy assigned at all, the tenant-wide compliance policy setting "mark devices with no policy as" decides the result; check it in compliance policy settings.
5. For a failing setting, fix the actual condition on the device (BitLocker off, Defender off, OS below minimum), then sync and re-evaluate.
6. If the user is blocked from apps while you work, check whether the policy has a grace period: a device inside the grace window is non-compliant but not yet blocked by Conditional Access.
7. When the device is compliant in Intune but the user is still blocked, look at the Conditional Access sign-in log entry: the device state the token carries can lag a fresh compliance flip, and a new sign-in or a re-sync refreshes it.

## Verify
- The device shows compliant on its page and per-policy state agrees.
- The user gets into the app that was blocked.

## Rollback
- If you relaxed a compliance policy setting to unblock, put it back after the fleet catches up; loosened compliance silently weakens Conditional Access everywhere it is referenced.

## Escalate when
- Many devices flipped non-compliant at once: suspect a policy change or a service issue rather than device drift.
- The failing signal comes from Defender for Endpoint risk score: hand the device to security.
- Compliance state disagrees between Intune and Entra for hours: that sync problem is beyond the desk.
