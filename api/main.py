from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import router
from db.main import init_db
from db.sample_data import create_sample_data

@asynccontextmanager
async def lifespan(app: FastAPI):
  """Initialize the db and create sample data (if there is no data) on api startup."""
  init_db()
  create_sample_data()
  yield
  # add cleanup (free resource) code here if needed

app = FastAPI(lifespan=lifespan)
app.include_router(router)