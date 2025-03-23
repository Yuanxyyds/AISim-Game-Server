import random
from data.models import SessionLocal, Game, Player, init_db

# Define skill cooldowns in minutes
HOURS_24 = 1440  # 24 hours in minutes
HOURS_48 = 2880  # 48 hours in minutes

# Define role-based skills with cooldowns
ROLES = {
    "Assassin": {"skill": {"assassinate": HOURS_24}},
    "Secretary": {"skill": {"block": -1}},
    "Spy": {"skill": {}},
    "Businessman": {"skill": {}},
    "Media Creators/Inviters": {"skill": {}},
    "Trader": {"skill": {"trade": HOURS_24}},
    "Double-facer": {
        "skill": {
            "assassinate": HOURS_48,
            "block": HOURS_24,
        }
    },
}


def load_game():
    db = SessionLocal()
    game = Game()
    db.add(game)
    db.commit()
    db.refresh(game)

    # Shuffle roles and assign one per player
    role_list = list(ROLES.keys())
    random.shuffle(role_list)

    names = ["Alice", "Bob", "Catherine", "David", "Edison", "Franklin", "Georgia"]

    # Initialize players
    players = []
    for i, name in enumerate(names):
        role = role_list[i]
        players.append({"name": name, "role": role, "skills": ROLES[role]["skill"]})

    # Create player objects with memory initialized for all others
    for player_info in players:
        name = player_info["name"]
        role = player_info["role"]
        skills = player_info["skills"]

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
            identity=role,
            dollar=0,
            is_alive=True,
            is_outside=False,
            skills=skills,
            memory=memory,
        )
        db.add(player)

    db.commit()
    db.refresh(game) 
    db.close()
    print(f"🎮 Game {game.id} created with 7 players, roles, and initialized memory.")