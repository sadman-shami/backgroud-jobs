from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from router import router
from database import tasks
from models import Task
from TaskManager import taskmanager

def create_tasks():
  for i in range(10):
    new_task = Task(expression=f"{(i+1)**2}+{(i+2)**2}", id=uuid4(), created_at=datetime.now(timezone.utc))
    tasks[new_task.id] = new_task
  print('[Automated Task]: Task Created')
  for i in range(10, 20):
    new_task = Task(expression=f"{(i+1)**2}+{(i+2)**2}", id=uuid4(), created_at=datetime.now(timezone.utc), status="DONE", result=eval(f"{(i+1)**2}+{(i+2)**2}"))
    tasks[new_task.id] = new_task
  print('[Automated Task]: Task Created')
  for i in range(20, 30):
    new_task = Task(expression=f"{(i+1)**2}+{(i+2)**2}", id=uuid4(), created_at=datetime.now(timezone.utc), status="FAILED")
    tasks[new_task.id] = new_task
  print('[Automated Task]: Task Created')

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
