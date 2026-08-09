from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from router import router
from TaskManager import taskmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
  await taskmanager.start()
  yield
  await taskmanager.stop()


app = FastAPI(title="Background Jobs", lifespan=lifespan)
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=['*'],
  allow_methods=['*'],
  allow_headers=['*']
)

app.include_router(router)
