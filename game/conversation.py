import random
from sqlalchemy.orm import Session
from data.models import SessionLocal, Player, Conversation

def create_group_conversation(inviter_name: str, game_id: int):
    db: Session = SessionLocal()

    # Get all alive players
    players = db.query(Player).filter(Player.game_id == game_id, Player.is_alive == True).all()

    if not players:
        print("❌ No alive players found.")
        db.close()
        return

    # Set all players to indoors and make them participants
    for p in players:
        p.is_outside = False
        p.is_indoors = True

    db.commit()

    # Determine inviter (if alive) or pick someone at random
    inviter = next((p for p in players if p.name == inviter_name), None)
    if not inviter or not inviter.is_alive:
        inviter = random.choice(players)
        print(f"⚠️ Inviter {inviter_name} is dead, randomly selecting {inviter.name} as speaker.")

    # Create opening chat message to each participant
    messages = []
    for other in players:
        if other.name != inviter.name:
            messages.append({
                "speaker": inviter.name,
                "text": f"Hey {other.name}, let's talk!"
            })

    # Create the conversation entry
    convo = Conversation(
        game_id=game_id,
        participants=[p.name for p in players],
        heard_by=[],
        chat=messages
    )

    db.add(convo)
    db.commit()
    db.close()

    print(f"💬 Group conversation created with {len(players)} participants, initiated by {inviter.name}.")
