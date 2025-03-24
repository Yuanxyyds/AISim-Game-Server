from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from resources.shared_queue import simulation_message_queue
from resources.llm import init_models
from controllers.conversation_controller import create_conversation
from controllers.game_state_controller import create_game
from controllers.player_controller import get_all_players_identity, update_memory
from prompts.utils import get_identity_prompts
from data.enums import ConversationType
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

    # init_models()
    # asyncio.create_task(simulate_introductions())
    # await asyncio.sleep(0)
    # print("✅ Player connected")

    # try:
    #     while True:
    #         if not simulation_message_queue.empty():
    #             print("Message Detected!")
    #             message = simulation_message_queue.get()
    #             await websocket.send_json(
    #                 {"message": message["speaker"], "content": message["content"]}
    #             )

    #         await asyncio.sleep(5)
    # except WebSocketDisconnect:
    #     print("❌ Player disconnected")
    # finally:
    #     active_player = None


def simple_simulation():
    # Initialize any models or resources needed
    init_models()
    game_id, player_ids = create_game()
    identities = get_all_players_identity(game_id=game_id)
    assert len(player_ids) == len(identities)
    identity_prompt = get_identity_prompts(identities)

    # Introduction
    conversation = create_conversation(
        game_id=game_id,
        type=ConversationType.INTRODUCTION,
        participants=[
            "Alice",
            "Bob",
            "Catherine",
            "David",
            "Edison",
            "Franklin",
            "Georgia",
        ],
        identity_prompts=identity_prompt,
        identities=identities,
    )
    print(f"Conversation ID: {conversation.id}")

    for play_id in player_ids:
        update_memory(
            player_id=play_id,
            chat_history=conversation.formatted_chat(),
            identity_prompts=identity_prompt,
        )


if __name__ == "__main__":
    simple_simulation()
