# from pydantic import BaseModel
from sqlmodel import SQLModel, Field

# Base class
class YugiohCardBase(SQLModel):
  name: str = Field(index=True)

# Table class for DB operations (private model)
class YugiohCard(YugiohCardBase, table=True):
  id: int | None = Field(default=None, primary_key=True)

# class for http responses (public model)
class YugiohCardRead(YugiohCardBase):
  id: int

# class for creating cards (public model)
class YugiohCardCreate(YugiohCardBase):
  pass

# class for updating cards (public model)
class YugiohCardUpdate(YugiohCardBase):
  name: str | None = None

