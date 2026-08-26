# 03 : Defender XDR

The unified SOC portal: `https://security.microsoft.com` (GCC High: `security.microsoft.us`).
Covers Defender for Endpoint (MDE), Office 365 (MDO), Identity (MDI), Cloud Apps (MDCA),
Vulnerability Management (MDVM), Threat Intelligence (MDTI), Exposure Management, and hosts
the unified Sentinel experience (doc 04).

---

## 1. Product family (the parts)

| Product | Protects | Plans |
|---|---|---|
| Defender for Endpoint (MDE) | Windows/macOS/Linux/Android/iOS devices | P1 (E3), P2 (E5), Business (Bus. Premium) |
| Defender for Office 365 (MDO) | Exchange/Teams/SPO/ODB mail & collab | P1, P2 (E5) |
| Defender for Identity (MDI) | on-prem AD / ADFS / ADCS signals | EMS E5 / E5 Security |
| Defender for Cloud Apps (MDCA) | SaaS discovery, OAuth apps, session control | E5 / standalone |
| Defender Vulnerability Management (MDVM) | vuln + secure config assessment | core in P2, standalone/add-on full |
| Defender Threat Intelligence (MDTI) | TI articles, intel profiles, IOC data | free tier + premium `VERIFY` post-unification |
| Security Exposure Management | attack surface, attack paths, initiatives | E5-ish gating `VERIFY` |
| Defender for Business | SMB bundle of MDE | Business Premium |
| Defender for Cloud | Azure/multicloud workloads (lives in Azure portal, `azdefender`) | Azure meters, doc 05 |

## 2. Portal area map (the smaller parts)

### 2.1 Investigation & response core
- Incidents (`deincidents`) + alerts, incident queue tuning tips card.
- Advanced hunting (`dehunting`): KQL over XDR tables, custom detections, functions,
  query resource quota report (`derepquery`), bookmark/export.
- Action center (`deactions`): pending + history (approve AIR actions).
- Automated investigations (`deinvestigations`).
- Threat explorer / real-time detections (`deexplorer`) (MDO P2/P1).
- Threat intelligence (`deti`): intel explorer, intel profiles, threat analytics reports
  (own record `dethreatanalytics`, `/threatanalytics3`).
- Secure Score (`dess`) + recommended actions workflow.
- Exposure management (own records): attack surface map, attack paths, critical assets,
  initiatives, metrics.
- Restricted entities (`dere`): unblock user/app runbook.
- Submissions (own record `/reportsubmission`): user reported, admin submissions (email,
  URL, file), result interpretation runbook.
- Quarantine (`deqre`) + quarantine policies (`deqp`): release flows, end-user spam
  notifications.

### 2.2 Assets & identities
- Device inventory (`dedevices`): onboarding state, exposure, tags, device groups.
- Identities (`deusers`): MDI-enriched identity pages, lateral movement paths.
- Cloud app catalog (`decacat`), OAuth apps (`decaoauth`), app governance
  (bridge: lives under Purview cmd `pucloudgov` `VERIFY` actual home is Defender portal).

### 2.3 Email & collaboration (MDO)
- Threat policies hub (`detp`): preset security policies (Standard/Strict), configuration
  analyzer, anti-phishing (`deap`), anti-spam (`deasp`), anti-malware (`deamp`),
  safe attachments (`desap`), safe links (`deslp`), tenant allow/block list (`detallow`),
  quarantine policies, advanced delivery (SecOps mailboxes + phishing sim exceptions, own
  record), enhanced filtering note.
- Email authentication: DKIM (`dedkim`), plus own records for SPF/DMARC guidance pages,
  ARC sealing config.
- Attack simulation training (`deast`, `deastrep`): payloads, automations, training.
- Exchange mail flow reports in Defender (`exmailflowrep`).
- Campaigns, threat trackers (P2, own records).

### 2.4 Reports hub (imported set is rich already)
`dereport` (hub), `desecreport`, `devulnreport`, `deasrreport`, `dedevcontrol`,
`dedevhealth`, `defwreport`, `demonsum`, `dewebprotect`, `deemailcoll`, `deschedules`,
`dedwnrep`, `demcasreports`, `deidrepmgmt`.

### 2.5 Settings pages (`desettings` and children)

This is the same "settings encyclopedia" treatment Sentinel gets. Known deep links from
cmd.ms (all under `security.microsoft.com/securitysettings/`):

| Area | Page | cmd |
|---|---|---|
| Endpoints | landing | `demdesettings` |
| Endpoints | Advanced features (the big toggle wall) | `demdeadvfeats` |
| Endpoints | Licenses | `demdelicenses` |
| Endpoints | Email notifications: alerts / vulns | `demdemailalerts`, `demdemailvulns` |
| Endpoints | Roles (legacy MDE RBAC) | `demderoles` |
| Endpoints | Device groups | `demdedevgrps` |
| Endpoints | Indicators: files/IPs/URLs/certs | `demdetifiles`, `demdetiip`, `demdetiurls`, `demdeticerts` |
| Endpoints | Isolation exclusions | `demdeier` |
| Endpoints | Process memory indicators | `demdepmi` |
| Endpoints | Web content filtering | `demdewcf` |
| Endpoints | Automation uploads / folder exclusions | `demdeau`, `demdeafe` |
| Endpoints | Security settings management (MDE-managed) | `demdessm` |
| Endpoints | Intune permissions | `demdeinperms` |
| Endpoints | Onboarding / Offboarding | `demdeonboard`, `demdeoffboard` |
| Endpoints | Library management | `demdelibrary` |

Own additions to document (settings encyclopedia phase 4):
- Microsoft Defender XDR settings: unified RBAC (roles + permission groups), alert service
  settings, email notifications, streaming API (event hub/storage export!), alert tuning
  (suppression successor), critical asset management, preview features toggle.
- Identities (MDI) settings: sensors install + health, directory service accounts, entity
  tags (honeytoken/sensitive), exclusions, action accounts, notifications.
- Cloud apps settings: information protection, connected apps (app connectors), Cloud
  Discovery (log collectors, snapshot reports), session controls / Conditional Access App
  Control, IP ranges + tags.
- Email & collaboration settings: user reported settings page, priority accounts.
- Device discovery settings (standard vs basic, exclusions, Corelight `VERIFY`).
- Tenant allow/block list expiry behavior.
- Endpoint advanced features full toggle table: each toggle documented (live response,
  tamper protection, EDR in block mode, automatically resolve alerts, custom network
  indicators, ...): each becomes a `setting` record.

### 2.6 Niche corners (records to add; several answer direct license questions)

- **AIR, Automated investigation and response**: own concept record `air` (keywords:
  air, automated investigation, self-healing) distinguishing email AIR (MDO P2:
  `deinvestigations`, `deactions`) from device AIR (MDE P2 automation levels). License
  fields set so searching "air" surfaces it with the MDO P2 gate visible: this is a
  named acceptance test (roadmap phase 3).
- Automation levels per device group (Full / Semi / No automation): setting records.
- **Exclusions hierarchy card**: AV exclusions vs ASR per-rule exclusions vs indicators
  (allow) vs automation folder exclusions vs isolation exclusions: which layer acts
  where, and the audit path for each.
- Automatic attack disruption (contain user/device): prerequisites, exclusion settings.
- Deception (decoys + lures) `VERIFY` GA state + licensing.
- Device control: removable storage policies, printer protection (Intune + MDE
  security settings management surfaces).
- Network protection + web protection + SmartScreen relationship card; controlled
  folder access.
- Live response niche: unsigned script toggle, library management, role gates.
- Custom detection rules: schedules, actions, management page.
- MDO niche: priority account protection, campaigns, threat trackers, advanced delivery
  (SecOps mailbox + phishing simulation), enhanced filtering for connectors, ARC
  trusted sealers, email entity page anatomy.
- MDI niche: classic sensor vs unified agent `VERIFY`, action accounts (gMSA),
  honeytoken entity tags, ADFS/ADCS sensor coverage, ITDR dashboard.
- MDCA niche: session policies (Conditional Access App Control) deployment checklist,
  access policies, file policies, per-SaaS app connectors, Cloud Discovery log
  collector on-prem.
- Multi-tenant XDR (MTO) view for MSPs: bridge to doc 15 §4.

### 2.7 Scenario location maps (concept records tying the portals together)

The answer to "where do I follow up on X": one `concept` record per scenario whose card
lists every location in working order, each row linking an existing record.

**`scenario-phishing`: a phishing mail was reported/suspected**

| Order | Location | What you do there | Record |
|---|---|---|---|
| 1 | User reported tab (Submissions) | see the report, grade it | own (`/reportsubmission` user tab) |
| 2 | Email entity page | verdict, detonation, headers | own (§2.6) |
| 3 | Threat Explorer / RTD | find all recipients of the campaign | `deexplorer` |
| 4 | Advanced hunting (`EmailEvents`, `EmailUrlInfo`, `UrlClickEvents`) | blast-radius query | `dehunting` + KQL lib |
| 5 | Action center | approve purge / soft delete | `deactions` |
| 6 | Quarantine | release false positives / verify catches | `deqre` |
| 7 | TABL | block sender/URL/domain | `detallow` |
| 8 | Admin submission | report to Microsoft, track verdict | own |
| 9 | Message trace (EXO) | delivery path when Explorer isn't enough | `exmt` |
| 10 | Campaigns + Threat analytics | is it a known wave | own + own |
| 11 | Anti-phish/spam/safe-links policies | close the gap that let it in | `deap` `deasp` `deslp` |
| 12 | Attack simulation training | assign training to clickers | `deast` |
| 13 | Purview audit | post-click activity (inbox rules, mass reads) | `puaudit` |
| 14 | Entra sign-in logs + risky users | did credentials get used | `ensign` `enidp` |
| 15 | MDCA OAuth apps | consent-phishing grants | `decaoauth` |
| 16 | Sentinel incident | correlation + automation trail | doc 04 §5 |

**`scenario-compromise`: account compromise / BEC confirmed** (containment order):
block sign-in + revoke sessions + reset password (doc 06 §1.1 pair) -> re-register MFA
+ revoke refresh tokens -> hunt inbox rules + forwarding (`New-InboxRule` audit) ->
message trace what was sent -> risky user dismiss/confirm -> device check (MDE) ->
notify + case notes. Ships as runbook 11 below plus the concept card.

**`scenario-incident`: any XDR/Sentinel incident follow-up**: incidents queue
(`deincidents`) -> incident page tabs -> action center pending approvals -> AIR
investigations (`deinvestigations`) -> advanced hunting pivot -> Sentinel incident
tasks/automation (doc 04) -> post-incident: alert tuning, secure score action, report.

## 3. MDE operational surfaces to index (own records)

- Onboarding packages per platform + MDE Client Analyzer download.
- Live response console + library.
- Device timeline, flight recorder.
- Evaluation lab status (retired?) `VERIFY`.
- Troubleshooting mode (tamper-protected devices) concept card.
- `https://aka.ms/mdatpservicehealth` style aka links collection.

## 4. Enrichment per record

- Role: map to unified RBAC permission (e.g. "Authorization and settings / Security settings")
  and legacy fallback role.
- License gate per plan table above.
- API/PS: `Microsoft.Graph.Security` (incidents, alerts v2, advanced hunting
  `Start-MgSecurityHuntingQuery`), MDE API (machines, isolate, live response), ExO
  cmdlets for MDO policies (`Set-AntiPhishPolicy`, `Set-HostedContentFilterPolicy`, ...).

## 5. KQL tables (XDR advanced hunting)

Device*: `DeviceInfo`, `DeviceEvents`, `DeviceProcessEvents`, `DeviceNetworkEvents`,
`DeviceFileEvents`, `DeviceRegistryEvents`, `DeviceLogonEvents`, `DeviceImageLoadEvents`,
`DeviceTvm*` (vuln). Email*: `EmailEvents`, `EmailAttachmentInfo`, `EmailUrlInfo`,
`EmailPostDeliveryEvents`, `UrlClickEvents`. Identity*: `IdentityLogonEvents`,
`IdentityQueryEvents`, `IdentityDirectoryEvents`. Apps: `CloudAppEvents`, `OAuthAppInfo`.
Alerts: `AlertInfo`, `AlertEvidence`. Exposure: `ExposureGraphNodes/Edges`.

## 6. Runbook seeds

1. Phishing report triage: submission -> explorer -> purge (soft delete) -> block sender/URL (L1/L2).
2. Release from quarantine safely + when not to (L1).
3. Isolate device + collect investigation package + release (L2).
4. User restricted from sending email: unblock + root cause (L1).
5. False positive file: indicator allow + submission to Microsoft (L2).
6. Onboard a server vs client to MDE (paths differ) (L2).
7. Tune a noisy alert with alert tuning rules (L2).
8. ZAP explained: what it undid and where to see it (L1 concept).
9. Full-access OAuth app found: app governance response (L2).
10. Monthly secure score review workflow (L2).
11. Account compromise / BEC containment end-to-end (per §2.7 scenario-compromise;
    MSP cross-tenant variant in doc 15 §7.6) (L2, flagship).

## 7. Backlog

- Advanced-features toggle encyclopedia (every switch, default, blast radius).
- Streaming API setup guide (XDR -> Event Hub -> Sentinel/data lake decision tree).
- MDI sensor health error table.
- MDO preset policy diff viewer (Standard vs Strict as data).
