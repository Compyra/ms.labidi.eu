# Tenant verification checklist

Everything that cannot be confirmed without a real tenant. Bring one and we work
straight down this list; each item says exactly what to look at and what to write back
into which file.

Rules while verifying:
- One source of truth per fact: the tenant beats a blog, Microsoft Learn beats memory.
- Anything confirmed gets `verified: YYYY-MM` in its content row.
- Anything that turns out wrong gets corrected the same session; we never leave a known
  wrong fact shipped, even for an hour.
- Anything that no longer exists gets `deprecated` with a successor id, not deletion.

---

## A. Blocking gates (a phase is not "done" until these pass)

| # | Item | How to check | Lands in |
|---|---|---|---|
| A1 | Phase 5 gate: 10 library snippets run unedited | Pick 10 rows across `#/ps`, paste as-is, confirm no edit needed beyond placeholders | roadmap phase 5 gate |
| A2 | KQL queries return rows (not just parse) | Run 10 across `#/kql` in Log Analytics / advanced hunting | `content/kql.csv` verified stamps |
| A3 | Deep links land on the right blade | Click through every `path` for the top 50 records | `content/enrich-*.csv` |
| A4 | Role claims are least-privilege *and sufficient* | Test with a scoped account per role tier | `roles` column everywhere |

## B. Deep links and portal paths

- B1. Every `settings-sentinel.csv` path: confirm the menu route still exists in the
  Defender portal (Sentinel moved; several paths are written from documentation).
- B2. `settings-defender.csv` advanced-features toggles: confirm each toggle name and
  its section, and note the tenant default for each (we ship guidance, not defaults).
- B3. `settings-intune.csv` paths, especially Endpoint Privilege Management, Cloud PKI
  and Device query, which differ by license.
- B4. Records whose `url` is a `#view/...` deep link: confirm they open the blade
  directly rather than the portal home (Azure deep links rot quietly).
- B5. GCC High / GCC / DoD variants: confirm the `clouds` URLs actually resolve in a
  sovereign tenant if you have one; otherwise mark them unverified rather than claim.

## C. Licensing claims (highest risk of shipping something wrong)

- C1. MDE P1 vs P2 boundary for **custom indicators** (file/IP/URL/cert): our records
  say P1; confirm in the tenant's licensing comparison. *(already open in todo.md)*
- C2. Defender for Business caps vs MDE P2 features on Business Premium.
- C3. Which Purview features light up on E3 vs E5 vs E5 Compliance for the records in
  `enrich-*`/`settings-*` that claim a license.
- C4. Intune Suite gating: Remote Help, EPM, Advanced Analytics, Cloud PKI, Device query.
- C5. Entra Suite / Governance composition (we tagged `entra-suite` from documentation).
- C6. Teams Rooms Pro (we removed a false Teams Premium claim; confirm the correct SKU).
- C7. Sentinel E5 data grant: confirm the current per-user allowance and which data
  types qualify, then update `sencost`.
- C8. `licenses.csv` `includes[]` bundle map: verify each bundle really contains what we
  claim, because it drives the "included in your licensing" badge.

## D. Product naming and lifecycle (the `VERIFY` tags in docs/)

Roughly 60 tags across docs 00-16. The ones that affect shipped records first:

- D1. Portal host migrations: `admin.microsoft.com` -> `admin.cloud.microsoft`,
  Exchange admin center host, Office home -> `m365.cloud.microsoft`.
- D2. Sentinel in the Azure portal: confirm what remains vs Defender-portal only.
- D3. Purview: classic compliance portal status, Unified Catalog naming.
- D4. Defender for Cloud Apps classic portal (`portal.cloudappsecurity.com`) status.
- D5. AVD web client host (`client.wvd.microsoft.com` vs `windows.cloud.microsoft`).
- D6. Azure OpenAI vs AI Foundry naming and host.
- D7. MDI sensor: classic vs unified agent naming.
- D8. Deception, Summary rules, Arc gateway, table-level RBAC v2: GA state each.
- D9. Message trace: confirm the current interactive vs downloadable windows and
  whether `Get-MessageTraceV2` has replaced `Get-MessageTrace`.
- D10. `Search-UnifiedAuditLog` status and its Purview replacement path.

## E. Behaviour we describe but have not observed

- E1. Intune check-in cadence and the compliance re-evaluation timing card (doc 02 §2.5)
  and how quickly Conditional Access reflects a fixed device.
- E2. The compliance fail-open switch: confirm the default and what flipping it does to
  devices with no policy assigned.
- E3. Grace period behaviour: does an in-grace device still satisfy the CA compliant
  grant (we claim it does).
- E4. Quarantine release permissions: confirm Quarantine Administrator is sufficient and
  what Security Operator genuinely cannot do.
- E5. AIR automation levels: confirm the Full/Semi/None behaviour per device group.
- E6. Sentinel daily cap: confirm that security tables are also stopped (we rate this
  high blast radius on that basis).
- E7. Playbook permissions: reproduce the "playbook never fired" case and confirm the
  fix path we document.

## F. Data we could import if the tenant allows

- F1. Real AADSTS error samples to seed an error-code lookup (phase 7 backlog).
- F2. Intune enrollment failure codes actually seen in the tenant.
- F3. The tenant's own table inventory, to grow `content/tables.csv` beyond the 49 we
  ship and to record real retention defaults.
- F4. Connector inventory in Sentinel to build the connector encyclopedia (doc 04 §16).
- F5. Screenshot-free path capture: for each blade, copy the breadcrumb text verbatim so
  our `path` strings match the UI word for word.

## G. Things we deliberately will not claim until verified

These currently ship with no license/role claim rather than a guess. Fill them in only
with tenant evidence: `teamsrooms` (SKU), `enagentid` (licensing), `demdepmi` (P1/P2),
`demto` (partner prerequisites), `cdx` (eligibility).
