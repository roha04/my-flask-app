# Manual test cases

**Project:** Job Hunt CRM  
**Total cases:** 120  
**Types:** F = Functional, UI = UI, NF = Non-functional, API = API via Swagger/curl

---

## Authentication (TC-AUTH)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-AUTH-001 | US-AUTH-01 | F | Register with valid email/password | 201, user created | H |
| TC-AUTH-002 | US-AUTH-01 | F | Register duplicate email | 409 Conflict | H |
| TC-AUTH-003 | US-AUTH-01 | F | Register password 7 chars | 422 validation error | M |
| TC-AUTH-004 | US-AUTH-02 | F | Login correct credentials | 200, session cookie set | H |
| TC-AUTH-005 | US-AUTH-02 | F | Login wrong password | 401 | H |
| TC-AUTH-006 | US-AUTH-03 | F | Logout after login | 204, /me → 401 | H |
| TC-AUTH-007 | US-AUTH-04 | API | GET /me authenticated | name, email returned | H |
| TC-AUTH-008 | US-AUTH-05 | API | GET /companies without auth | 401 | H |
| TC-AUTH-009 | US-AUTH-06 | UI | Open `/` logged out | Redirect to /login | H |
| TC-AUTH-010 | US-AUTH-06 | UI | Login page renders | Email/password fields visible | M |
| TC-AUTH-011 | US-AUTH-01 | UI | Register via `/register` form | Redirect to dashboard | M |
| TC-AUTH-012 | US-AUTH-02 | NF | 5 failed logins | Still 401, no crash | L |

---

## Companies (TC-COMP)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-COMP-001 | US-COMP-02 | UI | Create company via form | Listed on /companies | H |
| TC-COMP-002 | US-COMP-01 | API | GET /companies | JSON array | H |
| TC-COMP-003 | US-COMP-04 | UI | Edit company size field | Saved and shown in list | M |
| TC-COMP-004 | US-COMP-05 | API | DELETE company | 204, gone from list | H |
| TC-COMP-005 | US-COMP-06 | F | Create company empty name | 422 | M |
| TC-COMP-006 | US-COMP-02 | F | Website URL stored | Valid link on list | L |
| TC-COMP-007 | US-COMP-05 | F | Delete company with jobs | Jobs cascade deleted | H |
| TC-COMP-008 | US-COMP-01 | UI | Empty state message | "No companies yet" | L |
| TC-COMP-009 | US-COMP-03 | API | GET unknown company id | 404 | M |
| TC-COMP-010 | US-COMP-04 | API | PATCH partial update | Only sent fields change | M |

---

## Contacts (TC-CONT)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-CONT-001 | US-CONT-02 | API | POST contact valid | 201 with company_id | M |
| TC-CONT-002 | US-CONT-05 | API | POST invalid company_id | 404 | M |
| TC-CONT-003 | US-CONT-01 | API | GET contacts?company_id=X | Filtered list | M |
| TC-CONT-004 | US-CONT-03 | API | PATCH contact name | Updated value | M |
| TC-CONT-005 | US-CONT-04 | API | DELETE contact | 204 | M |
| TC-CONT-006 | US-CONT-02 | F | Optional email omitted | Contact saved | L |
| TC-CONT-007 | US-CONT-06 | F | LinkedIn URL stored | Field persisted | L |
| TC-CONT-008 | US-CONT-01 | API | GET /contacts unauthenticated | 401 | H |

---

## Jobs (TC-JOB)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-JOB-001 | US-JOB-02 | UI | Create job with JD text | Appears in /jobs | H |
| TC-JOB-002 | US-JOB-03 | UI | Open job detail | Description + keywords | H |
| TC-JOB-003 | US-JOB-06 | F | salary_min > salary_max | 422 validation | M |
| TC-JOB-004 | US-JOB-07 | F | Set status closed | Badge shows closed | M |
| TC-JOB-005 | US-JOB-01 | API | Filter jobs by company | Correct subset | M |
| TC-JOB-006 | US-JOB-04 | UI | Edit job title | Updated in list | M |
| TC-JOB-007 | US-JOB-05 | API | DELETE job | 204 | H |
| TC-JOB-008 | US-JOB-08 | F | Missing company on create | 404 | M |
| TC-JOB-009 | US-JOB-03 | F | Keywords include tech terms | Badges on detail page | M |
| TC-JOB-010 | US-JOB-02 | F | Long description 5k chars | Saved without error | L |
| TC-JOB-011 | US-JOB-01 | API | GET /jobs?status=open | Only open jobs | M |
| TC-JOB-012 | US-JOB-03 | UI | "Track application" link | Opens /applications/new?job_id= | L |

---

## Resumes (TC-RES)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-RES-001 | US-RES-02 | UI | Create resume | Listed on /resumes | H |
| TC-RES-002 | US-RES-05 | UI | Activate resume v2 | Only one active badge | H |
| TC-RES-003 | US-RES-03 | UI | Edit resume content | Updated preview | M |
| TC-RES-004 | US-RES-04 | API | DELETE resume | 204 | M |
| TC-RES-005 | US-RES-01 | API | User A cannot GET user B resume | 404 | H |
| TC-RES-006 | US-RES-02 | F | Empty content | Allowed (empty string) | L |
| TC-RES-007 | US-RES-05 | API | POST activate | is_active true | H |
| TC-RES-008 | US-RES-06 | F | Activate deactivates previous | Single active in DB | H |
| TC-RES-009 | US-RES-02 | UI | Checkbox set active on create | Active immediately | M |
| TC-RES-010 | US-RES-04 | UI | Delete with confirm | Removed from list | M |

---

## Applications (TC-APP)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-APP-001 | US-APP-01 | UI | Create application with resume | Redirect to detail | H |
| TC-APP-002 | US-APP-07 | F | match_score present | Value between 0 and 1 | H |
| TC-APP-003 | US-APP-04 | UI | Change stage on kanban dropdown | Card moves column | H |
| TC-APP-004 | US-APP-05 | F | Move to Applied | applied_at populated | H |
| TC-APP-005 | US-APP-06 | UI | View stage history | ≥ 2 entries after transition | M |
| TC-APP-006 | US-APP-12 | UI | Suggest next action shown | Non-empty action text | H |
| TC-APP-007 | US-APP-02 | UI | Kanban shows 8 columns | All stages visible | M |
| TC-APP-008 | US-APP-10 | API | DELETE application | 204 | M |
| TC-APP-009 | US-APP-08 | F | priority_score displayed | Badge on kanban | M |
| TC-APP-010 | US-APP-09 | F | response_likelihood on detail | Percentage shown | M |
| TC-APP-011 | US-APP-01 | F | Create without resume | match_score null OK | M |
| TC-APP-012 | US-APP-04 | API | PATCH /stage to Offer | stage updated | M |
| TC-APP-013 | US-APP-02 | API | Filter ?stage=Applied | Filter works | M |
| TC-APP-014 | US-APP-03 | UI | Detail shows job company | Company name visible | M |
| TC-APP-015 | US-APP-11 | UI | Kanban horizontal scroll | Usable on narrow viewport | L |

---

## Notes (TC-NOTE)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-NOTE-001 | US-NOTE-01 | UI | Add note on application | Note appears in list | H |
| TC-NOTE-002 | US-NOTE-02 | API | POST company note | 201 | M |
| TC-NOTE-003 | US-NOTE-01 | F | Empty note body | 422 | M |
| TC-NOTE-004 | US-NOTE-04 | API | GET notes?application_id= | Filtered | M |
| TC-NOTE-005 | US-NOTE-05 | API | PATCH note body | Updated text | L |
| TC-NOTE-006 | US-NOTE-03 | API | Job note missing job_id | 422 | M |

---

## Analytics (TC-ALG)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-ALG-001 | US-ALG-01 | API | POST /analytics/match similar texts | score > 0.5 | H |
| TC-ALG-002 | US-ALG-01 | API | POST match empty resume | score 0 | M |
| TC-ALG-003 | US-ALG-02 | API | POST extract-keywords | List length = top_n | H |
| TC-ALG-004 | US-ALG-03 | API | GET /analytics/pipeline | transitions_count ≥ 0 | M |
| TC-ALG-005 | US-ALG-04 | API | GET /analytics/stale | stale_application_ids array | M |
| TC-ALG-006 | US-ALG-05 | API | GET salary-benchmark?salary=90000 | percentile present | M |
| TC-ALG-007 | US-ALG-06 | UI | Dashboard stale count | Matches API stale count | M |
| TC-ALG-008 | US-ALG-06 | UI | Dashboard avg match | Numeric % displayed | M |
| TC-ALG-009 | US-ALG-03 | F | Bottleneck label on dashboard | String or em dash | L |
| TC-ALG-010 | US-ALG-02 | UI | Job detail keywords | Match API extract | M |
| TC-ALG-011 | US-ALG-01 | F | Unrelated texts low score | < 0.2 | M |
| TC-ALG-012 | US-ALG-04 | F | Recent app not in stale list | ID absent | M |

---

## Web UI (TC-UI)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-UI-001 | US-ALG-06 | UI | Navbar links | All main routes reachable | H |
| TC-UI-002 | US-SYS-02 | UI | API docs link opens | Swagger loads | M |
| TC-UI-003 | US-AUTH-06 | UI | Logout from navbar | Session cleared | H |
| TC-UI-004 | US-COMP-02 | UI | Success message after create | Green alert | L |
| TC-UI-005 | US-JOB-02 | UI | Cancel on job form | Returns to list | L |
| TC-UI-006 | US-APP-03 | UI | Back link on application detail | Returns to kanban | M |
| TC-UI-007 | — | NF | Page load dashboard | < 3s local | L |
| TC-UI-008 | — | UI | Mobile viewport 375px | No broken layout | M |
| TC-UI-009 | US-RES-01 | UI | Resume content truncated in card | Preview with ellipsis | L |
| TC-UI-010 | US-APP-03 | UI | Score badges readable | Contrast sufficient | L |
| TC-UI-011 | US-COMP-01 | UI | Company table responsive | Horizontal scroll if needed | L |
| TC-UI-012 | US-JOB-03 | UI | Pre-formatted JD text | Line breaks preserved | M |
| TC-UI-013 | US-APP-11 | UI | Stage select on card | Does not navigate on select | M |
| TC-UI-014 | US-AUTH-01 | UI | Register invalid email | Browser validation | L |
| TC-UI-015 | US-ALG-06 | UI | KPI cards aligned | 4 cards in row desktop | L |

---

## System & DevOps (TC-SYS)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-SYS-001 | US-SYS-01 | API | GET /health | status ok, db ok | H |
| TC-SYS-002 | US-SYS-01 | API | GET /version | version string | M |
| TC-SYS-003 | US-SYS-03 | NF | Push PR with lint error | CI lint fails | H |
| TC-SYS-004 | US-SYS-03 | NF | Push PR all green | CI test passes | H |
| TC-SYS-005 | US-SYS-04 | NF | Merge to main | CD workflow triggers | H |
| TC-SYS-006 | US-SYS-04 | NF | Staging smoke script | 5 health checks pass | H |
| TC-SYS-007 | US-SYS-05 | NF | Manual rollback workflow | Green redeploys | M |
| TC-SYS-008 | US-SYS-06 | F | Run app.seed | Demo login works | M |
| TC-SYS-009 | US-SYS-01 | NF | /health on Railway | 200 after deploy | H |
| TC-SYS-010 | US-SYS-03 | NF | Coverage artifact uploaded | coverage.xml in Actions | L |

---

## API smoke checklist (TC-API)

| ID | Story | Type | Steps | Expected result | P |
|----|-------|------|-------|-----------------|---|
| TC-API-001 | US-SYS-02 | API | Swagger lists auth tag | Endpoints visible | M |
| TC-API-002 | US-COMP-01 | API | Try it POST company | 201 in Swagger | M |
| TC-API-003 | US-JOB-01 | API | Try it GET jobs | 200 JSON | M |
| TC-API-004 | US-APP-01 | API | Try it POST application | Scores in response | H |
| TC-API-005 | US-ALG-01 | API | Try it match | Float 0-1 | M |
| TC-API-006 | US-NOTE-01 | API | Try it POST note | 201 | M |
| TC-API-007 | US-RES-05 | API | Try it activate | 200 | M |
| TC-API-008 | US-APP-04 | API | Try it PATCH stage | 200 | M |
| TC-API-009 | US-ALG-03 | API | Try it pipeline | JSON metrics | M |
| TC-API-010 | US-AUTH-03 | API | Try it logout | 204 | M |

---

**Summary:** 120 manual test cases (12+10+8+12+10+15+6+12+15+10+10)

Execute against local or staging URL. Record results in test run log or issue tracker.
