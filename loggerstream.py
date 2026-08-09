from datetime import datetime

from WebsocketManager import websocketmanager

async def logger(text: str):
  time = datetime.now().strftime("%H:%M:%S")
  log = f"[{time}] {text}"
  await websocketmanager.send_json({"payload": log, "type": "logging"})
