from llama_cpp import Llama
import threading
import time
from llm import load_llama_model, load_deepseek_model, call_deepseek, call_llama
from prompts.roles import (
    ASSASIN_PROMPT,
    SECRETARY_PROMPT,
    SPY_PROMPT,
    BUSINESSMAN_PROMPT,
    TRADER_PROMPT,
    DOUBLE_FACER_PROMPT,
    MEDIA_CREATOR_INVITER_PROMPT,
)
from prompts.actions import (
    YOUR_TURN_TO_SPEAK_IN_GROUP,
    YOUR_TURN_TO_INTRODUCE,
    MEDIA_CREATOR_INVITER_INITIAL_PROMPT,
)

load_deepseek_model()
from llm import llama, deepseek

# Players participating and their roles (in order)
players = ["Alice", "Bob", "Catherine", "David", "Edison", "Franklin", "Georgia"]
roles = [
    "Assassin",
    "Secretary",
    "Spy",
    "Businessman",
    "Trader",
    "Double-Facer",
    "Media Creator/Inviter",
]

# Assign role-based prompts
role_prompts = {
    "Alice": ASSASIN_PROMPT.format(YOUR_NAME="Alice"),
    "Bob": SECRETARY_PROMPT.format(YOUR_NAME="Bob", BUSINESSMAN_NAME="David"),
    "Catherine": SPY_PROMPT.format(YOUR_NAME="Catherine"),
    "David": BUSINESSMAN_PROMPT.format(YOUR_NAME="David"),
    "Edison": TRADER_PROMPT.format(YOUR_NAME="Edison"),
    "Franklin": DOUBLE_FACER_PROMPT.format(YOUR_NAME="Franklin"),
    "Georgia": MEDIA_CREATOR_INVITER_PROMPT.format(YOUR_NAME="Georgia"),
}

# Chat history as a list of dictionaries
chat_history = []


# Function to format conversation history for input prompt
def format_chat_history(history, limit=7):
    """Format the last 'limit' messages as context for the model."""
    recent_history = history[-limit:]  # Get the last `limit` messages
    formatted_history = "\n".join(
        [f"{msg['speaker']}: {msg['content']}" for msg in recent_history]
    )
    return formatted_history


# Function to simulate player introductions
def simulate_introductions():
    print("📢 Starting introductions...")

    # The Media Creator starts the conversation
    media_creator = "Georgia"
    first_message = MEDIA_CREATOR_INVITER_INITIAL_PROMPT.format(YOUR_NAME=media_creator)
    chat_history.append({"speaker": media_creator, "content": first_message})
    print(f"🗣️ {media_creator}: {first_message}\n")

    time.sleep(2)

    # Each player introduces themselves
    for player in players:
        if player == media_creator:
            continue  # Skip Media Creator since they already spoke

        chat_context = format_chat_history(chat_history, limit=7)
        messages = [
            {"role": "system", "content": role_prompts[player]},
            {
                "role": "user",
                "content": "Conversation History:\n"
                + "Georgia: "
                + MEDIA_CREATOR_INVITER_INITIAL_PROMPT
                + "\n\n"
                + YOUR_TURN_TO_INTRODUCE,
            },
        ]

        response_text = call_deepseek(messages=messages)

        # Store in chat history
        chat_history.append({"speaker": player, "content": response_text})
        print(f"🗣️ {player}: {response_text}\n")
        time.sleep(2)


# Function to simulate free talk session
def simulate_free_talk():
    print("💬 Free talk session has started... Players are conversing.")

    for i in range(10):  # Simulate multiple rounds of free talk
        speaker = players[i % len(players)]  # Rotate turns
        chat_context = format_chat_history(chat_history, limit=i)

        messages = [
            {"role": "system", "content": role_prompts[speaker]},
            {
                "role": "user",
                "content": "Conversation History:\n"
                + chat_context
                + "\n\n"
                + YOUR_TURN_TO_SPEAK_IN_GROUP,
            },
        ]

        response_text = call_deepseek(messages=messages)

        # Store conversation in chat history
        chat_history.append({"speaker": speaker, "content": response_text})
        print(f"🗣️ {speaker}: {response_text}\n")
        time.sleep(3)  # Add delay for realism


simulate_introductions()
print("\n🎭 Everyone has introduced themselves! Now, let’s begin free talk.\n")
simulate_free_talk()
