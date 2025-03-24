from resources.llm import call_chat, call_summarizer, _call_deepseek
from resources.shared_queue import simulation_message_queue
import asyncio
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
async def simulate_introductions():
    print("📢 Starting introductions...")

    # The Media Creator starts the conversation
    media_creator = "Georgia"
    first_message = MEDIA_CREATOR_INVITER_INITIAL_PROMPT.format(YOUR_NAME=media_creator)
    chat_history.append({"speaker": media_creator, "content": first_message})
    print(f"🗣️ {media_creator}: {first_message}\n")

    await asyncio.sleep(2)

    # Each player introduces themselves
    for player in players:
        if player == media_creator:
            continue

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

        response_text = call_chat(messages=messages)
        chat_history.append({"speaker": player, "content": response_text})
        add_message_to_queue(player, response_text)
        print(f"🗣️ {player}: {response_text}\n")
        await asyncio.sleep(2)

    # Each player introduces themselves
    for i in range(6):
        speaker = players[i % len(players)]
        chat_context = format_chat_history(chat_history, limit=2)

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

        response_text = call_chat(messages=messages)

        # Store conversation in chat history
        chat_history.append({"speaker": speaker, "content": response_text})
        add_message_to_queue(player, response_text)
        print(f"🗣️ {speaker}: {response_text}\n")
        await asyncio.sleep(2)


def add_message_to_queue(speaker, content):
    simulation_message_queue.put({"speaker": speaker, "content": content})
    print("Added to Queue!")


