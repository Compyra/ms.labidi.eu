---
id: rb-graph-apponly
title: Graph app-only auth: certificate, least privilege
level: L3
subject: automation
tags: graph|app-only|certificate auth|application permissions
related: graphps|enappreg|enconsent|ps-connect-apponly|ps-find-permission|ps-app-secrets-expiring
verified: 2026-08
---

## Preconditions
- Rights to create an app registration and a Global Administrator available for the consent step.
- The exact task list the automation performs, because permissions get derived from tasks, not guessed.

## Steps
1. Create a dedicated app registration per automation purpose; shared "one app for all scripts" registrations grow into unauditable god-apps.
2. Derive the application permissions from the tasks: use Find-MgGraphPermission (or the Graph docs per API call) and pick the narrowest that works, preferring Read over ReadWrite and resource-specific over Directory-wide.
3. Add those as Application permissions on Microsoft Graph and get admin consent granted; app-only permissions do nothing until consented.
4. Create the certificate: a self-signed certificate from a machine or vault is fine to start; export only the public key to the app registration's certificates, and keep the private key in the certificate store or Key Vault, never in the repo.
5. Connect with the client ID, tenant ID and certificate thumbprint and confirm the context says app-only with exactly the expected scopes; a delegated context here means the connect call was wrong.
6. Run the automation's operations once end to end and remove any permission that turned out unnecessary; the first guess usually over-asks.
7. Schedule the operational hygiene: certificate expiry in the credential inventory, an owner on the app registration, and a note in the script header pointing at this app's purpose.

## Verify
- The script performs its tasks with the app identity and nothing prompts interactively.
- The app registration lists only the consented permissions the tasks need.
- The private key is retrievable only from the intended store or vault.

## Rollback
- Remove the app registration (or just its certificate) to kill the access instantly; automations stop with it, which is also the emergency stop if the identity misbehaves.

## Escalate when
- A requested permission is tenant-wide write (Directory.ReadWrite.All and friends): that needs a security review, not a quick consent.
- The workload can run in Azure: a managed identity with federated credentials removes the certificate problem entirely and should win the design.
- Anyone asks to reuse this app's credentials for a second, unrelated script.
