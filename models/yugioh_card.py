from sqlmodel import SQLModel, Field, Column, Enum
import enum

class CardType(str, enum.Enum):
  SPELL = "Spell"
  MONSTER = "Monster"
  TRAP = "Trap"

  @staticmethod
  def get_type_by_str(type: str | None):
    type = type.lower().strip() if type is not None else ''
    result: CardType

    match type:
      case '':        result = None
      case 'spell':   result = CardType.SPELL
      case 'trap':    result = CardType.TRAP
      case 'monster': result = CardType.MONSTER
      case _:         result = CardType.MONSTER
    
    return result

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

  @staticmethod
  def get_type_by_str(type: str | None):
    type = type.lower().strip() if type is not None else ''
    result: MonsterType

    match type:
      case '':                result = None
      case 'aqua':            result = MonsterType.AQUA
      case 'beast':           result = MonsterType.BEAST
      case 'beast-warrior':   result = MonsterType.BEAST_WARRIOR
      case 'creator god':     result = MonsterType.CREATOR_GOD
      case 'cyberse':         result = MonsterType.CYBERSE
      case 'dinosaur':        result = MonsterType.DINOSAUR
      case 'divine-beast':    result = MonsterType.DIVINE_BEAST
      case 'dragon':          result = MonsterType.DRAGON
      case 'fairy':           result = MonsterType.FAIRY
      case 'fiend':           result = MonsterType.FIEND
      case 'fish':            result = MonsterType.FISH
      case 'insect':          result = MonsterType.INSECT
      case 'machine':         result = MonsterType.MACHINE
      case 'plant':           result = MonsterType.PLANT
      case 'psychic':         result = MonsterType.PSYCHIC
      case 'pyro':            result = MonsterType.PYRO
      case 'reptile':         result = MonsterType.REPTILE
      case 'rock':            result = MonsterType.ROCK
      case 'sea serpent':     result = MonsterType.SEA_SERPENT
      case 'spellcaster':     result = MonsterType.SPELLCASTER
      case 'thunder':         result = MonsterType.THUNDER
      case 'warrior':         result = MonsterType.WARRIOR
      case 'winged beast':    result = MonsterType.WINGED_BEAST
      case 'wyrm':            result = MonsterType.WYRM
      case 'zombie':          result = MonsterType.ZOMBIE
      case _:                 result = MonsterType.SPELLCASTER
      
    return result

# Base class
class YugiohCardBase(SQLModel):
  name: str = Field(index=True, unique=True)
  card_type: CardType = Field(sa_column=Column(Enum(CardType)))
  monster_type: MonsterType | None = Field(default=None, sa_column=Column(Enum(MonsterType)))
  image_url: str = Field(default="https://images.ygoprodeck.com/images/assets/CardBack.jpg")

# Table class for DB operations (private model)
# Tabela da carta, possui atributos nome, tipo da carta e tipo do monstro
class YugiohCard(YugiohCardBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  card_type: CardType = Field(index=True)
  monster_type: MonsterType | None = Field(default=None, index=True)
  image_url: str = Field(default="https://images.ygoprodeck.com/images/assets/CardBack.jpg")

# class for http responses (public model)
class YugiohCardRead(YugiohCardBase):
  id: int

# class for creating cards (public model)
class YugiohCardCreate(YugiohCardBase):
  pass

# class for updating cards (public model)
class YugiohCardUpdate(YugiohCardBase):
  name: str | None = None # type: ignore
  card_type: CardType | None = None # type: ignore
  monster_type: MonsterType | None = None
