# 07 : Purview / Compliance & Data Governance

`https://purview.microsoft.com` (GCC High: `purview.microsoft.us`). One portal, two worlds:
**risk & compliance** (the old compliance center) and **unified data governance** (the old
Azure Purview, `puudg`). cmd.ms ships ~40 commands here, most with GCC-High twins to fold.

---

## 1. Solutions map (the parts)

| Solution | cmd | What the desk/SOC uses it for |
|---|---|---|
| Audit | `puaudit` | the master activity log: searches, exports, retention (180d std / 1y premium + 10y add-on) `VERIFY` |
| eDiscovery | `puedisc`, Content search `pucontentse` | legal holds, searches, exports; premium adds custodians/review sets |
| Data Loss Prevention | `pudlp` | policies across EXO/SPO/ODB/Teams/Endpoint/on-prem; alerts to Defender portal |
| Information Protection | `puinfoprot` | sensitivity labels, auto-labeling, encryption |
| Data Lifecycle Management | `pudlm` | retention policies + labels, adaptive scopes |
| Records Management | `purecmon` | declared records, disposition review |
| Insider Risk Management | `puirm` | risky-user signals, cases; feeds CA adaptive protection |
| Communication Compliance | `pucomms` | monitored channels, policy violations |
| Compliance Manager | `pucmgr` | assessments, improvement actions, score |
| Information Barriers | own | segment isolation |
| Privacy (Priva) | `puprivaprm`, `puprivasrr` | privacy risk, subject rights requests |
| App governance | `pucloudgov` | OAuth app policies (surfaced with MDCA, doc 03) |
| Data governance (unified catalog) | `puudg` | scans, classification, lineage, domains `VERIFY` new Unified Catalog naming |
| DSPM for AI | own | AI usage posture: Copilot + third-party AI prompts, oversharing findings, policies `VERIFY` portal naming |
| Data classification explorers | `puactexp`, `pucontentex`, `pusit`, `puclassifiers` | see what got labeled/found where |
| Permissions in Purview | `puperms` | Purview role groups admin |

## 2. Settings & concepts to document (the smaller parts)

- **Audit**: enable auditing (new tenants on by default), search UX (new async jobs),
  `Search-UnifiedAuditLog` PS + Graph AuditLog API `VERIFY` availability, activities cheat
  table (FileAccessed, Send, New-InboxRule, UserLoggedIn...), audit retention policies per
  record type, the "audit vs sign-in logs vs message trace: which tool when" flagship card.
- **Sensitivity labels**: scopes (files/emails/meetings/groups/sites/schematized data),
  publishing policies, mandatory labeling, auto-label (client vs service side), encryption
  (rights, co-authoring), label change justification, PDF support, and the "label applied
  but user can't open" runbook.
- **Sensitive info types**: built-ins, custom SITs (regex + keywords + confidence), EDM,
  trainable classifiers, testing a SIT (tool page record).
- **DLP**: policy structure (locations, conditions, actions, user notifications, incident
  reports), policy modes (test/test-with-tips/on), Endpoint DLP settings page (restricted
  apps, browser/domain restrictions, advanced classification), alert triage in Defender
  portal (`security.microsoft.com` DLP alerts page own record), oversharing popup for
  Teams `VERIFY`.
- **Retention**: policies vs labels precedence flowchart card (the classic exam question,
  genuinely needed at the desk), adaptive vs static scopes, principles of retention
  (longest-wins etc.), Teams/Yammer special handling, PST import service record.
- **eDiscovery**: hold vs retention distinction, search query KQL-in-Purview syntax card,
  export limits, premium workflow (custodian -> collection -> review set), the new unified
  eDiscovery UX `VERIFY`.
- **IRM**: policy templates (departing employee data theft etc.), HR connector, adaptive
  protection tiers -> Conditional Access integration (bridge doc 01).
- **Roles**: Purview role groups (Compliance Administrator, eDiscovery Manager vs
  Administrator, Records Management, Security Reader overlap card), permission model
  differences vs Entra roles.
- **DSPM for AI + Copilot readiness**: AI activity reports, oversharing assessments,
  one-click policies (block sensitive prompts to consumer AI), Copilot interaction
  audit records, pairing with SharePoint Advanced Management (doc 06 §3): the
  "make Copilot safe" bundle card.
- **Alert policies** (`security.microsoft.com/alertpoliciesv2` `VERIFY` path): default
  policies inventory, custom activity alerts, routing to email/SIEM: where "why did
  nobody get told" investigations end.

## 3. Data governance side (lighter treatment, cloud-engineer facing)

Accounts/scans/classification/lineage/glossary/domains records + Data Map pricing model
card; integration runtimes; connections to on-prem SQL; the Fabric/OneLake catalog
convergence pointer `VERIFY`.

## 4. Enrichment per record

- Path breadcrumbs within Purview portal (post-redesign paths `VERIFY` each).
- Role: least-priv Purview role group.
- License gates: E3 vs E5 compliance features table (doc 11 matrix rows: audit premium,
  auto-labeling, IRM, CC, EDM, records mgmt...).
- PS: `ExchangeOnlineManagement` compliance cmdlets (`New-ComplianceSearch`,
  `New-RetentionCompliancePolicy`...) + Security & Compliance PowerShell
  (`Connect-IPPSSession`) registry entry.

## 5. KQL/Sentinel bridges

`OfficeActivity` table field guide, Purview DLP connector for Sentinel, audit log ->
Sentinel ingestion decision card (native connector vs Graph API collection).

## 6. Runbook seeds

1. Audit search: "who deleted this file / who set this inbox rule" (L1/L2, flagship).
2. Content search + export for a leaver's mailbox (L2).
3. Place/verify/release a litigation hold (L2).
4. DLP false positive: tune conditions vs add exception, with change control (L2).
5. Sensitivity label not appearing in Office: publishing + client cache chain (L2).
6. Subject rights request end-to-end (L2).
7. Retention label not applying: precedence + timing expectations (L2).

## 7. Backlog

- Built-in SIT catalog as searchable records (100+).
- Audit activities encyclopedia (operation names per workload).
- DLP condition/predicate reference table.
