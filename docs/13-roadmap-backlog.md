# 13 : Roadmap & Backlog

Executable checklists per phase. A phase is done when every box is ticked and the gate
passes. Phases 1-2 make the site; 3-7 make it valuable; 8 launches; 9 keeps it alive.

Test discipline (added after phase 3): run `tests/run-tests.ps1` before starting and
after finishing every phase. Future-phase gates in `tests/test_content.py` and
`dev/selftest.html` report PENDING today and enforce automatically once the phase's
data exists; a phase is not "done" while its gate still skips.

---

## Phase 1 : Scaffold + import + search MVP (DONE 2026-08-26)

- [x] Repo scaffold: `index.html`, `style.css`, `app.js`, `search.js`, `404.html`,
      `robots.txt`, `CNAME` (`ms.labidi.eu`), `icons/` placeholder, README rewrite.
- [x] `vendor/cmdms-commands.csv` pinned (commit `4cf2aa6`, meta sidecar) + invariants
      verified with `tools/analyze_upstream.py`.
- [x] `tools/build_data.py`.
- [x] `content/overrides.csv` with category remaps + sovereign fold table (doc 12 §2):
      49 folds, 3 exceptions, synthetic `ppage` seeded.
- [x] Synonym/acronym expansion wired into the search index
      (`content/synonyms.csv`, 105 terms; expansion requires all >3-char words,
      boostIds are the primary path).
- [x] Generate `data-commands-*.js`; validation gates all green
      (307 records = 306 cmdms + 1 own; per-subject files + synonyms + meta).
- [x] Search palette: input autofocus, `/` and `Ctrl+K`, arrow/enter navigation,
      ranking per doc 12 §5, result count in header (cmd.ms-style).
- [x] `?go=` redirect path (cloud-aware for folded twin ids) + `#q=` deep-linkable
      searches + `#/s/<slug>` hub routes rendered as `cat:` searches.
- [x] Local check: `python -m http.server 8905 --bind 127.0.0.1`.
- Gate PASSED: all 355 upstream commands searchable and redirect-capable locally
      (377 go-tokens resolved: 306 ids + 71 folded twin ids/aliases, 0 failures;
      `?go=enca` navigates to the Entra portal; `air`/`gdap`/`arc` acceptance
      searches return the right records).
- [x] Hardening pass (same day): valid markup (div host + dynamic `ul#listbox`,
      no div-in-ul), `aria-expanded`/`aria-activedescendant` lifecycle correct,
      `#status` is a polite live region, URL hygiene (stale `?q=`/`?go=` dropped on
      input), Shift+Enter copy feedback on the copy chip + clipboard failure prompt
      fallback, deprecated records rank below successors at equal tier, inline SVG
      favicon (no 404 noise), minimal `sitemap.xml` so robots.txt tells no lies,
      360px layout verified overflow-free via CDP metrics.

## Phase 2 : Hubs, cards, PWA (DONE 2026-08-26)

- [x] Subject hub pages (hash routes `#/s/<slug>`), grouped by `group` field with
      kind-label fallback (groups arrive in phase 3); empty-hub explainer.
- [x] UI per [14-ui-design.md](14-ui-design.md): tokens, components, keyboard model;
      §10 decisions settled first.
- [x] Record permalink cards `#/c/<id>` with Open/copy actions (URL, id, go-link),
      per-cloud open buttons, attribution badge, deprecation banner + successor link,
      related links, title pattern `id - Name | ms.labidi.eu`.
- [x] Cloud switcher (topbar select, localStorage `mshub-cloud`); rewrites open links,
      card buttons and `?go=` resolution (folded twin ids keep their explicit cloud).
- [x] Theme: auto/dark/light cycle (button + `t`), `prefers-color-scheme` respected,
      reduced-motion honored, AA token pairs.
- [x] Keyboard + screen-reader pass: combobox/listbox semantics with dynamic
      `aria-controls`, skip link, focus rings, `g`+letter hub jumps, `?` help,
      Enter=card / Ctrl+Enter=portal / Shift+Enter=copy.
- [x] `opensearch.xml` + help page (`#/about`: keyboard table, keyword setup,
      filters, cloud notes, attribution).
- [x] PWA: `manifest.webmanifest` (SVG icon), `sw.js` `mshub-v2` (network-first
      navigations, precached versioned assets, old-cache cleanup, skipWaiting+claim),
      registered with `updateViaCache:'none'`; assets bumped to `?v=2`.
- [x] `sitemap.xml`, canonical + OG tags, meta descriptions, theme-color; CSP extended
      with `manifest-src`/`worker-src`.
- [x] Recents on home (localStorage ids, max 8, clear button).
- Gate PASSED: offline reload serves the full app (307 records searchable, tiles
      render, search works with network cut); SW active; manifest valid; mouse-free
      navigation verified; 360px card/hub views overflow-free.
- [x] Doublecheck pass (same day): fixed light-theme AA colors for ok/warn/bad
      (measured: dark min 5.11, light min 4.75, no failing pairs), conditional
      `role=option` (valid ARIA in hub/recents), SW shell-poisoning guard (404
      navigations no longer overwrite `./`); assets `?v=3`, cache `mshub-v3`;
      OpenSearch verified over HTTP.

## Phase 3 : Enrichment pass 1 (DONE 2026-08-26)

- [x] `content/enrich-*.csv`: 235 records now carry path + desc (target was 150),
      priority order honored: all Entra Protection, all Defender Settings > Endpoints
      pages, all Intune endpoint security, M365 L1 surfaces, Sentinel settings seed.
- [x] Roles + licenses registries expanded (55 roles, 40 licenses incl. `includes[]`
      bundle links) and shipped to the client as `data-registry.js`; cards render
      role/license NAMES, not ids.
- [x] License profile: "My licenses" checkboxes on the help page (localStorage),
      `included` badge on rows and cards, +5 rank nudge, bundle-aware via
      `includes[]`. Acceptance PASSED: profile `mdo-p2` badges the AIR records on
      an `air` search; `m365-e5` covers via bundle; nothing is hidden.
- [x] Synonym registry at 128 terms (target 120+).
- [x] `related[]` wiring: zero dangling references across 373 records (validated in
      build and re-checked in the browser).
- [x] Own-record additions: 67 shipped this pass (air + scenario maps, Sentinel
      settings seed, toolbox 12, MSP 5, quick-action/restore concepts, mypages
      shareText). Remaining ~130 land with the phase 4 settings encyclopedias as
      planned.
- Gate PASSED: 20-random-card sample all complete (path + desc + role/license/docs);
      spot-checked enca/mymfa/senplaybookperms cards render names, shareText and
      attribution correctly.

## Phase 4 : Settings encyclopedia (DONE 2026-08-26)

- [x] `content/settings-sentinel.csv`: 30 sentinel `setting` records covering doc 04
      §12 (pricing, caps, retention, table plans/RBAC, purge, UEBA, anomalies, fusion,
      health, playbook permissions, onboard/remove, TI upload/TAXII, search jobs/
      restore, resource-context RBAC, workspace manager, CMK, AMPLS) + §15 niche
      concepts (ASIM, cross-workspace, latency, KQL functions).
- [x] `content/settings-defender.csv`: 15-toggle advanced-features wall (tamper, EDR
      block, live response x3, indicator enablers, deception, preview, attack
      notifications, Intune connection, correlation scoping, device discovery) +
      XDR settings (unified RBAC activation, attack-disruption exclusions, email
      notifications) + niche cards (exclusions hierarchy, automation levels, network
      protection stack, custom detections, MDI action accounts, CAAC, priority
      accounts).
- [x] Niche record passes: doc 02 §2.5 chain (partner compliance, co-management,
      check-in timing) + §2.6 corners (LAPS policy, EPM, Remote Help, Cloud PKI, DDM,
      device query, MDMWinsOverGP, scope tags) in `settings-intune.csv`; doc 03
      §2.6/§2.7 (phase 3); doc 04 §15; doc 05 §2.1 Arc (ESU, extensions); doc 06 §1.1
      (phase 3); doc 08 §2.1 (Dataverse security, ALM, flow ops, capacity); doc 15 §3
      (CA starter set, GDAP bundles); doc 16 (phase 3).
- [x] Settings render with `blastRadius` badge + "Friday test" styling; standards
      tags render on cards (verified live).
- [x] VERIFY sweep: shipped records contain zero VERIFY markers (test-enforced).
      Doc-level tags that require a live tenant remain in docs/ as research markers
      (open point in todo.md, revisit in phase 9 sweeps).
- Gate PASSED: 10 arbitrary Sentinel settings all in top-3 search results with
      correct path + role + license + desc; python gates enforce (sentinel settings
      30/25, toggles 15/15, no VERIFY shipped); selftest ALL PASS; 439 records;
      360px overflow-free; duplicate-name sweep clean after disambiguation.

## Phase 5 : KQL + PowerShell libraries (DONE 2026-08-26)

Pipeline loads/validates `content/kql.csv` + `content/ps.csv` (id prefixes, collision
checks against command ids, subject validation, KQL table names checked against
`tables.csv`, `related` ids resolved, single-line code rule), emits `data-kql.js` /
`data-ps.js` + counts in meta, wired into index.html and the SW.

- [x] `content/kql.csv`: 60 queries across entra/defender/sentinel/m365/intune/azure/
      windows/purview, each with table, tags, docs where useful and `related` links
      back into the record set.
- [x] `content/ps.csv`: 69 snippets across Graph, Exchange Online, SharePoint, Teams,
      Az, Power Platform, LAPS and Maester, each with module + required role/scope.
- [x] Library views `#/kql` and `#/ps`, grouped by subject, plus library tiles on the
      home page; every row copies its code with one click.
- [x] Search integration: library entries are indexed by title, tags, table/module and
      code text, filterable with `kind:kql` / `kind:ps`, and reachable as cards at
      `#/c/<id>` (result cap raised to 100 so filter-only searches are not truncated).
- [x] Snippets cross-linked from record cards ("Queries & snippets" section, driven by
      the library's `related` ids) and back again ("Used with").
- [x] Table registry rendered at `#/tables` with per-table query counts linking into
      search; shipped in `data-registry.js`.
- [x] Gates enforce in both layers: python suite (schema, kinds, namespacing,
      cross-link resolution, table registration, no VERIFY) and the browser selftest
      (search, filters, all three views, card rendering, cross-links, overflow guard).
- [x] Offline syntax gates: `tools/check_snippets.ps1` parses every PowerShell snippet
      with the PowerShell language parser (69/69 pass), and a pure-Python KQL lint in
      the test suite checks balance, quoting, source tables and pipe operators (60/60).
- [x] `ps` hints that name a snippet id render as links on record cards, validated at
      build time so a typo cannot ship a dead link.
- [x] noscript block lists the library and table routes alongside the subject hubs.
- [>] Open, needs a tenant: execute 10 snippets unedited (tracked as gate A1 in
      [17-tenant-verification.md](17-tenant-verification.md)).

## Phase 6 : Runbooks : DONE 2026-08-26

Prep 2026-08-26: `load_runbooks()` reads `content/runbooks/*.md` (YAML-ish
frontmatter + `## Preconditions/Steps/Verify/Rollback/Escalate when`), validating id
prefix `rb-`, uniqueness against commands, level in L1/L2/L3, known subject, mandatory
steps/verify/escalate sections, resolvable `related` ids (records *and* library
entries) and absence of VERIFY markers. Emits `data-runbooks.js`
(`window.MSHUB.runbooks`).

- [x] 23 more runbooks written from the seed lists (26 total, 13 subjects covered):
      entra 4 (password reset, MFA re-register, app credential rotation), intune 4
      (wipe vs retire, compliance chain, APNs recovery, BitLocker), defender 5
      (phishing triage, quarantine release, device isolation, compromise), sentinel 2
      (tenant onboarding flagship, cost spike), azure 2 (RBAC grant, Arc
      disconnected), m365 4 (mail trace, offboarding flagship, shared mailbox, name
      change), plus purview, power, windows, automation, licensing, msp and toolbox
      (PRT repair) with one flagship each.
- [x] `#/runbooks` view (grouped by subject) + runbook cards: numbered steps,
      level badge (L1 service desk / L2 escalation / L3 expert), preconditions,
      verify, rollback, escalate-when sections, Copy steps action.
- [x] Runbooks in search (`kind:runbook`, steps indexed), `HUB.runbooksFor()`
      cross-links on record cards ("Runbooks" section), home tile, footer + noscript
      routes; go-links fall back to the card (runbooks have no portal URL).
- [x] Gates enforcing in both layers: python (prefix, uniqueness, kind, title,
      levels, sections, >=4 steps, >=25 rows, >=10 subjects) and browser selftest
      (54 assertions incl. view, card, cross-links, search filter).
- [>] Human gate stays open: one real service desk shift uses two runbooks unaided
      (tracked as gate A5 in [17-tenant-verification.md](17-tenant-verification.md)).

## Phase 7 : Licensing matrix + error codes : DONE 2026-08-26

Prep 2026-08-26: `load_licensing()` reads `content/licensing.csv` into
`data-licensing.js` (`window.MSHUB.licensing`), validating `lic-` prefix, uniqueness,
subject, `min`/`alsoIn` against the license registry, resolvable `related` and no
VERIFY markers.

- [x] 80 matrix rows across 9 subjects, every one with a learn.microsoft.com docs
      link and verified stamp: Entra tiers (CA, risk CA, PIM, reviews, governance,
      GSA, included-for-free rows), Intune Plan 1/Plan 2/Suite splits, the Defender
      P1/P2/MDO/MDI/MDCA/MDB boundaries incl. gotchas (Safe Documents needs E5
      Security not MDO P2), premium Purview set vs E3 baseline, EXO Plan 1 vs 2,
      W365/AVD, bundle-contents rows (E5 Security, E5 Compliance, EMS E3, Business
      Premium, F3 limits). Registry grew 5 SKUs (win-e3, win-e5, exo-p1, exo-p2,
      teams-phone) plus completed includes[] chains.
- [x] Error-code encyclopedia: 41 records in three families: 28 AADSTS (sign-in,
      consent, device-state, automation credentials), 3 Intune enrollment
      (0x801c0003, 0x80180018, 0x80180014), 10 NDR (5.1.x, 5.2.x, 5.4.1, 5.7.x,
      4.4.7), each with cause, first fix move and docs link.
- [x] `#/licensing` view: per-subject tables (feature | minimum | also in), rows
      linking to lic cards, license names from the registry, owned rows highlighted
      from the license profile. Lic cards show minimum/also-in with in-profile
      badges. `kind:lic` search; SKU ids and names indexed so "insider risk license"
      or "safe documents" answer directly.
- [x] Found and fixed while verifying: `coveredByProfile` was not transitive
      (M365 E5 -> MDE P2 -> MDE P1 failed to highlight P1 rows); replaced with a
      closure computed at profile-set time, free tier included once any SKU is
      owned. Selftest-guarded.
- [x] Gates enforcing: python (80-row shape gate + error-code families gate) and
      browser selftest at 65 assertions. Runner green at v=14.
- Gate met in-suite: feature-word searches land on the right matrix row in one
      query ("is this E3 or E5" in seconds); ongoing validation is real desk use.
- [>] Tenant verification of the highest-risk license claims stays tracked as
      docs/17 section C (incl. new C9 matrix spot-check).

## Phase 8 : Launch : DONE 2026-08-26

Prep 2026-08-26: brand PNGs generated by `tools/make_icons.py` (Pillow: 192/512
any + 512 maskable + apple-touch 180 + favicon-32 + 1200x630 OG image), manifest and
head wired (og:image absolute + twitter card + apple-touch + PNG favicon). Versioning
is single-sourced: `content/version.txt` drives `?v=` rewriting of index/404 and
`sw.js` generation from `tools/sw_template.js` inside `build_data.py`.

- [x] A11y/SEO sweep across all 11 views (headless-Edge harness): one finding fixed
      (About kbd table headers); no Lighthouse binary on this machine, so the sweep
      + prod checks stand in; a formal Lighthouse run on prod remains a
      nice-to-have.
- [x] Deployed: both repos pushed; live at https://ms.labidi.eu serving v=18 over
      Cloudflare with Rocket Loader / Email Obfuscation / Analytics confirmed OFF
      (no injected scripts in served HTML).
- [x] robots.txt AI-block prepend verified as expected behavior (Cloudflare managed
      content-signals block above our directives; sitemap line intact).
- [x] Family registry: labidi.eu catalogue shows MS Portal Hub (four languages)
      and todo-rami.md carries the tenant-verification pointer; verified live.
- [x] README: license & attribution section (MIT + cmd.ms provenance + verified-
      stamps policy + issue routing).
- [x] Gate MET: live on https://ms.labidi.eu; PWA install criteria all green from
      prod (manifest + SW + 192/512 icons over HTTPS, correct MIME); `?go=` proven
      live in both directions (enca leaves the origin; unknown ids fall back to
      cards); real 404 status; **dev/selftest.html runs 66/66 ALL PASS against
      production**.
- [ ] Optional follow-ups: formal Lighthouse run; first human PWA install.

## Phase 9 : Maintenance loop (recurring)

- [ ] Quarterly: `sync_upstream.py` diff review; `check_links.py` run;
      `audit_consistency.py` run (matrix vs records vs registry); VERIFY-tag sweep
      of volatile facts (portal hosts, retirements, license names); verified stamps
      refreshed on touched records.
- [ ] Per Microsoft wave (Ignite/Build): new-product triage into subject docs.
- [ ] Issue template for "broken link / wrong role / wrong license" reports.

## Icebox (explicitly not now)

Community submissions, per-tenant deep links (`?tenant=` rewriting: privacy questions),
i18n, browser extension (cmd.ms already ships one), alias collision game with cmd.ms
domains, Dynamics 365 depth, on-prem-only products (Exchange Server, AD DS beyond hybrid
touchpoints), API cost calculators.
