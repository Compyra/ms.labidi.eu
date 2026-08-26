# 13 : Roadmap & Backlog

Executable checklists per phase. A phase is done when every box is ticked and the gate
passes. Phases 1-2 make the site; 3-7 make it valuable; 8 launches; 9 keeps it alive.

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

## Phase 4 : Settings encyclopedia (Sentinel first)

- [ ] `content/settings-sentinel.csv` covering doc 04 §12 table + §3-§11 setting bullets.
- [ ] `content/settings-defender.csv` covering doc 03 §2.5 (incl. advanced-features wall).
- [ ] Niche record passes: doc 02 §2.5 compliance-enforcement chain + §2.6 corners,
      doc 03 §2.6 (AIR et al.) + §2.7 scenario maps, doc 04 §15, doc 05 §2.1 Azure Arc,
      doc 06 §1.1 user-management quick actions + restore matrix, doc 08 §2.1
      support-side, doc 15 §3 hardening baseline (msp hub), doc 16 toolbox records.
- [ ] Settings render kind with `blastRadius` badge + "Friday test" styling.
- [ ] VERIFY sweep: every doc 04 `VERIFY` tag resolved against a live tenant + Learn.
- Gate: the brief's test: pick 10 arbitrary Sentinel settings, all findable by search
      with correct path/role/license.

## Phase 5 : KQL + PowerShell libraries

- [ ] `content/kql.csv` (60 seeds, doc 10 §5), `content/ps.csv` (60 seeds, doc 10 §4).
- [ ] Library views `#/kql`, `#/ps` with language chips + copy; snippets cross-linked
      from records via `ps` field.
- [ ] Table registry (`content/tables.csv`, seed exists) rendered as lookup.
- Gate: 10 snippets executed against a test tenant without edits.

## Phase 6 : Runbooks

- [ ] 25 seeds picked from docs 01-11 + 15 runbook lists (flagships first: doc 06
      §7.1/§7.5, doc 04 §14.1, doc 11 §6.2, doc 15 §7.1/§7.3).
- [ ] Frontmatter pipeline + sanitized HTML embedding (build-time).
- [ ] Level badges (L1/L2/L3), escalate-when sections mandatory.
- Gate: one real service desk shift uses two runbooks unaided.

## Phase 7 : Licensing matrix + error codes

- [ ] `content/licensing.csv` seed 80 rows (doc 11 §2).
- [ ] AADSTS starter set (top 40 codes), Intune enrollment codes, NDR families as records.
- Gate: "is this E3 or E5" answered in <10 seconds for the seed rows.

## Phase 8 : Launch

- [ ] Icons/favicons/OG image; Lighthouse a11y/SEO/best-practices green; CSP headers via
      meta (GitHub Pages limitation noted).
- [ ] Asset versioning bump + SW `CACHE` const set (family rule; Cloudflare 4h edge cache).
- [ ] Deploy to GitHub Pages, DNS + Cloudflare (Rocket Loader / Email Obfuscation /
      Analytics OFF), verify robots.txt AI-block prepend is expected behavior.
- [ ] Family registry updates: `labidi.eu/js/projects.js` (all four language descs),
      `labidi.eu/todo-rami.md`, plus rami.party registries only if it ever lived there
      (it did not; skip tombstones).
- [ ] README: purpose, attribution/NOTICE, local dev, data pipeline how-to.
- Gate: live on https://ms.labidi.eu, PWA installs from prod, `?go=enca` works.

## Phase 9 : Maintenance loop (recurring)

- [ ] Quarterly: `sync_upstream.py` diff review; `check_links.py` run; VERIFY-tag sweep
      of volatile facts (portal hosts, retirements, license names); verified stamps
      refreshed on touched records.
- [ ] Per Microsoft wave (Ignite/Build): new-product triage into subject docs.
- [ ] Issue template for "broken link / wrong role / wrong license" reports.

## Icebox (explicitly not now)

Community submissions, per-tenant deep links (`?tenant=` rewriting: privacy questions),
i18n, browser extension (cmd.ms already ships one), alias collision game with cmd.ms
domains, Dynamics 365 depth, on-prem-only products (Exchange Server, AD DS beyond hybrid
touchpoints), API cost calculators.
