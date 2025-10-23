import socketio
from app.core.redis import redis_client
from sqlalchemy import event

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

async def broadcast_update(collection_name: str, action: str, item_id: int, data: dict):
    await sio.emit('update', {'collection': collection_name, 'action': action, 'id': item_id, 'data': data}, room=f"user_room_{data.get('user_id', 1)}")  # Room per user