"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from datetime import datetime

TitleStr = Annotated[str, Field(..., min_length=1, max_length=200, description="Book title must be unique")]
DescriptionStr = Annotated[Optional[str], Field(default=None, max_length=500)]

class BookBase(BaseModel):
    title: TitleStr
    description: DescriptionStr

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[TitleStr] = None
    description: DescriptionStr = None

    model_config = ConfigDict(from_attributes=True)

class BookOut(BookBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)