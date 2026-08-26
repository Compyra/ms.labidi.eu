# todo.md : phase audits + carry-over work

Working file per the "check previous phases before starting the next" rule.
Statuses: [x] fixed, [>] deferred to a named phase, [ ] open.

## Phase 7 integration doublecheck (2026-08-26)

Built tools/audit_consistency.py (now permanent, wired into the phase 9 loop): it
cross-checks matrix min/alsoIn against related records' license fields through the
bundle closure, hunts deprecated targets, dangling lic- references, thin error-code
descs and orphaned registry SKUs. Findings:

- [x] Real bug: the avd-ext pseudo-SKU was not reachable in any includes[] chain, so
      an M365 E3/E5/F3/Business Premium profile never badged the AVD records or the
      lic-avd row as included. Wired avd-ext into those bundles and win-e3; verified
      live (E3 profile now covers azavd and lic-avd).
- [x] Wrong cross-link: lic-mde-air (device AIR) pointed at deinvestigations, which
      is the MDO email-AIR record: exactly the P2-vs-P2 confusion the air card
      exists to prevent. Now points at the air disambiguation card.
- [x] Coverage hole: sam-spo sat in the registry with no matrix row; added
      lic-sam-spo (min sam-spo, alsoIn copilot-m365 per current bundling terms,
      tenant-check under docs/17 C). Matrix now 81 rows.
- [x] Triaged as correct (not bugs): 7 remaining audit-A hits are premium rows
      deliberately linking baseline surfaces (endpoint DLP row -> pudlp portal at
      E3, etc.); 3 registry "orphans" (bus-basic, bus-std, m365-f1) are base SKUs
      kept for the profile picker.
- [x] Cross-phase fit re-verified: ?go=lic-* falls back to cards, error-code records
      carry no urls, no lic- ids leak into library/runbook related fields, suite
      green with zero skips/pendings (39 py, 69/69, 66 browser) at v=17.

Phase 8 prep: already complete (previous entry); execution items remain
prod-dependent (Lighthouse, deploy, DNS/Cloudflare, family registry, live gate).

## Phase 7 close-out check + phase 8 prep (2026-08-26)

Phase 7 verified finished: roadmap DONE, both python gates enforcing and green,
"is this E3 or E5" answerable in one search; only tenant items remain (docs/17 C).

Phase 8 prepared (and its two pending gates flipped to enforcing):

- [x] Brand PNGs via tools/make_icons.py (Pillow, supersampled): 192/512 any,
      512 maskable (safe-zone glyph), apple-touch 180, favicon-32, 1200x630 OG
      image (eyeballed before shipping). Manifest + head wired: og:image absolute
      URL with dimensions, twitter card, apple-touch and PNG favicon links.
- [x] Versioning single-sourced: content/version.txt -> build rewrites every ?v=
      token in index.html/404.html and generates sw.js from tools/sw_template.js;
      the precache enumerates data/*.js from disk so a new data file can never be
      forgotten again. Manual three-file version sweeps are gone. v=17.
- [x] Suite now runs with ZERO skips and ZERO pendings: 39 python + 69/69 parse +
      66 browser. Manifest JSON and all PNG headers/dimensions verified offline
      (the in-page fetch check wedged on our own connect-src 'none' CSP: expected).
- [ ] Phase 8 execution remaining (needs prod/user): Lighthouse pass, GitHub Pages
      deploy + DNS/Cloudflare, family registry updates (labidi.eu repo), README
      attribution polish, live gate (?go=enca from prod, PWA install).

## All-subject coverage audit (2026-08-26, follow-up to the purview question)

Inventoried every subject for its own layer (own records, settings, concepts, hub
groups). Sentinel/defender/intune/entra/purview/toolbox/msp passed; five did not:

- [x] windows 4 -> 23: settings-windows.csv (W365 provisioning/ANC/user settings/
      remote actions/Boot-Switch-Frontline; AVD host pools, app groups, scaling,
      RDP properties, Start VM, Shortpath, Teams optimization, FSLogix, agent
      servicing, required endpoints; UP connectors; safeguard holds) +
      enrich-windows.csv (groups on the 4 upstream records; devbox + winrelhealth
      portals; new Printer Administrator registry role). New python gate mirrors
      the purview one (>=12 settings, groups, no hedge markers).
- [x] licensing 5 -> 10: assignment mechanics, lifecycle stages, removal-impact
      flagship, channels/NCE, self-service purchase toggle; groups on all rows.
      Record ids deliberately avoid the reserved lic- matrix prefix (licassign,
      liclifecycle, licremoval, licchannels).
- [x] power 13 -> 18: gateways portal, environment types + default trap, managed
      environments, publish-to-web (fabricadmin, public-exposure warning), CoE kit.
- [x] mypages 9 -> 11: mysignins + mydevices were genuinely missing self-service
      links (upstream never had them); shipped with shareText per the test contract.
- [x] automation 10 -> 11: Graph throttling / polite-scripts concept.
- [x] Caught during the pass: unquoted commas in one desc (win365) misaligned the
      CSV columns (build caught it); a garbled docs URL in licchannels (dropped
      rather than shipping a guessed slug); rb-* ids in record related (records
      validate against records only); the mypages test pinned ==9 (hard-coded
      count lesson again: now >=9). Total 503 -> 535 records at v=16; 39 py tests
      + 65 browser green; windows hub verified live (5 groups, search chains
      portal -> setting -> runbook).
- [>] azure/m365 walls stay documented backlog (org-settings ~60 toggles, Azure
      role encyclopedia); breadcrumb walks: docs/17 B6 + new B7.

## Purview coverage audit (2026-08-26, user question "are all purview portals and settings added?")

Honest answer was NO: all 19 upstream cmd.ms portals were imported (sovereign twins
folded) but Purview never got a phase-4 settings pass and doc 07 §2 was unbuilt.

- [x] enrich-purview.csv: groups (7), least-priv Purview role groups (incl. two new
      registry roles: Audit Reader, Records Management), license gates and descs for
      all 19 portals; three missing own portals added: puib (Information barriers),
      pudspmai (DSPM for AI), pualerts (Alert policies).
- [x] settings-purview.csv: 20 settings/concept records covering doc 07 §2: audit
      enable/retention, the which-log flagship, mandatory labeling, auto-label
      client-vs-service, one-way co-authoring toggle (blast high), custom SITs, EDM,
      trainable classifiers, DLP mode ladder (blast high), Endpoint DLP, DLP-alerts-
      moved concept, the four retention-precedence principles, adaptive scopes, PST
      import, hold-vs-retention, search syntax, IRM templates, role-groups model,
      Copilot readiness bundle. Purview 19 -> 42 records; total 503. v=15.
- [x] Caught before shipping: two "?" hedge markers had leaked into path text; a new
      python gate asserts >=15 set-pu- records, groups on the hub, and NO hedge
      markers in paths. 38 py tests + 65 browser green; hub verified live (7 groups).
- [>] Breadcrumb walk of every Purview path: docs/17 B6 (tenant).
- [ ] Doc 07 backlog unchanged: SIT catalog (100+), audit activities encyclopedia.

## Phase 7 execution (2026-08-26)

Pre-phase audit: the prerequisite audit below (commit 8b0d5cf) certified gates,
registry integrity and source material before work started.

- [x] Matrix grown 14 -> 80 rows across 9 subjects; 5 new registry SKUs (win-e3,
      win-e5, exo-p1, exo-p2, teams-phone) and completed includes[] chains
      (E3/E5 carry EXO P2 and Windows E3/E5; Business plans carry EXO P1).
- [x] Error-code encyclopedia 4 -> 41 records (28 AADSTS, 3 enrollment, 10 NDR);
      only documented meanings shipped, each with the first fix move and docs link.
      Total records 443 -> 480.
- [x] #/licensing view + lic cards + kind:lic search (SKU ids AND display names
      indexed); home tile, footer, noscript, help updated. v=14.
- [x] Bug found by the browser walkthrough, not by the assertions: coveredByProfile
      was one-hop only, so an M365 E5 profile failed to highlight MDE P1 / Entra P1 /
      free rows (E5 -> MDE P2 -> MDE P1 needs two hops). Replaced with a transitive
      closure built at profile-set time; free tier counts once any SKU is owned.
      Verified live: owned rows 36 -> 52 with the same profile. Selftest-guarded.
- [x] Search-text gap: the word "licensing" was not in lic-row index text (only
      "lic license"), so "licensing pim" missed; fixed and asserted.
- [x] Gates flipped to enforcing: python 37 tests (80-row shape gate + error-code
      family gate; only phase-8 skips remain), 69/69 PS parse, 65 browser assertions
      ALL PASS. Content sweep on new CSVs clean (no dashes, BOM, VERIFY, TODO).
- [>] Tenant verification of license claims: docs/17 section C, new C9 spot-check.
- [ ] Phase 8 (launch) remains: PNG icons + og:image, final sweeps.

## Phase 6 doublecheck + phase 7 prep (2026-08-26)

Phase 7 prerequisite audit (run after prep, certifying its foundations):

- [x] Gates green on the committed tree (36 py, 69/69 parse, 56 browser + 2 pending).
- [x] License registry integrity: 40 SKU ids; every shipped `record.license` resolves;
      every seed row's min/alsoIn resolves; no dangling `includes[]` bundle ids.
- [x] Source material present: doc 11 §2 priority list, doc 02 Intune plan table,
      doc 03 Defender plan table, doc 07 E3-vs-E5 pointers, doc 09 W365/AVD; error
      code sources in doc 01 §7, doc 02 §6.7, doc 06 backlog.
- [x] coveredByProfile (direct + bundle + none) selftest-verified: matrix highlighting
      can build on it.
- [ ] Execution will need 1-2 new registry SKUs (Windows 10/11 Enterprise E3/E5 for
      AVD/Windows rows); Teams Rooms Pro stays no-claim until docs/17 C6 verifies.
- [>] Licensing rows are not yet in the search index and there is no #/licensing view:
      deliberate, that IS phase 7 execution (roadmap).

Phase 6 audit result: content sweep clean (26 runbooks: no em-dashes, no BOM, no
VERIFY, no TODO, no stray URLs), all gates green, one real inconsistency found:

- [x] The copy chip on url-less rows (runbooks, concepts) said "Copy URL" but copied
      the bare id, useless in a ticket. Rows and Shift+Enter now copy the shareable
      go-link (`https://ms.labidi.eu/?go=<id>`) for url-less records; help text
      updated; selftest-guarded ("url-less row copy yields a shareable go-link").
- [x] Verified non-issues: runbook rows navigate correctly from the copy-chip branch,
      recents accept runbook ids, `?go=rb-*` falls back to the card, runbook data
      deterministic across double builds (hash test).

Phase 7 prepared:

- [x] `load_licensing()` pipeline: `content/licensing.csv` -> `data-licensing.js`,
      validating lic- prefix, uniqueness, subject, min/alsoIn against the license
      registry, related resolution, no VERIFY. 14 verified seed rows spanning 8
      subjects prove the shape (doc 12 §3.5).
- [x] Error-code record pattern proven: `enrich-errorcodes.csv` (per-row category)
      ships AADSTS50076, AADSTS53003, 0x80180018 and NDR 5.7.1 as concept records;
      verified live: search "mfa required error" and "bounce 5.7.1" hit them.
- [x] Gates strengthened but count-tolerant: python phase-7 test validates shape
      (prefix, kind, feature, registry membership, docs link) and skips below 80;
      selftest adds "licensing seed rows complete" (pends until the file exists).
      Runner green at v=13: 36 py, 69/69 parse, 56 browser + 2 pending.
- [ ] Phase 7 execution: grow the matrix to ~80 rows, top-40 AADSTS + enrollment +
      NDR sets, `#/licensing` view with license-profile highlighting (roadmap).

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
