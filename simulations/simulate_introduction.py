from resources.llm import call_chat
import asyncio
from prompts.actions import (
    YOUR_TURN_TO_INTRODUCE,
    MEDIA_CREATOR_INVITER_INITIAL_PROMPT,
)

from data.models import Conversation
from data.enums import ConversationStatus

# Players participating and their roles (in order)
players = ["Alice", "Bob", "Catherine", "David", "Edison", "Franklin", "Georgia"]
chat_history = []


def simulate_introductions(
    conversation: Conversation, db, identity_prompts: dict, identities: dict
):
    print("📢 Starting introductions...")
    chat_history = []

    try:
        # The Media Creator starts the conversation
        media_creator = next(
            (
                name
                for name, identity in identities.items()
                if identity == "Media Creator/Inviter"
            ),
            "",
        )

        assert media_creator != ""

        first_message = MEDIA_CREATOR_INVITER_INITIAL_PROMPT.format(
            YOUR_NAME=media_creator
        )
        chat_history.append({"speaker": media_creator, "content": first_message})
        conversation.chat = chat_history
        db.commit()
        print(f"🗣️ {media_creator} {identities[media_creator]}: {first_message}\n")

        # Each player introduces themselves
        for player in players:
            if player == media_creator:
                continue

            messages = [
                {"role": "system", "content": identity_prompts[player]},
                {
                    "role": "user",
                    "content": "Conversation History:\n"
                    + conversation.formatted_chat()
                    + "\n\n"
                    + YOUR_TURN_TO_INTRODUCE,
                },
            ]

            response_text = call_chat(messages=messages)
            message_obj = {"speaker": player, "content": response_text}
            chat_history.append(message_obj)

            # ✅ Update conversation.chat and commit each time
            conversation.chat = chat_history
            db.commit()

            print(f"🗣️ {player} {identities[player]}: {response_text}\n")

        # ✅ Mark conversation as completed
        conversation.status = ConversationStatus.COMPLETED
        db.commit()
        print("✅ Introduction conversation complete!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during introduction simulation: {e}")
        raise e
