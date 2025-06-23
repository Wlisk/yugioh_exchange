from sqlmodel import Session, select
from db.main import ENGINE
from models.offer import Exchange, Offer, OfferCardsGiven, OfferCardsWants
from models.user import User, UserCard
from models.yugioh_card import CardType, MonsterType, YugiohCard

CARDS = [
    YugiohCard(
        name="Blue-Eyes White Dragon",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.DRAGON,
    ),
    YugiohCard(
        name="Dark Magician",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.SPELLCASTER,
    ),
    YugiohCard(
        name="Red-Eyes Black Dragon",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.DRAGON,
    ),
    YugiohCard(
        name="Exodia the Forbidden One",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.SPELLCASTER,
    ),
    YugiohCard(
        name="Summoned Skull",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.FIEND,
    ),
    YugiohCard(name="Pot of Greed", card_type=CardType.SPELL),
    YugiohCard(name="Mirror Force", card_type=CardType.TRAP),
    YugiohCard(
        name="Black Luster Soldier",
        card_type=CardType.MONSTER,
        monster_type=MonsterType.WARRIOR,
    ),
    YugiohCard(name="Harpie's Feather Duster", card_type=CardType.SPELL),
    YugiohCard(name="Solemn Judgment", card_type=CardType.TRAP),
]

USERS = [
    User(name="Gui", password="ggg"),
    User(name="Mat", password="mmm"),
    User(name="Ric", password="rrr"),
    User(name="admin", password="admin"),
]

def delete_db() -> None:
  """Delete all cards and users from the database"""
  with Session(ENGINE) as session:
    for table in [YugiohCard, User, Offer, OfferCardsWants, OfferCardsGiven, Exchange, UserCard]:
      statement = select(table)
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      for i in results:
        session.delete(i)
      session.commit()

# Cria entradas de teste na database
def create_sample_data() -> None:
  """Add sample data to the database"""
  with Session(ENGINE) as session:
    # Clear existing data first
    # TODO: add an if to verify if the database is empty before deleting and modifying it
    delete_db()

    # Add cards to db
    for card in CARDS:
      session.add(card)
    session.commit()
    for card in CARDS:
      session.refresh(card)

    # Add users to db
    for user in USERS:
      session.add(user)
    session.commit()
    for user in USERS:
      session.refresh(user)

    # Add user cards to db
    users = session.exec(select(User)).all()
    cards = session.exec(select(YugiohCard)).all()

    # verified user ids
    user_ids: list[int] = []
    for i, user in enumerate(users):
      user_ids.append(user.id if user.id is not None else i)

    # verified card ids
    card_ids: list[int] = []
    for i, card in enumerate(cards):
      card_ids.append(card.id if card.id is not None else i)

    USER_CARDS = [
      {"user_id": user_ids[0], "card_id": card_ids[1]},  # Dark Magician
      {"user_id": user_ids[0], "card_id": card_ids[2]},  # Exodia
      {"user_id": user_ids[0], "card_id": card_ids[5]},  # Pot of Greed
      {"user_id": user_ids[0], "card_id": card_ids[9]},  # Solemn Judgment
      {"user_id": user_ids[1], "card_id": card_ids[0]},  # Blue-Eyes
      {"user_id": user_ids[1], "card_id": card_ids[7]},  # Black Luster Soldier
      {"user_id": user_ids[1], "card_id": card_ids[8]},  # Harpie's Feather Duster
      {"user_id": user_ids[2], "card_id": card_ids[2]},  # Red-Eyes
      {"user_id": user_ids[2], "card_id": card_ids[4]},  # Summoned Skull
      {"user_id": user_ids[2], "card_id": card_ids[6]},  # Mirror Force
      {"user_id": user_ids[2], "card_id": card_ids[3]}
    ]
    for user_card in USER_CARDS:
      session.add(UserCard(**user_card))
    session.commit()
    
    # Create user offer and add to db
    offer1 = Offer(user_id=USERS[0].id)
    session.add(offer1)
    session.commit()
    session.refresh(offer1)

    offer2 = Offer(user_id=USERS[1].id)
    session.add(offer2)
    session.commit()
    session.refresh(offer2)

    session.add(OfferCardsGiven(offer_id=offer1.id, card_id=CARDS[0].id))
    session.add(OfferCardsWants(offer_id=offer1.id, card_id=CARDS[3].id))

    session.add(OfferCardsGiven(offer_id=offer2.id, card_id=CARDS[2].id))
    session.add(OfferCardsWants(offer_id=offer2.id, card_id=CARDS[1].id))
    session.commit()