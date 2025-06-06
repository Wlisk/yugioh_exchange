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

    USER_CARDS = [
      {"user_id": users[0].id, "card_id": cards[1].id},  # Dark Magician
      {"user_id": users[0].id, "card_id": cards[2].id},  # Exodia
      {"user_id": users[0].id, "card_id": cards[5].id},  # Pot of Greed
      {"user_id": users[0].id, "card_id": cards[9].id},  # Solemn Judgment
      {"user_id": users[1].id, "card_id": cards[0].id},  # Blue-Eyes
      {"user_id": users[1].id, "card_id": cards[7].id},  # Black Luster Soldier
      {"user_id": users[1].id, "card_id": cards[8].id},  # Harpie's Feather Duster
      {"user_id": users[2].id, "card_id": cards[2].id},  # Red-Eyes
      {"user_id": users[2].id, "card_id": cards[4].id},  # Summoned Skull
      {"user_id": users[2].id, "card_id": cards[6].id},  # Mirror Force
      {"user_id": users[2].id, "card_id": cards[3].id}
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