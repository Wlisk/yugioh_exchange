from typing import Union

from models.yugioh_card import YugiohCard
from api.errors import CardNotFoundException

def check_card(card: YugiohCard | None, id: Union[int, None] = None) -> CardNotFoundException | None:
  """Raise an error if the card is not valid"""
  if card is None:
    raise CardNotFoundException(id if id is not None else 0)