# FlexJD SBA Resource Hub

A student-maintained resource site for the Northeastern University School of Law FlexJD community. The site is maintained by the SBA Chair of FlexJD Interests and is designed as an accessible, mobile-first hub for community updates, academic resources, opportunities, and student advocacy campaigns.

> **Independent student resource.** This repository and its deployed site are not official publications of Northeastern University or Northeastern University School of Law. Policies, deadlines, requirements, contacts, and opportunities must be confirmed with the relevant official source before reliance.

## Public-interest purpose

The project helps a geographically distributed student body locate information that is otherwise scattered across institutional pages, employer postings, student communications, and external legal-career resources. It does not replace official academic advising, registrar guidance, career counseling, financial-aid advice, or legal advice.

## Structure

- `index.html` — homepage and community hub
- `newsletter.html` — FlexJD Community Update newsletter
- `resources.html` — student guide, program overview, requirements, contacts, and alumni-outreach guidance
- `opportunities.html` — searchable and filterable opportunity tracker
- `campaigns/` — monthly awareness and advocacy campaign pages
- `institutional-disclaimer.html` — institutional-status and reliance notice
- `privacy.html` — privacy and data-handling notice
- `docs/source-verification-policy.md` — sourcing, freshness, correction, and archival rules
- `scripts/check_stale_opportunities.py` — opportunity-freshness audit
- `.github/workflows/` — automated link, freshness, and secret-history controls
- `style.css` — shared design system
- `vercel.json` — deployment and routing configuration

## Deployment

The site uses static HTML, CSS, and vanilla JavaScript with no build step. It is deployed on Vercel from this GitHub repository. Changes merged into `main` may publish automatically, so substantive content updates should be reviewed before merge.

## Source and freshness standard

Every policy, requirement, deadline, contact, or opportunity should be traceable to an authoritative source. Records should identify a source URL and a last-verified date wherever the page structure permits. Expired, superseded, or unverifiable material should be corrected, archived, or removed rather than silently retained.

See [`docs/source-verification-policy.md`](docs/source-verification-policy.md).

## Privacy standard

Do not commit private student records, disability information, financial-aid records, grades, personal schedules, nonpublic contact lists, private correspondence, application materials, or other sensitive personal information. Public contact information should be limited to what is necessary and already intentionally published for the relevant role.

See [`privacy.html`](privacy.html) and [`SECURITY.md`](SECURITY.md).

## Automated controls

The repository includes workflows for:

- full-history secret scanning with Gitleaks;
- scheduled and pull-request link checking;
- scheduled opportunity-freshness reporting;
- reviewable reports rather than silent assumptions of accuracy.

Automated checks reduce risk but do not replace human review of institutional claims, rights, privacy, or source context.

## Corrections

Corrections should identify the affected page or record, the authoritative source, and the requested change. Material institutional corrections should be verified against an official Northeastern source before publication.

Maintained by RN Collins (she/they), Northeastern University School of Law FlexJD Class of 2029.