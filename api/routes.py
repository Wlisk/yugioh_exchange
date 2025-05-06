from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from models.yugioh_card import YugiohCard, YugiohCardRead, \
  YugiohCardCreate, YugiohCardUpdate
from db.main import get_session
from api.utils import check_card

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

###############################################################################
@router.get("/", response_model=list[YugiohCardRead])
async def get_cards(session: SessionDep):
  """Get all Yu-gi-oh cards"""
  db_cards = session.exec(select(YugiohCard)).all()
  return db_cards

###############################################################################
@router.get("/card/{card_id}", response_model=YugiohCardRead)
def get_card(card_id: int, session: SessionDep):
  """Get an Yu-gi-oh card base on its id"""
  db_card = session.get(YugiohCard, card_id)
  check_card(db_card, card_id)
  return db_card

###############################################################################
@router.post("/card/", response_model=YugiohCardRead)
def create_card(card: YugiohCardCreate, session: SessionDep):
  """add an Yu-gi-oh card"""
  db_card = YugiohCard.model_validate(card)
  session.add(db_card)
  session.commit()
  session.refresh(db_card)
  return db_card

###############################################################################
@router.patch("/card/{card_id}", response_model=YugiohCardRead)
def update_card(
  card_id: int, 
  card: YugiohCardUpdate, 
  session: SessionDep
):
  """Update an Yu-gi-oh card based on its id"""
  db_card = session.get(YugiohCard, card_id)
  check_card(db_card, card_id)

  # converts the requisiton card obj to a dict
  card_data = card.model_dump(exclude_unset=True)
  # updates the card based on a dict
  db_card.sqlmodel_update(card_data)

  session.add(db_card)
  session.commit()
  session.refresh(db_card)
  return db_card

###############################################################################
@router.delete("/card/{card_id}")
def delete_card(card_id: int, session: SessionDep):
  """Delete an Yu-gi-oh card based on its id"""
  db_card = session.get(YugiohCard, card_id)
  check_card(db_card, card_id)

  session.delete(db_card)
  session.commit()
  return {"ok": True, "message": f"Card {card_id} deleted"}