import enum
from sqlmodel import Enum, Relationship, SQLModel, Field, Column

from models.yugioh_card import YugiohCard

class UserRole(enum.Enum):
   USER = 'user'
   ADMIN = 'admin'

class UserCard(SQLModel, table=True):
    """Association table for user-card ownership"""
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    card_id: int = Field(foreign_key="yugiohcard.id", primary_key=True)

class UserWishlist(SQLModel, table=True):
    """Association table for user-card ownership"""
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    card_id: int = Field(foreign_key="yugiohcard.id", primary_key=True)

class User(SQLModel, table=True):
  """User model, holder of cards"""
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True)
  password: str
  cards: list[YugiohCard] = Relationship(link_model=UserCard)  
  wishlist_cards: list[YugiohCard] = Relationship(link_model=UserWishlist)  
  role: UserRole = Field(sa_column=Column(Enum(UserRole)))