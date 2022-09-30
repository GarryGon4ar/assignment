from sqlalchemy import Column, Integer, String, DateTime, Date

from database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, unique=True)
    created_at = Column(DateTime)


class Identity(Base):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150))
    birthday = Column(Date)
