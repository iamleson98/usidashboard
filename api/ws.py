from fastapi import APIRouter, WebSocket

SocketRouter = APIRouter(prefix="/ws", tags=["web sockets"])

@SocketRouter.websocket("/checking")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
