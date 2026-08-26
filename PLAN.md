# ms.labidi.eu : Master Plan

Status: phases 0-6 complete; phase 7 (licensing matrix + error codes) prepared with seeds.
Tenant-dependent verification is collected in
[docs/17-tenant-verification.md](docs/17-tenant-verification.md).
Last updated: 2026-08-26.

The working name for the product is **MS Portal Hub**: one fast, keyboard-first reference site
for people who run Microsoft environments all day.

---

## 1. Mission

Every service desk agent, helpdesk engineer, cloud engineer and security engineer working in a
Microsoft shop loses minutes per day hunting for the right portal, the right blade, the right
setting, the right cmdlet or the right KQL query. [cmd.ms](https://cmd.ms/) solved the first
10% of this brilliantly with ~355 portal shortcuts. We take that idea much further:

1. **Every shortcut cmd.ms has**, imported and kept in sync (MIT licensed, fully attributed).
2. **Every setting that matters**, findable by name. Example from the brief: someone needs a
   specific Sentinel setting (say, where to toggle UEBA data sources, or where playbook
   permissions live). They type "ueba" and get the exact page, the path to click, the role
   needed, the license needed and the PowerShell/Graph equivalent.
3. **The knowledge around the link**: which RBAC role you need, which license unlocks it,
   which cmdlet does the same thing, which KQL finds the evidence, and the step-by-step
   runbook for the 50 most common service desk tasks.

Non-goals for v1: user accounts, server-side anything, community submissions, non-Microsoft
clouds, mobile apps.

## 2. Audience personas

| Persona | Cares about | Example query |
|---|---|---|
| L1 service desk | password/MFA resets, unlock, message trace, quarantine release | "mfa reset" |
| L2 helpdesk / endpoint | Intune device actions, BitLocker keys, enrollment errors, app installs | "bitlocker recovery" |
| Cloud engineer | Azure blades, Entra config, Exchange/SPO/Teams admin, automation | "conditional access what if" |
| Security engineer / SOC | Sentinel, Defender XDR, KQL, incident response actions, TI | "sentinel automation rules" |
| MSP / multi-tenant admin | Lighthouse, GDAP, Partner Center, per-tenant deep links | "gdap" |

## 3. What we build (feature set)

### v1 core
- **Command palette** (`/` or `Ctrl+K` focuses search): instant fuzzy search over every record
  type (shortcut, setting, snippet, runbook). Ranked: exact command id > alias > name > keyword.
  Acronym/synonym aware via a curated registry: searching `air` surfaces Automated
  investigation & response, `gdap`, `zap`, `asr`, `tap` and friends all resolve.
- **Directory browsing**: subject hubs (Entra, Intune, Defender, Sentinel, Azure, M365,
  Purview, Power Platform, Windows endpoints, Automation, Licensing) with grouped links.
- **Record cards**: every entry shows open button, copy-URL button, breadcrumb path inside the
  portal ("Entra admin center > Protection > Conditional Access"), required role(s), required
  license, docs link, related entries, PowerShell/Graph equivalent when known.
- **Go-redirects**: `ms.labidi.eu/?go=enca` resolves and redirects instantly, so the browser
  address bar works like cmd.ms: register a custom search engine `ms` pointing to
  `https://ms.labidi.eu/?q=%s` (shows results) or `?go=%s` (jumps). Ship an OpenSearch
  description XML so browsers can discover it.
- **Cloud switcher**: commercial / GCC / GCC High / DoD / China (21Vianet) variants per record
  where they exist (cmd.ms already carries many `*.microsoft.us` twins; we model them as one
  record with per-cloud URLs instead of separate commands).

### v1.x expansions (in priority order)
1. **Settings encyclopedia**: deep pages per subject documenting settings areas that have no
   stable deep link (path-to-click documented instead). Sentinel first, then Defender
   settings, then Entra and Intune. See [docs/04-sentinel.md](docs/04-sentinel.md).
2. **License profile**: pick the SKUs you own; records included in them get badged and
   boosted (the "searching AIR while holding MDO P2" case) without hiding anything else.
3. **KQL library**: copy-ready queries tagged by table, product and scenario.
4. **PowerShell / Graph library**: task-oriented snippets ("revoke all sessions", "get
   BitLocker key", "message trace last 48h") with module + minimum role noted.
5. **Runbooks**: step-by-step L1/L2 procedures with decision points.
6. **Licensing matrix**: feature -> minimum SKU lookup (the eternal "is this E3 or E5?").
7. **Error code lookup**: AADSTS codes, Intune enrollment hex codes, Exchange NDR codes.
8. **MSP hardening baseline**: per-customer checklist as browsable, standards-tagged
   records (see [docs/15-msp-hardening.md](docs/15-msp-hardening.md)).

## 4. Information architecture

```
/                        home = search + subject tiles
/#q=<query>              search results (hash keeps it static-host friendly)
/?go=<command>           instant redirect (JS resolves from data, falls back to search)
/#/s/<subject>           subject hub (entra, intune, defender, sentinel, azure, m365,
                         purview, power, windows, automation, licensing, msp, toolbox,
                         mypages)
/#/c/<command-id>        single record permalink card
/#/kql /#/ps /#/runbooks libraries (v1.x)
/404.html                hard 404 for GitHub Pages
```

Navigation: one top bar (brand, search box, theme toggle, cloud selector), subject tiles on
home, footer with attribution (cmd.ms, MIT) and site family links.

## 5. Technical architecture

Family conventions apply (same stack as md/oasis/breach sites):

- **Plain HTML + CSS + vanilla JS. No framework, no build step for the site itself.**
- Data ships as **`data-*.js` files** (script tags assigning to `window.MSHUB`), not fetched
  JSON: works on `file://`, no CORS, no async waterfall. Split per subject to keep each file
  reviewable: `data-commands-entra.js`, `data-commands-azure.js`, `data-settings-sentinel.js`,
  `data-kql.js`, ...
- A small **Python pipeline** (`tools/build_data.py`) converts the upstream cmd.ms CSV plus
  our own YAML/CSV enrichment files into those `data-*.js` files. Python, not Node (no Node on
  the dev machine). Pipeline detail: [docs/12-data-model-import.md](docs/12-data-model-import.md).
- **Search** is built client-side at load: a lowercase token index over id/alias/name/keywords,
  simple subsequence-fuzzy fallback, result cap + ranking. ~600-1500 records is trivial for this.
- **Files at repo root**: `index.html`, `404.html`, `app.js`, `search.js`, `style.css`,
  `data/*.js`, `manifest.webmanifest`, `sw.js`, `robots.txt`, `sitemap.xml`, `CNAME`,
  `opensearch.xml`, `icons/`.
- **PWA**: installable, offline-capable (the whole point of a reference site is that it also
  works when everything is on fire). SW rules per family conventions: network-first shell,
  versioned assets (`style.css?v=N` with same `N` in SW), `updateViaCache:'none'`.
- **CSP**: strict, `script-src 'self'`, no external calls at runtime, no analytics, no fonts
  from CDNs. All outbound links `rel="noopener noreferrer"` and `target="_blank"`.
- **Theme**: dark default (terminal/SOC aesthetic, a respectful nod to cmd.ms without copying
  it), light theme available, `prefers-color-scheme` respected, WCAG AA contrast.
- **A11y**: full keyboard operation, visible focus, `role="listbox"` semantics on results,
  skip link, reduced-motion support.
- **i18n**: English only at v1 (audience is technical); architecture must not block adding
  `?lang=` later (family pattern exists).
- **Deployment**: GitHub Pages behind Cloudflare, `CNAME` = `ms.labidi.eu`. Remember the
  family gotchas: Cloudflare edge-caches CSS/JS for 4h, so version every asset URL; keep
  Rocket Loader / Email Obfuscation / Web Analytics off (CSP blocks them).

## 6. Data model (summary)

One record type, `command`, covers every linkable thing; `kind` distinguishes flavor.

```js
{
  id: "enca",                    // unique, lowercase, the "command"
  kind: "portal",                // portal | setting | tool | docs | enduser
  aliases: ["adca", "ca"],
  name: "Conditional Access",
  category: "entra",             // our taxonomy, mapped from cmd.ms categories
  group: "Protection",           // grouping inside a subject hub
  url: "https://entra.microsoft.com/#view/...",
  clouds: { gcch: "https://...microsoft.us/...", dod: null, cn: null },
  path: "Entra admin center > Protection > Conditional Access",
  desc: "Create and manage Conditional Access policies.",
  keywords: ["ca", "policy", "zero trust"],
  roles: ["Security Administrator", "Conditional Access Administrator"],
  license: "Entra ID P1",
  docs: "https://learn.microsoft.com/entra/identity/conditional-access/",
  ps: "Get-MgIdentityConditionalAccessPolicy",
  related: ["enauthstrength", "enidp"],
  source: "cmdms"                // cmdms | own
}
```

Settings-encyclopedia records, KQL snippets and runbooks get their own small schemas; all
defined in [docs/12-data-model-import.md](docs/12-data-model-import.md).

## 7. Content sources, attribution, freshness

- **cmd.ms**: upstream truth for shortcut URLs. Source file
  `https://github.com/merill/cmd/blob/main/website/config/commands.csv` (MIT). Attribution in
  the footer, the README and every imported record (`source: "cmdms"`). We never claim those
  as ours.
- **Microsoft Learn**: canonical docs links per record, licensing and role facts.
- **Own capture**: blade URLs and paths verified by hand in a test tenant; each own record
  carries a `verified: "2026-08"` stamp so staleness is measurable.
- **Volatile-facts policy**: portal URLs churn (examples currently in motion:
  `admin.microsoft.com` -> `admin.cloud.microsoft`, Sentinel's Azure-portal experience retired
  into the Defender portal, classic Purview portal retired). Every doc in this repo marks
  such facts with `VERIFY` so the build phase re-checks them instead of trusting this
  snapshot. A quarterly link-check script is part of maintenance (see roadmap).

## 8. Build phases

Detailed checklist lives in [docs/13-roadmap-backlog.md](docs/13-roadmap-backlog.md).

| Phase | Deliverable | Gate to next |
|---|---|---|
| 0 | This documentation set | you approve the plan |
| 1 | Repo scaffold, data pipeline, cmd.ms import, search palette MVP | 355+ records searchable locally |
| 2 | Subject hubs, record cards, go-redirects, OpenSearch, PWA shell | usable daily driver |
| 3 | Enrichment pass 1: roles, licenses, docs links, paths for top 150 records | cards feel "complete" |
| 4 | Sentinel + Defender settings encyclopedia | the brief's Sentinel test passes |
| 5 | KQL + PowerShell libraries (seed: 60 KQL, 60 PS) | copy-paste value proven |
| 6 | Runbooks (seed: 25 L1/L2 procedures) | service desk value proven |
| 7 | Licensing matrix + error-code lookups | |
| 8 | Launch: SEO, sitemap, icons, README, registries updated across the site family | live on ms.labidi.eu |
| 9 | Maintenance loop: quarterly link check, upstream CSV diff sync | ongoing |

## 9. Documentation index (this mapping phase)

| Doc | Subject |
|---|---|
| [docs/00-ecosystem-map.md](docs/00-ecosystem-map.md) | The whole Microsoft ecosystem, every top-level part, portal atlas, cloud table |
| [docs/01-entra-identity.md](docs/01-entra-identity.md) | Entra: identity, governance, hybrid, protection |
| [docs/02-intune-endpoint-management.md](docs/02-intune-endpoint-management.md) | Intune, Autopilot, endpoint security, Intune Suite |
| [docs/03-defender-xdr.md](docs/03-defender-xdr.md) | Defender portal, MDE, MDO, MDI, MDCA, MDVM, exposure mgmt |
| [docs/04-sentinel.md](docs/04-sentinel.md) | Sentinel end to end, every settings area (the deep one) |
| [docs/05-azure-platform.md](docs/05-azure-platform.md) | Azure portal, governance, monitor, infra services |
| [docs/06-m365-admin-collab.md](docs/06-m365-admin-collab.md) | M365 admin, Exchange, SharePoint/OneDrive, Teams, apps, end-user portals |
| [docs/07-purview-compliance.md](docs/07-purview-compliance.md) | Purview: audit, eDiscovery, DLP, IP, retention, IRM |
| [docs/08-power-platform.md](docs/08-power-platform.md) | Power Platform, Fabric/Power BI, Copilot Studio, Dynamics touchpoints |
| [docs/09-windows-cloud-endpoints.md](docs/09-windows-cloud-endpoints.md) | Windows 365, AVD, Windows servicing, Universal Print |
| [docs/10-automation-graph-powershell.md](docs/10-automation-graph-powershell.md) | Graph, PowerShell modules, CLI, community tooling |
| [docs/11-licensing-tenancy-support.md](docs/11-licensing-tenancy-support.md) | Licensing, tenants, sovereign clouds, support, MSP/multi-tenant |
| [docs/12-data-model-import.md](docs/12-data-model-import.md) | Schemas, taxonomy mapping, import pipeline, validation |
| [docs/13-roadmap-backlog.md](docs/13-roadmap-backlog.md) | Phase checklists, launch checklist, maintenance |
| [docs/14-ui-design.md](docs/14-ui-design.md) | UI/interaction spec: wireframes, tokens, components, keyboard model |
| [docs/15-msp-hardening.md](docs/15-msp-hardening.md) | MSP multi-tenant ops, GDAP bundles, customer hardening baseline |
| [docs/16-client-troubleshooting-toolbox.md](docs/16-client-troubleshooting-toolbox.md) | On-device diagnostics: dsregcmd, IME logs, Outlook/Teams/OneDrive repair ladders, field network tests |
| [docs/17-tenant-verification.md](docs/17-tenant-verification.md) | Everything that needs a real tenant: gates, deep links, licensing claims, naming, behaviour |

Prepared artifacts (beyond docs): `vendor/cmdms-commands.csv` + `.meta.json` (pinned
upstream, commit `4cf2aa6`), `tools/analyze_upstream.py` (invariants verified),
`content/overrides.csv` (category remaps + 49 sovereign folds + 3 heuristic exceptions),
registry seeds `content/roles.csv` (~45), `content/licenses.csv` (~38),
`content/tables.csv` (~48), `content/synonyms.csv` (~95 acronym expansions),
`content/enrich-power.csv` (synthetic `ppage`).

## 10. Risks

| Risk | Mitigation |
|---|---|
| Portal URL churn breaks deep links | quarterly link check, `verified` stamps, prefer stable root portals + documented click-paths for fragile blades |
| Scope explosion (the ecosystem is bottomless) | phases ship independently; every phase is useful alone |
| Upstream cmd.ms changes schema/moves | pipeline pins a commit, diff-review on sync, our own data never depends on upstream shape |
| Licensing/role facts go stale | facts carry `verified` dates, corrections are one-line data edits |
| Blade URLs behind auth cannot be link-checked | treat 200/302-to-login as alive, only flag DNS/404 |

## 11. Definition of done, v1

- All cmd.ms commands imported, searchable, redirect-capable, attributed.
- Acronym searches resolve (`air`, `zap`, `asr`, `tap`, `gdap`, `ueba`, ...); with
  `mdo-p2` in the license profile, searching `air` badges the AIR records as included.
- At least 150 records enriched (path, roles, license, docs, ps).
- Sentinel settings encyclopedia complete enough that "any specific Sentinel setting" resolves
  to a page + path + role + license.
- Installable PWA, offline shell, Lighthouse a11y/SEO green, deployed to ms.labidi.eu with
  family launch checklist done.
