# ms.labidi.eu

MS Portal Hub (working name): a fast, keyboard-first reference site for service desk,
helpdesk, cloud and security engineers in Microsoft environments. Every portal shortcut
from [cmd.ms](https://cmd.ms/) (MIT, by Merill Fernando & contributors), plus deep
settings paths, roles, licenses, KQL, PowerShell and runbooks on top.

**Status: phases 0-7 complete.** 535 records (settings encyclopedias for Sentinel,
Defender, Intune, Purview and Windows cloud, a 41-code error encyclopedia,
blast-radius ratings) plus a 60-query KQL library, 69 PowerShell snippets, a 49-table
registry, 26 runbooks and an 81-row license matrix (feature to minimum license,
highlighted against your license profile), all searchable together with copy-ready
cards. Tenant-dependent facts are collected in
[docs/17-tenant-verification.md](docs/17-tenant-verification.md).

Quality gates: `tests\run-tests.ps1` runs 39 Python tests, a PowerShell parse gate over
every shipped snippet, and a 66-assertion browser selftest.

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
- [docs/00-ecosystem-map.md](docs/00-ecosystem-map.md): the whole ecosystem + portal atlas
- docs/01-11 + 15-16: per-subject deep dives (Entra, Intune incl. the compliance
  enforcement chain, Defender incl. AIR and niche surfaces, Sentinel down to the setting
  level, Azure incl. Arc, M365, Purview, Power Platform, Windows cloud endpoints,
  automation, licensing, MSP multi-tenant hardening, client troubleshooting toolbox)
- [docs/12-data-model-import.md](docs/12-data-model-import.md): schemas + import pipeline
- [docs/13-roadmap-backlog.md](docs/13-roadmap-backlog.md): executable phase checklists
- [docs/14-ui-design.md](docs/14-ui-design.md): UI/interaction spec