from app.seed import seed
from app.services import company as company_service


def test_seed_creates_demo_data(db_session):
    seed(db_session)
    assert len(company_service.list_companies(db_session)) >= 2


def test_seed_is_idempotent(db_session):
    seed(db_session)
    count_after_first = len(company_service.list_companies(db_session))
    seed(db_session)
    assert len(company_service.list_companies(db_session)) == count_after_first
