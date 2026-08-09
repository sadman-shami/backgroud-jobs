# Fast API background task

Python asyncio queue has been used to do background jobs. Implemented websocket to get realtime data.

```
POST /task
DELETE /task/{task_id}

WS /task -> Realtime Data communication
```
