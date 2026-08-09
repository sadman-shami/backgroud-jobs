from fastapi import WebSocket
from typing import Any

class WebsocketManager():
  def __init__(self):
    self.client: WebSocket | None = None
  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.client = websocket
  async def disconnect(self):
    self.client = None
  async def send_json(self, message: Any):
    await self.client.send_json(message)

websocketmanager = WebsocketManager()