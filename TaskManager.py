from asyncio import Queue, Task, create_task, gather, sleep
from random import randint
from typing import List

from models import Task as AppTask
from database import tasks
from WebsocketManager import websocketmanager

class TaskManager():
  def __init__(
      self,
      maxsize: int = 100,
      worker: int = 4
  ):
    self._queue: Queue = Queue(maxsize=maxsize)
    self.worker = worker
    self._worker_tasks: List[Task] = []

  async def start(self):
    self._worker_tasks = [
      create_task(self._worker())
      for i in range(self.worker)
    ]

  async def stop(self):
    await self._queue.join()

    for task in self._worker_tasks:
      task.cancel()

    await gather(
      *self._worker_tasks,
      return_exceptions=True
    )

  async def add(self, task: AppTask):
    if task.status == "PROCESSING":
      await self._queue.put(task)

  async def _worker(self):
    while True:
      task: AppTask = await self._queue.get()
      try:
        await self._do_task(task)
      except ZeroDivisionError:
        task.result = None
        task.status = "FAILED"
        tasks[task.id] = task
      finally:
        tasks_list = [tasks[task_id].model_dump_json() for task_id in tasks.keys()]
        await websocketmanager.send_json({"payload": tasks_list, "type": "get_todos"})
        self._queue.task_done()

  async def _do_task(self, task: AppTask):
    await sleep(randint(1,5))
    result = eval(task.expression)
    task.result = result
    task.status = "DONE"
    await sleep(randint(5,10))
    tasks[task.id] = task

taskmanager = TaskManager()