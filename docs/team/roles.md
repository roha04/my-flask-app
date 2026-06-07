# Team structure and roles

| Role | Member | Responsibilities | Decision authority |
|------|--------|------------------|-------------------|
| Tech Lead | _Name_ | Architecture, code review, CI/CD, API design | Technical stack, deployment strategy |
| Backend Engineer | _Name_ | FastAPI services, algorithms, database, tests | Implementation details, API contracts |
| Frontend Engineer | _Name_ | Jinja2 UI, UX flows, dashboard | UI layout, user flows |
| QA Engineer | _Name_ | Manual test cases, bug reports, smoke testing | Test coverage scope, release sign-off |
| Product Owner | _Name_ | Backlog priority, acceptance criteria | Feature scope, MVP boundaries |

## Communication

- **Daily sync:** async updates in team chat
- **Decisions:** consensus; Tech Lead breaks ties on technical topics
- **Artifacts:** GitHub repo (code, docs, issues), GitHub Projects board

## RACI (key deliverables)

| Deliverable | Tech Lead | Backend | Frontend | QA | PO |
|-------------|-----------|---------|----------|----|----|
| User stories / SRS | C | C | C | I | A |
| CI/CD pipeline | A/R | C | I | C | I |
| Automated tests | C | A/R | C | C | I |
| Manual test plan | I | C | C | A/R | C |
| Deployment (Railway) | A/R | C | I | C | I |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*
