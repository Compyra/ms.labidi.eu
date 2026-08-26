# 04 : Microsoft Sentinel (flagship deep-dive)

The brief's acceptance test lives here: **"if someone needs a specific Sentinel setting,
they will be able to find it."** So this doc maps Sentinel to the setting level; every bullet
below becomes at least one searchable record (kind `portal` when a deep link exists, kind
`setting` with a documented click-path when it does not).

Where Sentinel lives in 2026: the **Defender portal** (`security.microsoft.com`) is the
primary experience; the Azure-portal experience was retired for most tenants (July 2026)
`VERIFY`. Management-plane objects (workspace, pricing, RBAC, DCRs) are still ARM resources
managed from the Azure portal / CLI. Both surfaces get records, tagged accordingly.

cmd.ms only carries five Sentinel entries (`azsentinel`, `azsentinelg`, `xdrthreathunt`,
`xdranalytics`, `xdrwatchlist`), so nearly everything below is our own content: this is the
site's main value-add.

---

## 1. Concept model (cards to write)

- Sentinel = SIEM + SOAR on top of a **Log Analytics workspace**; ingestion, retention and
  table plans are Azure Monitor concepts with Sentinel pricing on top.
- Unified SOC: Sentinel incidents + XDR incidents correlate into one queue in the Defender
  portal once the workspace is onboarded.
- Data tiers: Analytics tier vs Data Lake tier (and the older Basic/Auxiliary table plans)
  `VERIFY` current naming; total-cost mental model.
- Two APIs: ARM (`Microsoft.OperationalInsights` + `Microsoft.SecurityInsights`) for
  management, Log Analytics query API for data.

## 2. Onboarding & workspace management

| Item | Where | Notes |
|---|---|---|
| Create LA workspace | Azure portal > Log Analytics workspaces | region matters (data residency + cost) |
| Enable Sentinel on workspace | Azure portal `azsentinel` / Defender portal onboarding | first workspace onboarding wizard in Defender portal |
| Connect workspace to Defender portal | Defender portal > System > Settings > Microsoft Sentinel `VERIFY` path | primary/secondary workspace concept (multi-workspace) |
| Workspace manager (MSSP multi-workspace) | content distribution to member workspaces | `VERIFY` status post-unification |
| Azure Lighthouse for MSSP access | Azure portal | cross-tenant Sentinel ops |
| Disconnect/offboard Sentinel | Settings > remove Sentinel from workspace | order of operations runbook |

## 3. Data collection (connectors, DCRs, ingestion)

### 3.1 Data connectors page
Records for the connector gallery itself plus one record per high-traffic connector:
- **First-party**: Entra ID (SigninLogs, AuditLogs, + NonInteractive/SP/MI/Provisioning/
  RiskEvents tables: each toggle documented), Microsoft 365 (OfficeActivity: Exchange/
  SharePoint/Teams toggles), Defender XDR connector (incidents + raw events tables selection,
  alerts-only vs full telemetry cost warning), MDE/MDO/MDI/MDCA legacy single connectors
  (superseded by XDR connector card), Azure Activity (via Azure Policy assignment),
  Defender for Cloud, Purview Information Protection, Entra ID Protection, Threat
  Intelligence (upload API / TAXII / defender TI), Windows Security Events via AMA
  (all vs common vs minimal vs custom event sets), Windows DNS via AMA, Syslog via AMA,
  CEF/CommonSecurityLog via AMA (facility + DCR gotcha: dedupe with Syslog), custom logs
  via AMA (text/JSON), Logstash/Cribl patterns (concept), codeless connector platform.
- **Deprecations**: MMA/OMS agent retired, HTTP Data Collector API superseded by Logs
  Ingestion API + DCE (cards so people stop following old blogs).
- Content-hub note: connectors install with solutions now; "connector missing? install the
  solution first" tip card.

### 3.2 Data collection rules (DCRs)
- DCR anatomy (streams, transformations KQL, destinations), workspace transformation DCR,
  ingestion-time transformations (project-away cost trimming recipe), DCE when needed.
- AMA agent install paths: Azure VM extension, Arc for on-prem, client OS (AMA on Windows
  client via installer) `VERIFY`.

### 3.3 Ingestion cost control (the questions every engineer asks)
- Commitment tiers vs PAYG; Defender E5 data grant (5 MB/user/day, which data types qualify);
  free data sources list (SentinelHealth, SecurityAlert, ...) `VERIFY` current list.
- Table-plan switching (Analytics vs Basic/Auxiliary vs Data Lake), interactive vs long-term
  retention per table, `Usage` table queries for who-costs-what (KQL library entries),
  workspace daily cap and its risks (security data loss), benefit: P2 grant stacking.

## 4. Analytics (detections)

- Rule types, each a card: **Scheduled** (KQL, frequency vs lookback, event grouping, alert
  grouping, suppression), **NRT**, **Fusion** (ML multi-stage, config = enable/disable +
  source signals), **Microsoft security** (promote alerts from MDx products, filter by
  severity/name), **ML behavior analytics** (SSH/RDP anomalous login), **Anomalies**
  (UEBA-powered, customizable thresholds in some), **Threat intelligence** (TI map rules).
- Rule management: templates vs active rules (content hub versioning), duplicate-then-tune
  workflow, enable/disable/bulk operations, export to ARM, analytics rule wizard fields
  explained (entity mapping!, custom details, alert details override, incident settings tab,
  automated response tab).
- Entity mapping deep card: why unmapped rules make bad incidents; the 10-entity/alert cap.
- MITRE ATT&CK coverage view (own record): where, how coverage is computed.
- Scheduled rule quota + query limits (10k results cap etc.) troubleshooting card.
- **Summary rules** (aggregate high-volume logs into summary tables) `VERIFY` GA state.

## 5. Incidents & investigation

- Incident page anatomy: entities, similar incidents, activity log, tasks (incident tasks
  via automation), owner/status/severity/classification taxonomy (TP/BP/FP with sub-reasons:
  these exact enums become a cheat card because closing reasons feed reporting).
- Investigation graph (classic), new unified incident experience in Defender portal.
- Advanced hunting from incident, "run playbook on incident" surface, add-to-threat-intel
  from entities, bookmarks -> incident promotion.
- SOC optimization page (recommendations engine): what it changes, how to action.
- Incident retention: 90 days SecurityIncident table note, export patterns for metrics
  (KQL library: MTTR query).

## 6. Hunting, notebooks, watchlists

- Hunting hub (`xdrthreathunt`): hunts (hypothesis workflow), queries gallery, bookmarks,
  livestream.
- Custom hunting queries: save, tag with tactics, promote to analytics rule runbook.
- Notebooks: Azure ML compute attach, MSTICPy, when notebooks beat workbooks (concept card).
- Watchlists (`xdrwatchlist`): create from CSV (size limits), watchlist templates (VIP users,
  terminated employees, service accounts, network mapping), `_GetWatchlist('x')` usage
  snippet, large watchlist via SAS upload, watchlist as allowlist-in-rules pattern.

## 7. Threat intelligence

- TI management page: indicators (STIX objects now: indicator/threat actor/relationship)
  `VERIFY` object model, manual indicator add, bulk upload (flat file), relationships graph.
- Ingest paths: **Upload API** (new, via Graph-adjacent endpoint `VERIFY`), **TAXII 2.x
  connector** (collections config), **MDTI connector** (free curated feed), premium feeds.
- Matching analytics rule (Microsoft TI matching), `ThreatIntelligenceIndicator` table vs new
  `ThreatIntelIndicators`/`ThreatIntelObjects` tables migration `VERIFY` (KQL differs, big
  gotcha card).
- IOC lifecycle: expiration, confidence, source dedupe.

## 8. Automation (SOAR)

- **Automation rules**: triggers (incident created/updated, alert created), conditions
  (analytics rule name, entities, severity...), actions (assign, tag, status, severity,
  run playbook, add task), order + "and stop processing" semantics, expiry (great for
  maintenance windows runbook).
- **Playbooks** = Logic Apps: Standard vs Consumption decision card, Sentinel trigger types
  (incident/alert/entity), managed identity auth to Sentinel (assign **Microsoft Sentinel
  Responder** to the Logic App MI), API connections auth walkthrough, gallery/templates in
  content hub.
- **Playbook permissions**: Settings > Playbook permissions grants Sentinel permission to run
  playbooks in selected resource groups (the #1 "playbook didn't fire" cause; dedicated
  setting record + troubleshooting runbook).
- Run history / failures: Logic Apps runs blade, common auth failures.
- Entity-triggered manual playbooks from incident page.

## 9. Content management

- **Content hub**: solutions (connector + rules + workbooks + playbooks bundles), install/
  update flow, standalone content, version pinning gotchas.
- **Repositories** (CI/CD from GitHub/Azure DevOps): what it deploys, PAT/app auth, drift.
- ARM/Bicep/Terraform export patterns for rules (automation doc 10 bridge).

## 10. UEBA & entity pages

- Enable UEBA: Settings > Analytics `VERIFY` exact page, source selection (AuditLogs,
  AzureActivity, SigninLogs, SecurityEvent), what it builds (`BehaviorAnalytics`,
  `IdentityInfo`, `UserPeerAnalytics` tables).
- Entity pages (user/host/IP), entity timeline, insights cards.
- Anomalies tab coupling, scoring explanation card.

## 11. Workbooks & reporting

- Workbooks hub: saved vs template, edit mode basics, param patterns.
- Flagship templates to index individually: Security operations efficiency, Usage & billing
  (cost!), Data collection health, Entra sign-ins, CA insights, MITRE coverage.
- Export/print/pin to Azure dashboard; scheduled email via Logic App recipe (KQL library).

## 12. Settings pages, exhaustively (the acceptance test)

`Microsoft Sentinel > Settings` (Azure portal) and Defender-portal equivalents; every row =
one `setting` record with click-path, role, license, API route:

| Setting | What it controls |
|---|---|
| Pricing tier / commitment tier | per-workspace ingestion pricing |
| Data lake / auxiliary logs opt-in | tiering features `VERIFY` |
| Analytics: UEBA toggle + sources | behavior analytics pipeline |
| Analytics: anomalies toggle | anomaly rule family |
| Health monitoring (auditing & health) | `SentinelHealth`/`SentinelAudit` tables to LA |
| Playbook permissions | Sentinel -> Logic Apps RG grants |
| Remove Microsoft Sentinel | offboard workspace |
| Workspace: retention default | Log Analytics workspace > Usage and estimated costs |
| Per-table retention/plan | LA workspace > Tables blade |
| Daily cap | LA workspace |
| RBAC | workspace IAM: Sentinel Reader / Responder / Contributor / Automation Contributor / Playbook Operator; resource-context RBAC; table-level RBAC v2 `VERIFY` |
| Defender portal: Sentinel workspaces connect/disconnect | unified SOC wiring |
| Defender portal: preview features | feature flags |

## 13. KQL table registry (Sentinel-side seed)

`SecurityIncident`, `SecurityAlert`, `SigninLogs`, `AuditLogs`, `OfficeActivity`,
`AzureActivity`, `SecurityEvent`, `Syslog`, `CommonSecurityLog`, `DnsEvents`, `Heartbeat`,
`Usage`, `Watchlist`, `ThreatIntelligenceIndicator` (+ successors), `BehaviorAnalytics`,
`IdentityInfo`, `SentinelHealth`, `SentinelAudit`, `AADRiskyUsers`, plus every Device*/Email*
table when XDR raw telemetry is connected. Each table record: product, cost tier eligibility,
retention default, 2-3 starter queries.

## 14. Runbook seeds

1. Onboard a brand-new tenant to Sentinel (workspace -> solution installs -> connectors ->
   baseline rules -> automation) (L2/L3, the flagship runbook).
2. "Playbook didn't run": permission chain triage (L2).
3. Ingestion cost spike: find the offender with Usage KQL, then DCR transform to trim (L2).
4. Connector shows disconnected: per-connector health matrix (L2).
5. Migrate MMA -> AMA leftovers check (L2).
6. Create a scheduled rule from a hunting query properly (entity mapping!) (L2).
7. False-positive storm: automation rule with expiry vs rule tuning decision (L2).
8. Multi-tenant MSSP access via Lighthouse (L3).
9. TI feed onboarding via upload API (L3).
10. Close-out hygiene: classification taxonomy + MTTR reporting query (L1/L2).

## 15. Niche surfaces (records to add)

- ASIM: normalized schemas, `_Im_*` parsers, raw-vs-normalized decision card, custom
  parser onboarding.
- Cross-workspace queries: `workspace()` scoping, limits, Lighthouse-backed MSSP
  patterns (doc 15 §4).
- Search jobs + restore from long-term retention + purge API (privacy/GDPR): the
  retrieval trio card.
- Table-level RBAC (v2 `VERIFY`) + resource-context RBAC recipes.
- CMK, dedicated cluster, AMPLS/Private Link: when compliance forces each, cost notes.
- Ingestion latency expectations per connector class + `ingestion_time()` measurement
  query (KQL library entry).
- KQL user-defined/saved functions as a shared SOC library pattern.
- BYO-ML notebooks, Azure ML compute attach, MSTICPy starter.
- Specialized solution pointers: SAP, Dynamics 365, Power Platform monitoring.
- Automation niche: entity-trigger playbooks, incident webhook -> PSA/ticketing sync
  recipes (MSP), bulk incident close scripts, automation-rule expiry for maintenance
  windows.
- Cost niche: per-customer attribution queries, workspace-per-customer vs shared model
  card (doc 15 §4).

## 16. Backlog

- Full connector encyclopedia (100+ connectors) as generated records from a curated CSV.
- Analytics rule template index (searchable by tactic/table).
- Sentinel data lake KQL jobs / notebooks surfaces once stable `VERIFY`.
