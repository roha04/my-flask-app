# Job Hunt CRM

Особистий трекер відгуків на роботу: компанії, вакансії, резюме, kanban-дошка заявок і аналітика з оцінкою відповідності резюме тексту вакансії (TF-IDF).

---

## Живе демо

| Середовище | URL |
|------------|-----|
| **Production** | _додай свій URL (jobcrm-prod-green)_ |
| **Staging** | _додай свій URL (jobcrm-staging)_ |

**Демо-вхід:** `xxxxxxxxxx` / `xxxxxxxx`

- Веб-інтерфейс: `/`
- API (Swagger): `/docs`
- Health check: `/health`

> На free tier перший запит після простою може зайняти 10–30 секунд.

---

## Репозиторій і CI/CD

- **GitHub:** [roha04/my-flask-app](https://github.com/roha04/my-flask-app)
- **GitHub Actions:** [workflows](https://github.com/roha04/my-flask-app/actions) — **CI** автоматично на push; **CD** вручну (Actions → CD → `deploy-all`): Railway, smoke tests, blue-green, rollback

---

## Можливості

- CRUD: компанії, контакти, вакансії, резюме, заявки, нотатки
- Kanban за 8 стадіями pipeline (Wishlist → Offer / Rejected)
- 8 алгоритмів: match score, keywords, priority, likelihood, salary benchmark, stale detection, next action, pipeline velocity
- Dashboard з KPI: активні заявки, stale, середній match, bottleneck
- REST API `/api/v1` + Jinja2 UI

---

## Стек

FastAPI · SQLAlchemy · Alembic · PostgreSQL (Railway) · pytest · GitHub Actions · Railway

---

## Документація проєкту

Повний пакет артефактів курсу: [docs/README.md](docs/README.md)

- [Хартія проєкту](docs/product/charter.md)
- [58 user stories](docs/requirements/user-stories.md)
- [120 ручних тест-кейсів](docs/testing/manual-test-cases.md)
- [Процес CD](docs/process/cd-process.md)
