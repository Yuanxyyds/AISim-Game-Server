from data.models import SessionLocal, Player
from simulations.simulate_memory import simulate_memory


def update_memory(
    player_id: int,
    chat_history: str,
    identity_prompts: dict,
):
    """
    Updates the player's memory based on the chat history and simulates thoughts.

    Args:
        player_id (int): ID of the player to update.
        chat_history (str): String of recent conversation/chat context.

    Returns:
        Player: The updated player object.
    """
    db = SessionLocal()

    try:
        player = db.get(Player, player_id)
        if not player:
            raise ValueError(f"Player with ID {player_id} not found")

        memory = simulate_memory(player, chat_history, identity_prompts)
        player.memory = memory
        db.commit()

        print(f"✅ Updated memory and simulated thoughts for player #{player.id}")
        return player

    except Exception as e:
        db.rollback()
        print(f"❌ Failed to update player memory: {str(e)}")
        raise e

    finally:
        db.close()


def get_all_players_identity(game_id: int) -> dict:
    """
    Fetch all players for a given game ID and return a mapping of name to identity (role).

    Args:
        game_id (int): The ID of the game.

    Returns:
        dict: Dictionary of {name: identity}.
    """
    db = SessionLocal()
    try:
        players = db.query(Player).filter(Player.game_id == game_id).all()
        return {player.name: player.identity for player in players}
    finally:
        db.close()
