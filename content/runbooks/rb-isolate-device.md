---
id: rb-isolate-device
title: Isolate a device: contain, collect, release
level: L2
subject: defender
tags: isolation|investigation package|containment|mde
related: dedevices|deactions|demdeier|scenario-incident|kql-av-detections
verified: 2026-08
---

## Preconditions
- MDE role with active remediation actions rights over the device's device group.
- A reason you can defend in the ticket: isolation is visible and disruptive to the user.

## Steps
1. Confirm you have the right machine on the device page: hostname, logged-on user, and the alert that brought you here.
2. Collect the investigation package before or right after isolating; it grabs autoruns, processes, network state and logs for later analysis while the evidence is fresh.
3. Isolate the device from the device page actions. Isolation cuts the machine off from the network while keeping the Defender channel alive, so you can keep investigating and can undo it remotely.
4. Prefer selective isolation when the user must keep limited productivity (it exempts Teams and Outlook traffic); use full isolation for anything that looks hands-on-keyboard.
5. Run an antivirus full scan from the same actions menu and review the device timeline around the alert time for what executed and what it touched.
6. Remediate what you find: quarantine files, remove persistence, and reset credentials used on the device if theft is plausible.
7. Release from isolation only when the alert story is explained and remediation is done; a device released early and re-isolated twice burns user trust.

## Verify
- The device shows healthy: no new alerts after release and a clean scan result.
- The investigation package is stored with the case notes.
- The user confirms normal network function after release.

## Rollback
- Release from isolation is the rollback, available from the same device page; releasing from the portal is the supported path, and a device that cannot be released because the console is unreachable is a Microsoft support case, not a local hack.

## Escalate when
- The timeline shows lateral movement or credential dumping: this is an incident, stop touching the device solo.
- The device is a server or shared infrastructure where isolation equals outage: get the owner and security together first.
- Ransomware indicators appear anywhere in the story.
