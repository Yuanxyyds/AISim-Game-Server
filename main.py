from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from session.shared_queue import simulation_message_queue
from llm import load_llama_model, load_deepseek_model
from simulations.introduction import simulate_introductions
import asyncio

app = FastAPI()
active_player: WebSocket = None


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

    load_llama_model()
    asyncio.create_task(simulate_introductions())
    await asyncio.sleep(0)
    print("✅ Player connected")

    try:
        while True:
            if not simulation_message_queue.empty():
                print("Message Detected!")
                message = simulation_message_queue.get()
                await websocket.send_text(f"{message['speaker']}: {message['content']}")
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("❌ Player disconnected")
    finally:
        active_player = None
    
