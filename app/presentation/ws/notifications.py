from fastapi import WebSocket, WebSocketDisconnect
from app.presentation.ws.connection_manager import manager
from app.presentation.api.dependencies import get_current_user_id_ws


async def notifications_ws(websocket: WebSocket):
    user_id = await get_current_user_id_ws(websocket)

    await manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
