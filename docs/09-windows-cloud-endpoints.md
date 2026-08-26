# 09 : Windows Cloud Endpoints

Cloud-delivered Windows: Windows 365, Azure Virtual Desktop, Dev Box, plus endpoint-adjacent
services (Universal Print, Windows servicing surfaces) that did not fit doc 02.

Shipped 2026-08-26: `settings-windows.csv` (17 records: W365 provisioning/ANC/user
settings/actions/Boot-Switch-Frontline, AVD host pools through required endpoints,
Universal Print connectors, safeguard holds) + `enrich-windows.csv` (groups/roles/
licenses on the 4 upstream records; own portals `devbox`, `winrelhealth`).
Breadcrumb walk pending: docs/17 B7. Unshipped depth below stays backlog.

---

## 1. Windows 365 (Cloud PC)

- Portals: end-user `https://windows365.microsoft.com` (`win365`), new unified
  `https://windows.cloud.microsoft` `VERIFY`; admin lives inside Intune (Devices >
  Windows 365 `VERIFY` path).
- Admin parts, each a record: provisioning policies, custom images, Azure network
  connection (ANC) health checks, user settings policies (local admin toggle, restore
  point frequency), Cloud PC actions (restart/resize/restore/reprovision/point-in-time
  restore), Windows 365 Boot / Switch / Frontline concepts, alerts (Intune Tenant admin).
- Editions/licensing: Business vs Enterprise vs Frontline table (doc 11 rows).
- Troubleshooting runbook: user cannot connect (license -> provisioning state -> ANC ->
  client version -> UDP/TCP paths).
- Niche: user-initiated restore/restart from windows365.microsoft.com, connection
  quality report, W365 alerts in Intune, **Windows 365 Link** (dedicated thin device)
  `VERIFY` availability, W365 + Universal Print pairing, GPU sizes.

## 2. Azure Virtual Desktop (`azavd`)

- Objects, each a record: host pools (pooled/personal, validation env), app groups
  (desktop/RemoteApp), workspaces, session hosts, scaling plans (autoscale), RDP
  properties (the string builder card), FSLogix profiles (config + common errors runbook),
  MSIX app attach / App attach `VERIFY` naming, custom image templates, Start VM on
  connect, screen capture protection, watermarking.
- Clients: web (`avdweb`), Windows App (new universal client) `VERIFY`, per-platform.
- Monitoring: AVD insights workbook, required diagnostic tables (`WVDConnections`,
  `WVDErrors`: KQL library entries).
- **Connectivity niche**: required URL list + session-host URL validation tool, RDP
  Shortpath (managed networks + public via STUN/TURN) verify-it's-active card, service
  traffic vs media split.
- **Teams on AVD**: media optimization (WebRTC redirector + `IsWVDEnvironment`),
  version pairing checks, what breaks without it (flagship VDI card) `VERIFY` new
  SlimCore/plugin naming.
- **Multimedia redirection** (browser video offload), camera/USB redirection matrix,
  printing via Universal Print in sessions.
- **Session host servicing**: agent + side-by-side stack update mechanics, drain +
  image update cycle (bridge runbook 3), scaling plan ramp behavior.
- Runbooks: user session stuck (logoff via host pool), profile not loading (FSLogix event
  IDs), "no available session host" triage, drain mode for maintenance.

## 3. Dev Box & Deployment Environments (light)

`https://devportal.microsoft.com` (own record) `VERIFY`; dev center/projects/pools records;
audience note: service desks increasingly field these tickets.

## 4. Universal Print (`print`)

Printers, printer shares, connectors, quota model card; register + share runbook; Intune
policy deployment of printers.

## 5. Windows servicing quick surfaces (bridges to doc 02)

Windows release health in M365 AC (own record), known issues + safeguard holds card,
`aka.ms/WindowsUpdateHistory` pointer, Delivery Optimization concept, hotpatch `VERIFY`
availability for client.

## 6. Runbook seeds

1. Cloud PC vs AVD vs RDS decision one-pager (concept, pre-sales-ish but the desk gets
   asked) (L2).
2. Resize a Cloud PC (license swap flow) (L2).
3. AVD golden image update cycle (L3).
4. FSLogix profile corruption recovery (L2).
5. Printer deployment via Universal Print + Intune (L2).

## 7. Backlog

- FSLogix error/event encyclopedia.
- RDP property reference as searchable records.
- Windows App migration notes (client consolidation).
