---
id: rb-bitlocker-key
title: Find a BitLocker recovery key
level: L1
subject: intune
tags: bitlocker|recovery key|encryption
related: endevices|enlaps|ps-bitlocker-keys|in-lapspolicy
verified: 2026-08
---

## Preconditions
- Cloud Device Administrator, Intune Administrator, or Helpdesk Administrator depending on the path you use.
- Verify the caller's identity before reading out a key; this is a full disk unlock.

## Steps
1. Ask the user for the key ID shown on the recovery screen: the first eight characters are enough to match.
2. Open the device in Entra devices, or in Intune device properties, and read the recovery keys section.
3. Match the key ID from the screen to the listed key, then read out the 48-digit key in blocks.
4. If the device is not listed, check whether it was ever escrowed: a device encrypted before policy applied may hold keys only locally or in on-prem AD.
5. If the user is self-service capable, point them at their own device list instead of reading the key out.

## Verify
- The user boots into Windows after entering the key.
- Confirm the device reports as encrypted and compliant after the next check-in.

## Rollback
- Nothing to roll back for a read. If the key was exposed to the wrong person, rotate it.

## Escalate when
- No key exists for a device that policy says should be encrypted: the escrow path is broken and other devices are likely affected too.
- The device is not recognised by the tenant at all, which may indicate a personal or rogue device.
