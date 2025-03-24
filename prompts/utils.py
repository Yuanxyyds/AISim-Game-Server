from prompts.identity import (
    ASSASIN_PROMPT,
    SECRETARY_PROMPT,
    SPY_PROMPT,
    BUSINESSMAN_PROMPT,
    TRADER_PROMPT,
    DOUBLE_FACER_PROMPT,
    MEDIA_CREATOR_INVITER_PROMPT,
)


def get_identity_prompts(players: dict) -> dict:
    """
    Returns a dictionary mapping each player name to their role-specific prompt.

    Args:
        players (dict): A dictionary of {name: identity}.

    Returns:
        dict: { player_name: prompt_string }
    """
    prompts = {}
    businessman_name = next(
        (name for name, identity in players.items() if identity == "Businessman"), ""
    )

    assert businessman_name != "", "Businessman role is required for Secretary prompt."

    for name, identity in players.items():
        if identity == "Assassin":
            prompts[name] = ASSASIN_PROMPT.format(YOUR_NAME=name)
        elif identity == "Secretary":
            prompts[name] = SECRETARY_PROMPT.format(
                YOUR_NAME=name, BUSINESSMAN_NAME=businessman_name
            )
        elif identity == "Spy":
            prompts[name] = SPY_PROMPT.format(YOUR_NAME=name)
        elif identity == "Businessman":
            prompts[name] = BUSINESSMAN_PROMPT.format(YOUR_NAME=name)
        elif identity == "Trader":
            prompts[name] = TRADER_PROMPT.format(YOUR_NAME=name)
        elif identity == "Double-Facer":
            prompts[name] = DOUBLE_FACER_PROMPT.format(YOUR_NAME=name)
        elif identity == "Media Creator/Inviter":
            prompts[name] = MEDIA_CREATOR_INVITER_PROMPT.format(YOUR_NAME=name)
        else:
            raise ValueError(f"Unknown identity: {identity}")

    return prompts
