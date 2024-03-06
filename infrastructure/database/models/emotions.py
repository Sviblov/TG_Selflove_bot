from datetime import datetime
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func

from sqlalchemy.dialects.postgresql import TEXT

from .base import Base

class emotionRecord(Base):
    __tablename__ = "emotion_records"
    """
    This class represents a users' emotion record
    """
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id",ondelete='CASCADE'))
    timestamp: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    emotion: Mapped[str]= mapped_column(String(16))
    what_thinking: Mapped[str] = mapped_column(TEXT)
    what_doing: Mapped[str] = mapped_column(TEXT)

    def __repr__(self):
        return f"<Emotion user:{self.user_id} >"
    
