# Security Policy

## Reporting

Do not open a public issue containing a suspected secret, private student record, or other sensitive information. Report the affected file or page privately to the repository owner through an established private contact channel.

Include:

- the affected path or URL;
- the type of information exposed;
- whether it appears in current files or Git history;
- the minimum detail necessary to locate it.

Do not reproduce a credential or personal record in the report unless necessary.

## Scope

Security-sensitive material includes:

- API keys, access tokens, passwords, private keys, database URLs, webhook secrets, and session credentials;
- private student records, grades, disability or health information, financial-aid records, student IDs, private correspondence, and application materials;
- nonpublic contact lists and meeting links;
- unpublished institutional documents or restricted employer materials.

## Response

When a credible report is received:

1. remove public access where possible;
2. rotate or revoke exposed credentials immediately;
3. determine whether the item exists in Git history, forks, caches, deployment logs, or artifacts;
4. notify affected people or institutions when appropriate;
5. document remediation without republishing the sensitive value;
6. add a preventive control or test.

Deleting a file in a new commit does not remove it from Git history.

## Repository controls

Pull requests and scheduled workflows should run a full-history Gitleaks scan. Automated scanning is a control, not a guarantee. Contributors remain responsible for reviewing changes before commit.

## Supported branch

Security remediation is supported for the current `main` branch and active deployment.