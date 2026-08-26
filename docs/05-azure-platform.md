# 05 : Azure Platform

`https://portal.azure.com` (GCC High/DoD: `portal.azure.us`, China: `portal.azure.cn`,
preview: `preview.portal.azure.com`). cmd.ms is strongest here (~90 commands): mostly
BrowseResource deep links. Our added value: grouping, governance context, roles and the
monitor/security wiring into Sentinel.

---

## 1. Structure & governance (the parts)

- Tenancy chain concept card: Entra tenant -> management groups (`azmg`) -> subscriptions
  (`azsubs`) -> resource groups (`azrg`) -> resources.
- Azure Policy (`azpolicy`): definitions/initiatives/assignments/exemptions, compliance,
  remediation tasks. Guest configuration (`azguestconfig`).
- RBAC: IAM blade pattern (own record kind `setting`: "any resource > Access control"),
  built-in roles cheat table (Owner/Contributor/Reader/UAA, Sentinel roles bridge, VM roles,
  Key Vault data-plane roles), PIM for Azure resources (`azpim`).
- Cost Management + Billing (`azcost`), price calculator (`azprice`), Advisor (`azadvisor`),
  carbon (`azcarbon`).
- Resource Manager surfaces: ARM blade (`azrm`), templates (`aztemp`), Resource Graph
  Explorer (`arg`, GCC High `argg`) + starter Kusto queries (KQL library), Create hub
  (`azcreate`), Management groups, Subscriptions, Tags (own record).
- Service Health (`azhealth`) vs Resource Health (own record) distinction card.
- Support: Help + support (`azhelp`), severity levels + response SLA table (doc 11).

## 2. Compute & infra

VMs (`azvm`), availability sets (`azvmas`), scale sets (`azvmss`), disks (`azdisks`),
snapshots (`azsnap`), SSH keys (`azssh`), AKS (`azaks`), container instances
(`azcontainer`), container registries (`azacr`), App Services (`azapps`), plans (`azasp`),
Function Apps (`azfn`), Logic Apps (`azlogic`), Automation accounts (`azauto`),
Automanage (`azautomanage`), Arc servers (`azhybridcompute`), AVS (`avs`),
Azure Migrate (own record), Bastion (own record), Update Manager (`azumc`),
Backup center (`azbackup`), Business Continuity Center (`azbcc`), Site Recovery (own),
Dev Box + Deployment Environments (own, bridge doc 09).

### 2.1 Azure Arc family (deep; the hybrid estate)

Only `azhybridcompute` (servers browse) and `azpgaa` come from cmd.ms; the rest is own
content, each a record:

- **Arc-enabled servers**: onboarding paths (single-server script, at-scale service
  principal, `azcmagent` CLI card), agent health + disconnected troubleshooting,
  extensions management (AMA via Arc is the on-prem -> Sentinel highway, bridge doc 04
  §3.2), proxy configuration, agent local security (`azcmagent config` allow/deny of
  incoming connections, extension allowlist/blocklist: `setting` records with blast
  radius).
- **Licensing hooks**: ESU enrollment through Arc (2012/R2 era and onward), Windows
  Server pay-as-you-go via Arc, Windows Server management enabled by Azure Arc (SA
  benefit) `VERIFY` current terms, SQL Server extension registration + billing.
- **Arc-enabled SQL Server**: inventory, best-practices assessment, backup/TDE surfaces.
- **Arc-enabled Kubernetes**: connect clusters, GitOps (Flux) config, cluster connect
  vs public endpoint.
- **Arc-enabled data services**: SQL MI + PostgreSQL (`azpgaa`) on any infrastructure.
- **Arc-enabled VMware vSphere / SCVMM**: resource bridge concept, guest management.
- **Arc gateway** (outbound consolidation) `VERIFY` GA + **Azure Arc Private Link
  Scope** for no-public-egress estates.
- **What Arc unlocks elsewhere** (bridge cards): Defender for Servers without Azure VMs
  (§6), Azure Update Manager (`azumc`), machine configuration/guest assignments
  (`azguestconfig`), Automanage (`azautomanage`), Azure Policy on hybrid, inventory +
  change tracking, SSH via Arc, Windows Admin Center in the portal `VERIFY`.
- **RBAC**: Azure Connected Machine Onboarding vs Resource Administrator (roles.csv),
  HybridCompute resource provider registration prerequisite card.

## 3. Networking

VNets (`azvn`), NSGs (`aznsg`), route tables (`azroutes`), public IPs (`azpip`), DNS zones
(`azdns`) + Private DNS (own), load balancing hub (`azlb`), App Gateway (`azappgw`), WAF
(`azwaf`), Front Door/CDN (`azfdcdn`), Firewall Manager (`azfwmg`) + Azure Firewall (own),
Network Watcher (`aznwatch`) (+ packet capture, NSG flow logs -> VNet flow logs migration
`VERIFY`), VPN gateways (own), ExpressRoute (own), Private endpoints/Link (own), NAT
gateway (own). Concept card: hub-spoke vs vWAN in one paragraph.

## 4. Data & storage

Storage accounts (`azsa`) (+ SAS/keys rotation runbook, lifecycle rules), SQL family
(`azsql`, `azsqldb`, `azsqlep`, `azsqlmi`), PostgreSQL family (`azpg`, `azpgfs`, `azpgh`,
`azpgaa`), Cosmos (`azcosmos`, `cosmos`), Redis (`azredis`), Service Bus (`azservicebus`),
Event Hubs (own: Sentinel export dependency), Data Factory (`azadf`, `adf`), Synapse
(`azsynapse`, `synapse`), Databricks (`azdatabricks`), Data Explorer (`azkusto`),
Purview-in-Azure governance (`puudg`).

## 5. Monitor & observability (feeds Sentinel)

- Azure Monitor (`azmonitor`): metrics, alerts (action groups! own record), activity log.
- Log Analytics workspaces (`azloganalytics`): tables, DCRs (`azdcr`), DCEs (own), agents.
- Application Insights (`azappinsights`), Workbooks (`azwb`).
- Diagnostic settings pattern card (kind `setting`): "any resource > Diagnostic settings >
  send to LA workspace": the single most reused click-path in the site.
- Alert processing rules, service health alerts recipe (runbook).

## 6. Security surfaces in Azure portal

- Microsoft Defender for Cloud (`azdefender`): CSPM (secure score, recommendations,
  attack paths), CWPP plans per resource type (servers P1/P2, storage, SQL, containers,
  app service, key vault, ARM, DNS retired `VERIFY`), regulatory compliance, workflow
  automation, continuous export to Sentinel/Event Hub, JIT VM access, file integrity
  monitoring, agentless scanning toggles: each plan gets a `setting` record.
- Key Vault (`azkv`): access policies vs RBAC mode card, secret/cert/key expiry alerting
  runbook, purge protection concept.
- Managed identities (`azmi`) concept + where-used audit (Resource Graph KQL).
- Sentinel entry (`azsentinel`, bridge to doc 04).
- Microsoft Entra blade in Azure portal (`azad`) marked legacy-pointer.

## 7. Tools & misc

Cloud Shell (`azshell`), Azure Mobile app card, Azure status page (own:
`status.azure.com` `VERIFY` moving into portal Service Health), OpenAI/AI Foundry
(`azoai`), Content Safety (`azcs`), ML studio (`azml`), DevOps (`dev`), shared dashboards
(`azsd`), Universal Print (`print`, doc 09 bridge), Engage Center (`engage`).

## 8. Enrichment per record

- Role: least-priv built-in role for the service.
- CLI/PS: `az` command group + `Az.*` module per record where obvious (e.g. VMs:
  `az vm` / `Az.Compute`).
- Docs link pattern `learn.microsoft.com/azure/<service>/`.

## 9. Runbook seeds

1. Grant someone access to a resource the right way (scope decision -> role pick -> PIM
   eligible vs active) (L2).
2. Diagnose "you don't have permission": effective RBAC + deny assignments + PIM check (L2).
3. Wire any resource's logs into Sentinel (diagnostic settings pattern) (L2).
4. VM unreachable triage: NSG effective rules -> Network Watcher connection troubleshoot ->
   boot diagnostics -> serial console (L2).
5. Storage key/SAS leaked: rotation + audit trail (L2).
6. Cost spike triage with Cost analysis + Resource Graph (L2).
7. Create service health alerts for the platforms you run (L1 setup).
8. Key Vault secret expiry watch (Event Grid + Logic App recipe) (L3).
9. Onboard an on-prem server fleet to Arc + AMA + DCR into Sentinel (L2/L3, flagship
   hybrid runbook).
10. Arc agent disconnected/expired: triage chain (service, proxy, cert, heartbeat) (L2).
11. Enroll Arc-managed servers into ESUs and prove activation (L2).

## 10. Backlog

- Azure built-in role encyclopedia (filtered to the ~40 that matter).
- Resource Graph query cookbook as KQL records.
- Landing zone / CAF pointer cards (link-only, no rewrite).
