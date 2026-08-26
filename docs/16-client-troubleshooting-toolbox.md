# 16 : Client & Field Troubleshooting Toolbox

The missing half of every portal-first reference: what to run **on the device** when the
portal says fine but the user is broken. New subject slug: `toolbox` (14th hub). Records
here are mostly kind `tool`/`concept` with commands, log paths and decision flows; they
pair with the portal records via `related[]`. Offline PWA value peaks here (field work).

---

## 1. Windows identity & enrollment diagnostics

- **`dsregcmd /status` field guide** (flagship record): what AzureAdJoined /
  DomainJoined / EnterpriseJoined combos mean, `AzureAdPrt: YES/NO` (+ PRT expiry,
  update time), `WamDefaultSet`, `NgcSet` (Hello), TenantId/DeviceId sanity, the
  SSO state block; a decision table from symptom -> field -> fix.
- **PRT troubleshooting flow**: lock/unlock refresh, network/time prerequisites,
  `dsregcmd /refreshprt` `VERIFY` availability, when to leave/rejoin vs never-do-that.
- **MDM diagnostics**: `mdmdiagnosticstool.exe -area DeviceEnrollment;DeviceProvisioning;
  Autopilot;Tpm -zip`, reading MDMDiagReport.html, registry enrollment state keys.
- **Event Viewer channel map** (record per channel): DeviceManagement-Enterprise-
  Diagnostics-Provider/Admin, AAD/Operational, User Device Registration/Admin,
  Shell-Core (kiosk), BitLocker-API.
- **Intune agent logs**: IME logs path (`%ProgramData%\Microsoft\IntuneManagementExtension
  \Logs`), AgentExecutor, Win32 app install decoding, IME service restart runbook,
  Company Portal logs collection, `Collect diagnostics` remote action contents map
  (what lands in the zip, so you stop RDPing in).
- **Autopilot diagnostics**: ESP troubleshooting page, `Get-AutopilotDiagnostics`
  (community), HWID re-capture, white-glove/pre-provisioning failure codes.
- **Kerberos/AD side**: `klist` tickets + cloud Kerberos TGT check, time skew card
  (auth's silent killer), `whoami /upn /groups`, `gpresult -h` vs Settings Catalog
  reality check.
- **TPM & hardware**: `tpm.msc`, `Get-Tpm`, attestation-ready check for Autopilot
  self-deploy, Secure Boot confirm (`Confirm-SecureBootUEFI`).
- **WAM/token cache repair**: symptom map (AADSTS on one app only, "connected to
  Windows" loops), safe reset order (sign out > Access work or school re-add >
  TokenBroker cache), what never to delete first.

## 2. Office / Outlook client

- **SaRA / Get Help successor** `VERIFY` current tool + enterprise silent scenarios;
  what each scenario actually fixes.
- Outlook triage ladder (record with the order): new profile > `/safe` > disable
  add-ins > OST rebuild > search index rebuild; when each rung applies.
- **Test Email AutoConfiguration** (Ctrl+right-click tray icon), Autodiscover v2
  expectations, "keeps prompting for credentials" flow (WAM vs basic vs proxy).
- Shared mailbox automapping mechanics + disable procedure; delegate vs permission
  reality card; "send as delay" expectation setting.
- New Outlook vs classic differences that hit support (PST, COM add-ins, shared
  mailbox behavior) `VERIFY` current parity table pointer.
- **Activation & servicing**: vNext license check (`Account` page states), C2R repair
  (quick vs online), update channel verify + set, grace/reduced functionality states.

## 3. Teams client

- New Teams cache clear procedure (per-OS paths) + when it actually helps (rare).
- Diagnostic logs hotkey (Ctrl+Alt+Shift+1) + media logs location; the Test Call.
- Presence stuck triage sequence; policy propagation delay expectations (hours card).
- Sign-in on shared/kiosk PCs, multiple-account rules, VDI note (bridge doc 09 Teams
  on AVD optimization).

## 4. OneDrive sync

- `onedrive.exe /reset` per-install-type paths; when reset loses nothing (and the one
  case it does).
- Sync state icon table; Files On-Demand attrib states (`attrib` P/U flags).
- KFM verification (regkeys + gpo/Intune policy ids), "sync pending forever" triage
  (blocked types, path length, lock files), library sync limits card.

## 5. Browser & auth debugging

- `jwt.ms` decode walkthrough (aud/iss/scp/roles claims for support cases).
- Entra sign-in diagnostic tool + how to read CA evaluation results; correlation ID
  capture for tickets (bridge doc 11 support artifacts).
- HAR capture how-to per browser (+ scrubbing warning card), MSAL/browser cache clear
  matrix, InPrivate as isolation test, TLS-inspection symptom card, clock skew.

## 6. macOS

- Company Portal + Intune agent log paths, sysdiagnose pointer, enrollment profile
  verification (System Settings > Profiles), secure token / bootstrap token concept
  card, Platform SSO state + troubleshooting basics `VERIFY` maturity.

## 7. Mobile (Android/iOS)

- Android: work profile creation failures (OEM quirks), Company Portal update-first
  rule, Google services dependency card.
- iOS/iPadOS: enrollment profile check path, activation lock surprises, Authenticator
  as broker ("this app was blocked" flows), number matching UX questions.

## 8. Network field tests

- `Test-NetConnection` recipe set (443 to login/graph/outlook, UDP note), Teams media
  UDP 3478-3481 verify, `connectivity.office.com` full test, traceroute expectation
  card, captive portal detection, VPN split-tunnel recommendation card (Teams/W365
  media out of tunnel), M365 endpoint categories concept (Optimize/Allow/Default) +
  `endpoints.office.com` API record (bridge doc 11 §3).

## 9. Master quick tables (two flagship records)

1. **"Where are the logs"**: product -> client log path/command -> what to grep.
2. **"Which command answers what"**: symptom -> one command -> field to read
   (dsregcmd, klist, mdmdiagnostics, Get-Tpm, tnc, whoami, gpresult...).

## 10. Runbook seeds

1. PRT broken / "sign in with work account" loop repair (L2, flagship).
2. Outlook keeps prompting for credentials (L1/L2, flagship).
3. OneDrive stuck syncing: the 10-minute ladder (L1).
4. Teams cannot sign in on a shared device (L1).
5. Autopilot pre-provisioning failed at ESP: read the diagnostics zip (L2).
6. Office deactivated / grace period: license path check end-to-end (L1).
7. "Slow everything" on one device: auth + proxy + DNS field isolation (L2).

## 11. Backlog

- Error-string index for client dialogs (exact dialog text -> record).
- Per-OEM Android quirk table.
- Localized client path variants (paths differ on non-EN Windows installs).
