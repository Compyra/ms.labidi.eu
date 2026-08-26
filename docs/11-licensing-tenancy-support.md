# 11 : Licensing, Tenancy & Support

The subject nobody enjoys and everybody needs: which SKU unlocks what, how tenants and
sovereign clouds work, where to get help, and the MSP/multi-tenant toolchain.

Shipped 2026-08-26 (§1 records): assignment mechanics (`licassign`), lifecycle stages
(`liclifecycle`), the removal-impact flagship (`licremoval`), channels/NCE
(`licchannels`), self-service purchase toggles (`set-lic-selfservice`); subject now 10
grouped records plus the 80-row matrix of §2.

---

## 1. License architecture (concept cards)

- Stack model: base (Office 365 E1/E3/E5, M365 E3/E5/F1/F3, Business Basic/Standard/
  Premium) + add-ons (E5 Security, E5 Compliance, Copilot, Intune Suite, Entra Suite...).
- Where licenses live: M365 AC billing (`adlicense`, `vlsc`, `macvlsc`), Entra
  license blade (`enlicense`), group-based licensing (+ error states runbook).
- Service plans vs SKUs: `Get-MgSubscribedSku`, friendly-name mapping (the GUID -> name
  community table, pointer card), disabling sub-plans per user.
- Purchase channels: CSP vs EA vs MCA vs direct; NCE term/seat rules (downgrade windows);
  trial sprawl control (self-service purchase toggles: `MSCommerce` PS record).
- **Assignment mechanics**: direct vs group-based coexistence, reprocess action,
  common error states (no free seats, conflicting service plans, usage location
  missing: each a record), license change auditing (audit log operations + who).
- **Subscription lifecycle**: active -> expired (30d grace) -> disabled (customer data
  kept ~90d) -> deprovisioned `VERIFY` exact windows per channel; renewal failure
  symptoms per stage.
- **License removal impact matrix** (flagship record): what actually happens when a
  license/plan is pulled: mailbox (unlicensed -> 30d then deletion), OneDrive (departed
  user retention window), Intune (device stays managed but user apps stop `VERIFY`),
  Defender per-user features, Copilot, Power Platform premium (flows suspend). Pairs
  with the offboarding runbook (doc 06 §7.5).

## 2. The matrix (phase 7 flagship): feature -> minimum license

Shipped 2026-08-26: 80 rows in `content/licensing.csv` -> `data-licensing.js` with the
`#/licensing` view; schema in doc 12 §3.5. The list below remains the source frame.
Build as data (`data-licensing.js`), rows seeded from the per-subject docs, three columns:
feature, minimum path, notes. Priority rows (~80 at v1): Conditional Access (P1),
risk-based CA (P2), PIM (P2), access reviews (P2), lifecycle workflows (Governance),
Intune plans/Suite splits (doc 02 table), Defender plans (doc 03 table), audit premium,
auto-labeling, IRM, records mgmt (doc 07), AVD/W365 entitlements (doc 09), Copilot
prerequisites, Teams Premium features, Power Platform premium connectors, Sentinel
benefit (E5 grant), Defender for Business boundaries.
Sources: Microsoft Learn service descriptions (link every row, `VERIFY` quarterly).

## 3. Tenancy & sovereign clouds

- Tenant anatomy: tenant ID/initial domain, custom domains (`endom`, `domains`), org
  relationships, multi-tenant orgs (MTO) `VERIFY` GA scope, tenant switcher UX.
- Sovereign cloud matrix lives in doc 00 §3; records here: how to tell where a tenant
  lives (`login.microsoftonline.com/<domain>/.well-known/openid-configuration` trick card),
  endpoint allowlists (`aka.ms/o365ips`, `endpoints.office.com` API record).
- Tenant-to-tenant migration pointer card (out of scope for how-to, in scope for "what
  tooling exists").
- CDX demo tenants (`cdx`) for testing.

## 4. Support & escalation

- Paths: M365 AC service requests, Azure Help + support (`azhelp`) + severity/response
  table, Premier/Unified vs Pro Direct vs included support card, Entra support blade
  (`ensupport`), what-to-collect-before-you-open-a-case runbooks per product family
  (fiddler/HAR, `MSDiag`, Intune diagnostics, message trace IDs, correlation IDs: the
  correlation-ID-finding card is a flagship).
- Health surfaces: `mshealth`, `mc` message center (+ how to route MC posts to Teams/
  Planner), Azure Service Health alerts recipe (doc 05), `status.cloud.microsoft` public
  fallback `VERIFY` URL, `@MSFT365Status` outage comms pattern.
- Known-issue trackers: Windows release health, Exchange EHLO blog, Intune What's New,
  message center archive tools (community, mark 3rd-party).

## 5. MSP / multi-tenant operations

- M365 Lighthouse (`lh`, `lhbsl`, `lhdi`, `lhtnt`): tenant list, baselines, deployment
  insights; eligibility (partner + license caps) `VERIFY`.
- Azure Lighthouse: delegated resource management (Sentinel MSSP bridge, doc 04).
- Partner Center (`partner`): GDAP (roles, expiry, the "GDAP relationship expired and
  everything broke" runbook), CSP customer management, admin-on-behalf-of.
- Cross-tenant sync (doc 01 bridge), B2B collab defaults per partner.
- The full MSP programme (access architecture, GDAP bundles, per-customer hardening
  baseline, multi-tenant SOC) lives in [15-msp-hardening.md](15-msp-hardening.md).

## 6. Runbook seeds

1. License a user correctly with groups + resolve assignment errors (L1).
2. "Feature not working": is it licensing? service-plan check sequence (L1, flagship).
3. Open a support case that gets traction: per-portal artifact checklist (L1/L2).
4. Reconcile purchased vs assigned vs consumed seats (L2).
5. GDAP relationship audit + renewal (MSP) (L2).
6. Track an outage properly: health dashboard -> MC post -> comms template (L1).

## 7. Backlog

- SKU GUID <-> friendly name dataset (generated, refreshed quarterly).
- Per-feature license matrix expansion beyond the seed 80 rows.
- Trial/expiry calendar recipe (Graph subscription list + Planner).
