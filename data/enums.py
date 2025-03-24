import enum

class ConversationType(enum.Enum):
    PRIVATE = "private"
    GROUP_TALK = "group_talk"
    INTRODUCTION = "introduction"


class ConversationStatus(enum.Enum):
    QUEUED = "queued"
    INCOMPLETED = "incompleted"
    COMPLETED = "completed"