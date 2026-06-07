from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.exceptions import NotFoundError


def list_companies(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    return db.query(Company).order_by(Company.name).offset(skip).limit(limit).all()


def get_company(db: Session, company_id: int) -> Company:
    company = db.query(Company).filter(Company.id == company_id).one_or_none()
    if company is None:
        raise NotFoundError("Company not found")
    return company


def create_company(db: Session, payload: CompanyCreate) -> Company:
    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company_id: int, payload: CompanyUpdate) -> Company:
    company = get_company(db, company_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: int) -> None:
    company = get_company(db, company_id)
    db.delete(company)
    db.commit()
