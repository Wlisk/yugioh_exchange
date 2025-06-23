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
  def create_card(name: str, card_type: CardType, monster_type: MonsterType = None) -> None:
    with Session(ENGINE) as session:
      session.add(YugiohCard(name=name, card_type=card_type, monster_type=monster_type))
      session.commit()

  def select_card(name: str = "", card_type: CardType = None, monster_type: MonsterType = None, return_one: bool = False) -> YugiohCard | Sequence[YugiohCard]:
    with Session(ENGINE) as session:
      # Seleciona todas as linhas da database que possuem o parâmetro passado, se tiver parâmetro
      statement = select(YugiohCard)\
        .where(YugiohCard.name.like('%' + name + '%'))\
        .where(or_(YugiohCard.card_type == card_type, card_type == None))\
        .where(or_(YugiohCard.monster_type == monster_type, monster_type == None))
      
      results = session.exec(statement, execution_options={"prebuffer_rows": True})
      if return_one:
        return results.one()
      else:
        return results.all()

#########################################################################################
class user_operations:
  def create_user(name: str, password: str) -> None:
    with Session(ENGINE) as session:
      session.add(User(name=name, password=password))
      session.commit()

  def get_user(name: str) -> Sequence[User]:
    with Session(ENGINE) as session:
      statement = select(User).where(User.name.like('%' + name + '%'))
      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results
    
  def add_card_wishlist(user_id: int, card_id: int) -> None:
    with Session(ENGINE) as session:
      session.add(UserWishlist(user_id=user_id,card_id=card_id))
      session.commit()

  def get_user_wishlist(user_id: int) -> Sequence[YugiohCard]:
    with Session(ENGINE) as session:
      wishlist_id = session.exec(select(UserWishlist.card_id).where(UserWishlist.user_id == user_id)).all()
      statement = select(YugiohCard).where(YugiohCard.id.in_(wishlist_id))
      results = session.exec(statement).all()
      return results
    
  def add_user_card(user_id: int, card_id: int) -> None:
    with Session(ENGINE) as session:
      session.add(UserCard(user_id=user_id,card_id=card_id))
      session.commit()

  def get_row_wishlist(user_id: int, card_id: int) -> UserWishlist:
    with Session(ENGINE) as session:
      statement = select(UserWishlist).where(UserWishlist.card_id == card_id, UserWishlist.user_id == user_id)
      result = session.exec(statement).one()
      return result

  def get_row_user_card(user_id: int, card_id: int) -> UserWishlist:
    with Session(ENGINE) as session:
      statement = select(UserCard).where(UserCard.card_id == card_id, UserCard.user_id == user_id)
      result = session.exec(statement).one()
      return result
    
#########################################################################################
class offer_operations:
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

  def get_offer_from_id(id:int) -> Sequence[Offer]:
    with Session(ENGINE) as session:
      statement = text("SELECT offer.id AS offer_id, u.name AS user_name, card_given.name AS given_card_name, card_want.name AS wants_card_name " \
      "FROM offer LEFT JOIN offercardsgiven given ON offer.id = given.offer_id JOIN offercardswants wanted ON offer.id = wanted.offer_id " \
      "LEFT JOIN user u ON offer.user_id = u.id LEFT JOIN yugiohcard card_given ON card_given.id = given.card_id LEFT JOIN yugiohcard card_want ON card_want.id = wanted.card_id WHERE (offer.id = :id_2)").bindparams(id_2 = id)

      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results

#########################################################################################
class exchange_operations:
  def create_exchange(user_id:int, offer_id:int) -> None:
    with Session(ENGINE) as session:
      session.add(Exchange(user_accepted=user_id, offer_id=offer_id, date= "")) #TODO data
      session.commit()

  def get_exchange(id:int = None, user_id:int = None, offer_id:int = None) -> Sequence[Exchange]:
    with Session(ENGINE) as session:
      statement = select(Exchange).where(
        or_(Exchange.id == id, id == None)).where(
        or_(Exchange.user_accepted == user_id, user_id == None)).where(or_(Exchange.offer_id == offer_id, offer_id == None))
      results = session.exec(statement, execution_options={"prebuffer_rows": True}).all()
      return results
