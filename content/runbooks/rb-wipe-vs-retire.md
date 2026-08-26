---
id: rb-wipe-vs-retire
title: Wipe or retire: pick the right device removal
level: L1
subject: intune
tags: wipe|retire|byod|offboarding device
related: indevices|inprorem|ps-intune-wipe|ps-intune-devices
verified: 2026-08
---

## Preconditions
- Intune role with remote task rights (Help Desk Operator covers wipe and retire).
- Know the ownership type before acting: corporate or personal changes the answer.

## Steps
1. Open the device in Intune and confirm you have the right one: check primary user, serial, and last check-in; wiping the wrong serial is the classic error here.
2. Personal or BYOD device where the person leaves or unenrolls: Retire. It removes company apps, profiles and data made available through Intune, and leaves personal data alone.
3. Corporate device that is lost, stolen, or holds sensitive data: Wipe. It restores factory defaults.
4. Corporate device being reassigned to another user: Wipe, and consider the option to retain the enrollment state only when you know the flow expects it; a clean start is usually safer.
5. Remember both actions need the device to check in to take effect: an offline device executes the command the next time it talks to the service.
6. For lost or stolen devices that may never check in again, wipe anyway (the command waits), and pair the action with blocking sign-in and revoking sessions for the user.
7. After the action reports complete, delete the Intune object if the device is not coming back, and clean up Autopilot registration for Windows before the hardware is sold or recycled.

## Verify
- The device action status shows complete, or pending with the device known to be offline.
- The device stops appearing as compliant/managed in Intune and, for wipe, boots to out-of-box setup.

## Rollback
- Treat both actions as irreversible the moment you issue them: a pending action that the device has not yet received can sometimes be cancelled from the device page, but never plan on it.

## Escalate when
- Legal hold or an investigation touches the device: imaging may be required before any wipe.
- The device is a shared kiosk or belongs to a pool where a wipe hits multiple users.
- Retire leaves company data behind because the app protection design was incomplete.
