from sqlalchemy.orm import Session

from models import Scan, Identity


def get_scan(db: Session, id_: int):
    return db.query(Scan).filter(Scan.id == id_).first()


def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Scan).offset(skip).limit(limit).all()


def get_identity(db: Session, id_: int):
    return db.query(Identity).filter(Identity.id == id_).first()


def get_identities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Identity).offset(skip).limit(limit).all()
