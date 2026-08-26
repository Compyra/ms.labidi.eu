# 15 : MSP Multi-Tenant Operations & Customer Hardening

For MSP/MSSP engineers running fleets of customer tenants. New subject slug: `msp`
(13th hub). Covers the access architecture into customer tenants, least-privilege
delegation, the per-customer hardening baseline (every checklist row becomes a record),
multi-tenant SOC patterns, and the tooling ecosystem. Doc 11 keeps licensing/support;
this doc owns everything operational and security-shaped about running other people's
tenants.

---

## 1. Access architecture into customer tenants

- **GDAP** (granular delegated admin privileges): relationships, role assignments to
  security groups, expiry (max 2 years, auto-extend option `VERIFY`), approval flow on
  the customer side, audit surfaces on both sides. DAP is dead; card documents the
  migration history so old guides stop confusing people.
- **Partner tenant hygiene** (the MSP's own tenant is the crown jewel target):
  Partner Center security requirements (MFA enforced on all partner users), CA baseline
  for technicians (phishing-resistant MFA, compliant device required, no legacy auth),
  PIM for AdminAgents/HelpdeskAgents membership (the group grants access to every
  customer!), separate accounts + PAWs for high tiers, CAE awareness.
- **Secure Application Model (SAM)**: refresh-token based CSP API automation, secret
  storage (Key Vault), rotation runbook; what breaks when the consenting user's MFA
  changes.
- **Azure Lighthouse**: delegated resource management for Azure/Sentinel, offer
  definitions (ARM template), eligible authorizations (PIM-in-Lighthouse), difference
  vs GDAP card (ARM plane vs Graph/M365 plane: the perennial confusion).
- **M365 Lighthouse** (`lh`, `lhbsl`, `lhdi`, `lhtnt`): eligibility rules (CSP, seat
  caps `VERIFY`), tenant onboarding states, baselines, deployment insights, alerts.
- **Cross-tenant access settings from the customer side** (`enctas`): how customers can
  scope the MSP down (trusted MFA/device claims, B2B allowlists); what MSP-side device
  compliance can be trusted cross-tenant.
- **Entra B2B vs GDAP for engineer access** decision card (guest accounts in customer
  tenants: when acceptable, how to review them).

## 2. GDAP role bundle recipes (records, one per tier)

| Tier | Roles (least-priv set) | For |
|---|---|---|
| Read/triage | Global Reader, Reports Reader, Message Center Reader | monitoring, QBRs |
| Helpdesk L1 | Helpdesk Administrator, User Administrator (scoped need check), Groups Administrator | resets, unlocks, group membership |
| Endpoint L2 | Intune Administrator, Cloud Device Administrator | device ops |
| Messaging L2 | Exchange Administrator, Teams Administrator, SharePoint Administrator | workload ops |
| Security L3 | Security Administrator, Conditional Access Administrator, (Security Operator) | policy + response |
| Identity escalation | Privileged Role Administrator, Privileged Authentication Administrator | break-glass class work, time-boxed |
| Never | Global Administrator standing | use time-boxed escalation only |

Each bundle record: role ids (roles.csv), justification, what it cannot do, expiry
recommendation. Plus: mapping GDAP roles -> what Lighthouse features light up `VERIFY`.

## 3. Customer tenant hardening baseline (the checklist as records)

Every row: `setting`/`concept` record with click-path, PS/Graph check, and a "verify
in bulk across tenants" snippet reference. Keyword-tag all of these `hardening` + `msp`.

### 3.1 Identity
- Two cloud-only break-glass accounts, excluded from CA, monitored (KQL alert on use).
- Security defaults vs CA baseline decision (license-dependent); CA starter set records:
  block legacy auth, require MFA for admins, require MFA for users, require compliant or
  hybrid device for admins, block device-code flow where unused, risk policies when P2,
  block unknown platforms, session controls for unmanaged devices.
- Admin hygiene: <= 4 GAs, no standing GA for daily work, role-assignable groups, PIM
  when licensed, quarterly access review of directory roles.
- Password protection (banned list + on-prem agents when hybrid), SSPR enabled + MFA
  registration campaign, legacy per-user MFA migrated to CA/auth methods policy.
- Guest hygiene: collaboration restrictions, guest access reviews, stale guest sweep.
- App consent: user consent disabled or verified-publisher-only, admin consent workflow
  on, risky OAuth grants review cadence (bridge doc 03 app governance).

### 3.2 Email
- SPF/DKIM/DMARC per accepted domain (DMARC to enforce, not just monitor), ARC for
  gateway chains, MTA-STS pointer `VERIFY` adoption.
- Preset security policies Standard (default) or Strict (VIPs); priority account
  protection on; external sender tagging; first-contact safety tip.
- Outbound: external auto-forwarding off in anti-spam outbound policy, transport-rule
  audit, connector audit.
- Mailbox auditing verified on + audit retention understood; quarantine policies +
  end-user notifications tuned; TABL hygiene review cadence.

### 3.3 Endpoint
- Enrollment restrictions (block personal Windows unless MAM-only strategy), compliance
  policies per platform + fail-closed tenant switch (doc 02 §2.5) + CA "require
  compliant device".
- BitLocker escrowed + LAPS on + local admin lockdown; ASR rules audited then enforced;
  Defender AV baseline (tamper protection on, cloud protection high, PUA block);
  update rings with deadlines; security baselines applied and drift-checked.
- MDE onboarded on servers + clients, EDR block mode, automation level "Full" for
  workstations, device groups per customer standard.

### 3.4 Data & collaboration
- SPO external sharing tier decision + anyone-link expiry/permissions, ODB retention for
  leavers, Teams external access allowlist vs open federation decision, meeting policy
  baseline (lobby, who can present, recording), DLP starter policies (credentials, PII),
  sensitivity label starter taxonomy, unified audit confirmed on.

### 3.5 Monitoring & response
- Alert policies routed somewhere humans look (shared mailbox -> PSA/ticketing
  connector); Secure Score target + monthly delta report per tenant; service health +
  message center digest per tenant; Defender XDR email notifications per customer;
  Sentinel or XDR-only decision per size (cost model card).

### 3.6 Lifecycle
- Onboarding checklist: GDAP established -> baseline deployed -> monitoring wired ->
  documentation (tenant ID, domains, break-glass custody, licensing inventory).
- Offboarding checklist: remove GDAP + Lighthouse delegations + guest accounts + SAM
  consents, hand over break-glass, export documentation, revoke partner relationship.
- Technician leaver: disable partner account, PIM/group sweep, rotate SAM secrets,
  audit recent cross-tenant activity.

## 4. Multi-tenant SOC patterns

- Defender XDR multi-tenant view (`security.microsoft.com/mto` `VERIFY`): tenant list,
  cross-tenant incidents/hunting, GDAP + unified-RBAC interplay card.
- Sentinel architectures: workspace-per-customer (in customer's Azure) + Azure
  Lighthouse into each vs central multi-workspace queries; workspace manager / content
  repositories for at-scale rule deployment (doc 04 §9/§15); cross-workspace
  `workspace()` query limits; per-customer cost attribution (Usage table by workspace).
- Cross-tenant automation: one Logic Apps set per customer vs centralized with managed
  identity federation `VERIFY` patterns; incident sync into PSA tools (webhook records).

## 5. Tooling (mark ownership clearly)

| Tool | What | Origin |
|---|---|---|
| M365 Lighthouse | baselines + tenant ops | Microsoft, imported cmds |
| Azure Lighthouse | ARM delegation | Microsoft |
| Partner Center + APIs | CSP lifecycle, GDAP | Microsoft |
| CIPP | self-hosted MSP portal (standards, BPA, per-tenant apply) | 3rd-party OSS |
| Maester | tenant security test framework | community |
| ORCA | MDO config analyzer | community |
| ScubaGear / SCuBA baseline | M365 secure config assessment | CISA (US gov) |
| Monkey365 | M365/Azure review tool | 3rd-party OSS |
| Config analyzers in-product | MDO configuration analyzer, CA gap analyzer workbook | Microsoft |

## 6. Standards to map the baseline against (link-only cards)

CIS Microsoft 365 Foundations Benchmark, CIS Azure Foundations, Microsoft Secure Score
recommended actions, CISA SCuBA M365 baselines, Essential Eight (AU) mapping, Cyber
Essentials (UK) pointer. The hardening records carry `standards:` tags so a filter like
`standard:cis` lists the mapped subset (add `standards[]` to the setting schema, doc 12).

## 7. Runbook seeds

1. Onboard a new customer tenant end-to-end (GDAP -> baseline -> monitoring) (L2, flagship).
2. GDAP expiry audit + renewal sweep across all customers (L2, scheduled).
3. Technician offboarding across N tenants in one hour (L2, flagship).
4. Break-glass verification day: test both accounts everywhere, rotate creds (L2).
5. Monthly per-tenant security report (Secure Score delta + incident stats + baseline
   drift) (L2).
6. Customer hit by BEC: MSP-side containment sequence with GDAP security tier (L3).
7. Lighthouse baseline deviation triage (L1/L2).
8. SAM secret rotation without breaking automations (L3).

## 8. Data-model notes

- Records here use `category: msp`; hardening rows double-tag their native subject
  (keyword) so they surface in both hubs.
- New optional schema field `standards: string[]` on `setting` records (doc 12 §3.2).
- The license matrix (doc 11) gains an "MSP variant" column note: what Business Premium
  covers vs E5 for the SMB-heavy MSP book of business.
