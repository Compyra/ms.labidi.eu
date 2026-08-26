# todo.md : phase audits + carry-over work

Working file per the "check previous phases before starting the next" rule.
Statuses: [x] fixed, [>] deferred to a named phase, [ ] open.

## Phase 0 audit (docs + seeds), 2026-08-26

- [x] All 17 docs present; every PLAN link resolves; no real TODO/TBD markers.
- [x] Seed bug: enrich-power.csv referenced role `pp-admin`, registry id is `ppadmin`.
- [x] LICENSE file was missing although doc 12 §7 promises MIT: added repo LICENSE.
- [x] .gitignore missing (Python cache noise): added.
- [x] doc 14 §9 claimed the sitemap lists all hubs: hash routes are fragments and
      invisible to crawlers; doc corrected to canonical-page-only sitemap.
- [x] doc 14 §10 open design decisions blocked phase 2: settled (brand `[::]`,
      compact rows only, recents kept with clear button, one accent color).
- [ ] Nothing committed to git yet (repo has only the initial README commit).
      Suggest a local commit after phase 2 review; push stays a user decision.
- [>] VERIFY-tagged volatile facts sweep: phase 4 as planned.

## Phase 1 audit (pipeline + search MVP), 2026-08-26

- [x] BUG (verified live): synonym boost ignored other query tokens, so
      `air xyzzy` still returned the AIR records. Fixed: every token must be
      satisfied (text match or synonym-boost membership) before scoring/boost.
- [x] BUG: `aria-controls="listbox"` dangled while the tiles view showed (no
      such element). Fixed by the phase 2 view refactor (listbox exists whenever
      results render; expanded state already toggled).
- [x] CSP lacked `manifest-src`/`worker-src` needed for PWA: added with phase 2.
- [x] Toolbox tile leads to "0 hits" dead end: hub view now explains records
      arrive with phase 3 enrichment.
- [>] SW precache list is maintained by hand in sw.js; generate it from
      build_data.py in phase 8 (launch hardening) to prevent drift.
- [>] tools/check_links.py and sync_upstream.py not yet written: phase 9 items,
      unchanged.
- Notes, by design (do not "fix"): resolveGo('ca') is null (synonym, not alias);
  upstream `puauditg` URL points at .com (flagged in overrides.csv).

## Phase 2 doublecheck (2026-08-26, second pass)

Verdict before the pass: NOT complete: three real defects found, all fixed, assets
bumped to `?v=3` + cache `mshub-v3` (changed files were precached).

- [x] WCAG AA: light theme had no `--ok/--warn/--bad` overrides (amber on light
      chip ≈ 1.6:1). Added AA-safe values (#146b41 / #8a5a00 / #b3261e). Measured
      programmatically across the full token-usage map: dark min 5.11, light min
      4.75, zero failing pairs.
- [x] ARIA: `role="option"` was stamped on rows outside any listbox (hub/recents).
      `makeRow(rec, asOption)` now only sets it for search results; verified no
      stray option roles in any view.
- [x] SW shell poisoning: any navigation response (including 404s) was cached as
      `./`. Now only `res.ok` responses for `/` or `/index.html` update the shell;
      verified offline app still serves after visiting a 404 path online.
- [x] OpenSearch descriptor verified over HTTP (200, text/xml, correct template).

## Phase 2 carry-over (audited at phase 2 close, 2026-08-26)

- Phase 2 shipped and gate passed (offline, installable, keyboard-only, cards/hubs).
- [>] Real PNG icons (192/512 + maskable) and og:image: phase 8. SVG icon ships now
      (installable in Chromium).
- [>] Hub grouping uses `group` field when present, else kind sections; groups
      arrive with phase 3 enrichment.
- [>] License profile + "included in your licensing" badge: phase 3 (needs
      enriched license fields).
- [>] SW precache list maintained by hand in sw.js; generate from build_data.py in
      phase 8 to prevent drift (repeat of phase 1 note, still true).
- [ ] DEV RULE while sw.js is registered: before re-testing any edit, unregister
      the SW + delete `mshub-*` caches (or bump `?v=` + CACHE), else stale assets
      serve and edits look ignored.
- [ ] Local git commit of phases 0-2 output pending (user decision; push separate).
