---
id: rb-rbac-grant
title: Grant Azure access the right way
level: L2
subject: azure
tags: rbac|least privilege|pim|role assignment
related: azpim|azsubs|azrg|ps-az-role-audit|kql-rbac-assignments
verified: 2026-08
---

## Preconditions
- Owner or User Access Administrator at the scope in question, or the PIM rights to manage eligibility.
- A concrete task description from the requester: "access to Azure" is not a request.

## Steps
1. Translate the task into the narrowest scope that covers it: a single resource beats a resource group, which beats a subscription; management group grants are for platform teams only.
2. Pick the least-privileged built-in role that does the job: Reader to look, a service-specific data or contributor role for the actual work; Owner is for almost nobody, and Contributor only when a narrower role truly does not exist.
3. Grant to a group, not the individual: create or reuse an access group so the next joiner and leaver are membership changes, not new assignment archaeology.
4. Prefer PIM eligible over permanently active for anything that changes state: the engineer activates the role when working, with justification, and it expires after.
5. Record the why: use the assignment description or the ticket link so the next auditor does not have to guess.
6. Have the requester test the task immediately; a wrong guess found now costs minutes, found next week it costs another ticket.

## Verify
- The requester completes their task with the granted role and scope.
- The role assignment audit shows the assignment at the intended scope, on the group, not the user.
- For PIM: activation works and the role shows as eligible, not permanently active.

## Rollback
- Remove the role assignment or group membership; PIM eligible assignments can simply be removed with no standing access to clean up.

## Escalate when
- The request needs Owner, User Access Administrator, or any scope above subscription: that is platform governance, not a desk grant.
- The identity is external (guest) or a workload identity touching production data.
- A deny assignment or Azure Policy blocks the action even after a correct grant.
