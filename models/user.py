from sqlmodel import SQLModel, Field

# Tabela do usuario tem nome e senha (por enquanto)
class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str
  password: str