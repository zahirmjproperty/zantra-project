# Zantra Project

New-launch sales system for property developers — Zentra Property Group.

- **Host:** https://project.zentrapropertygroup.com
- **Status:** Phase 1 (environment). Deployment is phased; no application modules are live yet.
- **Visibility:** internal system, `noindex` until approved for public discovery.
- **Interactive preview:** https://zahirmjproperty.github.io/mockup-hartanah/zantra-project/

## What the system covers

| Stage | Module |
|---|---|
| Publish | Project microsite (per launch) |
| Capture | Registrations of interest (EOI) · agent and walk-in leads |
| Hold | Timed unit locks with buffers and audit trail |
| Sell | Unit booking, buyer pack, eKYC, SPA/HIMS tracking |
| Bill | Third Schedule progressive billing · e-invoice |
| Pay | Agent commission release on event triggers |
| Assure | Compliance (DL/APDL, HPPH, PDPA) · full audit log |

## Naming

| Layer | Name |
|---|---|
| Client-facing brand | Zentra Property Group |
| System | **Zantra Project** (decided by Zahir, 19 September 2026) |
| Previous working names | Zentra Sales Suite · Zentra Build *(now reserved for the ZPG construction arm)* |
| Internal operator | Mr Tanah |

## Structure

| Path | Purpose |
|---|---|
| `index.html` | Landing page for this environment |
| `CNAME` | Custom domain binding for GitHub Pages |
| `robots.txt` | Disallow all crawlers (internal system) |
| `.gitignore` | Blocks snapshot/data artifacts from being committed |
| `assets/` | Design system (Zentra CSS), brand font, hero imagery |
| `portal/` | (Phase 2+) application modules — added only after tenant separation |

## Related systems

| System | Host |
|---|---|
| Zentra Asset — property, tenancy & asset management | `asset.zentrapropertygroup.com` |
| Mr Tanah — public property listings | `mrtanah.com` |
| Zahir MJ Property | `zahirmjproperty.com` |

Zantra Project is a **separate** system. Mr Tanah/ZMP remain listings-only.

## Deployment

Static site served by GitHub Pages from `main`. Never commit data snapshots, buyer records or credentials into this repository.
