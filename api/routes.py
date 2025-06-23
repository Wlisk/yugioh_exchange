from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select

from api.errors import CardNotFoundException
from models.offer import Exchange, Offer, OfferCardsGiven, OfferCardsWants, OfferRejections
from models.user import User, UserCard
from models.yugioh_card import CardType, MonsterType, YugiohCard, YugiohCardRead, \
  YugiohCardCreate, YugiohCardUpdate
from db.main import card_operations, user_operations, get_session
from api.utils import check_card

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

###############################################################################
@router.get("/cards", response_model=list[YugiohCardRead])
async def get_cards_all(session: SessionDep):
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
  if db_card is None:
    raise CardNotFoundException(card_id)

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
      sql_not_in = Offer.id.not_in(rejected_offers) # type: ignore
      query = query.where(sql_not_in)
  
  offers = session.exec(query).all()
  
  results = []
  for offer in offers:
    # Get owner info
    owner = session.get(User, offer.user_id)
    if owner is None:
      raise Exception(f'Owner not found for offer id {offer.user_id}')
    
    # Get cards being offered
    cards_given = session.exec(
      select(YugiohCard)
      .join(OfferCardsGiven)
      .where(OfferCardsGiven.card_id == YugiohCard.id)
      .where(OfferCardsGiven.offer_id == offer.id)
    ).all()
    
    # Get cards wanted
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants)
      .where(OfferCardsWants.card_id == YugiohCard.id)
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
    if owner is None:
      raise Exception(f'Owner not found for offer id {offer.user_id}')

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
  
  if offering_user is None or responding_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  if accepted:
    # First get all cards the offer wants
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants)
      .where(OfferCardsWants.card_id == YugiohCard.id)
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
      user_cards = session.exec(
        select(UserCard)
        .where(UserCard.user_id == offer.user_id)
        .where(UserCard.card_id == card.id)
      ).all()
    
      # Remove selected cards from the offering user
      for user_card in user_cards:
        session.delete(user_card)
      
      if card.id is None:
        raise Exception('Card not found')
      
      # Add the offering card to the user
      session.add(UserCard(user_id=user_id, card_id=card.id))

    # Transfer wanted cards from accepting user to offering user
    for card in offer.cards_wants:
      # Remove from accepting user
      user_cards = session.exec(
        select(UserCard)
        .where(UserCard.user_id == user_id)
        .where(UserCard.card_id == card.id)
      ).all()
      
      # Remove selected cards from the accepting user
      for user_card in user_cards:
        session.delete(user_card)
      
      if card.id is None or offer.user_id is None:
        raise Exception('Error due to user or card id not found')
      
      # Add the accepting cards to the offering user
      session.add(UserCard(user_id=offer.user_id, card_id=card.id))
    
    session.commit()
    message = "Offer accepted and cards exchanged"

  else:
    # Record rejection
    rejection = OfferRejections(offer_id=offer_id, user_id=user_id)
    session.add(rejection)
    message = "Offer rejected"
  
  session.commit()
  
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
  sql_in = YugiohCard.id.in_(user_card_ids) # type: ignore
  user_cards = session.exec(
    select(YugiohCard)
    .where(sql_in)
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
      (Exchange.user_accepted == user_id)
    ).join(Offer, Exchange.offer_id == Offer.id)
  
  exchanges = session.exec(query).all()
  
  results = []
  for exchange in exchanges:
    # Format the date
    formatted_date = ""
    if exchange.date:
      try:
        date_obj = datetime.fromisoformat(exchange.date)
        formatted_date = date_obj.strftime('%d/%m/%Y às %H:%M')
      except ValueError:
        formatted_date = "Data Inválida"

    # Get related offer
    offer = session.get(Offer, exchange.offer_id)

    if offer is None:
      raise Exception('Offer not found')
    
    # Get user info
    offering_user = session.get(User, offer.user_id)
    accepting_user = session.get(User, exchange.user_accepted)

    if offering_user is None or accepting_user is None:
      raise Exception('Accepting user or Offering user not found')
    
    # Get cards involved
    cards_given = session.exec(
      select(YugiohCard)
      .join(OfferCardsGiven)
      .where(OfferCardsGiven.card_id == YugiohCard.id)
      .where(OfferCardsGiven.offer_id == offer.id)
    ).all()
    
    cards_wanted = session.exec(
      select(YugiohCard)
      .join(OfferCardsWants)
      .where(OfferCardsWants.card_id == YugiohCard.id)
      .where(OfferCardsWants.offer_id == offer.id)
    ).all()
    
    # Format response
    results.append({
      "exchange": {
        "id": exchange.id,
        "date": formatted_date,
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

###############################################################################
@router.get("/cards/{filters}", response_model=list[YugiohCardRead])
def get_cards_filtered(filters: str, session: SessionDep):
  """Get some Yu-gi-oh cards"""
  name, card_type, monster_type = filters.split("|")
  if (card_type == ""):
    card_type = None
  if (monster_type == ""):
    monster_type = None

  card_type = CardType.get_type_by_str(card_type)
  monster_type = MonsterType.get_type_by_str(monster_type)

  db_cards = card_operations.select_card(name=name, card_type=card_type, monster_type=monster_type)
  return db_cards

###############################################################################
@router.get("/user/{user_id}/cards/{filters}", response_model=list[YugiohCardRead])
def get_user_cards_filtered(
  user_id: int,
  filters: str,
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

  name, card_type, monster_type = filters.split("|")
  if (card_type == ""):
    card_type = None
  if (monster_type == ""):
    monster_type = None

  card_type = CardType.get_type_by_str(card_type)
  monster_type = MonsterType.get_type_by_str(monster_type)
  # Get filtered cards
  filtered_cards = card_operations.select_card(name=name, card_type=card_type, monster_type=monster_type)

  # Get the full card details for user cards
  sql_in_id = YugiohCard.id.in_(user_card_ids) # type: ignore
  user_cards = session.exec(
    select(YugiohCard)
    .where(sql_in_id)
  ).all()

  filtered_user_cards = [card for card in user_cards if card in filtered_cards]

  return filtered_user_cards

###############################################################################
@router.get("/user/{user_id}/wishlist", response_model=list[YugiohCardRead])
def get_wishlist_cards(
  user_id: int,
  session: SessionDep,
):
  cards = user_operations.get_user_wishlist(user_id)
  return cards

###############################################################################
@router.post("/user/{user_id}/wishlist/{card_id}")
def set_wishlist_card(
  user_id: int,
  card_id: int,
  session: SessionDep,
):
  user_operations.add_card_wishlist(user_id=user_id, card_id=card_id)

###############################################################################

@router.delete("/user/{user_id}/wishlist/{card_id}")
def delete_wishlist_card(
  user_id: int,
  card_id: int,
  session: SessionDep,
):
  row = user_operations.get_row_wishlist(user_id, card_id)
  session.delete(row)
  session.commit()

###############################################################################

@router.post("/user/{user_id}/cards/{card_id}")
def add_user_card(
  user_id: int,
  card_id:int,
  session: SessionDep,
):
  user_operations.add_user_card(user_id=user_id, card_id=card_id)

###############################################################################

@router.delete("/user/{user_id}/cards/{card_id}")
def delete_user_card(
  user_id: int,
  card_id: int,
  session: SessionDep,
):
  row = user_operations.get_row_user_card(user_id, card_id)
  session.delete(row)
  session.commit()
