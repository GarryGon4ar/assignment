from datetime import datetime, date

from pydantic import BaseModel


class Scan(BaseModel):
    id: int
    scan_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Identity(BaseModel):
    id: int
    full_name: str
    birthday: date | None

    class Config:
        orm_mode = True
