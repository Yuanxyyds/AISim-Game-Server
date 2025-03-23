from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, ForeignKey, JSON, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# SQLite DB file
DATABASE_URL = "sqlite:///./data/game.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------------
# Game Table
# -------------------------------
class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    current_time = Column(Integer, default=0)         # Minute unit in a 6-day game
    is_night = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    is_paused = Column(Boolean, default=False)

    players = relationship("Player", back_populates="game", cascade="all, delete")
    logs = relationship("ActionLog", back_populates="game", cascade="all, delete")
    conversations = relationship("Conversation", back_populates="game", cascade="all, delete")

# -------------------------------
# Player Table
# -------------------------------
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))

    name = Column(String, index=True)       # Alice, Bob, etc.
    dollar = Column(Integer)       
    identity = Column(String)               # Role: Assassin, King, Trader, etc.
    is_alive = Column(Boolean, default=True)
    is_outside = Column(Boolean, default=False)

    skills = Column(JSON, default={})       # {"assassinate": cooldown, "block": cooldown, "trade": cooldown}
    memory = Column(JSON, default={})       # {"memory": "...", "shortplan": "...", "Bob": "I trust Bob"}

    game = relationship("Game", back_populates="players")

# -------------------------------
# Action Logs Table
# -------------------------------
class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_name = Column(String)
    action = Column(String)  # e.g., "initiate conversation", "eavesdrop", "assassinate", "block", "trade", "gift", "go out", "go home".
    details = Column(JSON, default={})  # e.g., {"success": True, "heard_by": [...], "target": "Bob"}
    timestamp = Column(Integer, default=0)  # Game timestamp in minutes

    game = relationship("Game", back_populates="logs")

# -------------------------------
# Conversation Table
# -------------------------------
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    participants = Column(JSON, default=[])   # List of participant names
    heard_by = Column(JSON, default=[])       # List of names who overheard
    chat = Column(JSON, default=[])           # [{"speaker": "Alice", "text": "Hey Bob!"}, ...]

    game = relationship("Game", back_populates="conversations")

# -------------------------------
# Create DB
# -------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()