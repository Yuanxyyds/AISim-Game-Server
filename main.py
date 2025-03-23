from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
active_player: WebSocket = None  # Store the active player's WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_player

    if active_player:  # If someone is already connected, reject new connections
        await websocket.accept()
        await websocket.send_text("❌ Game is already being played by another player.")
        await websocket.close()
        return

    # Assign the new player
    active_player = websocket
    await websocket.accept()
    print("✅ Player connected")

    try:
        while True:
            ai_update = generate_ai_action()  # Simulate AI action
            await websocket.send_text(ai_update)
            await asyncio.sleep(3)  # Send AI updates every 3 seconds
    except WebSocketDisconnect:
        print("❌ Player disconnected")
    finally:
        active_player = None  # Allow a new player to connect
