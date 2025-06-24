from typing import Any, Generator, Sequence
from sqlmodel import Sequence, create_engine, SQLModel, Session, select, or_
from sqlalchemy import text

from models import YugiohCard
from models.yugioh_card import YugiohCard, CardType, MonsterType
from models.offer import Exchange, Offer, OfferCardsGiven, OfferCardsWants
from models.user import User, UserCard, UserWishlist

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
  # Create a Singleton for this class, so only one instance can be called
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  @staticmethod
  def create_card(name: str, card_type: CardType, monster_type: MonsterType | None) -> None:
    with Session(ENGINE) as session:
      session.add(YugiohCard(name=name, card_type=card_type, monster_type=monster_type))
      session.commit()

  @staticmethod
  def select_card(name: str = "", card_type: CardType | None = None, monster_type: MonsterType | None = None, return_one: bool = False):
    with Session(ENGINE) as session:
      # Seleciona todas as linhas da database que possuem o parâmetro passado, se tiver parâmetro
      sql_like_name = YugiohCard.name.like(f'%{name}%') # type: ignore
      statement = select(YugiohCard)\
        .where(sql_like_name)\
        .where(or_(YugiohCard.card_type == card_type, card_type == None))\
        .where(or_(YugiohCard.monster_type == monster_type, monster_type == None))
      
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      cards: list[YugiohCard]
      if return_one:
        cards =  [results.one()]
      else:
        cards = list(results.all())
      return cards

  # TODO: check for errors
  @staticmethod
  def select_cards_by_name(names: list[str]) -> list[YugiohCard]:
    result: list[YugiohCard] = []
    for card_name in names:
      selected_cards = card_operations.select_card(name=card_name, return_one=True)
      result.extend(selected_cards)

    return result

#########################################################################################
class user_operations:
  # Create a Singleton for this class, so only one instance can be called
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance
  
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
  
  @staticmethod
  def add_card_wishlist(user_id: int, card_id: int) -> None:
    with Session(ENGINE) as session:
      session.add(UserWishlist(user_id=user_id,card_id=card_id))
      session.commit()

  @staticmethod
  def get_user_wishlist(user_id: int):
    with Session(ENGINE) as session:
      wishlist_id = session.exec(select(UserWishlist.card_id).where(UserWishlist.user_id == user_id)).all()
      sql_in = YugiohCard.id.in_(wishlist_id) # type: ignore
      statement = select(YugiohCard).where(sql_in)
      results = session.exec(statement).all()
      return results
    
  @staticmethod
  def add_user_card(user_id: int, card_id: int) -> None:
    with Session(ENGINE) as session:
      session.add(UserCard(user_id=user_id,card_id=card_id))
      session.commit()

  @staticmethod
  def get_row_wishlist(user_id: int, card_id: int) -> UserWishlist:
    with Session(ENGINE) as session:
      statement = select(UserWishlist).where(UserWishlist.card_id == card_id, UserWishlist.user_id == user_id)
      result = session.exec(statement).one()
      return result

  @staticmethod
  def get_row_user_card(user_id: int, card_id: int) -> UserCard:
    with Session(ENGINE) as session:
      statement = select(UserCard).where(UserCard.card_id == card_id, UserCard.user_id == user_id)
      result = session.exec(statement).one()
      return result
    
#########################################################################################
class offer_operations:
  # Create a Singleton for this class, so only one instance can be called
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance
  
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
  # Create a Singleton for this class, so only one instance can be called
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance
  
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
