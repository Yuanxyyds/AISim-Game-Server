import time
from resources.llm import call_reasoning, call_summarizer, init_models
from prompts.actions import (
    GENERATE_MEMORY_AFTER_GROUP_PROMPT,
    PLAYER_MEMORY_SUMMARY_PROMPT,
    SELF_MEMORY_SUMMARY_PROMPT,
)
from data.models import Player

# Players and their roles
players = ["Alice", "Bob", "Catherine", "David", "Edison", "Franklin", "Georgia"]


def _generate_new_player_memory(
    name,
    chat_history,
    identity_prompts: dict,
):
    """Generate memory using DeepSeek."""
    system_prompt = identity_prompts[name]
    user_prompt = (
        f"Conversation History:\n{chat_history}\n\n"
        + GENERATE_MEMORY_AFTER_GROUP_PROMPT.format(YOUR_NAME=name)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return call_reasoning(messages=messages)


def _summarize_memory_with_llama(
    name,
    memory,
    identity_prompts: dict,
):
    """Summarize the player's memory using LLaMA."""
    full_memory = {}

    # Full Summary
    system_prompt = identity_prompts[name]
    summary_prompt = SELF_MEMORY_SUMMARY_PROMPT.format(NAME=name, MEMORY=memory)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": summary_prompt},
    ]

    full_memory["summary"] = call_summarizer(messages)

    print(f'✅ Memory Summary for {name}: {full_memory["summary"]}')

    # Summarize thoughts about each player
    for player in players:
        if player == name:
            continue

        # Player-based prompt
        player_prompt = PLAYER_MEMORY_SUMMARY_PROMPT.format(
            PLAYER=player, MEMORY=memory
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": player_prompt},
        ]
        full_memory[player] = call_summarizer(messages)

        print(f"✅ {name} toward {player}: {full_memory[player]} \n")

    return full_memory


def simulate_memory(player: Player, chat_history: str, identity_prompts: dict):
    print("🧠 Generating player memories and LLaMA summaries...\n")
    reasoning = _generate_new_player_memory(player.name, chat_history, identity_prompts)
    print(reasoning)
    memory = _summarize_memory_with_llama(player.name, reasoning, identity_prompts)
    return memory
