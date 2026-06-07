# User stories та acceptance criteria

Формат: **Як** шукач роботи **я хочу** … **щоб** …

Пріоритет: `Must` | `Should` | `Could`

---

## Автентифікація (US-AUTH)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-AUTH-01 | Реєстрація з email і password | Валідний email, password ≥ 8 символів; duplicate email → 409 | Must | POST `/api/v1/auth/register`, `/register` |
| US-AUTH-02 | Вхід з credentials | Валідний user отримує session cookie; invalid → 401 | Must | POST `/api/v1/auth/login`, `/login` |
| US-AUTH-03 | Вихід | Session cleared; `/me` → 401 після logout | Must | POST `/api/v1/auth/logout`, `/logout` |
| US-AUTH-04 | Профіль поточного user | name і email для автентифікованого | Must | GET `/api/v1/auth/me` |
| US-AUTH-05 | Блок API без auth | CRUD endpoints → 401 без session | Must | Будь-який protected route |
| US-AUTH-06 | Redirect UI без auth | GET `/` → redirect на `/login` | Must | GET `/` |
| US-AUTH-07 | Password hashed | У БД bcrypt hash, не plain text | Must | Service layer |
| US-AUTH-08 | Session між запитами | Cookie для наступних API calls | Must | Integration test |

---

## Компанії (US-COMP)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-COMP-01 | Список компаній | Усі компанії, sorted by name | Must | GET `/api/v1/companies`, `/companies` |
| US-COMP-02 | Створити компанію | Name required; optional website, industry, size | Must | POST `/api/v1/companies`, `/companies/new` |
| US-COMP-03 | Деталі компанії | Get by ID або рядок списку | Must | GET `/api/v1/companies/{id}` |
| US-COMP-04 | Оновити компанію | PATCH полів; 404 якщо немає | Must | PATCH `/api/v1/companies/{id}`, `/companies/{id}/edit` |
| US-COMP-05 | Видалити компанію | 204; cascade contacts і jobs | Must | DELETE `/api/v1/companies/{id}` |
| US-COMP-06 | Валідація name | Порожнє name → 422 | Must | Schema validation |
| US-COMP-07 | Зв'язок з jobs | Jobs reference company_id FK | Must | Job create |

---

## Контакти (US-CONT)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-CONT-01 | Список контактів | Optional filter by company_id | Should | GET `/api/v1/contacts` |
| US-CONT-02 | Створити контакт | Valid company_id required | Should | POST `/api/v1/contacts` |
| US-CONT-03 | Оновити контакт | name, email, role, linkedin | Should | PATCH `/api/v1/contacts/{id}` |
| US-CONT-04 | Видалити контакт | 204 on success | Should | DELETE `/api/v1/contacts/{id}` |
| US-CONT-05 | Invalid company | 404 якщо company_id unknown | Should | POST create |
| US-CONT-06 | Метадані рекрутера | role і linkedin optional | Could | Model fields |

---

## Вакансії (US-JOB)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-JOB-01 | Список jobs | Filter by company_id і status | Must | GET `/api/v1/jobs`, `/jobs` |
| US-JOB-02 | Створити job | Title, description, salary range, status open/closed | Must | POST `/api/v1/jobs`, `/jobs/new` |
| US-JOB-03 | Деталі job | Description і extracted keywords | Must | GET `/jobs/{id}` |
| US-JOB-04 | Оновити job | PATCH editable fields | Must | PATCH `/api/v1/jobs/{id}`, `/jobs/{id}/edit` |
| US-JOB-05 | Видалити job | Cascade applications | Must | DELETE `/api/v1/jobs/{id}` |
| US-JOB-06 | Salary range | salary_min ≤ salary_max | Must | Service validation |
| US-JOB-07 | Status open/closed | Enum enforced | Must | JobStatus enum |
| US-JOB-08 | Link to company | company_id FK required | Must | Job create |

---

## Резюме (US-RES)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-RES-01 | Мої резюме | Лише versions поточного user | Must | GET `/api/v1/resumes`, `/resumes` |
| US-RES-02 | Створити resume | Title + text content | Must | POST `/api/v1/resumes`, `/resumes/new` |
| US-RES-03 | Оновити resume | Edit title і content | Must | PATCH `/api/v1/resumes/{id}`, `/resumes/{id}/edit` |
| US-RES-04 | Видалити resume | 204; не чужі resumes | Must | DELETE `/api/v1/resumes/{id}` |
| US-RES-05 | Активувати resume | One active per user | Must | POST `/api/v1/resumes/{id}/activate` |
| US-RES-06 | Deactivate інші | Previous active → false | Must | Service logic |
| US-RES-07 | Resume в application | resume_version_id on application | Must | Application create |

---

## Заявки (US-APP)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-APP-01 | Створити application | job + optional resume; default Wishlist | Must | POST `/api/v1/applications`, `/applications/new` |
| US-APP-02 | Список applications | Filter by stage і job_id | Must | GET `/api/v1/applications`, `/applications` kanban |
| US-APP-03 | Деталі application | Scores і job info | Must | GET `/api/v1/applications/{id}`, `/applications/{id}` |
| US-APP-04 | Змінити stage | PATCH stage; history recorded | Must | PATCH `/api/v1/applications/{id}/stage` |
| US-APP-05 | Auto applied_at | Move to Applied → timestamp if empty | Must | change_stage service |
| US-APP-06 | Stage history | Ordered transitions | Must | GET `/api/v1/applications/{id}/history` |
| US-APP-07 | Match on create | match_score when resume attached | Must | scoring service |
| US-APP-08 | Priority score | priority_score 0–1 after create/update | Must | scoring service |
| US-APP-09 | Response likelihood | response_likelihood 0–1 | Must | scoring service |
| US-APP-10 | Delete application | 204; user-scoped | Must | DELETE `/api/v1/applications/{id}` |
| US-APP-11 | Kanban alternative | Stage dropdown on card | Should | UI kanban |
| US-APP-12 | Suggest next action | Rule-based recommendation | Must | GET `/applications/{id}/suggest-action` |

---

## Нотатки (US-NOTE)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-NOTE-01 | Note на application | entity_type application + body | Must | POST `/api/v1/notes`, application detail form |
| US-NOTE-02 | Note на company | company_id required | Should | POST `/api/v1/notes` |
| US-NOTE-03 | Note на job | job_id required | Should | POST `/api/v1/notes` |
| US-NOTE-04 | Список notes | Filter by entity | Should | GET `/api/v1/notes` |
| US-NOTE-05 | Update note body | PATCH body text | Could | PATCH `/api/v1/notes/{id}` |

---

## Аналітика та алгоритми (US-ALG)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-ALG-01 | Match resume to JD | POST returns score 0–1 | Must | POST `/api/v1/analytics/match` |
| US-ALG-02 | Extract JD keywords | Top-N terms returned | Must | POST `/api/v1/analytics/extract-keywords` |
| US-ALG-03 | Pipeline analytics | avg days per stage + bottleneck | Must | GET `/api/v1/analytics/pipeline` |
| US-ALG-04 | Stale applications | IDs exceeding SLA | Must | GET `/api/v1/analytics/stale` |
| US-ALG-05 | Salary benchmark | Percentile vs stored jobs | Should | GET `/api/v1/analytics/salary-benchmark` |
| US-ALG-06 | Dashboard KPIs | Active count, stale, avg match, bottleneck | Must | GET `/` dashboard |
| US-ALG-07 | Empty text match | Returns 0.0 not error | Must | `match_resume_to_jd` |
| US-ALG-08 | Priority vs stage | Onsite > Applied | Must | Unit test |

---

## Система та DevOps (US-SYS)

| ID | Story | Acceptance criteria | Priority | API / UI |
|----|-------|---------------------|----------|----------|
| US-SYS-01 | Health check | `/health` → status, version, db | Must | GET `/health` |
| US-SYS-02 | OpenAPI docs | `/docs` lists all endpoints | Must | Swagger UI |
| US-SYS-03 | CI on PR | lint + test automatically | Must | `.github/workflows/ci.yml` |
| US-SYS-04 | CD to Railway | staging → smoke → prod | Must | `.github/workflows/cd.yml` |
| US-SYS-05 | Rollback production | workflow_dispatch with SHA | Must | CD rollback job |
| US-SYS-06 | Demo seed data | Optional seed script | Could | `python -m app.seed` |

---

**Всього user stories: 58**

Див. [traceability.md](traceability.md) для mapping на автотести.
