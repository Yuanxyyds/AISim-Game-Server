YOUR_TURN_TO_SPEAK_IN_GROUP = """
It is your turn to speak. Everyone is listening.

Consider what you want to say in front of the group. 
You may share your thoughts, ask questions, or react to what others have said.

Speak carefully — your words may reveal clues or influence others’ perceptions.  
**Respond with your speech only. Less than 75 words**
"""

YOUR_TURN_TO_INTRODUCE = """
It is your turn to introduce yourself. Everyone is listening.

Choose your words wisely—**reveal only what you want others to know**.  
You may speak openly or keep things vague, depending on your strategy.

**Respond with your speech only. Less than 75 words**
"""

GENERATE_MEMORY_AFTER_GROUP_PROMPT = """
You just participated in a group conversation. As {YOUR_NAME}, reflect deeply on the situation.

Write a short paragraph summarizing your current **strategy**, personal **goals**, and evolving **thoughts**.  
Then, for **each player**, describe what you currently think of them. Are they helpful, suspicious, irrelevant, or worth watching?

Your response should capture:
- Your overall mindset and tactical adjustments
- What you are trying to achieve next
- Your assessment of every other participant, even if briefly

Stay in-character and write as if you're thinking privately to yourself.
"""


MEDIA_CREATOR_INVITER_INITIAL_PROMPT = """Hello everyone! Welcome to this **special gathering** that I have arranged for all of us. I am {YOUR_NAME}, your **host and Inviter**, and my goal is simple-**to bring us together, to share, to learn, and to make this an unforgettable experience**. I want to hear about **you**—who you are, what you think of this place, and maybe even what you **hope to gain** from this game. I believe that **the more we talk, the more we can trust each other**. For now, let’s begin. I invite you all to speak freely!"""


PLAYER_MEMORY_SUMMARY_PROMPT = """
This is your last overall memory. 

Memory Log:
{MEMORY}

If it includes anything related to {PLAYER}, summarize it **in a paragraph**. It can includes your current opinion, level of trust, and any strategic plans involving {PLAYER}**.
"""

SELF_MEMORY_SUMMARY_PROMPT = """
You are {NAME}. The following is your internal memory log from your recent interactions:

{MEMORY}

Please summarize your current **strategy**, your **thoughts about the game**, and your **general view of others** in under 250 words.
"""
