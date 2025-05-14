from sqlmodel import SQLModel, Field, Column, Enum
import enum

class CardType(str, enum.Enum):
  SPELL = "Spell"
  MONSTER = "Monster"
  TRAP = "Trap"

class MonsterType(str, enum.Enum):
  AQUA = "Aqua"
  BEAST = "Beast"
  BEAST_WARRIOR = "Beast-Warrior"
  CREATOR_GOD = "Creator God"
  CYBERSE = "Cyberse"
  DINOSAUR = "Dinosaur"
  DIVINE_BEAST = "Divine-Beast"
  DRAGON = "Dragon"
  FAIRY = "Fairy"
  FIEND = "Fiend"
  FISH = "Fish"
  INSECT = "Insect"
  MACHINE = "Machine"
  PLANT = "Plant"
  PSYCHIC = "Psychic"
  PYRO = "Pyro"
  REPTILE = "Reptile"
  ROCK = "Rock"
  SEA_SERPENT = "Sea Serpent"
  SPELLCASTER = "Spellcaster"
  THUNDER = "Thunder"
  WARRIOR = "Warrior"
  WINGED_BEAST = "Winged Beast"
  WYRM = "Wyrm"
  ZOMBIE = "Zombie"

# Base class
class YugiohCardBase(SQLModel):
  name: str = Field(index=True)
  card_type: CardType = Field(sa_column=Column(Enum(CardType)))
  monster_type: MonsterType | None = Field(default=None, sa_column=Column(Enum(MonsterType)))

# Table class for DB operations (private model)
# Tabela da carta, possui atributos nome, tipo da carta e tipo do monstro
class YugiohCard(YugiohCardBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  card_type: CardType = Field(index=True)
  monster_type: MonsterType | None = Field(default=None, index=True)

# class for http responses (public model)
class YugiohCardRead(YugiohCardBase):
  id: int

# class for creating cards (public model)
class YugiohCardCreate(YugiohCardBase):
  pass

# class for updating cards (public model)
class YugiohCardUpdate(YugiohCardBase):
  name: str | None = None
  card_type: CardType | None = None
  monster_type: MonsterType | None = None
