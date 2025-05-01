from typing import Union

from models.yugioh_card import YugiohCard
from api.errors import CardNotFoundException

def check_card(card: YugiohCard, id: Union[int, None] = None) -> CardNotFoundException:
  """Raise an error if the card is not valid"""
  if not card:
    raise CardNotFoundException(id)