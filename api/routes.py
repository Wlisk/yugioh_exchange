from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select

from models.offer import Exchange, Offer, OfferCardsGiven, OfferCardsWants, OfferRejections
from models.user import User, UserCard
from models.yugioh_card import YugiohCard, YugiohCardRead, \
  YugiohCardCreate, YugiohCardUpdate
from db.main import get_session
from api.utils import check_card

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

###############################################################################
@router.get("/cards", response_model=list[YugiohCardRead])
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

###############################################################################
@router.get("/offers", response_model=list[dict])
def list_available_offers(
  session: SessionDep,
  user_id: int | None = None,
):
  """Get all available offers (not accepted and not rejected by current user)
  Returns:
      list[dict]: Each offer with:
          - offer: Basic offer info
          - owner: Owner details
          - cards_given: List of cards being offered
          - cards_wanted: List of cards requested
  """
  # Base query for available offers
  query = select(Offer).where(Offer.accepted_by == None)

  # Exclude offers rejected by this user
  if user_id:
    rejected_offers = session.exec(
      select(OfferRejections.offer_id)
      .where(OfferRejections.user_id == user_id)
    ).all()

    if rejected_offers:
      query = query.where(Offer.id.not_in(rejected_offers))
  
  offers = session.exec(query).all()
  
  results = []
  for offer in offers:
    # Get owner info
    owner = session.get(User, offer.user_id)
    
    # Get cards being offered
    cards_given = session.exec(
      select(YugiohCard)
      .join(OfferCardsGiven, YugiohCard.id == OfferCardsGiven.card_id)
      .where(OfferCardsGiven.offer_id == offer.id)
    ).all()
    
    # Get cards wanted
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants, YugiohCard.id == OfferCardsWants.card_id)
      .where(OfferCardsWants.offer_id == offer.id)
    ).all()
    
    # Format the response
    results.append({
      "offer": {
        "id": offer.id,
        "user_id": offer.user_id,
        "accepted_by": offer.accepted_by
      },
      "owner": {
        "id": owner.id,
        "name": owner.name
      },
      "cards_given": [
        {
          "id": card.id,
          "name": card.name,
          "card_type": card.card_type.value,
          "monster_type": card.monster_type.value if card.monster_type else None
        }
        for card in cards_given
      ],
      "cards_wanted": [
        {
          "id": card.id,
          "name": card.name,
          "card_type": card.card_type.value,
          "monster_type": card.monster_type.value if card.monster_type else None
        }
        for card in cards_wanted
      ]
    })

  return results


###############################################################################
@router.get("/offers/accepted/{user_id}", response_model=list[dict])
def list_accepted_offers(user_id: int, session: SessionDep):
  """Get all offers that the specified user has accepted"""
  offers = session.exec(
    select(Offer).where(Offer.accepted_by == user_id)
  ).all()
    
  results = []
  for offer in offers:
    owner = session.get(User, offer.user_id)
    results.append({
      "offer": offer,
      "owner": {
        "id": owner.id,
        "name": owner.name
      }
    })
    
  return results

###############################################################################
@router.post("/offers/respond")
def respond_to_offer(
  offer_id: int,
  user_id: int,  # The user responding to the offer
  accepted: bool,
  session: SessionDep
):
  """Respond to an offer (accept or reject)
  - If accepted: transfers cards between users and creates exchange record
  - If rejected: records the rejection for this user"""

  # First get just the offer without relationships
  offer = session.exec(
    select(Offer)
    .where(Offer.id == offer_id)
  ).first()
  
  if not offer:
    raise HTTPException(status_code=404, detail="Offer not found")
  
  # Check if offer is already accepted
  if offer.accepted_by is not None:
    raise HTTPException(status_code=400, detail="Offer already accepted")
  
  # Get both users
  offering_user = session.get(User, offer.user_id)
  responding_user = session.get(User, user_id)
  
  if not offering_user or not responding_user:
    raise HTTPException(status_code=404, detail="User not found")
  
  if accepted:
    # First get all cards the offer wants
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants, YugiohCard.id == OfferCardsWants.card_id)
      .where(OfferCardsWants.offer_id == offer_id)
    ).all()

    # Check if responding user owns all wanted cards
    for card in cards_wanted:
      ownership = session.exec(
        select(UserCard)
          .where(UserCard.user_id == user_id)
          .where(UserCard.card_id == card.id)
      ).first()
        
      if not ownership:
        raise HTTPException(
          status_code=400,
          detail=f"Card {card.id} ({card.name}) not found in your collection"
        )
      
    offer.accepted_by = user_id
    session.add(offer)

    # Create the exchange record
    exchange = Exchange(
      user_accepted=user_id,
      offer_id=offer_id,
      date=datetime.now().isoformat()
    )
    session.add(exchange)

    # Transfer cards from offering user to accepting user
    for card in offer.cards_given:
      # Remove from offering user
      session.exec(
        delete(UserCard)
        .where(UserCard.user_id == offer.user_id)
        .where(UserCard.card_id == card.id)
      )
      # Add to accepting user
      session.add(UserCard(user_id=user_id, card_id=card.id))

    # Transfer wanted cards from accepting user to offering user
    for card in offer.cards_wants:
      # Remove from accepting user
      session.exec(
        delete(UserCard)
        .where(UserCard.user_id == user_id)
        .where(UserCard.card_id == card.id)
      )
      # Add to offering user
      session.add(UserCard(user_id=offer.user_id, card_id=card.id))
    
    session.commit()
    message = "Offer accepted and cards exchanged"

  else:
    # Record rejection
    rejection = OfferRejections(offer_id=offer_id, user_id=user_id)
    session.add(rejection)
    message = "Offer rejected"
  
  #session.commit()
  
  return {
    "ok": True,
    "message": message,
    "offer_id": offer_id,
    "accepted": accepted
  }

###############################################################################
@router.get("/user/{user_id}/cards", response_model=list[YugiohCardRead])
def get_user_cards(
  user_id: int,
  session: SessionDep,
):
  """get all the user cards"""
  # Get all card IDs owned by the user
  user_card_ids = session.exec(
    select(UserCard.card_id)
    .where(UserCard.user_id == user_id)
  ).all()

  if not user_card_ids:
    return []

  # Get the full card details for these cards
  user_cards = session.exec(
    select(YugiohCard)
    .where(YugiohCard.id.in_(user_card_ids))
  ).all()

  return user_cards

#########################################################################################
@router.get("/exchanges", response_model=list[dict])
def list_all_exchanges(
  session: SessionDep,
  user_id: int | None = None  # Optional filter by user
):
  """
  Get all completed exchanges.
  
  Args:
    user_id: Optional filter to only show exchanges involving this user
  Returns:
    List of exchanges with details including:
    - exchange: Basic exchange info
    - offer: Original offer details
    - offering_user: User who created the offer
    - accepting_user: User who accepted the offer
    - cards_given: Cards that were exchanged
    - cards_wanted: Cards that were requested
  """
  # Base query
  query = select(Exchange)
  
  # Optional user filter
  if user_id:
    query = query.where(
      (Exchange.user_accepted == user_id) |
      (Offer.user_id == user_id)
    ).join(Offer, Exchange.offer_id == Offer.id)
  
  exchanges = session.exec(query).all()
  
  results = []
  for exchange in exchanges:
    # Get related offer
    offer = session.get(Offer, exchange.offer_id)
    
    # Get user info
    offering_user = session.get(User, offer.user_id)
    accepting_user = session.get(User, exchange.user_accepted)
    
    # Get cards involved
    cards_given = session.exec(
      select(YugiohCard)
      .join(OfferCardsGiven, YugiohCard.id == OfferCardsGiven.card_id)
      .where(OfferCardsGiven.offer_id == offer.id)
    ).all()
    
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants, YugiohCard.id == OfferCardsWants.card_id)
      .where(OfferCardsWants.offer_id == offer.id)
    ).all()
    
    # Format response
    results.append({
      "exchange": {
        "id": exchange.id,
        "date": exchange.date,
        "offer_id": exchange.offer_id
      },
      "offer": {
        "id": offer.id,
        "created_by": offer.user_id
      },
      "offering_user": {
        "id": offering_user.id,
        "name": offering_user.name
      },
      "accepting_user": {
        "id": accepting_user.id,
        "name": accepting_user.name
      },
      "cards_given": [
        {
          "id": card.id,
          "name": card.name,
          "card_type": card.card_type.value,
          "monster_type": card.monster_type.value if card.monster_type else None
        }
        for card in cards_given
      ],
      "cards_wanted": [
        {
          "id": card.id,
          "name": card.name,
          "card_type": card.card_type.value,
          "monster_type": card.monster_type.value if card.monster_type else None
        }
        for card in cards_wanted
      ]
    })
  
  return results
