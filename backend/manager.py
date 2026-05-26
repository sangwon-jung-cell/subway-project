from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # 현재 접속 중인 웹소켓 연결 리스트
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # 연결된 모든 브라우저에게 메시지 전송
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()