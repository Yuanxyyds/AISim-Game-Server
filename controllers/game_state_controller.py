import random
from data.models import SessionLocal, Game, Player

# Define skill cooldowns in minutes
HOURS_24 = 1440  # 24 hours in minutes
HOURS_48 = 2880  # 48 hours in minutes

# Define role-based skills with cooldowns
IDENTITIES = {
    "Assassin": {"skill": {"assassinate": HOURS_24}},
    "Secretary": {"skill": {"block": -1}},
    "Spy": {"skill": {}},
    "Businessman": {"skill": {}},
    "Media Creator/Inviter": {"skill": {}},
    "Trader": {"skill": {"trade": HOURS_24}},
    "Double-Facer": {
        "skill": {
            "assassinate": HOURS_48,
            "block": HOURS_24,
        }
    },
}


def create_game():
    db = SessionLocal()
    game = Game()
    db.add(game)
    db.commit()
    db.refresh(game)

    # Shuffle roles and assign one per player
    identity_list = list(IDENTITIES.keys())
    random.shuffle(identity_list)

    names = ["Alice", "Bob", "Catherine", "David", "Edison", "Franklin", "Georgia"]

    player_ids = []

    # Initialize players
    for i, name in enumerate(names):
        identity = identity_list[i]
        skills = IDENTITIES[identity]["skill"]

        # Memory initialized for all other players
        memory = {
            "long_term": {},
            "short_term": {},
        }
        for other_player in names:
            if other_player != name:
                memory[other_player] = ""

        player = Player(
            game_id=game.id,
            name=name,
            identity=identity,
            dollar=0,
            is_alive=True,
            is_outside=False,
            skills=skills,
            memory=memory,
        )
        db.add(player)
        db.commit()
        db.refresh(player)
        player_ids.append(player.id)

    db.commit()
    db.refresh(game)
    db.close()

    print(f"🎮 Game {game.id} created with 7 players, roles, and initialized memory.")
    return game.id, player_ids