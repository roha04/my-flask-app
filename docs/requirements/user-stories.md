# User stories and acceptance criteria

Format: **As a** job seeker **I want** … **So that** …

Priority: `Must` | `Should` | `Could`

---

## Authentication (US-AUTH)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-AUTH-01 | Register with email and password | Valid email, password ≥ 8 chars; duplicate email returns 409 | Must | POST `/api/v1/auth/register`, `/register` |
| US-AUTH-02 | Login with credentials | Valid user gets session cookie; invalid returns 401 | Must | POST `/api/v1/auth/login`, `/login` |
| US-AUTH-03 | Logout | Session cleared; `/me` returns 401 after logout | Must | POST `/api/v1/auth/logout`, `/logout` |
| US-AUTH-04 | View current profile | Authenticated user sees name and email | Must | GET `/api/v1/auth/me` |
| US-AUTH-05 | Block unauthenticated API access | CRUD endpoints return 401 without session | Must | Any protected route |
| US-AUTH-06 | Redirect unauthenticated UI | Visiting `/` redirects to `/login` | Must | GET `/` |
| US-AUTH-07 | Password stored hashed | DB contains bcrypt hash, not plain password | Must | Service layer |
| US-AUTH-08 | Session persists across requests | Cookie enables subsequent API calls | Must | Integration test |

---

## Companies (US-COMP)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-COMP-01 | List companies | Returns all companies sorted by name | Must | GET `/api/v1/companies`, `/companies` |
| US-COMP-02 | Create company | Name required; optional website, industry, size | Must | POST `/api/v1/companies`, `/companies/new` |
| US-COMP-03 | View company details | Get by ID or list row | Must | GET `/api/v1/companies/{id}` |
| US-COMP-04 | Update company | PATCH updates fields; 404 if missing | Must | PATCH `/api/v1/companies/{id}`, `/companies/{id}/edit` |
| US-COMP-05 | Delete company | 204; cascades contacts and jobs | Must | DELETE `/api/v1/companies/{id}` |
| US-COMP-06 | Validate company name | Empty name rejected (422) | Must | Schema validation |
| US-COMP-07 | Link company to jobs | Jobs reference company_id FK | Must | Job create |

---

## Contacts (US-CONT)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-CONT-01 | List contacts | Optional filter by company_id | Should | GET `/api/v1/contacts` |
| US-CONT-02 | Create contact | Requires valid company_id | Should | POST `/api/v1/contacts` |
| US-CONT-03 | Update contact | Can change name, email, role, linkedin | Should | PATCH `/api/v1/contacts/{id}` |
| US-CONT-04 | Delete contact | 204 on success | Should | DELETE `/api/v1/contacts/{id}` |
| US-CONT-05 | Reject invalid company | 404 if company_id unknown | Should | POST create |
| US-CONT-06 | Store recruiter metadata | role and linkedin optional fields saved | Could | Model fields |

---

## Jobs (US-JOB)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-JOB-01 | List jobs | Filter by company_id and status | Must | GET `/api/v1/jobs`, `/jobs` |
| US-JOB-02 | Create job | Title, description, salary range, status open/closed | Must | POST `/api/v1/jobs`, `/jobs/new` |
| US-JOB-03 | View job detail | Shows description and extracted keywords | Must | GET `/jobs/{id}` |
| US-JOB-04 | Update job | PATCH all editable fields | Must | PATCH `/api/v1/jobs/{id}`, `/jobs/{id}/edit` |
| US-JOB-05 | Delete job | Cascades applications | Must | DELETE `/api/v1/jobs/{id}` |
| US-JOB-06 | Validate salary range | salary_min ≤ salary_max | Must | Service validation |
| US-JOB-07 | Job status open/closed | Enum enforced | Must | JobStatus enum |
| US-JOB-08 | Link to company | company_id FK required | Must | Job create |

---

## Resumes (US-RES)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-RES-01 | List my resumes | Only current user's versions | Must | GET `/api/v1/resumes`, `/resumes` |
| US-RES-02 | Create resume | Title + text content | Must | POST `/api/v1/resumes`, `/resumes/new` |
| US-RES-03 | Update resume | Edit title and content | Must | PATCH `/api/v1/resumes/{id}`, `/resumes/{id}/edit` |
| US-RES-04 | Delete resume | 204; cannot delete others' resumes | Must | DELETE `/api/v1/resumes/{id}` |
| US-RES-05 | Activate resume | One active resume per user | Must | POST `/api/v1/resumes/{id}/activate` |
| US-RES-06 | Deactivate others on activate | Previous active set to false | Must | Service logic |
| US-RES-07 | Use resume in application | resume_version_id on application | Must | Application create |

---

## Applications (US-APP)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-APP-01 | Create application | Links job + optional resume; default Wishlist | Must | POST `/api/v1/applications`, `/applications/new` |
| US-APP-02 | List applications | Filter by stage and job_id | Must | GET `/api/v1/applications`, `/applications` kanban |
| US-APP-03 | View application detail | Shows scores and job info | Must | GET `/api/v1/applications/{id}`, `/applications/{id}` |
| US-APP-04 | Change stage | PATCH stage endpoint; records history | Must | PATCH `/api/v1/applications/{id}/stage` |
| US-APP-05 | Auto-set applied_at | Moving to Applied sets timestamp if empty | Must | change_stage service |
| US-APP-06 | View stage history | Ordered list of transitions | Must | GET `/api/v1/applications/{id}/history` |
| US-APP-07 | Compute match on create | match_score populated when resume attached | Must | scoring service |
| US-APP-08 | Compute priority score | priority_score 0–1 after create/update | Must | scoring service |
| US-APP-09 | Compute response likelihood | response_likelihood 0–1 | Must | scoring service |
| US-APP-10 | Delete application | 204; user-scoped | Must | DELETE `/api/v1/applications/{id}` |
| US-APP-11 | Kanban drag alternative | Stage dropdown on kanban card | Should | UI kanban |
| US-APP-12 | Suggest next action | Rule-based recommendation | Must | GET `/applications/{id}/suggest-action` |

---

## Notes (US-NOTE)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-NOTE-01 | Add note to application | entity_type application + body | Must | POST `/api/v1/notes`, application detail form |
| US-NOTE-02 | Add note to company | company_id required | Should | POST `/api/v1/notes` |
| US-NOTE-03 | Add note to job | job_id required | Should | POST `/api/v1/notes` |
| US-NOTE-04 | List notes | Filter by entity | Should | GET `/api/v1/notes` |
| US-NOTE-05 | Update note body | PATCH body text | Could | PATCH `/api/v1/notes/{id}` |

---

## Analytics & algorithms (US-ALG)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-ALG-01 | Match resume to JD | POST returns score 0–1 | Must | POST `/api/v1/analytics/match` |
| US-ALG-02 | Extract JD keywords | Top-N terms returned | Must | POST `/api/v1/analytics/extract-keywords` |
| US-ALG-03 | Pipeline analytics | avg days per stage + bottleneck | Must | GET `/api/v1/analytics/pipeline` |
| US-ALG-04 | Stale applications | IDs exceeding SLA | Must | GET `/api/v1/analytics/stale` |
| US-ALG-05 | Salary benchmark | Percentile vs stored jobs | Should | GET `/api/v1/analytics/salary-benchmark` |
| US-ALG-06 | Dashboard KPIs | Active count, stale, avg match, bottleneck | Must | GET `/` dashboard |
| US-ALG-07 | Empty text match safety | Returns 0.0 not error | Must | `match_resume_to_jd` |
| US-ALG-08 | Priority increases with stage | Onsite > Applied | Must | Unit test |

---

## System & DevOps (US-SYS)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-SYS-01 | Health check | `/health` returns status, version, db | Must | GET `/health` |
| US-SYS-02 | OpenAPI docs | `/docs` lists all endpoints | Must | Swagger UI |
| US-SYS-03 | CI on PR | lint + test run automatically | Must | `.github/workflows/ci.yml` |
| US-SYS-04 | CD to Railway | staging → smoke → prod | Must | `.github/workflows/cd.yml` |
| US-SYS-05 | Rollback production | workflow_dispatch with SHA | Must | CD rollback job |
| US-SYS-06 | Demo seed data | Optional seed script | Could | `python -m app.seed` |

---

**Total user stories: 58**

See [traceability.md](traceability.md) for mapping to automated tests.
