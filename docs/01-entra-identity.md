# 01 : Entra / Identity

The identity plane. Everything starts here: users, groups, devices, apps, roles, sign-in
policy, hybrid sync, governance. Portal: `https://entra.microsoft.com` (GCC High:
`https://entra.microsoft.us`).

---

## 1. Product family (the parts)

| Product | What it is | License |
|---|---|---|
| Entra ID (was Azure AD) | core directory + authentication | Free tier with any M365; P1; P2 |
| Entra ID Governance | lifecycle workflows, entitlement mgmt, access reviews (advanced) | Governance add-on / Entra Suite `VERIFY` |
| Entra External ID | CIAM (successor of Azure AD B2C) + B2B collaboration | own meters |
| Entra Verified ID | decentralized identity credentials | included/add-on `VERIFY` |
| Entra Permissions Management | multicloud CIEM. **Retired 2025-10** `VERIFY` | retired |
| Entra Workload ID | CA + protection for service principals | premium per-workload |
| Entra Domain Services | managed AD DS in Azure | Azure meter |
| Entra Global Secure Access | SSE: Internet Access + Private Access (ZTNA) | Entra Suite / standalone |
| Entra Connect / Cloud Sync | hybrid sync engines (on-prem AD <-> Entra) | free with P-license usage |

## 2. Area map inside the Entra admin center (the smaller parts)

### 2.1 Users & groups
- All users (`enusers`), deleted users (30-day restore), user settings (`enusrsettings`),
  per-user MFA legacy page (`enpumfa`), licenses (`enlicense`).
- Groups (`engroups`): security, M365, dynamic membership rules, expiration policy, naming
  policy, self-service group settings.
- External identities (`enguests`): B2B invitations (`eninvite`), cross-tenant access
  settings (`enctas`), collaboration restrictions.
- Own additions: bulk operations page, group-based licensing errors blade, guest access
  reviews entry, **administrative units** (incl. restricted management AUs: scope
  helpdesk roles to a department, the delegation flagship), custom security attributes
  (+ their use as CA filters).

### 2.2 Devices
- All devices (`endevices`), device settings (`endevicesettings`): join/register rules, local
  admin policy, Entra join MDM scope.
- Windows LAPS view (`enlaps`), BitLocker keys (per device page; runbook: "find BitLocker
  recovery key").
- Stale device cleanup guidance (concept card + PS snippet).

### 2.3 Applications
- App registrations (`enappreg`): SPA/web/native, certificates & secrets (expiry!), API
  permissions, app roles.
- Enterprise applications (`enapps`): SSO config (SAML/OIDC), provisioning (SCIM), consent
  and permissions (`enconsent`), admin consent requests, app launcher settings.
- Consent policy: user consent settings, admin consent workflow, risky consent (link to MDCA
  OAuth apps `decaoauth`).
- **Application Proxy**: connectors + connector groups, pre-authentication modes, SPN/KCD
  for IWA apps, complex-app wildcards, health checks; positioning vs Entra Private
  Access (GSA) migration card.
- Own additions: token configuration, claims mapping, certificate expiry report runbook.

### 2.4 Protection (security engineer's home)
- Conditional Access (`enca`): policies, named locations, custom controls, terms of use,
  authentication context (`enac`), **What If tool** (own record), CA templates, report-only
  mode + insights workbook.
- Identity Protection (`enidp`): user risk, sign-in risk, risk detections, risky workload
  identities, MFA registration policy.
- Authentication methods (`enauth`): policies per method (FIDO2/passkeys, Authenticator,
  SMS, voice, TAP, certificate-based auth, QR `VERIFY`), registration campaign (nudge),
  authentication strengths (`enauthstrength`), activity report (`enauthactivity`),
  **migration off legacy MFA/SSPR policies** (deadline was 2025-09, mark done/check `VERIFY`).
- Password reset SSPR (`ensspr`): properties, methods, registration, notifications,
  on-prem writeback.
- Password protection: banned passwords, smart lockout, on-prem agents.
- Security defaults (tenants without P1) toggle location.
- MFA unblock (`enmfaunblock`), OATH tokens, fraud alert (legacy).
- Identity Secure Score (`enscore`).
- Continuous Access Evaluation concept card.

### 2.5 Identity governance
- PIM (`enpim`): roles (`enpimr`), groups (`enpimg`), Azure resources (`enpimz`), approvals,
  alerts, discovery. Runbook: "activate a role", "configure role settings".
- Entitlement management (`enelm`): catalogs, access packages, connected orgs.
- Access reviews (`enar`).
- Lifecycle workflows: joiner/mover/leaver automation (own record).
- Delegated admin partners (GDAP link-out to doc 11).

### 2.6 Hybrid identity
- Entra Connect sync: sync errors (`ensynclog`), Connect Health (agents, ADFS `enadfslog`),
  staging mode concept, attribute filtering.
- Cloud Sync (`encloudsync`): provisioning agents, config.
- Seamless SSO, Password Hash Sync vs Pass-through Auth decision card.
- ADFS decommission guidance card (everyone is migrating).
- Kerberos cloud trust for Windows Hello (concept).

### 2.7 Monitoring & health
- Sign-in logs (`ensign`): interactive/non-interactive/service principal/managed identity
  tabs, useful filters (own tips card).
- Audit logs (`enlogs` alias), provisioning logs.
- Diagnostic settings: route to Log Analytics/Sentinel (bridge card to doc 04).
- Workbooks: sign-in analysis, CA insights, sensitive operations.
- Login error lookup (`enerror`), `https://login.microsoftonline.com/error?code=`.
- What's new / change announcements (`ennew`).

### 2.8 Global Secure Access (if licensed)
- Traffic forwarding profiles, connectors, Private Access apps, Internet Access web filtering.
- Own records: GSA client download, remote networks page.

## 3. cmd.ms import notes for this subject

~60 commands with `Entra` category. Fold `eng`/`azadg` GCC-high twins into `clouds` maps.
Legacy `azad` (Azure-portal AAD blade) stays but gets `deprecated: true` display hint.
`l`, `dl`, `enerror` become kind `tool`.

## 4. Enrichment data to capture per record

- Path (breadcrumb in Entra admin center, e.g. `Protection > Conditional Access > Policies`).
- Min role: prefer least privilege (e.g. CA: Conditional Access Administrator, not GA).
- License gate: Free / P1 / P2 / Governance / Suite.
- Graph/PS equivalent (see doc 10): e.g. CA policies = `Get-MgIdentityConditionalAccessPolicy`,
  users = `Get-MgUser`, sign-in logs = `Get-MgAuditLogSignIn`.

## 5. Key roles registry seed (identity)

Global Administrator, Global Reader, Security Administrator, Security Reader, Conditional
Access Administrator, Authentication Administrator (reset MFA for non-admins), Privileged
Authentication Administrator, User Administrator, Helpdesk Administrator (password reset for
non-admins), Groups Administrator, Application Administrator, Cloud Application Administrator,
Privileged Role Administrator, Hybrid Identity Administrator, License Administrator, Identity
Governance Administrator, Reports Reader.
Helpdesk cheat card: "which role resets what" matrix (password vs MFA vs sessions revoke).

## 6. KQL tables (feeds doc 04)

`SigninLogs`, `AADNonInteractiveUserSignInLogs`, `AADServicePrincipalSignInLogs`,
`AADManagedIdentitySignInLogs`, `AuditLogs`, `AADProvisioningLogs`, `AADRiskyUsers`,
`AADUserRiskEvents`, `IdentityInfo`, `AADPasswordProtection` (via agent logs).

## 7. Runbook seeds (phase 6)

1. Reset password + revoke sessions + check sign-in logs (L1).
2. Re-register MFA safely (verify identity first; TAP flow) (L1).
3. Unlock "account locked" vs "sign-in blocked" vs "risk-blocked" triage (L1/L2).
4. Guest cannot access shared resource: cross-tenant checklist (L2).
5. App consent request handling (L2).
6. Certificate/secret expiring on app registration (L2).
7. New starter: license + groups + dynamic group timing expectations (L1).
8. Investigate AADSTS error code (lookup table) (L1).
9. Break-glass account policy check (concept/audit).
10. PIM activation walk-through for engineers (L2).

## 8. Backlog (post-v1 ideas)

- CA policy "gallery" of recommended baseline policies with pitfalls.
- AADSTS full error table as searchable records (hundreds; scrape Learn `VERIFY` licensing of
  content, else link-only).
- Sign-in log filter recipe collection.
- Entra recommendations feed explained.
