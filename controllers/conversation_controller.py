from data.models import SessionLocal, Conversation
from data.enums import ConversationType
from simulations.simulate_introduction import simulate_introductions


def create_conversation(
    game_id: int,
    type: ConversationType,
    participants: list,
    identity_prompts: dict,
    identities: dict,
):
    """
    Creates a conversation, simulates chat, and stores it in the database.

    Args:
        game_id (int): ID of the game.
        type (str): ConversationType
        participants (list): List of player names in the conversation.
        heard_by (list): List of player names who overheard it.

    Returns:
        Conversation: The created and updated conversation object.
    """
    db = SessionLocal()

    try:
        convo = Conversation(
            game_id=game_id,
            type=type,
            participants=participants,
            heard_by=participants,
            chat=[],
        )
        db.add(convo)
        db.commit()
        db.refresh(convo)
        simulate_introductions(
            conversation=convo,
            db=db,
            identity_prompts=identity_prompts,
            identities=identities,
        )
        db.refresh(convo)
        print(f"✅ Created and simulated conversation #{convo.id}")
        return convo

    except Exception as e:
        db.rollback()
        print(f"❌ Failed to create conversation: {str(e)}")
        raise e

    finally:
        db.close()
