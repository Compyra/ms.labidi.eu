# 14 : UI & Interaction Design

The visual and interaction contract for phases 1-2. Everything here is implementable with
hand-written CSS + vanilla JS; nothing requires a framework, icon font or web font.

---

## 1. Design intent

Terminal-adjacent, not terminal-cosplay: cmd.ms's ASCII charm acknowledged, then traded
for legibility under stress. The target user is mid-incident with 40 tabs open; the site
must read at a glance, work one-handed on keyboard, and never animate anything that
delays a click. Dark by default (SOC lighting), light theme equal-quality.

## 2. Layout wireframes

### Home (`/`)
```
+----------------------------------------------------------------------+
| [::] ms.labidi.eu          [search__________________]  [cloud] [sun] |
+----------------------------------------------------------------------+
|  > 355 commands. Type to filter. / focuses. Enter opens first hit.   |
|                                                                      |
|  [ Entra ]  [ Intune ]  [ Defender ]  [ Sentinel ]  [ Azure ]        |
|  [ M365 ]   [ Purview ] [ Power ]    [ Windows ]   [ Automation ]    |
|  [ Licensing ]  [ My Pages ]                                         |
|                                                                      |
|  Recently used (localStorage, max 8, clearable)                      |
+----------------------------------------------------------------------+
| data incl. cmd.ms (MIT) - about - keyboard help (?)                  |
+----------------------------------------------------------------------+
```

### Search results (same page, list replaces tiles as you type)
```
|  enca      Conditional Access                 Entra > Protection  [opener]
|  enac      Authentication context             Entra > Protection
|  xdranalytics  Analytic Rules                 Sentinel > Content
   ^ row = [id chip][name][subject > group breadcrumb][kind badge][cloud chips]
```

### Record card (`#/c/enca`)
```
| enca  (aliases: adca, ca)                       [portal] [cmd.ms]    |
| Conditional Access                                                   |
| Entra admin center > Protection > Conditional Access                 |
| Create and manage Conditional Access policies.                       |
| [ Open ]  [ Copy URL ]  [ Copy go-link ]        clouds: [com] [gcch] |
| Role: Conditional Access Administrator   License: Entra ID P1        |
| PowerShell: Get-MgIdentityConditionalAccessPolicy          [copy]    |
| Docs: learn.microsoft.com/entra/...                                  |
| Related: enauthstrength, enidp, enac                                 |
```

Subject hub (`#/s/entra`): h1 + group sections in doc-declared order, rows identical to
search rows (one component). Settings records add a blast-radius badge:
`[low]` gray, `[med]` amber, `[high]` red with "Friday test" tooltip.

Library views (`#/kql`, `#/ps`): same row component grouped by subject, each row
copying its code instead of a URL. Library cards (`#/c/kql-*`, `#/c/ps-*`) show
subject, table or module, required scope/role, tags, docs, a wrapped `pre.code` block,
Copy + go-link buttons and "Used with" links back to records. Record cards carry the
reverse: a "Queries & snippets" section listing library entries that reference them.
The table registry (`#/tables`) is a five-column table inside an `overflow-x` wrapper
(notes column hides under 720px) with per-table query counts linking into search.

## 3. Design tokens

| Token | Dark (default) | Light |
|---|---|---|
| `--bg` | `#0b0e14` | `#f7f8fa` |
| `--bg-raise` | `#131826` | `#ffffff` |
| `--text` | `#dbe2f0` | `#1a2233` |
| `--text-dim` | `#8b95ab` | `#5a6478` |
| `--accent` | `#4cc2ff` (MS-cyan adjacent) | `#0067b8` |
| `--accent-2` | `#9d7cff` | `#6b4fd8` |
| `--ok` / `--warn` / `--bad` | `#3fd68f` / `#ffc24b` / `#ff6b7a` | darkened equivalents |
| `--chip-bg` | `#1b2233` | `#e8ecf4` |
| `--focus` | 2px solid `--accent`, 2px offset | same |

All pairs must pass WCAG AA on their actual backgrounds (audit with the transition-free
measurement recipe; transitions disabled during tests). Radius 8px cards / 999px chips;
spacing scale 4-8-12-16-24-32; max content width 880px, results full-bleed to 1100px.

Typography: `ui-monospace, "Cascadia Mono", Consolas, monospace` for ids/paths/code;
`system-ui, "Segoe UI", sans-serif` for prose. No webfonts (CSP + speed). Base 16px,
rows 15px, chips 12.5px.

## 4. Component inventory (phase 2 build list)

1. `topbar`: brand glyph `[::]` + wordmark, search input, cloud select, theme toggle.
2. `palette`: the search input + results listbox (ARIA combobox pattern:
   `role="combobox"` input, `role="listbox"` list, `aria-activedescendant` tracking).
3. `result-row`: id chip, name, breadcrumb, badges. One component everywhere.
4. `record-card`: full schema render (§2 wireframe).
5. `chip`: id, alias, cloud, kind, table, role variants.
6. `badge`: `cmd.ms` attribution, `deprecated`, blast-radius, `verified YYYY-MM`.
7. `copy-btn`: clipboard write + 1.2s "copied" swap; graceful `document.execCommand`
   fallback not needed (https + modern browsers only).
8. `subject-tile`: glyph + name + record count.
9. `kbd-help`: `?` overlay listing shortcuts.
10. `footer`: attribution, about, GitHub link.
11. `toast`: single slot, used by copy errors + SW "update available, reload".

Glyphs: text/inline-SVG only. Subject glyphs are two-char monospace marks
(EN, IN, DF, SN, AZ, 365, PU, PW, WN, {}, LI, MP, TB, MY) inside colored chips: zero icon assets.

## 5. Keyboard model

| Key | Context | Action |
|---|---|---|
| `/` or `Ctrl+K` | anywhere | focus search, select existing text |
| `ArrowUp/Down` | search focused | move active result (wraps) |
| `Enter` | result active | open record card |
| `Ctrl+Enter` | result active | open portal URL in new tab directly |
| `Shift+Enter` | result active | copy portal URL |
| `Escape` | results open | clear query, then blur |
| `g` then subject key | anywhere (not typing) | jump to hub (g e = entra, g s = sentinel...) |
| `?` | anywhere (not typing) | keyboard help overlay |
| `t` | anywhere (not typing) | theme toggle |

Never trap focus except in the `?` overlay (standard dialog semantics + focus return).

## 6. States & edge cases

- Empty query: tiles + recents (recents stored as ids only; render from data).
- No results: "no hits for X" + two escape hatches: search cmd.ms upstream (link) and
  search Microsoft Learn (link with query). Both plain links, no runtime fetch.
- `?go=` miss: same no-results view with the query prefilled.
- Unknown `#/c/<id>`: soft 404 panel inside the shell + link home (hard 404.html only for
  real bad paths).
- Offline: SW serves shell + data; badge "offline" in topbar when `navigator.onLine`
  is false; external Open buttons still render (they simply fail like any offline link).
- JS disabled: `<noscript>` block listing the fourteen hub anchors as plain links into a
  static fallback note (data requires JS; accepted).

## 7. Responsive rules

- Breakpoints: 720px (single column, tiles 2-up, breadcrumb wraps under name), 480px
  (id chip above name, badges collapse into overflow "+n" chip).
- Grid: `minmax(0, 1fr)` everywhere; `min-width: 0` on row text; `[hidden]{display:none
  !important}` in the reset (both are prior-incident rules).
- Sticky topbar: `position: fixed` + sentinel spacer, heights measured into a CSS var
  (never hard-coded; two-row wrap on narrow screens must not break anchors).
- Touch targets >= 40px on coarse pointers; hover-only affordances forbidden (copy
  buttons always visible, dimmed not hidden).

## 8. Motion & performance budget

- Transitions: opacity/transform only, <= 120ms, all inside
  `@media (prefers-reduced-motion: no-preference)`.
- Budgets: HTML < 15KB, CSS < 25KB, app JS < 35KB, data JS ~ 150-250KB total (split per
  subject, loaded with `defer`; search index built once at load, target < 30ms for 700
  records). No layout shift after first paint: search box and tiles have reserved sizes.
- Zero runtime network beyond same-origin static files (CSP `connect-src 'none'` stands;
  SW fetch handler exempt).

## 9. SEO/meta specifics (phase 2 checklist feeds)

- Every hub gets a crawlable static anchor (`<a href="#/s/entra">`) in the noscript/footer
  so the hash routes are reachable; the sitemap lists canonical pages only (hash
  fragments are invisible to crawlers).
- Title pattern: `enca - Conditional Access | ms.labidi.eu` set on route change.
- OG image: single static card (terminal-frame brand, 1200x630), no per-record generation.

## 10. Design decisions (settled 2026-08-26, phase 2 builds on these)

1. Brand mark: `[::]` (monospace glyph, doubles as favicon/PWA icon).
2. Result row density: compact only (~36px); audience is technical, no toggle.
3. Recents on home: kept; localStorage ids only, with a visible clear button.
4. Accent: one accent everywhere + neutral chips; per-subject hues rejected (AA
   maintenance cost across two themes).
