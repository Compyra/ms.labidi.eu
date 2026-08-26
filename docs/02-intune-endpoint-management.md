# 02 : Intune / Endpoint Management

Devices and apps: enrollment, configuration, compliance, updates, endpoint security.
Portal: `https://intune.microsoft.com` (GCC High: `https://intune.microsoft.us`).

---

## 1. Product family (the parts)

| Product | What it is | License |
|---|---|---|
| Intune (Plan 1) | core MDM/MAM | in EMS E3, M365 E3/E5, Business Premium, F1/F3 |
| Intune Plan 2 | + tunnel for MAM, firmware-over-air, specialty devices | add-on |
| Intune Suite | + Remote Help, EPM, Advanced Analytics, Enterprise App Mgmt, Cloud PKI | add-on |
| Windows Autopilot (+ Device Preparation "APv2") | zero-touch provisioning | with Intune |
| Configuration Manager (SCCM/MECM) | on-prem management, co-management | with Intune licenses |
| Windows Update for Business / Autopatch | servicing rings, driver + feature updates | E3+; Autopatch entitlements `VERIFY` |
| Endpoint analytics | startup/health/work-from-anywhere scores | included |
| Microsoft Tunnel | per-app VPN gateway (Linux) | included/Plan 2 for MAM |

## 2. Area map inside the Intune admin center (the smaller parts)

### 2.1 Devices (`indevices`)
- Platform nodes: Windows (`inwin`), iOS/iPadOS (`inios`), macOS (`inmacos`), Android
  (`inandroid`), Linux (own), ChromeOS connector (own).
- Device actions catalog (own concept card): sync, restart, wipe vs retire vs fresh start vs
  autopilot reset, remote lock, locate (supported platforms matrix), collect diagnostics,
  BitLocker key rotation, passcode reset.
- Enrollment (`inenroll`): Windows (Autopilot profiles, deployment profiles, ESP enrollment
  status page, `inap` Autopilot devices, Device Preparation policies), Apple (ABM tokens,
  ADE profiles, APNs certificate renewal!), Android (managed Google Play link, work profile
  vs fully managed vs dedicated), enrollment restrictions, device limit, corporate identifiers.
- Compliance policies (`incompliance`): per-platform settings, actions for noncompliance,
  grace periods, the CA handshake (bridge card to doc 01).
- Configuration profiles (`inconfig`): Settings Catalog (the future), templates,
  administrative templates (ADMX), custom OMA-URI, ADMX import. Own card: "settings catalog
  vs template vs GPO: which wins" + MDMWinsOverGP CSP.
- Scripts & remediations (`inscripts`, `inprorem`): platform scripts (PS/shell), Remediations
  (detect+fix pairs, license gate) `VERIFY` naming.
- Windows updates: update rings (`inwur`), feature updates (`inwfu`), driver updates
  (`inwdu`), expedite quality updates, Autopatch groups `VERIFY` merged UX.
- Group Policy analytics (own): import GPO reports, migration readiness.
- Device cleanup rules, device categories, filters (assignment filters, own record: filter
  syntax cheat card).

### 2.2 Apps (`inapps`)
- App types: Win32 (.intunewin + IntuneWinAppUtil, detection rules, requirement rules,
  supersedence, dependencies), LOB (MSI/APPX), Microsoft Store apps (winget-backed), web
  links, iOS/VPP apps + tokens, Android Managed Google Play, macOS (PKG/DMG/LOB).
- Enterprise App Management catalog (Suite) `VERIFY`.
- App configuration policies (`inappconfig`), app protection policies MAM (own record:
  APP data protection framework levels 1/2/3 cheat card).
- App install troubleshooting runbook: IME logs, error code table (0x87D...).

### 2.3 Endpoint security (`insecurity`)
- Security baselines (Windows, Edge, HoloLens, M365 apps): baseline versioning pitfalls.
- Antivirus (`inantivirus`): Defender AV policy, exclusions (link runbook "safe exclusion
  review"), tamper protection.
- Disk encryption: BitLocker policy, key escrow to Entra, recovery key retrieval paths
  (device blade + user myaccount + Graph). FileVault for macOS.
- Firewall (`infirewall`) + rules profiles.
- EDR (`inedr`): onboarding blob via Intune, bridge to MDE (doc 03).
- ASR (`inasr`): attack surface reduction rules (audit vs block, per-rule GUID cheat card),
  device control, exploit protection.
- Account protection: Windows Hello for Business, LAPS policy (bridge to Entra LAPS view),
  local admin group membership policy.
- Conditional launch / device compliance widgets.
- Security settings management for MDE-only devices (no enrollment) concept card.

### 2.4 Reports, tenant admin, troubleshooting
- Reports hub: device compliance, update compliance, app install status, endpoint analytics,
  work from anywhere.
- Tenant admin (`intenant`): tenant status, connectors and tokens health (APNs! VPP! ABM!
  certificate expiry watchlist runbook), roles + scope tags (RBAC model card), diagnostics
  settings export to LA, Intune add-ons page.
- Troubleshooting + support (`introubleshoot`): per-user troubleshooting pane.
- Windows 365 provisioning shares nodes here (bridge to doc 09).

### 2.5 Compliance: where, what and how it is enforced (deep treatment)

The full enforcement chain, every step a record:

1. **Author**: Devices > Compliance (`incompliance`), per-platform checks: min/max OS,
   password, encryption/BitLocker, AV + firewall on, TPM, jailbreak/root, **MDE machine
   risk score threshold** (requires the Intune-MDE connector, own setting record), custom
   compliance (JSON rules + discovery script, Windows/Linux).
2. **Tenant-wide switches** at Endpoint security > Device compliance > Compliance policy
   settings: **"Mark devices with no compliance policy assigned as"** (fail-open default
   Compliant; the flagship flip-to-Not-compliant record) and **"Compliance status
   validity period"** (default 30 days; stale check-in = noncompliant).
3. **Built-in Device Compliance Policy** rows every device gets (Is active, Enrolled
   user exists...) and how they confuse per-setting reports (explainer card).
4. **Actions for noncompliance** per policy: mark noncompliant immediately vs after N
   grace days (InGracePeriod still passes CA: gotcha card), notification templates +
   extra recipients, remote lock, retire, push notification; sequencing rules.
5. **Signal to Entra**: `isCompliant` on the device object, consumed by the CA grant
   **"Require device to be marked as compliant"** (+ device filters for exclusions);
   MAM fallback grant "Require app protection policy" for unenrolled BYOD.
6. **Partner compliance**: Jamf connector (macOS), device compliance partners page
   (third-party MDM attestation into Entra).
7. **Co-management**: the SCCM workloads slider decides which authority computes
   compliance; tenant-attach compliance surfaces in the Intune console.
8. **Timing**: check-in cadence table (~8h steady state, tighter right after enrollment
   and on notification-triggered sync), compliance re-evaluation triggers, and CA
   enforcing at token evaluation (CAE nuance: not instant either way): the "user fixed
   it but is still blocked" expectations card.
9. **Troubleshoot**: per-device per-setting states (Not applicable vs Not evaluated),
   conflict resolution across policies (per-setting most restrictive; noncompliant
   wins), report exports, `DeviceComplianceOrg` in Log Analytics.

### 2.6 Niche corners to index (one record minimum each)

ESP deep-dive (blocking apps, timeout behavior, skip conditions), Autopilot device
preparation (v2) vs classic, enrollment notifications, corporate device identifiers,
primary user effects + shared PC mode, kiosk/assigned access, DFCI firmware management,
Windows LAPS policy internals, EPM elevation rules + support-approved workflow, Remote
Help RBAC + deep link, organizational messages, ADMX ingestion (third-party ADMX),
OEMConfig (Android), Apple declarative device management (DDM), managed device
attestation, activation lock bypass, iOS lost mode + locate, eSIM deployment, Surface
Management Portal, certificate strategy card (SCEP vs PKCS vs Cloud PKI, NDES connector
internals), derived credentials, per-app VPN, Wi-Fi/wired 802.1x profiles, Delivery
Optimization profiles, driver update approval flow, expedite quality updates mechanics,
endpoint analytics anomaly detection + battery health, device query (on-demand KQL
against one device; multi-device query `VERIFY` license gate), tenant attach vs
co-management vs cloud-native decision card, GPO analytics -> Settings Catalog migration
path, MDMWinsOverGP behavior, IME internals (log locations, agent restart runbook),
Company Portal branding + self-service actions matrix, app supersedence + dependency
graphs, scope tag design for delegation (MSP bridge: doc 15).

## 3. Related tools to index

- `shell.intune.microsoft.com` alternative host `VERIFY`; Intune connector for AD (hybrid
  join), Certificate Connector (SCEP/PKCS/Cloud PKI), Win32 Content Prep tool download,
  Autopilot HWID capture script (`Get-WindowsAutopilotInfo`), Company Portal deep links
  (`companyportal://`), Microsoft Store winget, VPP/ABM/Play external consoles (kind `tool`).

## 4. Enrichment data per record

- Path breadcrumb (`Devices > Windows > Configuration profiles`).
- Role: Intune Administrator vs built-in Intune RBAC roles (Policy and Profile Manager,
  Help Desk Operator, Read Only Operator, Application Manager) + scope tags note.
- License gate: Plan 1 / Plan 2 / Suite / Remote Help add-on / Advanced Analytics.
- Graph equivalents: `deviceManagement/*` endpoints; PS: `Microsoft.Graph.DeviceManagement`,
  community `IntuneWin32App`, `WindowsAutopilotIntune` modules.

## 5. KQL tables (via diagnostics export)

`IntuneAuditLogs`, `IntuneOperationalLogs`, `IntuneDeviceComplianceOrg`, plus Update
Compliance/Windows Update for Business reports tables (`UCClient*`) `VERIFY` names.

## 6. Runbook seeds

1. Wipe vs retire decision + execution (L1/L2).
2. Find + rotate BitLocker recovery key (L1, three paths).
3. Device stuck "not compliant": evaluation chain triage (L2).
4. Autopilot device not appearing / profile not applying (hash, group tag, dynamic group lag) (L2).
5. Win32 app failed: IME log walk + error code lookup (L2).
6. APNs certificate expired: recovery order of operations (L2, critical).
7. Enrollment error table: 0x801c0003, 0x80180018, 0x80180014, MDM scope/license causes (L1).
8. Remote Help session flow (L1).
9. Remove a device from Autopilot cleanly (deregister vs delete order) (L2).
10. Sync loop: what "Sync" actually triggers per platform, expectations to set with users (L1).

## 7. Backlog

- ASR rule GUID -> friendly name -> recommended mode table as searchable records.
- Settings Catalog "where did the GPO setting go" mapping mini-tool.
- Intune connector/token expiry dashboard runbook (Graph script).
- Error code encyclopedia expansion (enrollment + app install + compliance).
