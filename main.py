from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Scan, Identity
from utils import get_token, parse_scans, parse_identities

description = """
Test assignment written using following technologies: 
- FastApi 
- MySql
- Docker
- alembic 

"""

app = FastAPI(
    title="Test assignment",
    description=description,
    contact={
        "name": "Erlan Dzhumabaev",
        "email": "garrygon4ar@gmail.com",
    },
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/parse_data")
def parse_data(db: Session = Depends(get_db)):
    token = get_token()
    scans = parse_scans(token)
    identities = parse_identities(token, [scan_item["IdentityID"] for scan_item in scans])
    db.bulk_save_objects(
        objects=[
            Scan(scan_id=scan["ID"], created_at=datetime.strptime(scan['CreatedAt'], '%Y-%m-%d %H:%M:%S')) for scan in
            scans
        ]
    )
    db.bulk_save_objects(
        objects=[
            Identity(full_name=identity["FullName"], birthday=datetime.strptime(identity['Birthday'], '%Y-%m-%d').date() if identity['Birthday'] else None) for identity in
            identities
        ]
    )
    db.commit()


@app.get("/scans/", response_model=List[schemas.Scan])
def read_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    scans = crud.get_scans(db, skip=skip, limit=limit)
    return scans


@app.get("/scans/{id_}", response_model=schemas.Scan)
def read_scan(id_: int, db: Session = Depends(get_db)):
    scan = crud.get_scan(db, id_=id_)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@app.get("/identities/", response_model=List[schemas.Identity])
def read_identities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    identities = crud.get_identities(db, skip=skip, limit=limit)
    return identities


@app.get("/identities/{identity_id}", response_model=schemas.Identity)
def read_identity(id_: int, db: Session = Depends(get_db)):
    identity = crud.get_identity(db, id_=id_)
    if identity is None:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity
