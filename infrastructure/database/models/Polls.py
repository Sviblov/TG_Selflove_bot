from typing import Optional
from datetime import datetime 
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, Float, INT, BOOLEAN
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import TIMESTAMP

from .base import Base, TimestampMixin, TableNameMixin


class sentPoll(Base):
    __tablename__ = "sent_polls"
    """
    This class represents a sent poll
    """
    poll_id: Mapped[str] = mapped_column(String(32),primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("communication_history.message_id",ondelete='CASCADE'))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.question_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    selected_answer: Mapped[int] = mapped_column(INT, nullable=True)

class pollResults(Base):
    __tablename__ = "poll_results"
    """
    This class represents a sent poll
    """
    poll_id: Mapped[int] = mapped_column(INT,primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    score: Mapped[int] = mapped_column(INT)
    is_valid: Mapped[bool] = mapped_column(BOOLEAN)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    
