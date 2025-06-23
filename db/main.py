from typing import Any, Generator
from sqlmodel import Sequence, create_engine, SQLModel, Session, select, or_
from sqlalchemy import text
from models.yugioh_card import YugiohCard, CardType, MonsterType
from models.offer import Exchange, Offer, OfferCardsGiven, OfferCardsWants
from models.user import User

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

#########################################################################################
class card_operations: 
  @staticmethod
  def create_card(name: str, card_type: CardType, monster_type: MonsterType | None) -> None:
    with Session(ENGINE) as session:
      session.add(YugiohCard(name=name, card_type=card_type, monster_type=monster_type))
      session.commit()

  @staticmethod
  def select_card(name: str = "", card_type: CardType | None = None, monster_type: MonsterType | None = None):
    with Session(ENGINE) as session:
      # Seleciona todas as linhas da database que possuem o parâmetro passado, se tiver parâmetro
      sql_like_name = YugiohCard.name.like(f'%{name}%') # type: ignore
      statement = select(YugiohCard)\
        .where(sql_like_name)\
        .where(or_(YugiohCard.card_type == card_type, card_type == None))\
        .where(or_(YugiohCard.monster_type == monster_type, monster_type == None))
      
      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results

#########################################################################################
class user_operations:
  @staticmethod
  def create_user(name: str, password: str) -> None:
    with Session(ENGINE) as session:
      session.add(User(name=name, password=password))
      session.commit()

  @staticmethod
  def get_user(name: str):
    with Session(ENGINE) as session:
      sql_like_name = User.name.like(f'%{name}%') # type: ignore
      statement = select(User).where(sql_like_name)
      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results

#########################################################################################
class offer_operations:
  @staticmethod
  def create_offer(user_id:int, cards_given:list[YugiohCard], cards_wanted:list[YugiohCard]) -> None:
    with Session(ENGINE) as session:
      offer = Offer(user_id=user_id)
      session.add(offer)
      session.commit()
      session.refresh(offer)
      for card in cards_given:
        session.add(OfferCardsGiven(offer_id=offer.id, card_id=card.id))
      for card in cards_wanted:
        session.add(OfferCardsWants(offer_id=offer.id, card_id=card.id))
      session.commit()

  @staticmethod
  def get_offer_from_id(id:int):
    with Session(ENGINE) as session:
        offer = session.get(Offer, id)
        if not offer:
            return None
            
        session.refresh(offer)
        return offer

#########################################################################################
class exchange_operations:
  @staticmethod
  def create_exchange(user_id:int, offer_id:int) -> None:
    with Session(ENGINE) as session:
      session.add(Exchange(user_accepted=user_id, offer_id=offer_id, date= "")) #TODO data
      session.commit()

  @staticmethod
  def get_exchange(id:int|None = None, user_id:int|None = None, offer_id:int|None = None):
    with Session(ENGINE) as session:
      statement = select(Exchange)\
      .where(or_(Exchange.id == id, id == None)) \
      .where(or_(Exchange.user_accepted == user_id, user_id == None)) \
      .where(or_(Exchange.offer_id == offer_id, offer_id == None))

      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results
    