# 06 : Microsoft 365 Admin & Collaboration

Tenant administration plus the collab workloads: Exchange Online, SharePoint/OneDrive,
Teams, M365 Apps, and the end-user "My Pages" surfaces the helpdesk hands out all day.

Portal churn warning: `admin.microsoft.com` and per-workload centers are consolidating under
`admin.cloud.microsoft` and `*.cloud.microsoft`; import both hosts where cmd.ms already does,
tag the old one `legacy` `VERIFY` at build time.

---

## 1. Microsoft 365 admin center (`admin`)

The smaller parts, each a record:
- Users: active users (`musers`), deleted users, guest users; license assignment
  (`adlicense`); admin role assignment view.
- Groups: M365 groups/distribution lists/mail-enabled security/shared mailbox conversions.
- Billing: subscriptions (`vlsc` new home, `macvlsc` keys), licenses, payment, invoices.
- Health: service health (`mshealth`), Message center (`mc`), network connectivity
  (own record: `connectivity test` tool `connectivity.office.com` `VERIFY`).
- Settings: org settings catalog (dozens of toggles: index the top 20 as `setting` records:
  modern auth, self-service trials, Copilot data, Sway, Forms external sharing...),
  Domains (`domains`), domain DNS records reference runbook.
- Setup page, Reports > usage, Health > windows release readiness.
- Multi-tenant: all tenants (`tenants`), multi-tenant collaboration doc pointer.
- Feature explorer / Migration manager (`mmig`).
- Edge admin surfaces: `edge`, `edgeconfig`.
- Syntex/SAM admin (`syntex`).
- Support: new service request flow + what to prepare card (doc 11 bridge).

### 1.1 Everyday user management quick actions (the L1 cheat map)

One consolidated concept record (`usermgmt`) plus one record per action, because this is
what the desk does fifty times a day. For each action: fastest portal path (M365 AC user
panel vs Entra user blade), required role (least-priv from roles.csv), and the
Graph/PS one-liner (snippet lib link).

| Action | Fastest surface | Notes for the record |
|---|---|---|
| Reset password (+ require change) | M365 AC user panel | roles matrix: helpdesk vs authadmin scope |
| Block sign-in + revoke sessions | M365 AC / Entra + `Revoke-MgUserSignInSession` | the pair belongs together; CA/CAE timing note |
| Re-register MFA / auth methods | Entra user > Authentication methods | TAP issue flow (bridge doc 01 §2.4) |
| Assign/remove licenses | M365 AC Licenses + group-based | group-based errors runbook bridge |
| Group membership + ownership | M365 AC / Entra groups | dynamic-group "why can't I add" card |
| Manager + org fields | M365 AC user panel | drives My Staff + lifecycle workflows |
| Name change (display/UPN/primary SMTP) | M365 AC + EXO aliases | dedicated runbook: what breaks (Teams cache, ODB URL stays) |
| Add/remove SMTP aliases | M365 AC user > mail | proxyAddresses vs UPN card |
| Auto-reply set by admin | M365 AC user > mail settings | also `Set-MailboxAutoReplyConfiguration` |
| Mail forwarding (user-level) | M365 AC user > mail | the 3-layer block bridge (§7.10) |
| Mailbox permissions (full access / send as / send on behalf) | M365 AC or EXO recipients | auto-mapping gotcha |
| Convert to shared mailbox | M365 AC user panel | license reclaim timing |
| OneDrive access grant + files handover | M365 AC user > OneDrive | offboarding bridge |
| Restore deleted user | M365 AC deleted users | 30-day window + what restores with it |
| Invite a guest | Entra / M365 AC | cross-tenant checklist bridge |
| Create user from template | M365 AC > user templates | own record: templates page |
| Bulk create/edit via CSV | M365 AC bulk operations + Entra bulk | size limits + UPN pitfalls |
| Delegate simple resets to managers | My Staff (`mystaff`) | setup card: staff hub policy |

Also: per-user sign-in diagnosis quick path (Entra sign-in logs filtered to user, bridge
doc 01 §2.7) and the "which role can reset whom" matrix already planned in doc 01 §5.

## 2. Exchange Online (`ex`)

- Recipients: mailboxes (shared conversion runbook), resources, contacts, groups.
- Mail flow: message trace (`exmt`) (the L1 tool: dedicated tips card on time ranges +
  detail levels), rules/transport rules (`exrules`), connectors, accepted domains,
  remote domains, enhanced filtering.
- Protection handoff card: EOP policy pages live in Defender portal (doc 03), but
  quarantine remains the shared L1 surface.
- Reports: mail flow reports (also `exmailflowrep` in Defender).
- Migration: batches (cutover/staged/remote moves), endpoint config.
- Org settings: sharing policies, add-ins/integrated apps, OWA policies, mobile device
  access (legacy quarantine), retention tags/policies (MRM vs Purview retention decision
  card, doc 07 bridge).
- **Calendaring & delegation** (top-5 desk topic): calendar permission levels + PS
  (`Set-MailboxFolderPermission`), delegate vs folder permission distinction, free/busy
  troubleshooting sequence, resource booking policies (bridge §7.7), room finder
  requirements (places/floors), "meeting updates not reaching delegate" card.
- **Message recall (cloud recall)**: how modern recall works, tenant toggle, per-message
  status report, what it cannot recall `VERIFY` current scope.
- Settings encyclopedia candidates: external forwarding controls (3 layers: EXO remote
  domain, anti-spam outbound policy, transport rule), plus-addressing, focused inbox org
  toggle, mailbox auditing (on by default nuance).
- Hybrid: HCW pointer, decommission-last-Exchange guidance card `VERIFY` current stance.
- PowerShell: `ExchangeOnlineManagement` v3 (REST), key cmdlets registry
  (`Get-Mailbox`, `Get-MessageTrace`/`Get-MessageTraceV2` `VERIFY`, `Set-CASMailbox`,
  `Get-MobileDevice`, `Search-UnifiedAuditLog` moving to Purview `VERIFY`).

## 3. SharePoint & OneDrive (`sp`, `one`)

- Sites: active sites, sharing settings (org-level external sharing matrix card:
  anyone/new+existing/existing/only-your-org, per-site override), access control
  (unmanaged devices, IP ranges, idle session sign-out), policies (retention bridge).
- OneDrive: storage defaults, sync restrictions (domain join/tenant allow), retention for
  departed users (30-365 days setting), Known Folder Move policy bridge to Intune.
- Term store, content type gallery, migration (SPMT, Migration Manager `mmig`).
- **Modern permission model card** (flagship concept): site permissions vs M365 group
  membership vs sharing links vs inheritance breaks; where "manage access" actually
  lives; why "remove from site" does not kill a link.
- **SharePoint Advanced Management (SAM)**: restricted access control (RAC), restricted
  content discovery, data access governance reports, site access reviews: the Copilot
  oversharing remediation kit (bridge doc 07 DSPM) `VERIFY` which parts fold into the
  Copilot license.
- Runbooks: restore deleted site, restore user's OneDrive after offboarding, sharing
  link audit, "who has access" review, storage quota bump.
- PowerShell: `Microsoft.Online.SharePoint.PowerShell` vs `PnP.PowerShell` (registry).

## 4. Teams (`teams`)

- Users, teams list, team policies, update policies.
- Meetings: meeting policies (recording/transcription toggles: setting records), live
  events, audio conferencing, Places/rooms (`places`, `teamsrooms`).
- Messaging policies, app permission + setup policies (app governance for Teams apps),
  external access (federation) vs guest access distinction card (perennial confusion:
  flagship concept card), voice (calling plans/direct routing/operator connect pointer
  cards, emergency addresses), policy packages, Advisor for Teams.
- Call quality dashboard + per-user call analytics (L1 triage runbook).
- Teams web (`teamsweb`), Yammer/Viva Engage admin (`yam`).
- PowerShell: `MicrosoftTeams` module registry entry.

## 5. M365 Apps & other workloads

- Apps admin center (`m365apps`): servicing profiles, inventory, security policy advisor,
  cloud update `VERIFY` current features; OCT (`oct`); update channels cheat table
  (Current/MEC/SAC naming history card).
- Planner (`planner`), Forms (`forms`), Loop (`loop`) admin toggles (Loop = Cloud Policy
  service setting record), Bookings org settings, Viva suite admin pointers (Insights
  `cpd`, Engage, Learning, Connections), Stream (on SPO), Whiteboard settings.
- Copilot for M365: admin page in M365 AC (own record), Copilot dashboard (`cpd`),
  readiness/licensing card (doc 11 bridge), `cp` end-user surface, **agent governance**
  (agent inventory, who can build/share, blocked agents) `VERIFY` current admin surfaces.
- **Microsoft 365 Backup** (Syntex-billed): enable, backup policies per workload
  (EXO/SPO/ODB), restore points + fast restore, billing meters; positioning vs retention
  vs recycle bins.
- **Restore & recovery matrix** (flagship concept record): object -> window -> tool.
  Mail item (Recoverable Items 14-30d + single item recovery) / mailbox (soft-deleted
  30d) / SPO-ODB item (93d two-stage recycle) / site (93d) / OneDrive of leaver
  (retention setting 30-365d) / Teams chat-channel (retention rules) / group-team
  (soft-deleted 30d) / user (30d) / M365 Backup restore points where enabled. Every
  cell links its runbook.
- School Data Sync (`sds`), Lifecycle Services (`lcs`) pointer, Dynamics admin pointer
  (kept minimal per audience; full Dynamics is out of scope v1).

## 6. My Pages (end-user surfaces the helpdesk shares)

All ten cmd.ms `My Pages` entries import as kind `enduser` with an extra field
`shareText`: a one-line instruction agents can paste to users. Examples:
- `mymfa`: "Go to https://mysignins.microsoft.com/security-info to manage your MFA methods."
- `mypw`: SSPR portal; runbook bridge "user cannot SSPR: check registration + policy".
- `myaccess`, `myapps`, `myaccount`, `mygroups`, `mystaff`, `mysubscriptions`, `myvs`.
- Own additions: `aka.ms/mfasetup` (the classic), `outlook.office.com/mail`,
  `portal.office.com` vs `m365.cloud.microsoft` note, `aka.ms/ssprsetup` legacy.

## 7. Runbook seeds

1. Message trace end-to-end: user says "mail not arriving" (L1, flagship).
2. Shared mailbox: create + grant + map in Outlook, and the auto-mapping gotcha (L1).
3. Restore deleted user + mailbox + OneDrive within/after 30 days (L2).
4. External sharing broken for one partner: SPO + Entra cross-tenant + Teams federation
   triage order (L2).
5. Offboarding checklist: block sign-in, revoke sessions, convert mailbox, OneDrive
   transfer, license reclaim, device wipe decision (L1/L2, flagship).
6. Teams call quality complaint triage (L1).
7. "Room calendar not booking" resource mailbox checks (L1).
8. DNS records for a new domain: the required-records table (L2).
9. Litigation hold vs retention policy quick decision (bridge doc 07) (L2).
10. Forwarding not working / silently blocked: the three-layer check (L2).
11. Name change end-to-end: display name, UPN, primary SMTP, and what breaks after
    (Teams cache, OneDrive URL persistence, calendar delegates) (L1/L2).

## 8. Backlog

- Org settings encyclopedia (all ~60 toggles in M365 AC > Settings > Org settings).
- Message trace status/detail code table.
- NDR code encyclopedia (5.1.x, 5.4.x, 5.7.x families) as searchable records.
- Update channel/version history quick reference (link out, do not mirror).
