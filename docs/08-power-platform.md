# 08 : Power Platform & Analytics

Low-code plus BI. Audience angle: engineers rarely build here, but they administer, secure
and troubleshoot it (environments, DLP-for-connectors, licensing, tenant isolation).

Shipped 2026-08-26: gateways portal, environment types + default-environment trap,
managed environments, publish-to-web control, CoE kit concept (enrich-power.csv);
subject now 18 grouped records. Unshipped depth stays backlog.

---

## 1. Portals (the parts)

| Surface | URL | cmd |
|---|---|---|
| Power Platform admin center | `https://admin.powerplatform.microsoft.com` | `pp` |
| Power Apps maker | `https://make.powerapps.com` | `powerapps` |
| Power Automate maker | `https://make.powerautomate.com` | `pa` |
| Power Pages | `https://make.powerpages.microsoft.com` (own) | + GCC twins `ppageg`, `ppagegh` |
| Copilot Studio | `https://copilotstudio.microsoft.com` | `cps` (+ `cpsg`) |
| Power BI service / Fabric | `https://app.powerbi.com` | `pbi` (+ `pbig`, `pbigh`, `pbidod`) |
| Fabric admin | `https://app.powerbi.com/home?experience=fabric-developer` / `app.fabric.microsoft.com` `VERIFY` | `fabric` |
| Dataverse | inside PPAC per environment | concept |
| Sovereign twins | `ppg`, `ppgh`, `ppdod`, `pappsg`, `pappsdod`, `pag`, `pagh`, `pflowdod` | fold into clouds map |

## 2. Admin center areas (the smaller parts)

- Environments: types (default/production/sandbox/dev/Teams), the "rename + restrict the
  default environment" best-practice card, backups/restore, copy/reset.
- Security: DLP policies for connectors (business/non-business/blocked groups, connector
  action control, endpoint filtering), tenant isolation (inbound/outbound), cross-tenant
  restrictions, IP firewall for Dataverse, customer-managed keys pointer.
- Licensing/capacity: Dataverse capacity model, per-app vs per-user, pay-as-you-go, the
  "why is my flow throttled" (Power Platform request limits) card.
- Analytics: usage per product; COE starter kit pointer card (community tooling).
- Data integration: gateways cluster admin (on-prem data gateway record + update runbook),
  connections, dataflows.
- Policies: billing policies, environment routing `VERIFY`, managed environments feature
  gate table (sharing limits, solution checker enforcement...).
- Dynamics 365 touchpoint: LCS (`lcs`), admin pointer cards only (out of scope otherwise).

### 2.1 Support-side deep dives (the tickets IT actually gets)

- **Dataverse security model**: business units, security roles (+ record ownership),
  teams (owner vs access), column-level security, hierarchy security: the "user cannot
  see records" triage card.
- **ALM basics for admins**: managed vs unmanaged solutions, environment variables +
  connection references (the deploy-broke-the-flow classic), pipelines in PPAC, who can
  deploy where.
- **Flow operations**: run history windows, resubmit, flow owners vs run-only users,
  suspended flows (license/DLP causes), child flow permissions, retry policies.
- **App sharing model**: canvas app share (user vs co-owner) vs model-driven (security
  roles), "app not found" causes, app quarantine state `VERIFY`.
- **Power Pages security**: site visibility (public/private toggle: the accidental-
  public classic), authentication providers, table permissions + web roles, WAF/CDN.
- **Copilot Studio governance**: agent sharing rules, authentication modes, DLP applied
  to agents, usage/billing (messages) `VERIFY` meters.
- **Dataverse backups & restore**: system vs manual, restore-to-sandbox-only rule,
  retention windows per environment type; deleted environment recovery window (7 days
  `VERIFY`).
- **Capacity**: database/file/log split, what consumes what, over-capacity effects
  (restore blocked!), per-app vs per-user consumption.

## 3. Power BI / Fabric admin specifics

- Tenant settings page (the giant toggle wall: index top 20 as `setting` records: export
  controls, publish to web!, external sharing, service principal access...).
- Workspaces admin view, capacities (Premium/Fabric F-SKUs), embed codes, usage metrics.
- Fabric items pointer (lakehouse/warehouse/pipelines) + OneLake concept card.
- Sentinel bridge: Power BI activity via `PowerBIActivity` audit -> OfficeActivity/audit
  `VERIFY` table names.

## 4. Enrichment per record

- Roles: Power Platform Administrator, Fabric Administrator, Dynamics 365 admin, environment
  admin vs maker distinction card.
- PS/CLI: `Microsoft.PowerApps.Administration.PowerShell`, `pac` CLI, Fabric REST/PS
  `VERIFY` module names.

## 5. Runbook seeds

1. Flow owned by a leaver: reassign/co-own before disabling the account (L2, ties into the
   offboarding flagship in doc 06).
2. Connector blocked by DLP: identify policy, request path (L1/L2).
3. Gateway offline triage + update (L2).
4. "Publish to web" audit and lockdown (L2).
5. Find orphaned/unused apps + flows for cleanup (L3 script).

## 6. Backlog

- Connector DLP classification starter matrix.
- Managed environments feature comparison record set.
- Fabric admin API inventory scripts.
