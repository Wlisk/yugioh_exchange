from sqlmodel import SQLModel, Field, Relationship
from .yugioh_card import YugiohCard

# Tabela de associação entre 1 oferta e várias cartas dadas
class OfferCardsGiven(SQLModel, table=True):
  """Association table for offer-cards that want to give"""
  offer_id: int | None = Field(foreign_key="offer.id", primary_key=True)
  card_id: int | None = Field(foreign_key="yugiohcard.id", primary_key=True)

# Tabela de associação entre 1 oferta e várias cartas requisitadas
class OfferCardsWants(SQLModel, table=True):
  """Association table for offer-cards that user wants"""
  offer_id: int | None = Field(foreign_key="offer.id", primary_key=True)
  card_id: int | None = Field(foreign_key="yugiohcard.id", primary_key=True)

# Tabela de ofertas disponiveis
class Offer(SQLModel, table=True):
  """User offer"""
  id: int | None = Field(default=None, primary_key=True)
  user_id: int | None = Field(foreign_key="user.id")
  cards_given: list[YugiohCard] = Relationship(link_model=OfferCardsGiven)
  cards_wants: list[YugiohCard] = Relationship(link_model=OfferCardsWants)
  accepted_by: int | None = Field(default=None, foreign_key="user.id")

# Tabela de trocas realizadas
class Exchange(SQLModel, table=True):
  """Tracks which users have accepted which offers"""
  id: int | None = Field(default=None, primary_key=True)
  user_accepted: int = Field(foreign_key="user.id")
  offer_id: int = Field(foreign_key="offer.id")
  date: str | None = Field(default=None)

class OfferRejections(SQLModel, table=True):
  """Tracks which users have rejected which offers"""
  offer_id: int = Field(foreign_key="offer.id", primary_key=True)
  user_id: int = Field(foreign_key="user.id", primary_key=True)