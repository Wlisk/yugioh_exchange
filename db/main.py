from typing import Any, Generator
from sqlmodel import create_engine, SQLModel, Session, select
from models.yugioh_card import YugiohCard, CardType, MonsterType

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



def create_sample_data() -> None:
  """Add sample data to the database"""
  with Session(ENGINE) as session:
    # execute only if there is no data in the table
    if not session.exec(select(YugiohCard)).first(): 
      cards = [
        #YugiohCard(id=1, name="Blue-Eyes White Dragon"),
        #YugiohCard(id=2, name="Dark Magician"),
        #YugiohCard(id=3, name="Red-Eyes Black Dragon"),
        #YugiohCard(id=4, name="Exodia the Forbidden One"),
        #YugiohCard(id=5, name="Summoned Skull"),
        YugiohCard(id=1, name="Blue-Eyes White Dragon", card_type=CardType.MONSTER, monster_type=MonsterType.DRAGON),
        YugiohCard(id=2, name="Dark Magician", card_type=CardType.MONSTER, monster_type=MonsterType.SPELLCASTER),
        YugiohCard(id=3, name="Red-Eyes Black Dragon", card_type=CardType.MONSTER, monster_type=MonsterType.DRAGON),
        YugiohCard(id=4, name="Exodia the Forbidden One", card_type=CardType.MONSTER, monster_type=MonsterType.SPELLCASTER),
        YugiohCard(id=5, name="Summoned Skull", card_type=CardType.MONSTER, monster_type=MonsterType.FIEND),
        YugiohCard(id=6, name="Pot of Greed", card_type=CardType.SPELL),
        YugiohCard(id=7, name="Mirror Force", card_type=CardType.TRAP)
      ]
      session.add_all(cards)
      session.commit()
