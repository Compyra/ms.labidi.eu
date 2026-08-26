---
id: rb-account-compromise
title: Account compromise: contain and clean up
level: L2
subject: defender
tags: bec|compromise|containment|incident response
related: scenario-compromise|ensign|enidp|dere|exrules|ps-block-user|ps-revoke-sessions|ps-inbox-rules-user
verified: 2026-08
---

## Preconditions
- Authentication Administrator or higher for credential actions, Security Administrator for mail actions.
- Agree who owns communications before you start; containment is visible to the user.

## Steps
1. Block sign-in for the account and revoke its refresh tokens; do both, because a password reset alone leaves live sessions.
2. Reset the password, and require change at next sign-in.
3. Review registered authentication methods and remove anything the user does not recognise, then re-register with a Temporary Access Pass.
4. Hunt persistence in the mailbox: list inbox rules and remove attacker rules, and check for forwarding addresses at mailbox, remote domain and transport rule level.
5. Check application consent: look for OAuth grants the user approved during the incident and revoke them.
6. Trace what was sent from the account during the exposure window and identify recipients who may have been phished onward.
7. Purge malicious mail sent internally, and submit external samples to Microsoft.
8. Review sign-in logs for the source IP and other accounts hit from it; repeat containment for any that match.
9. Confirm the device used is healthy in Defender before restoring access.
10. Restore access: unblock sign-in, confirm the user can sign in with the new credentials and methods.

## Verify
- Risk state for the user is dismissed or remediated, and no new risky sign-ins appear.
- No inbox rules or forwarding remain that the user did not create.
- The account no longer appears in restricted entities for outbound spam.

## Rollback
- If you blocked the wrong account, unblock sign-in and let the user re-authenticate; revoked tokens simply force a fresh sign-in.

## Escalate when
- Mailbox data was exfiltrated or a payment process was targeted: this is an incident, not a ticket.
- Multiple accounts are affected, or an admin account is involved.
- Persistence keeps returning after cleanup, which suggests a compromised device or app identity.
