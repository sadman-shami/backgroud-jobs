from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone

from models import (
  TaskCreate,
  Task
)
from database import tasks
from TaskManager import taskmanager
from WebsocketManager import websocketmanager

router = APIRouter(prefix="/task")

def get_tasks() -> List[Task]:
  tasks_list = [tasks[task_id].model_dump_json() for task_id in tasks.keys()]
  return tasks_list

@router.post("/")
async def create_task(task: TaskCreate):
  new_task = Task(id=uuid4(), expression=task.expression, status="PROCESSING", result=None, created_at=datetime.now(timezone.utc))
  tasks[new_task.id] = new_task
  await taskmanager.add(new_task)
  await websocketmanager.send_json({"payload": get_tasks(), "type": "get_todos"})
  return new_task

@router.delete("/{task_id}", response_model=Task)
async def delete_task(task_id: UUID):
  if task_id not in tasks:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task of ID {task_id} not found")
  if tasks[task_id].status == "PROCESSING":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Task of ID {task_id} is in background task")
  task = tasks[task_id]
  del tasks[task_id]
  await websocketmanager.send_json({"payload": get_tasks(), "type": "get_todos"})
  return task

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocketmanager.connect(websocket)
  await websocketmanager.send_json({"payload": get_tasks(), "type": "get_todos"})
  try:
    while True:
      await websocket.receive_json()
  except WebSocketDisconnect:
    await websocketmanager.disconnect()
