from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# TimeTravel 관련 예시 스키마
class TimePeriodBase(BaseSchema):
    period_name: str
    description: Optional[str] = None
    background_setting: Optional[str] = None

class TimePeriodCreate(TimePeriodBase):
    pass

class TimePeriod(TimePeriodBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime