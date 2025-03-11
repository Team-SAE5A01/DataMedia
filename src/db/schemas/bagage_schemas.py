from datetime import date
from enum import Enum, auto
from pydantic import BaseModel, field_validator
from typing import Optional

class BagageType(str, Enum):
    petit = "petit"
    moyen = "moyen"
    grand = "grand"

class BagageBase(BaseModel):
    user_id: int
    bagage_type: BagageType
    position: str
    status: str

    @field_validator("bagage_type")
    def validate_type(cls, v):
        if v not in {type.value for type in BagageType}:
            raise ValueError("Invalid luggage type value")
        return v
    
class BagageCreate(BaseModel):
    user_id: int
    bagage_type: BagageType
    position: str
    status: str

    @field_validator("bagage_type")
    def validate_type(cls, v):
        if v not in {type.value for type in BagageType}:
            raise ValueError("Invalid luggage type value")
        return v

class BagageResponse(BagageBase):
    id: int

    class Config:
        orm_mode = True

class BagageUpdate(BaseModel):
    bagage_type: Optional[BagageType] = None
    position: Optional[str] = None
    status: Optional[str] = None
