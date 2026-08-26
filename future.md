# future.md : remaining steps, improvements, requested features

Project state 2026-08-26: phases 0-8 complete, phase 9 maintenance loop operational,
live at https://ms.labidi.eu (537 records, 81-row license matrix, 41 error codes,
26 runbooks, 60 KQL, 69 PS; 41 python + 66 browser assertions green; prod selftest
66/66). This file is the forward log: what is left, what would make it better, and
what tools of this family get asked for. Statuses: [ ] open, [~] partially covered.

## 1. Blocked on things code cannot provide

- [ ] **Tenant verification** (docs/17, the big one): work sections A-G top to
      bottom when a test tenant arrives. Blocking gates first: A1 run 10 PS
      snippets unedited, A2 10 KQL queries return rows, A3 top-50 deep links land
      on the right blade, A4 role claims least-priv AND sufficient, A5 a service
      desk shift uses two runbooks unaided. Then B deep-link walks (B1-B7 incl.
      Purview and Windows breadcrumbs), C licensing claims (C1-C9 incl. the
      matrix spot-check), D naming/lifecycle, E behaviour claims, F importable
      data, G no-claim records.
- [ ] **Human gates**: first real PWA install from prod; runbook shift trial
      (same as A5); a colleague using the license matrix for a real quote.
- [ ] **Formal Lighthouse run** on prod (no Node on the dev machine; the manual
      a11y/SEO sweep stands in until then).

## 2. Recurring operations (phase 9 loop)

- [ ] Quarterly (~2026-11, then every 3 months): `check_freshness.py` then
      `sync_upstream.py` then `check_links.py` then `audit_consistency.py`;
      VERIFY-tag sweep of volatile facts; refresh `verified` stamps on touched
      records; adopt upstream host migrations once cmd.ms does (forms/loop
      `.cloud.microsoft` are pending there now).
- [ ] Per Microsoft wave (Ignite/Build): triage new products into subject docs,
      then into records.
- [ ] Watch the issue tracker (`wrong-info.yml` template routes corrections with
      record ids and proof links).

## 3. Content expansion backlog (per subject, from docs 01-16)

- [ ] Entra: CA baseline policy gallery with pitfalls; full AADSTS table as
      records (hundreds; check Learn content licensing first, else link-only);
      sign-in log filter recipes; Entra recommendations feed explained.
- [ ] Intune: ASR rule GUID to friendly-name to recommended-mode table;
      Settings Catalog "where did the GPO setting go" mapping; connector/token
      expiry dashboard runbook; error-code expansion (app install + compliance).
- [ ] Defender: advanced-features toggle encyclopedia completion; Streaming API
      setup decision tree; MDI sensor health error table; MDO preset policy diff
      (Standard vs Strict) as data.
- [ ] Sentinel: connector encyclopedia (100+, generated from curated CSV);
      analytics rule template index by tactic/table; data lake surfaces once GA.
- [ ] Azure: built-in role encyclopedia (the ~40 that matter); Resource Graph
      cookbook as KQL records; CAF pointer cards.
- [ ] M365: org settings encyclopedia (~60 toggles); message trace status code
      table; NDR family expansion beyond the 10 shipped.
- [ ] Purview: built-in SIT catalog (100+); audit activities encyclopedia
      (operation names per workload); DLP condition/predicate reference.
- [ ] Power Platform: connector DLP classification starter matrix; managed
      environments feature comparison; Fabric admin API inventory scripts.
- [ ] Windows cloud: FSLogix error/event encyclopedia; RDP property reference as
      records; Windows App migration notes.
- [ ] Automation: Graph permission reverse index ("what can Directory.Read.All
      actually do"); HTTP/Postman examples parallel to each PS snippet; Azure
      Automation + managed identity recipes.
- [ ] Licensing: SKU GUID to friendly-name dataset (generated, refreshed
      quarterly); matrix expansion beyond 81 rows; trial/expiry calendar recipe.
- [ ] Toolbox: client dialog error-string index (exact text to record); per-OEM
      Android quirk table; localized client path variants.
- [ ] Runbooks: ~69 seed ideas remain across the docs (26 of ~95 built); next
      flagships: Autopilot-not-appearing, Sentinel playbook-did-not-run, guest
      access cross-tenant checklist, restore deleted user end-to-end, DLP false
      positive with change control, monthly MSP security report.

## 4. Product improvements (engineering)

- [ ] **CI**: GitHub Action running the python suite + snippet parse on every
      push (the browser selftest needs Edge; keep it local or use a
      playwright-chromium job). Currently all gates run locally only.
- [ ] Scheduled Action for `check_links.py` + `sync_upstream.py` that opens an
      issue when something breaks or drifts (auto-filing the quarterly loop).
- [ ] Search: typo tolerance beyond the current subsequence fallback (edit
      distance 1 on ids); field weighting (name hits above keyword hits);
      result grouping by kind toggle.
- [ ] SW update toast ("new version available, reload") instead of silent
      next-load refresh.
- [ ] Payload budget: data is ~21 script files; consider lazy-loading library
      data (kql/ps/runbooks/licensing) after first paint if home-load speed
      ever degrades on slow links.
- [ ] Print stylesheet for runbook cards (service desks print checklists).
- [ ] `?copy=id` query action (go-link that lands with the snippet already on
      the clipboard is not possible without a click; a one-click copy landing
      view is).

## 5. Often requested in tools of this family (evaluate before building)

- [ ] Favorites/pinning (localStorage, like recents) and a `g f` hub for them.
- [ ] Custom user aliases (my own `?go=` shortcuts, stored locally).
- [ ] Tenant-aware deep links (`?tenant=` rewriting into portal URLs): privacy
      questions noted in the icebox; would need explicit opt-in and local-only
      storage.
- [ ] Copy-as-markdown for runbooks and cards (ticket-system friendly).
- [ ] JSON export / read-only API of the dataset (it is already static JS; a
      `data/export.json` would cost one build step).
- [ ] Browser extension omnibox keyword (cmd.ms ships one; ours would be a thin
      wrapper over `?go=`).
- [ ] i18n of UI chrome (records stay English; the family start page is 4-language).
- [ ] Community submissions via PR templates on the content CSVs (review gates
      exist: build validation + tests).

## 6. Explicitly not planned (icebox, unchanged)

Per-tenant deep links without the privacy answer, Dynamics 365 depth,
on-prem-only products (Exchange Server, AD DS beyond hybrid), API cost
calculators, alias-collision games with cmd.ms domains, analytics of any kind.
