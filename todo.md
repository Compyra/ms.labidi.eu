# todo.md : phase audits + carry-over work

Working file per the "check previous phases before starting the next" rule.
Statuses: [x] fixed, [>] deferred to a named phase, [ ] open.

## Phase 6 execution (2026-08-26)

Pre-phase audit: the post-interruption doublecheck below served as the full audit of
phases 0-5 (all gates green at v=11, two bugs fixed, nothing carried over).

- [x] 23 runbooks written (26 total across 13 subjects), every `related` id
      build-validated against records and libraries; steps kept to documented,
      generic behaviour so nothing tenant-specific is asserted.
- [x] Accuracy self-review pass over the riskiest claims; three sentences softened
      before shipping (Intune pending-action cancellation, MDE local un-isolation,
      shared-mailbox auto-blocked sign-in): each overstated portal behaviour we have
      not verified. Behaviour claims consistent with the settings cards we already
      ship (daily cap stops security data; grace period vs CA in docs/17 E3/E6).
- [x] `#/runbooks` view, runbook cards (numbered steps, level badge, Copy steps),
      search integration (`kind:runbook`, steps indexed, no go-link), record-card
      "Runbooks" cross-links via `runbooksFor()`, home tile, footer + noscript.
- [x] Gates flipped from pending to enforcing: python phase-6 test (prefix, unique,
      sections, >=4 steps, >=25 rows, >=10 subjects) + 8 new browser assertions.
      Runner green: 36 python (3 skips = phases 7/8), 69/69 PS parse, 54 browser.
- [x] Post-phase sweep: the "filter-only searches are never truncated" selftest
      broke by design when runbooks joined the index (expected-count formula did
      not include them); fixed to sum commands + kql + ps + runbooks. v=12 lockstep
      across index/404/sw. Docs updated: roadmap phase 6 DONE, README/PLAN status,
      doc 12 §3.4, docs/17 gate A5 added (two runbooks used unaided in a shift).
- [>] Human gate open: one real service desk shift uses two runbooks unaided
      (docs/17 A5); runbook step wording gets revised from where testers stall.

## Post-interruption doublecheck (2026-08-26)

Swept everything touched around the interrupted turn; git history confirmed nothing
was lost (the in-progress work landed as `373283b`, the continuation as `8f175a5`).
Two real bugs found in the interrupted code and fixed at v=11:

- [x] Filter-only truncation returned: `cat:defender` matches ~114 items (records +
      library entries) but the cap sliced at 100 and silently hid the rest. Browsing
      filters (no search tokens) are now uncapped; token searches keep the 100 cap.
      Guarded by a selftest assertion that computes the expected full count.
- [x] Shift+Enter on a library search result copied the entry id instead of its code
      (the row copy button was correct; the keyboard path was missed). Fixed and
      covered by a clipboard-stub e2e assertion.
- [x] Verified non-issues while sweeping: runbook ids are intentionally not routable
      yet (phase 6), `?go=` on them falls back to search, home tiles exclude the
      runbook library on purpose, the watchlist KQL passes the lint's pipe-splitting
      by construction, and `check_snippets.ps1` JSON extraction is banner-safe.

## Phase 5 completion sweep + phase 6 prep (2026-08-26)

Checked phase 5 for anything specified but not enabled; three gaps found and closed:

- [x] `ps` hints naming a snippet id now render as links on record cards (doc 12
      promised it; nothing used it). Four records wired (`exmt`, `deqre`, `enlaps`,
      `ensign`) and the build now fails on a `ps` hint that names a missing snippet.
- [x] noscript block omitted the library and table routes; added.
- [x] Offline syntax verification was never built: `tools/check_snippets.ps1` parses
      all 69 PowerShell snippets with the real PowerShell parser, and a Python KQL
      lint checks all 60 queries (balance, quoting, source table known, pipe operators
      known, no trailing pipe). Both wired into `tests/run-tests.ps1`.
- [x] Test-count assertion hard-coded 17 docs and broke when doc 17 landed; replaced
      with a sequential-numbering check that catches gaps and duplicates instead.
- [x] Phase 6 prepared: runbook loader, schema, three seed runbooks, `data-runbooks.js`
      wired at v=10, gates already armed.

## Tenant-dependent work (collected)

All of it now lives in [docs/17-tenant-verification.md](docs/17-tenant-verification.md):
blocking gates (A), deep links and paths (B), licensing claims (C), naming and
lifecycle (D), behaviour we describe but have not observed (E), data worth importing
(F), and the handful of records that deliberately ship no claim until verified (G).
Bring the tenant and we work down that list.

## Phase 5 close + selftest overhaul (2026-08-26)

- [x] Phase 5 finished: library views `#/kql` / `#/ps`, table registry at `#/tables`,
      home library tiles, search integration (`kind:kql`, `kind:ps`, code-text
      matching), library cards with copy actions, and two-way cross-links between
      records and library entries.
- [x] Selftests updated in both layers: python 30 -> 34 tests (library kinds,
      namespacing, cross-link resolution, table registration, plus a new guard that
      every generated data file is actually loaded by index.html *and* the harness);
      browser selftest 24 -> 42 assertions covering search, filters, all three new
      views, library cards and the overflow guard.
- [x] HARNESS BUG (false failures): `dev/selftest.html` loaded unversioned scripts, so
      a cached `search.js` made new tests fail. It now injects every file with a
      per-run timestamp, guaranteeing it tests the working tree.
- [x] HARNESS BUG (false passes/failures): `settle(selector)` returned immediately
      when the selector already existed from the previous view, so two view tests
      asserted against stale DOM. Replaced with predicate/title-based `until()`.
- [x] REAL BUG: search truncated at 50 results, so `kind:kql` silently showed 50 of
      60. Cap raised to 100.
- [x] REAL VIEW BUG: the `#/tables` view overflowed 360px viewports by 277px. Wrapped
      in an `overflow-x` container with the notes column hidden on narrow screens;
      verified 0 overflow and guarded by a selftest assertion.
- [x] Asset version bumped to v=9 (cache `mshub-v9`) after post-v8 edits; lockstep
      test enforces index/404/SW agreement.
- [ ] Open (needs a tenant): execute 10 library snippets unedited (phase 5 gate).

## Phases 0-4 confirmation (2026-08-26)

- [x] Gate suite re-run before touching phase 5: 30 python tests OK, browser
      selftest ALL PASS. Roadmap phases 0-4 all carry DONE + gate-passed notes.
      Confirmed finished, so phase 5 content work started.

## Phase 5 content build (2026-08-26)

- [x] `content/kql.csv` expanded to 60 validated queries with `related` links back
      into records; `content/ps.csv` to 69 snippets with module + role/scope.
- [x] Loader learned the `related` column for libraries and now resolves every id
      against the record set (build fails on a dangling link).
- [x] Validator caught a real gap: `IntuneDeviceComplianceOrg` was used by a query
      but missing from `content/tables.csv`; table registered (49 rows now).
- [x] Two accuracy bugs caught in my own drafts before shipping: the app-secret
      expiry snippet referenced an undefined `$app` variable, and the service
      principal sign-in query needs `Microsoft.Graph.Beta`, not `Microsoft.Graph`.
- [x] Test-harness gap fixed: `dev/selftest.html` never loaded the library data, so
      its phase 5 stubs reported a false PENDING. Now loads both files and adds a
      "library rows complete" assertion (unique ids, required fields, resolvable
      related). Selftest: ALL PASS (27 pass, 3 pending).
- [ ] Remaining for phase 5 proper: `#/kql` and `#/ps` views with copy buttons,
      record cross-links via the `ps` field, `tables.csv` rendered as a lookup,
      and search integration for library entries.
- [ ] Gate still open (needs a tenant): execute 10 snippets unedited.

## Full-check + accuracy audit before phase 5 (2026-08-26)

Drove a fact-by-fact review of every shipped role/license/path/cmdlet claim
("no false or wrong info to users"). 13 corrections shipped:

- [x] Quarantine, Tenant Allow/Block List, Restricted entities, Submissions and
      custom detections claimed Security Operator; management needs Security
      Administrator (quarantine desc now names Quarantine Administrator as the
      least-priv option). Explorer downgraded to Security Reader with a note that
      purging needs the Search and Purge role.
- [x] MFA block/unblock page: Authentication Administrator -> Authentication
      Policy Administrator.
- [x] teamsrooms wrongly claimed Teams Premium; Teams Rooms Pro is a separate SKU
      (license cleared, desc explains).
- [x] exmt message-trace window updated for the V2 era (90 days), old "10 days
      interactive" claim removed.
- [x] SSPR desc now states cloud-user SSPR ships with M365 subs; P1 = writeback.
- [x] inprorem renamed to current product name "Remediations".
- [x] set-sen-commitment role az-sentinelcontrib -> az-la-contrib (workspace op); 
      senworkbooks reader -> contributor (saving edits).
- [x] ps-stale-devices seed had a semicolon where PowerShell needs a comma
      (would have shipped broken code); fixed with proper CSV quoting.
- [ ] OPEN (tenant needed): MDE P1-vs-P2 boundary for custom indicators is cited
      from memory; verify against the live P1/P2 comparison during phase 9 sweep.

## Phase 5 preparation (2026-08-26)

- [x] Pipeline loads content/kql.csv + ps.csv when present: id prefix enforced
      (kql-/ps-), collision check against command ids, subject validated, KQL
      table names validated against tables.csv, single-line code rule documented
      (loader is line-based by design).
- [x] Emits data-kql.js/data-ps.js (window.MSHUB.kql/ps) + library counts in meta;
      index.html + SW precache wired at v=7 (cache mshub-v7).
- [x] 8 + 8 accuracy-checked seed rows (KQL uses single-quote literals to stay
      CSV-safe and valid; every cmdlet/scope vouched for).
- [x] Gates adjusted: partial libraries validate every row then report PENDING
      with counts (python + selftest); full enforcement at 60/60.
- Remaining for phase 5 proper: 52 more KQL + 52 more PS rows, #/kql + #/ps
      views with copy buttons, snippets cross-linked from records via ps field,
      tables.csv rendered as a lookup, search integration for library entries.

## Phase 4 close (2026-08-26)

- [x] Phase 4 complete and gate-passed (see roadmap): 439 records, 30 sentinel
      settings, 15-toggle wall, niche passes across docs 02/03/04/05/08/15.
- [x] Content sweep: shipped data has zero VERIFY markers and zero em-dashes
      (case-sensitive scan; the case-insensitive grep hit only prose "verify").
- [x] View sweep: sentinel hub 12 groups/40 rows renders clean, standards + blast
      rows on cards, 360px overflow-free, selftest ALL PASS (24+5 pending).
- [x] Duplicate-name wart fixed: adlicense/enlicense both rendered as "Licenses"
      in the licensing hub; now "Licenses (M365 admin)" / "Licenses (Entra)".
- [ ] OPEN (needs a live tenant): doc-level VERIFY tags in docs/ (portal URL
      migrations, feature GA states) cannot be resolved from here; shipped records
      deliberately avoid those claims. Revisit when tenant access exists or during
      phase 9 quarterly sweeps.

## Test suite (2026-08-26)

- [x] `tests/test_build.py`: phase 0-2 invariants (vendor/meta match, registries,
      folds, 355-command resolvability, alias uniqueness, deterministic build,
      LF/no-BOM/JSON-parseable output, asset-version lockstep incl. SW precache).
- [x] `tests/test_content.py`: phase 3 gates (enrichment volume, priority areas,
      AIR acceptance, shareText, related integrity, registry) + pending gates for
      phases 4-8 that self-skip with a PENDING message and enforce automatically
      once their data/files exist (settings coverage 25/15 thresholds, VERIFY
      sweep, kql/ps/runbooks/licensing libraries, PNG icons, generated precache).
- [x] `dev/selftest.html`: in-browser harness (family pattern): 24 assertions:
      engine (resolver, ranking tiers, boost constraints, filters), enrichment
      (registry names, coveredByProfile, shareText, blastRadius) and iframe e2e
      (tiles, ARIA lifecycle, cards, hubs, license badge, malformed-hash safety)
      + auto-activating future-data stubs. One harness race fixed during rollout
      (settle predicate matched a stale listbox).
- [x] `tests/run-tests.ps1`: one-shot runner (unittest + headless Edge on its own
      port 8907/throwaway profile). Verified exit 0 green, exit 1 on failure.
- Note: unittest verbose output lands on stderr; the runner treats stderr as text
      (PS NativeCommandError artifact otherwise).

## Phase 3 code review (2026-08-26, post-phase pass)

- [x] BUG: `decodeURIComponent(location.hash)` throws on malformed hashes
      (e.g. an external link ending in a bare `%`), crashing the router.
      Fixed with a safe-decode helper.
- [x] BUG: `?go=<id>` for URL-less records (concepts like `air`) fell back to a
      search instead of the record card, so copied go-links dead-ended.
      Fixed: go-miss now routes to `#/c/<id>` when the id exists.
- [x] Doc-parity gap: doc 12 §5 promises a `role:` filter next to `cat:`/`kind:`;
      it was never implemented. Added (`role:caadmin` filters on rec.roles).
- [x] Content wart: five root-portal enrich rows carried the URL in the `path`
      column (defender/admin/az/in/scp), rendering "Path: https://...". Replaced
      with proper breadcrumb text.
- [x] Phase 4 prep: pipeline + UI now understand optional `blastRadius`
      (low|med|high) and `standards` (cis|scuba|securescore|essential8|ce) columns
      on any content CSV; cards render a colored blast-radius row, high-blast rows
      get a "Friday test" badge; `content/settings-sentinel.csv` and
      `content/settings-defender.csv` exist with seed rows proving the pipeline.
      The bulk encyclopedia authoring remains phase 4 proper.

## Pre-phase-3 audit (2026-08-26)

- [x] Bug hunt on phases 0-2 output: clean except two structural gaps closed during
      phase 3: cards showed raw role/license ids (registry now ships to the client)
      and licenses.csv lacked `includes[]` bundle data (added; validated).
- [x] Local git commit of phases 0-2 done (`1b623ab`, 61 files); phase 3 committed
      separately. Push remains a user decision.
- [x] Phase 3 executed and gate passed (see roadmap): 373 records, 235 enriched,
      128 synonyms, license profile live with the AIR/mdo-p2 acceptance green.
- Test-harness note (not an app bug): reloading while `context.setOffline(true)`
      wedges the embedded tab's protocol queue AND can break the SW install race
      (precache fails offline; `serviceWorker.ready` then never resolves). Verify
      offline only on a fresh page after the SW is active, never via reload-while-
      offline mid-script.

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
- [x] DEV RULE while sw.js is registered: before re-testing any edit, unregister
      the SW + delete `mshub-*` caches (or bump `?v=` + CACHE), else stale assets
      serve and edits look ignored.
- [x] Local git commit of phases 0-2 output done (`1b623ab`); push separate.
