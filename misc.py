from fastapi import FastAPI, WebSocket
from llama_cpp import Llama
from fastapi.responses import StreamingResponse
from prompts.roles import ASSASIN_PROMPT

app = FastAPI()

# Load the AI model (DeepSeek 7B in GGUF format)
llm = Llama(
    model_path="/root/AISim-Game-server/models/DeepSeek-R1-Distill-Llama-8B-Q6_K.gguf",
    n_gpu_layers=32,
    n_ctx=1024,
    verbose=False,
)

messages = [
    {"role": "system", "content": ASSASIN_PROMPT.format(**{"YOUR_NAME": "Alice"})},
    {"role": "user", "content": "The game is about to start, what is my strategy?"},
]

# Run inference with formatted messages
response = llm.create_chat_completion(messages=messages, max_tokens=1024)["choices"][0][
    "message"
]["content"]

# Print model response
print(response)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")

messages = [
    {
        "role": "system",
        "content": "You are the central processor of thoughts. Your role is to gather and analyze information, then either summarize key points or engage in conversation based on the user's request.",
    },
    {"role": "user", "content": f"The game is about to start, what is my strategy, this is my mind {response}"},
]

llm2 = Llama(
    model_path="/root/AISim-Game-server/models/Llama-3.2-3B-Instruct-Q8_0.gguf",
    n_gpu_layers=32,
    n_ctx=1024,
    verbose=False,
)

# Run inference with formatted messages
response = llm2.create_chat_completion(messages=messages, max_tokens=1024)["choices"][0][
    "message"
]["content"]

# Print model response
print(response)

# # WebSocket endpoint for real-time NPC chat
# @app.websocket("/npc-chat")
# async def npc_chat(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         # Receive player's message
#         user_input = await websocket.receive_text()

#         # Generate NPC response token-by-token
#         async def token_stream():
#             for token in llm(user_input, max_tokens=100, stream=True):
#                 yield token["choices"][0]["text"]

#         # Stream response back to the player
#         await websocket.send_text("".join(await token_stream()))

# # Simple HTTP route to test NPC response
# @app.get("/test-chat/")
# async def test_chat(prompt: str):
#     response = llm(prompt, max_tokens=100)
#     return {"npc_response": response["choices"][0]["text"]}

# # HTTP route for NPC chat (Non-realtime)
# @app.get("/chat/")
# async def chat(prompt: str):
#     response = llm(prompt, max_tokens=100)
#     return {"npc_response": response["choices"][0]["text"]}

# # Health check endpoint
# @app.get("/health")
# def health():
#     return {"status": "OK"}
