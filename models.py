from pydantic import BaseModel, Field
from typing import Optional, Literal, Any
from uuid import UUID
from datetime import datetime

STATUS = Literal['DONE', 'PROCESSING', 'FAILED']

class TaskBase(BaseModel):
  expression: str = Field(..., min_length=1, description="Mathematical expression in string format")

class TaskCreate(TaskBase):
  pass

class Task(TaskBase):
  id: UUID = Field(..., description="ID for the task")
  status: Optional[STATUS] = Field(default="PROCESSING", description="Status of task")
  result: Optional[int | float] = Field(default=None, description="Result of the task")
  created_at: datetime = Field(..., description="Time of task creation")