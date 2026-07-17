# FlexJD SBA Resource Hub

> **Independent student resource.** This repository and its deployed site are maintained by a student leader for the convenience of the FlexJD community. They are not official statements, publications, or records of Northeastern University or Northeastern University School of Law. Verify degree requirements, policies, deadlines, contacts, and opportunities with the original institutional or third-party source before relying on them.

Resource site for the Northeastern University School of Law FlexJD community, maintained by the SBA Chair of FlexJD Interests. Rebuilt as a polished, accessible, mobile-first web experience.

## Structure

- `index.html` — homepage / hub
- `newsletter.html` — FlexJD Community Update newsletter
- `resources.html` — All-Purpose Guide (program overview, requirements, contacts, LinkedIn alumni outreach guide)
- `opportunities.html` — filterable opportunity tracker (fellowships, writing competitions, co-ops, clerkships, bar prep, journals, pro bono)
- `campaigns/` — seven monthly awareness campaign pages (Sept, Nov, Dec, Jan, Feb, Mar, Apr)
- `institutional-disclaimer.html` — site status, non-endorsement, and reliance notice
- `privacy.html` — privacy and data-handling notice
- `campaign-resource-request.html` — transparent fallback for campaign packets not currently published
- `docs/source-verification-policy.md` — sourcing, freshness, correction, and archival rules
- `site-governance.js` — sitewide status and policy notice
- `style.css` — shared design system (accessible color tokens, type scale, components)
- `vercel.json` — routing config for clean URLs

## Automated controls

- **Secret history scan:** Gitleaks checks the full Git history with `fetch-depth: 0`.
- **Internal-link integrity:** a deterministic local checker validates files, clean routes, and fragments.
- **External-link availability:** a non-blocking scheduled audit records third-party availability without treating bot-blocking as a broken local build.
- **Opportunity freshness:** a scheduled audit supports structured deadline, status, and last-verified metadata.
- **Sitewide governance links:** an idempotent CI injector ensures every HTML page loads the shared status, privacy, and source-policy notice.

## Deployment

Static HTML/CSS/vanilla JS, no build step. Deployed on Vercel directly from this GitHub repo — every push to `main` redeploys automatically.

## Maintenance principle

A listing or policy summary is not treated as current merely because it remains on the site. Time-sensitive records should identify their original source and, as the tracker is normalized, include machine-readable deadline, status, and last-verified fields. Broken or unpublished campaign downloads resolve to an honest status page rather than an unavailable file.

Maintained by RN Collins (she/they) · collins.ra@northeastern.edu · Class of 2029
