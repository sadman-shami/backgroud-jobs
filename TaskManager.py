from asyncio import Queue, Task, create_task, gather, sleep
from random import randint
from typing import List

from models import Task as AppTask
from database import tasks
from WebsocketManager import websocketmanager
from loggerstream import logger

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
      create_task(self._worker(i))
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

  async def _worker(self, worker_id: int):
    while True:
      task: AppTask = await self._queue.get()
      try:
        await logger(f"Worker {worker_id} Started job for Task - {task.id}")
        await self._do_task(task)
      except Exception:
        await logger(f"Worker {worker_id} Failed to do task for Task - {task.id}")
        task.result = None
        task.status = "FAILED"
        tasks[task.id] = task
      finally:
        tasks_list = [tasks[task_id].model_dump_json() for task_id in tasks.keys()]
        await websocketmanager.send_json({"payload": tasks_list, "type": "get_todos"})
        self._queue.task_done()
        await logger(f"Worker {worker_id} Finished task for Task - {task.id}")

  async def _do_task(self, task: AppTask):
    t1 = randint(5,10)
    await logger(f"Sleeping for {t1} for Task - {task.id}")
    await sleep(t1)
    await logger(f"Expression is Evaluating for Task - {task.id}")
    result = eval(task.expression)
    await logger(f"Evaluating Finished for Task - {task.id}")
    task.result = str(result)
    task.status = "DONE"
    tasks[task.id] = task
    t2 = randint(5,10)
    await logger(f"Sleeping for {t2} for Task - {task.id}")
    await sleep(t2)

taskmanager = TaskManager()