# 12 : Data Model & Import Pipeline

The technical contract between content (docs 00-11) and the site. Everything the site
renders is data in `data/*.js`; everything in `data/` is generated or hand-authored through
the schemas below.

---

## 1. Source of truth layout (repo)

```
/data/                     generated + published (script-tag JS, window.MSHUB.*)
  data-commands-<subject>.js
  data-settings-<subject>.js      (phase 4+)
  data-kql.js  data-ps.js         (phase 5)
  data-runbooks.js                (phase 6)
  data-licensing.js               (phase 7)
  data-meta.js                    (counts, buildstamp, sources)
/content/                  hand-authored source (CSV/JSON, reviewed in PRs)
  enrich-<subject>.csv            our additions + enrichment of cmd.ms rows
  settings-<subject>.csv
  kql.csv  ps.csv  runbooks/*.md  licensing.csv
/vendor/
  cmdms-commands.csv              pinned copy of upstream, byte-exact (keeps diffs clean)
  cmdms-commands.meta.json        commit hash + date + license of the pinned copy
/tools/
  build_data.py                   the only build step (Python 3, stdlib only)
  analyze_upstream.py             invariant checks + fold-candidate report (exists)
  check_links.py                  quarterly link checker
  sync_upstream.py                fetch + diff upstream CSV, never auto-merge
```

## 2. Upstream import (cmd.ms)

- Source: `merill/cmd` -> `website/config/commands.csv` (MIT). Pinned copy lives in
  `vendor/` with `cmdms-commands.meta.json` sidecar (commit
  `4cf2aa6f95748a8c76f32b6ac579e4687418e809`, 2026-04-17, 41964 bytes); surfaced in
  `data-meta.js` for the footer attribution line.
- Upstream schema: `Command,Alias,Description,Keywords,Category,Url,Icon`; aliases are
  `|`-separated; exactly 355 rows at the pinned commit; `Icon` is unused (0 rows).
  Categories with counts: Azure 93, Defender 71, Microsoft 365 62, Entra 47, Purview 36,
  Intune 28, My Pages 9, General 4, XDR Sentinel 3, Power Platform 2.
- Verified invariants (analyze_upstream.py, 2026-08; build_data.py asserts them forever):
  no duplicate ids, no alias used by two rows, no alias shadowing an id, all URLs https.
- Import rules:
  1. `Command` -> `id` (lowercase, unique; collision with own ids fails the build).
  2. Category -> our slug via the map in doc 00 §1, with row-level overrides in
     `content/overrides.csv` (e.g. `azsentinel` -> sentinel, `win365` -> windows,
     `powerapps` -> power, Sentinel XDR rows -> sentinel).
  3. Sovereign twins (`eng`, `azg`, `defenderg`, `*gcc*`, `*dod`...) fold into the
     commercial record's `clouds` map; the twin's id and aliases are preserved as aliases
     so `defenderg` still resolves. The fold table is written and verified in
     `content/overrides.csv`: 49 folds (39 gcch, 6 gcc, 4 dod) plus 3 heuristic
     exceptions that look like twins but are not (`enpimg` = PIM for Groups,
     `azpg`/`azpgh` = PostgreSQL). Quirks: `puauditg` points at `.com` upstream (kept,
     flagged), and GCC/GCC-High Power Pages fold into a synthetic commercial `ppage`
     record seeded in `content/enrich-power.csv` (upstream has no commercial row).
  4. `Keywords` merge into `keywords[]`; `Description` becomes `name` (upstream uses it as
     the display name), our `desc` comes from enrichment.
  5. Every imported record gets `source: "cmdms"`; enrichment never edits vendor CSV, it
     overlays by `id` from `enrich-*.csv`.
- Sync procedure (quarterly or on demand): `sync_upstream.py` fetches raw CSV, diffs
  against `vendor/`, writes a review file; human approves; commit updates hash.

## 3. Schemas

### 3.1 command (unified link record)
```
id            string, unique, ^[a-z0-9-]{1,32}$
kind          portal | setting | tool | docs | enduser | concept
aliases       string[]
name          string (<= 60 chars)
category      subject slug (doc 00 §1)
group         string, display grouping inside a subject hub
url           string | null (null allowed only for kind=setting|concept with `path`)
clouds        { gcch?, dod?, gcc?, cn?: string|null }
path          string, click-path breadcrumb, "Portal > Area > Page"
desc          string (<= 200 chars)
keywords      string[]
roles         string[] (ids into roles registry)
license       string | null (id into license registry)
docs          string | null (learn.microsoft.com deep link)
ps            string | null (cmdlet or api hint, links into snippet lib when id-prefixed)
related       string[] (command ids)
source        cmdms | own
verified      YYYY-MM | null
deprecated    bool (renders a badge + successor pointer in `related[0]`)
shareText     string | null (enduser kind only)
```

### 3.2 setting (encyclopedia entry, phase 4)
`{id, subject, area, name, what, default, blastRadius: low|med|high, path, url?, roles[],
license, api?, docs, related[], standards[]?, verified}`: `what` and `blastRadius` make
these more than links; they answer "can I flip this at 16:55 on a Friday". `standards`
tags hardening rows against CIS/SCuBA/Secure Score (doc 15 §6) for `standard:` filters.

### 3.3 kql / ps snippets (implemented phase 5)
`{id, title, subject, code, tags[], docs?, verified, related[]}` plus `table` for KQL
and `module` + `scopes` for PowerShell. Loaded from `content/kql.csv` and
`content/ps.csv` by `load_library()`, which enforces: `kql-`/`ps-` id prefixes, no
collision with command ids, unique ids, valid subject slug, KQL `table` present in
`tables.csv`, `related` ids resolving to real records, and title+code non-empty.
**Code must be single-line**: the CSV reader is line-based by design, so multi-line
quoted fields are not supported. KQL string literals use single quotes so no CSV
escaping is needed. Emitted as `window.MSHUB.kql` / `window.MSHUB.ps`, with counts in
`data-meta.js` under `libraries`.

### 3.4 runbook (implemented, 26 shipped)
Markdown files in `content/runbooks/` with frontmatter `{id (rb-*), title, level: L1|L2|L3,
subject, tags, related, verified}` and `## Preconditions / Steps / Verify / Rollback /
Escalate when` sections. `load_runbooks()` parses them into
`{id, kind:"runbook", title, level, subject, tags[], related[], pre[], steps[], verify[],
rollback[], escalate[]}`, converting list items to plain strings at build time (no HTML
is embedded, so nothing needs runtime sanitising). Steps, Verify and Escalate when are
mandatory; `related` may point at records **or** library entries. Runbooks surface as
`#/runbooks` (grouped view), `#/c/rb-*` cards (numbered steps, level badge, Copy steps),
`kind:runbook` in search (title, tags and steps indexed), and a "Runbooks" section on
record cards via `HUB.runbooksFor(recordId)` (reverse lookup over `related`). Levels
read L1 service desk, L2 escalation, L3 expert.

### 3.5 licensing matrix row (implemented, 80 rows shipped)
`content/licensing.csv` -> `data-licensing.js` (`window.MSHUB.licensing`) by
`load_licensing()`: `{id (lic-*), kind:"lic", feature, subject, min, alsoIn[], notes,
docs, verified, related[]}`. Validation: id prefix + charset, uniqueness against
command ids, subject slug, `min` and every `alsoIn` entry present in `licenses.csv`
(so the matrix can never name a SKU the registry cannot render), `related` resolving
to records or library entries, docs link required by the content gate, no VERIFY in
emitted fields. `min` is the cheapest single license that unlocks the feature;
`alsoIn` lists bundles that carry it when the `includes[]` map cannot express it.
Error-code records (AADSTS / enrollment / NDR) are ordinary `concept` records seeded
from `content/enrich-errorcodes.csv`, which carries a per-row `category` column
because it spans subjects.

### 3.6 registries
`roles.csv` (id, name, plane: entra|azure|xdr|workload, notes),
`licenses.csv` (id, name, family, includes[]),
`tables.csv` (KQL table registry: name, product, costTier, retentionDefault),
`synonyms.csv` (term, expandsTo, boostIds[;], note): acronym/synonym expansion for
search. Terms may overlap real aliases (alias wins, synonym adds boosts); boostIds
pointing at not-yet-created own records validate as warnings, not failures; two-letter
terms are curated exceptions to the 3-char minimum.

Roles, licenses **and tables** ship to the client in `data-registry.js`
(`window.MSHUB.registry.{roles,licenses,tables}`): cards render role and license
*names* rather than ids, and `#/tables` renders the table registry.

## 4. Build & validation (`build_data.py`)

- Stdlib only (csv, json, hashlib, pathlib). No pip deps, no Node (machine has none).
- Emits `data/*.js` as `window.MSHUB.commands.push(...)` style assignments, one file per
  subject, LF endings, UTF-8 no BOM (hard rule from past incidents; write bytes).
- Validation gates (build fails loudly): duplicate id/alias across all files, alias that
  shadows an id, empty url on kinds that require one, unknown category/roles/license ids,
  URL not https, name/desc length caps, `related` pointing nowhere, JS string escaping
  (single source of escaping: json.dumps every string).
- Determinism: sorted output, so diffs stay reviewable; buildstamp only in `data-meta.js`.
- `check_links.py`: HEAD/GET every unique host+path; expected outcomes: 200, or 30x to
  login endpoints (count as alive), 404/DNS fail -> report. Auth-walled blades cannot be
  deep-verified; only their host reachability is checked (accepted limitation, PLAN §10).

## 5. Search behavior contract (for app.js, phase 1)

- Index fields with weights: id (10), alias (9), name (7), keywords (5), group+category
  (3), desc (2), path (2).
- Synonym/acronym expansion (`synonyms.csv`): a term match counts at alias weight for
  its boostIds and injects its `expandsTo` tokens into matching. Acceptance example:
  searching `air` surfaces the AIR concept + `deinvestigations` even though no record id
  or upstream alias is "air".
- License profile: optional "my licenses" set (license ids, localStorage). Records whose
  `license` (or its containing bundle via `licenses.csv includes[]`) is in the profile
  get an "included in your licensing" badge and a small rank boost; nothing is ever
  hidden. Acceptance example: profile contains `mdo-p2`, search `air`, the AIR records
  pop up badged as included.
- Matching: exact id/alias first (that is the `?go=` path), then prefix, then all-tokens-
  somewhere, then subsequence fuzzy as last resort; tie-break by weight then shorter name.
- `?go=x`: resolve exact id/alias; hit -> `location.replace(url)` (cloud-aware: a stored
  cloud preference switches to `clouds[pref]` when present); miss -> render search for x.
- Filters: `cat:sentinel`, `kind:setting`, `role:` prefixes in the query string parse into
  facet filters (cheap, no UI dependency).
- Everything renders from data at load; zero network at runtime (CSP `connect-src 'none'`).

## 6. Page rendering contract

- Subject hub = groups in declared order, records as rows (name, id chip, cloud chips,
  open/copy buttons). Record card = full schema render + related links + attribution line
  when `source: "cmdms"`.
- Copy buttons: URL, id, and `ms.labidi.eu/?go=<id>` deep link.
- OpenSearch XML + "add ms as search keyword" how-to page (Chrome/Edge/Firefox steps).

## 7. Licensing & attribution obligations

- Repo carries `NOTICE` section in README: cmd.ms data (c) Merill Fernando & contributors,
  MIT; link to upstream; our additions under repo's own license (MIT to match, keeps
  reuse clean).
- Footer: "Shortcut data includes cmd.ms (MIT)". Per-record badge on cmdms rows.
- Never mirror Microsoft Learn prose; link + paraphrase one-liners only.
