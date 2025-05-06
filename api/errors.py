from fastapi import HTTPException

class CardNotFoundException(HTTPException):
  """Custom exception class for card not found errors."""
  
  def __init__(self, card_id: int):
    """Initialize the exception with a card ID."""
    super().__init__(status_code=404, detail=f"Card(ID={card_id}) not found")