import asyncio
from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def _send_to_user_async(self, user_id: int, payload: dict):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_json(payload)

    def send_to_user(self, user_id: int, payload: dict):
        """
        SAFE sync entry point (can be called from sync code)
        """
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._send_to_user_async(user_id, payload))
        except RuntimeError:
            # No event loop → ignore (user not connected or HTTP context)
            pass


manager = ConnectionManager()
