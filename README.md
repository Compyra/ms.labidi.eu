# ms.labidi.eu

MS Portal Hub (working name): a fast, keyboard-first reference site for service desk,
helpdesk, cloud and security engineers in Microsoft environments. Every portal shortcut
from [cmd.ms](https://cmd.ms/) (MIT, by Merill Fernando & contributors), plus deep
settings paths, roles, licenses, KQL, PowerShell and runbooks on top.

**Status: phase 4 done (settings encyclopedias).** 439 records: 30 Sentinel settings
down to daily caps and playbook permissions, the 15-toggle Defender advanced-features
wall with blast-radius badges, Intune niche settings, and the phase 3 enrichment.
Next: phase 5 (KQL + PowerShell libraries).

Local dev: `python tools/build_data.py` then `python -m http.server 8905 --bind
127.0.0.1` and open http://127.0.0.1:8905/.

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