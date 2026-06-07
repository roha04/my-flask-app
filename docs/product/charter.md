# Project Charter — Job Hunt CRM

## Problem statement

Job seekers track applications across spreadsheets, email, and job boards. There is no single place to manage pipeline stages, resume versions, match quality against job descriptions, and follow-up actions.

## Product vision

**Job Hunt CRM** is a personal application tracker (Linear-style) for job search: companies, jobs, applications, resume versions, and algorithm-assisted insights (match score, priority, next action).

## Goals

1. Centralize job search data (companies, jobs, contacts, applications, notes).
2. Automate resume-to-JD match scoring and application prioritization.
3. Provide analytics: pipeline velocity, stale applications, salary benchmark.
4. Deliver via web UI + REST API with CI/CD to Railway.

## Success criteria

| Criterion | Target |
|-----------|--------|
| Core CRUD entities | 7 entities fully functional |
| Algorithm modules | 8 modules with unit tests |
| Automated tests | ≥ 50, coverage ≥ 75% |
| Manual test cases | ≥ 100 documented |
| CI pipeline | lint + test on every PR |
| CD pipeline | staging → smoke → production with rollback |

## Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| Job seeker (end user) | Track applications, improve match rate |
| Course instructor | Process artifacts, testing, CI/CD |
| Team | Portfolio / academic project delivery |

## Constraints

- No paid cloud budget required beyond Railway free tier
- Single monolith deployment (FastAPI + Jinja2)
- SQLite locally; PostgreSQL on Railway
- Delivery timeline: one development sprint + documentation

## Out of scope (v1)

- Mobile native app
- Email/calendar integrations
- Multi-tenant SaaS billing
- ML model training (TF-IDF heuristics only)
