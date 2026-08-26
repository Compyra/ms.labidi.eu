# 10 : Automation, Graph & PowerShell

The "do it with code" layer that every other subject's records point into via their `ps`
field. Also a standalone library: task-first snippets an engineer can paste.

---

## 1. API planes (concept cards)

- **Microsoft Graph** (`graph.microsoft.com`): v1.0 vs beta discipline, permission types
  (delegated vs application), consent, throttling basics.
- **Graph eventing**: change notifications (webhooks) + lifecycle notifications, delta
  queries for sync jobs, when polling beats subscriptions: the automation-engineer
  trio card.
- **ARM** (`management.azure.com`): Azure + Sentinel management plane.
- Workload-specific REST that refuses to die: Exchange REST (via EXO module), Defender for
  Endpoint API (`api.securitycenter.microsoft.com`), MDCA API, LA Query API
  (`api.loganalytics.io`), Fabric/Power BI REST, Partner Center API.
- Auth patterns card set: interactive delegated, device code (and why CA may block it),
  client credentials + certificate, managed identity, `az login` chains, Graph PowerShell
  app-only setup runbook.

## 2. Tool surfaces to index (kind `tool`)

| Tool | URL/install | cmd |
|---|---|---|
| Graph Explorer | `https://developer.microsoft.com/graph/graph-explorer` | `ge` |
| Graph X-Ray | browser extension + `https://graphxray.merill.net` | own |
| Azure Cloud Shell | `azshell`, `shell.azure.com` | `azshell` |
| Azure Resource Graph Explorer | portal blade | `arg` |
| Microsoft Graph changelog | `https://developer.microsoft.com/graph/changelog` | own |
| Entra Chat / Lokka / Maester (merill family, credit alongside cmd.ms) | own records | own |
| KQL playground | `https://aka.ms/lademo` demo workspace | own |
| MSAL/JWT decode helper | `https://jwt.ms` | own (flagship helpdesk tool) |
| Sign-in diagnostics | Entra portal tool | own |
| M365 connectivity test | `https://connectivity.office.com` `VERIFY` | own |
| Remote Connectivity Analyzer | `https://testconnectivity.microsoft.com` | own |
| MXToolbox-class checks | external, mark 3rd-party | own |
| IdFix (dirsync prep) | download | own |
| ORCA / Maester / MDE Client Analyzer | modules/downloads | own |

## 3. PowerShell module registry (each a record: install, connect, killer cmdlets, gotchas)

| Module | Connect | Notes |
|---|---|---|
| `Microsoft.Graph` (+ `.Beta`) | `Connect-MgGraph -Scopes ...` | select modules to avoid 38-module install card |
| `ExchangeOnlineManagement` | `Connect-ExchangeOnline`, `Connect-IPPSSession` | v3 REST, no basic auth |
| `MicrosoftTeams` | `Connect-MicrosoftTeams` | policy cmdlets |
| `PnP.PowerShell` | `Connect-PnPOnline` | requires own app reg now `VERIFY` |
| `Microsoft.Online.SharePoint.PowerShell` | `Connect-SPOService` | admin-center scope |
| `Az` (`Az.Accounts`, `Az.SecurityInsights`, `Az.OperationalInsights`...) | `Connect-AzAccount` | Sentinel mgmt via `Az.SecurityInsights` |
| `MSOnline` / `AzureAD` | RETIRED | tombstone cards pointing to Graph equivalents table |
| `Microsoft.PowerApps.Administration.PowerShell` | `Add-PowerAppsAccount` | PP admin |
| `Maester` | `Invoke-Maester` | tenant security tests |
| Entra PowerShell (`Microsoft.Entra`) | `Connect-Entra` | Graph-based successor surface for identity admin `VERIFY` module scope |
| `ADSync` (on the Connect server) | local | `Start-ADSyncSyncCycle`, sync debugging |
| `IntuneWin32App`, `WindowsAutopilotIntune` | community | doc 02 bridges |
| Azure CLI `az` + `pac` CLI + `m365` CLI (CLI for Microsoft 365, community) | | cross-platform picks |

Migration table (own mini-encyclopedia): `MSOnline/AzureAD cmdlet -> Graph cmdlet + scopes`
for the ~30 cmdlets helpdesks still google (Get-MsolUser -> Get-MgUser etc.).

## 4. Snippet library spec (phase 5)

Schema: `{id, title, lang: ps|kql|graph|cli, code, scopes/role, module, subject, tags,
verified}`; one-click copy; grouped by task not by module. Seed list (60): sixteen identity
(revoke sessions, TAP create, CA report-only analyzer, stale guests...), ten Exchange
(trace, forwarding audit, shared mailbox grant, inbox rules dump...), ten Intune (device
compliance export, BitLocker keys via Graph, stale devices...), ten Sentinel/Defender
(incident bulk close, hunting via API, indicator push...), eight SPO/Teams, six Azure
(RBAC audit, resource graph sweeps).

## 5. KQL library spec (phase 5)

Schema mirrors snippets with `table` field. Seeds (60) spread over: identity sign-in
analysis (risky sign-ins by CA gap, legacy auth hunt, impossible travel confirm), audit
(new inbox rules, mass download, role changes), endpoint (ASR hits, LOLBins, USB writes),
email (delivery action stats, ZAP events, top phished users), Sentinel ops (ingestion by
table/GB, EPS by connector, rule failure health, incident MTTR), Azure (NSG denies,
Key Vault access, break-glass usage watch).

## 6. Runbook seeds

1. Set up Graph PowerShell app-only auth with a certificate, least privilege (L3).
2. First 10 minutes in any tenant: read-only recon script pack (L2).
3. Throttling: recognizing 429s and building polite scripts (L3 concept).
4. Migrate a script off MSOnline before it dies in prod (L2).

## 7. Backlog

- Graph permission -> tasks reverse index ("what can Directory.Read.All actually do").
- Postman/HTTP examples parallel to each PS snippet.
- Scheduled-automation recipes: Azure Automation + managed identity patterns per subject.
