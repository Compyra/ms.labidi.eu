# ms.labidi.eu

MS Portal Hub (working name): a fast, keyboard-first reference site for service desk,
helpdesk, cloud and security engineers in Microsoft environments. Every portal shortcut
from [cmd.ms](https://cmd.ms/) (MIT, by Merill Fernando & contributors), plus deep
settings paths, roles, licenses, KQL, PowerShell and runbooks on top.

**Status: all phases complete, live at https://ms.labidi.eu; maintenance loop
operational.** 537 records (settings
encyclopedias for Sentinel, Defender, Intune, Purview and Windows cloud, a 41-code
error encyclopedia, blast-radius ratings) plus a 60-query KQL library, 69 PowerShell snippets, a 49-table
registry, 26 runbooks and an 81-row license matrix (feature to minimum license,
highlighted against your license profile), all searchable together with copy-ready
cards. Tenant-dependent facts are collected in
[docs/17-tenant-verification.md](docs/17-tenant-verification.md).

Quality gates: `tests\run-tests.ps1` runs 41 Python tests, a PowerShell parse gate over
every shipped snippet, and a 66-assertion browser selftest.

Quarterly maintenance (run every few months, in order):
`python tools/check_freshness.py` (stale stamps + pin age, offline),
`python tools/sync_upstream.py` (cmd.ms drift report, never auto-merges),
`python tools/check_links.py` (link rot + portal host migrations),
`python tools/audit_consistency.py` (cross-layer meaning check, offline).

Local dev: `python tools/build_data.py` then `python -m http.server 8905 --bind
127.0.0.1` and open http://127.0.0.1:8905/.

Version bumps: edit [content/version.txt](content/version.txt) and run the build; it
rewrites every `?v=` token in index.html and 404.html and regenerates sw.js (cache
name + precache list) from [tools/sw_template.js](tools/sw_template.js). Brand PNGs
regenerate with `python tools/make_icons.py` (Pillow).

Tests: `powershell -NoProfile -ExecutionPolicy Bypass -File tests\run-tests.ps1`
(Python pipeline/content gates + headless-Edge browser selftest), or separately
`python -m unittest discover -s tests` and `dev/selftest.html` in a browser.
Future-phase gates report PENDING and enforce automatically once their phase lands.

Project map:

- [PLAN.md](PLAN.md): mission, architecture, phases, risks
- [future.md](future.md): remaining steps, improvements, requested features
- [docs/00-ecosystem-map.md](docs/00-ecosystem-map.md): the whole ecosystem + portal atlas
- docs/01-11 + 15-16: per-subject deep dives (Entra, Intune incl. the compliance
  enforcement chain, Defender incl. AIR and niche surfaces, Sentinel down to the setting
  level, Azure incl. Arc, M365, Purview, Power Platform, Windows cloud endpoints,
  automation, licensing, MSP multi-tenant hardening, client troubleshooting toolbox)
- [docs/12-data-model-import.md](docs/12-data-model-import.md): schemas + import pipeline
- [docs/13-roadmap-backlog.md](docs/13-roadmap-backlog.md): executable phase checklists
- [docs/14-ui-design.md](docs/14-ui-design.md): UI/interaction spec

License & attribution: own code and content are MIT (see [LICENSE](LICENSE)).
Shortcut data includes [cmd.ms](https://cmd.ms/) by Merill Fernando & contributors
(MIT), pinned in [vendor/](vendor/) with commit provenance in
[vendor/cmdms-commands.meta.json](vendor/cmdms-commands.meta.json). This site is not
affiliated with Microsoft; product names belong to their owners. Facts carry
`verified` stamps and docs links; anything tenant-dependent is tracked in
[docs/17-tenant-verification.md](docs/17-tenant-verification.md) rather than claimed.
Found something wrong? Open an issue with the record id.