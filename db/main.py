from typing import Any, Generator
from sqlmodel import create_engine, SQLModel, Session, select, or_
from sqlalchemy import text
from models.yugioh_card import YugiohCard, User, Offer, OfferCardsGiven, OfferCardsWants, CardType, MonsterType

DB_FILENAME = "yugioh.db"
DB_URL = f"sqlite:///{DB_FILENAME}"

ENGINE = create_engine(DB_URL, echo=True)  # show sql logs

def init_db() -> None:
  """Initialize db and create tables"""
  SQLModel.metadata.create_all(ENGINE)

def get_session() -> Generator[Session, Any, None]:
  """Dependency to get DB session"""
  with Session(ENGINE) as session:
    yield session

# Remove todas as cartas e usuários da database
def delete_db() -> None:
  with Session(ENGINE) as session:
    for table in [YugiohCard, User, Offer, OfferCardsWants, OfferCardsGiven]:
      statement = select(table)
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      for i in results:
        session.delete(i)
      session.commit()


# Cria entradas de teste na database
def create_sample_data() -> None:
  """Add sample data to the database"""
  with Session(ENGINE) as session:
    card_operations.create_card(name="Blue-Eyes White Dragon", card_type=CardType.MONSTER, monster_type=MonsterType.DRAGON),
    card_operations.create_card(name="Dark Magician", card_type=CardType.MONSTER, monster_type=MonsterType.SPELLCASTER),
    card_operations.create_card(name="Red-Eyes Black Dragon", card_type=CardType.MONSTER, monster_type=MonsterType.DRAGON),
    card_operations.create_card(name="Exodia the Forbidden One", card_type=CardType.MONSTER, monster_type=MonsterType.SPELLCASTER),
    card_operations.create_card(name="Summoned Skull", card_type=CardType.MONSTER, monster_type=MonsterType.FIEND),
    card_operations.create_card(name="Pot of Greed", card_type=CardType.SPELL),
    card_operations.create_card(name="Mirror Force", card_type=CardType.TRAP)

    user_operations.create_user(name="Mat", password="123")
    user_operations.create_user(name="Gui", password="111")
    user_operations.create_user(name="Ric", password="aaa")
    user_operations.create_user(name="admin", password="admin")

    user = user_operations.get_user("Mat").first()
    cardsIn = []
    for i in card_operations.select_card(name="drag"):
      cardsIn.append(i)
    print("\n\n\n")
    print(cardsIn)
    cardsOut = []
    for i in card_operations.select_card(card_type=CardType.TRAP):
      cardsOut.append(i)
    for i in card_operations.select_card(card_type=CardType.SPELL):
      cardsOut.append(i)
    print(cardsOut)
    print("\n\n\n")
    offer_operations.create_offer(user_id=user.id, cards_given=cardsIn, cards_wanted=cardsOut)

class card_operations:  
  def create_card(name: str, card_type: CardType, monster_type: MonsterType = None) -> None:
    with Session(ENGINE) as session:
      session.add(YugiohCard(name=name, card_type=card_type, monster_type=monster_type))
      session.commit()

  def select_card(name: str = "", card_type: CardType = None, monster_type: MonsterType = None): # -> list[YugiohCard]:
    with Session(ENGINE) as session:
      # Seleciona todas as linhas da database que possuem o parâmetro passado, se tiver parâmetro
      statement = select(YugiohCard)\
        .where(YugiohCard.name.like('%' + name + '%'))\
        .where(or_(YugiohCard.card_type == card_type, card_type is None))\
        .where(or_(YugiohCard.monster_type == monster_type, monster_type is None))
      
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      return results
    
class user_operations:
  def create_user(name: str, password: str) -> None:
    with Session(ENGINE) as session:
      session.add(User(name=name, password=password))
      session.commit()

  def get_user(name: str): # ->list[User]: Não é uma lista
    with Session(ENGINE) as session:
      statement = select(User).where(User.name.like('%' + name + '%'))
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      return results
    
class offer_operations:
  def create_offer(user_id:int, cards_given:list[YugiohCard], cards_wanted:list[YugiohCard]) -> None:
    with Session(ENGINE) as session:
      session.add(Offer(user_id=user_id, cards_given=cards_given, cards_wants=cards_wanted))
      session.commit()

  def get_offer_from_id(id:int): # -> list[Offer]: Não é uma lista

  ## TODO ARRUMAR ISSO QUE NÃO ESTÁ FUNCIONANDO
    with Session(ENGINE) as session:
      #statement = select(Offer, OfferCardsWants, OfferCardsGiven, YugiohCard).where(
      #            Offer.id == id, OfferCardsGiven.offer_id == id, OfferCardsWants.offer_id == id).join_from(
      #            from_=OfferCardsGiven, target=YugiohCard, onclause=OfferCardsGiven.card_id == YugiohCard.id).join_from(
      #            from_=OfferCardsWants, target=YugiohCard, onclause=OfferCardsWants.card_id == YugiohCard.id)
      #
      #statement = "SELECT offer.id, offer.user_id, offercardswants.offer_id, offercardswants.card_id, offercardsgiven.offer_id AS offer_id_1, offercardsgiven.card_id AS card_id_1, yugiohcard.name, yugiohcard.card_type, yugiohcard.monster_type, yugiohcard.id AS id_1" + \
      #            "FROM offercardsgiven JOIN yugiohcard ON offercardsgiven.card_id = yugiohcard.id, offercardswants JOIN yugiohcard ON offercardswants.card_id = yugiohcard.id, offer WHERE offer.id = :id_2 AND offercardsgiven.offer_id = :offer_id_2 AND offercardswants.offer_id = :offer_id_3"

      #statement = text("SELECT offer.id,\
      #                  user.name,\
      #                  yugiohcard.name as card_given,\
      #                  yugiohcard.name as card_,\
      #                  yugiohcard.card_type,\
      #                  yugiohcard.monster_type,\
      #                  yugiohcard.id AS card_id\
      #                  FROM offercardsgiven JOIN yugiohcard ON offercardsgiven.card_id = yugiohcard.id, user JOIN offer ON user.id = ofer.user_id, offercardswants JOIN yugiohcard ON offercardswants.card_id = yugiohcard.id, offer WHERE offer.id = :id_2 AND offercardsgiven.offer_id = :id_2 AND offercardswants.offer_id = :id_2").bindparams(id_2 = id)
      statement = text("SELECT offer.id AS offer_id, u.name AS user_name, card_given.name AS given_card_name, card_want.name AS wants_card_name FROM offer LEFT JOIN offercardsgiven given ON offer.id = given.offer_id LEFT JOIN offercardswants wanted ON offer.id = wanted.offer_id LEFT JOIN user u ON offer.user_id = u.id LEFT JOIN yugiohcard card_given ON card_given.id = given.card_id LEFT JOIN yugiohcard card_want ON card_want.id = wanted.card_id WHERE (offer.id = :id_2)").bindparams(id_2 = id)

      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results